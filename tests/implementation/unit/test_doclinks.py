import tempfile
import unittest
from pathlib import Path, PurePosixPath

import helpers  # noqa: F401  (adds plugin/scripts to sys.path)
from doclinks import check_file, check_project, doc_files, find_links, heading_slugs
from harness_config import parse_config


class FindLinksTest(unittest.TestCase):
    def targets(self, text):
        return [target for _, target in find_links(text)]

    def test_inline_link_with_line_number(self):
        self.assertEqual(find_links("a\n[Text](b/c.md#x) more\n"), [(2, "b/c.md#x")])

    def test_several_links_in_one_line(self):
        self.assertEqual(self.targets("[a](a.md) and [b](b.md)"), ["a.md", "b.md"])

    def test_image(self):
        self.assertEqual(self.targets("![alt](img/pic.png)"), ["img/pic.png"])

    def test_title_is_cut_off(self):
        self.assertEqual(self.targets('[a](a.md "Title") [b](b.md \'T\')'), ["a.md", "b.md"])

    def test_angle_brackets_allow_spaces(self):
        self.assertEqual(self.targets("[a](<my file.md>)"), ["my file.md"])

    def test_parentheses_in_target(self):
        self.assertEqual(self.targets("[a](a_(b).md)"), ["a_(b).md"])

    def test_reference_links(self):
        text = "see [x][id] here\n\n[id]: ../ref.md#top\n"
        self.assertEqual(self.targets(text), ["../ref.md#top"])

    def test_fenced_code_is_skipped(self):
        text = "```\n[a](a.md)\n```\n~~~\n[b](b.md)\n~~~\n[c](c.md)\n"
        self.assertEqual(find_links(text), [(7, "c.md")])

    def test_inline_code_is_skipped(self):
        self.assertEqual(self.targets("`[a](a.md)` and [b](b.md) and ``[c](c.md)``"), ["b.md"])

    def test_escaped_bracket_is_no_link(self):
        self.assertEqual(self.targets(r"\[a](a.md)"), [])

    def test_empty_target(self):
        self.assertEqual(self.targets("[a]()"), [])


class HeadingSlugsTest(unittest.TestCase):
    def test_github_slug(self):
        self.assertEqual(heading_slugs("# Hello, World! (v2)\n"), {"hello-world-v2"})

    def test_umlauts_digits_dash_underscore_are_kept(self):
        self.assertEqual(heading_slugs("## Größe_1 – Über-Sicht\n"), {"größe_1--über-sicht"})

    def test_duplicates_get_numbers(self):
        self.assertEqual(heading_slugs("# A\n## A\n### A\n"), {"a", "a-1", "a-2"})

    def test_headings_in_code_blocks_do_not_count(self):
        self.assertEqual(heading_slugs("```\n# Fake\n```\n# Real\n"), {"real"})

    def test_explicit_anchors(self):
        text = '<a id="one"></a> and <a name="two">x</a>\n'
        self.assertEqual(heading_slugs(text), {"one", "two"})

    def test_markup_in_heading(self):
        self.assertEqual(heading_slugs("# The `code` and [link](x.md)\n"), {"the-code-and-link"})

    def test_closing_hashes_and_setext(self):
        self.assertEqual(heading_slugs("# One #\n\nTwo\n===\n"), {"one", "two"})


class _Tree(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name).resolve() / "project"
        self.root.mkdir()

    def write(self, rel, text=""):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def check(self, rel):
        return check_file(self.root, PurePosixPath(rel))


class CheckFileTest(_Tree):
    def test_valid_links_are_silent(self):
        self.write("docs/a.md", "[b](b.md) [c](sub/c.md#intro) [d](sub/) [s](#self) [i](img.png)\n# Self\n")
        self.write("docs/b.md")
        self.write("docs/sub/c.md", "# Intro\n")
        self.write("docs/img.png")
        self.assertEqual(self.check("docs/a.md"), [])

    def test_missing_file(self):
        self.write("a.md", "x\n[b](b.md)\n")
        self.assertEqual(self.check("a.md"), ["a.md:2: b.md: target does not exist"])

    def test_missing_anchor(self):
        self.write("a.md", "[b](b.md#nope)\n")
        self.write("b.md", "# Yes\n")
        self.assertEqual(self.check("a.md"), ["a.md:1: b.md#nope: anchor not found in b.md"])

    def test_missing_anchor_in_same_file(self):
        self.write("a.md", "[b](#nope)\n")
        self.assertEqual(self.check("a.md"), ["a.md:1: #nope: anchor not found in a.md"])

    def test_anchor_umlaut_and_duplicate(self):
        self.write("a.md", "[1](b.md#überblick) [2](b.md#teil-1)\n")
        self.write("b.md", "# Überblick\n## Teil\n## Teil\n")
        self.assertEqual(self.check("a.md"), [])

    def test_anchor_is_case_insensitive(self):
        self.write("a.md", "[1](b.md#Yes)\n")
        self.write("b.md", "# Yes\n")
        self.assertEqual(self.check("a.md"), [])

    def test_anchor_on_non_markdown_target_is_not_checked(self):
        self.write("a.md", "[1](b.txt#L10)\n")
        self.write("b.txt")
        self.assertEqual(self.check("a.md"), [])

    def test_external_links_are_ignored(self):
        self.write("a.md", "[1](https://x.org/a.md) [2](mailto:a@b.c) [3](//host/a) [4](tel:1)\n")
        self.assertEqual(self.check("a.md"), [])

    def test_target_outside_project_is_an_error(self):
        self.write("a.md", "[1](../outside.md)\n")
        (self.root.parent / "outside.md").write_text("x")
        self.assertEqual(self.check("a.md"), ["a.md:1: ../outside.md: target lies outside the project"])

    def test_relative_to_linking_file(self):
        self.write("docs/x/a.md", "[1](../y/b.md)\n")
        self.write("docs/y/b.md")
        self.assertEqual(self.check("docs/x/a.md"), [])

    def test_encoded_and_query(self):
        self.write("a.md", "[1](my%20file.md) [2](b.md?plain=1)\n")
        self.write("my file.md")
        self.write("b.md")
        self.assertEqual(self.check("a.md"), [])

    def test_links_in_code_are_ignored(self):
        self.write("a.md", "```\n[1](nope.md)\n```\n`[2](nope.md)`\n")
        self.assertEqual(self.check("a.md"), [])

    def test_unreadable_file_is_silent(self):
        self.assertEqual(self.check("missing.md"), [])


class DocFilesTest(_Tree):
    def config(self, **tables):
        return parse_config({"version": 1, **tables})

    def files(self, config):
        return sorted(str(p) for p in doc_files(self.root, config))

    def test_techdocs_and_development(self):
        for rel in ("README.md", "docs/techdocs/a.md", "docs/techdocs/sub/b.md", "docs/development/c.md",
                    "docs/todo/x.md", "docs/techdocs/n.txt"):
            self.write(rel)
        config = self.config(modules={"techdocs": True, "development": True})
        self.assertEqual(
            self.files(config), ["README.md", "docs/development/c.md", "docs/techdocs/a.md", "docs/techdocs/sub/b.md"]
        )

    def test_modules_off(self):
        for rel in ("README.md", "docs/techdocs/a.md", "docs/development/c.md"):
            self.write(rel)
        self.assertEqual(self.files(self.config(modules={"techdocs": True})), ["README.md", "docs/techdocs/a.md"])
        self.assertEqual(self.files(self.config(modules={"development": True})), ["docs/development/c.md"])
        self.assertEqual(
            self.files(self.config(modules={"development": True}, development={"architecture": False})), []
        )
        self.assertEqual(self.files(self.config()), [])

    def test_missing_folders(self):
        self.write("README.md")
        self.assertEqual(self.files(self.config(modules={"techdocs": True, "development": True})), ["README.md"])


class CheckProjectTest(_Tree):
    def setUp(self):
        super().setUp()
        self.config = parse_config({"version": 1, "modules": {"techdocs": True, "development": True}})
        self.write("README.md", "[a](docs/techdocs/a.md) [x](docs/gone.md)\n")
        self.write("docs/techdocs/a.md", "[r](../../README.md#nope)\n")
        self.write("docs/development/b.md", "[a](../techdocs/a.md)\n")

    def test_all_files(self):
        self.assertEqual(
            check_project(self.root, self.config),
            [
                "README.md:1: docs/gone.md: target does not exist",
                "docs/techdocs/a.md:1: ../../README.md#nope: anchor not found in README.md",
            ],
        )

    def test_only_given_files(self):
        result = check_project(self.root, self.config, [PurePosixPath("docs/development/b.md")])
        self.assertEqual(result, [])

    def test_prefix_for_subprojects(self):
        result = check_project(self.root, self.config, [PurePosixPath("README.md")], prefix=PurePosixPath("sub"))
        self.assertEqual(result, ["sub/README.md:1: docs/gone.md: target does not exist"])


if __name__ == "__main__":
    unittest.main()
