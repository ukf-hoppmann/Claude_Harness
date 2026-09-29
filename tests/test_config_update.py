import dataclasses
import tomllib
import unittest

from helpers import REPO_ROOT
from harness_config import DEVELOPMENT_PARTS, KNOWN_MODULES, ConfigError, parse_config
from config_update import complete

TEMPLATE = (REPO_ROOT / "plugin/templates/config.toml").read_text(encoding="utf-8")
ALL_OFF = {f"modules.{name}": "false" for name in KNOWN_MODULES}


def decisions(result):
    return {d.key: d for d in result.decisions}


def keeps_lines(test, before, after):
    """Every line of before appears in after, in the same order."""
    remaining = iter(after.splitlines())
    for line in before.splitlines():
        test.assertIn(line, remaining, f"line {line!r} lost or reordered")


class CompleteTest(unittest.TestCase):
    def test_template_is_complete(self):
        result = complete(TEMPLATE, TEMPLATE)
        self.assertEqual(result.text, TEMPLATE)
        self.assertEqual(result.decisions, ())

    def test_missing_key_gets_template_line(self):
        project = TEMPLATE.replace('backend = "api"\n', "")
        result = complete(project, TEMPLATE, choices={})
        self.assertIn('backend = "api"\n', result.text)
        self.assertLess(result.text.index('path = "todo"'), result.text.index('backend = "api"'))
        keeps_lines(self, project, result.text)

    def test_backend_is_a_decision_when_todo_is_on(self):
        project = TEMPLATE.replace('backend = "api"\n', "")
        pending = decisions(complete(project, TEMPLATE))["todo.backend"]
        self.assertTrue(pending.pending)
        self.assertEqual(pending.value, '"api"')
        result = complete(project, TEMPLATE, choices={"todo.backend": "files"})
        self.assertFalse(decisions(result)["todo.backend"].pending)
        self.assertIn('backend = "files"', result.text)
        self.assertEqual(tomllib.loads(result.text)["todo"]["backend"], "files")

    def test_backend_is_no_decision_when_todo_is_off(self):
        project = TEMPLATE.replace("todo = true", "todo = false").replace('backend = "api"\n', "")
        result = complete(project, TEMPLATE)
        self.assertNotIn("todo.backend", decisions(result))
        self.assertIn('backend = "api"', result.text)

    def test_missing_module_is_a_decision_defaulting_to_off(self):
        project = TEMPLATE.replace("daily = false\n", "").replace("techdocs = true\n", "")
        result = complete(project, TEMPLATE)
        self.assertEqual({k for k, d in decisions(result).items() if d.pending}, {"modules.daily", "modules.techdocs"})
        self.assertFalse(tomllib.loads(result.text)["modules"]["techdocs"])
        chosen = complete(project, TEMPLATE, choices={"modules.daily": "false", "modules.techdocs": "true"})
        self.assertTrue(tomllib.loads(chosen.text)["modules"]["techdocs"])
        self.assertFalse(any(d.pending for d in chosen.decisions))

    def test_backend_decision_follows_a_new_todo_module(self):
        project = TEMPLATE.replace("todo = true\n", "").replace('backend = "api"\n', "")
        self.assertNotIn("todo.backend", decisions(complete(project, TEMPLATE)))
        result = complete(project, TEMPLATE, choices={"modules.todo": "true"})
        self.assertIn("todo.backend", decisions(result))

    def test_missing_section_is_inserted_in_template_order(self):
        start = TEMPLATE.index("# Daily development reports")
        end = TEMPLATE.index("# Technical documentation")
        project = TEMPLATE[:start] + TEMPLATE[end:]
        result = complete(project, TEMPLATE)
        self.assertEqual(result.text, TEMPLATE)

    def test_missing_section_comment_is_added(self):
        project = TEMPLATE.replace("# Daily development reports, relative to docs.root.\n", "")
        self.assertEqual(complete(project, TEMPLATE).text, TEMPLATE)

    def test_differing_section_comment_is_a_decision(self):
        old = "# Daily development reports, relative to docs.root.\n"
        project = TEMPLATE.replace(old, "# Our own words.\n")
        pending = decisions(complete(project, TEMPLATE))["comment:daily"]
        self.assertTrue(pending.pending)
        self.assertEqual(pending.project, "# Our own words.")
        self.assertEqual(pending.template, old.strip())
        self.assertEqual(complete(project, TEMPLATE, choices={"comment:daily": "keep"}).text, project)
        self.assertEqual(complete(project, TEMPLATE, choices={"comment:daily": "replace"}).text, TEMPLATE)

    def test_missing_inline_comment_is_appended(self):
        line = 'root = "docs"       # folder for all harness documents, relative to the project root\n'
        project = TEMPLATE.replace(line, 'root = "docs"\n')
        self.assertEqual(complete(project, TEMPLATE).text, TEMPLATE)

    def test_inline_comment_is_appended_to_own_value(self):
        project = TEMPLATE.replace(
            'root = "docs"       # folder for all harness documents, relative to the project root\n',
            'root = "documentation"\n',
        )
        result = complete(project, TEMPLATE)
        self.assertIn('root = "documentation"  # folder for all harness documents', result.text)
        self.assertEqual(tomllib.loads(result.text)["docs"]["root"], "documentation")

    def test_differing_inline_comment_is_a_decision(self):
        project = TEMPLATE.replace("# ISO 639-1 language of generated documents", "# German")
        self.assertIn("comment:docs.language", decisions(complete(project, TEMPLATE)))
        kept = complete(project, TEMPLATE, choices={"comment:docs.language": "keep"})
        self.assertEqual(kept.text, project)
        replaced = complete(project, TEMPLATE, choices={"comment:docs.language": "replace"})
        self.assertEqual(replaced.text, TEMPLATE)

    def test_top_comment(self):
        project = TEMPLATE.replace("# Claude_Harness project configuration.\n", "")
        self.assertEqual(complete(project, TEMPLATE).text, TEMPLATE)
        own = TEMPLATE.replace("# Claude_Harness project configuration.", "# Ours.")
        self.assertIn("comment:top", decisions(complete(own, TEMPLATE)))

    def test_harness_repo_is_a_decision_in_the_root_project(self):
        start = TEMPLATE.index("# Claude_Harness repository")
        project = TEMPLATE[:start]
        pending = decisions(complete(project, TEMPLATE))["harness.repo"]
        self.assertEqual(pending.value, "[]")
        result = complete(project, TEMPLATE, choices={"harness.repo": "~/GitHub/Claude_Harness"})
        self.assertEqual(tomllib.loads(result.text)["harness"]["repo"], ["~/GitHub/Claude_Harness"])
        listed = complete(project, TEMPLATE, choices={"harness.repo": '["/a", "/b"]'})
        self.assertEqual(tomllib.loads(listed.text)["harness"]["repo"], ["/a", "/b"])

    def test_subproject_gets_no_harness_table(self):
        start = TEMPLATE.index("# Claude_Harness repository")
        project = TEMPLATE[:start]
        result = complete(project, TEMPLATE, subproject=True)
        self.assertEqual(result.text, project)
        self.assertEqual(result.decisions, ())

    def test_own_content_is_kept(self):
        project = (
            "version = 1\n\n"
            "[modules]\n"
            "todo = true  # we use it\n"
            "daily = true\n\n"
            "# Our techdocs.\n"
            "[techdocs]\n"
            "documents = [\n"
            '    "architecture",\n'
            "]\n\n"
            "[projects]\n"
            'app = "app"\n'
        )
        choices = {k: v for k, v in ALL_OFF.items() if k not in ("modules.todo", "modules.daily")}
        choices |= {"todo.backend": "api", "comment:techdocs": "keep", "harness.repo": "[]"}
        result = complete(project, TEMPLATE, choices=choices)
        keeps_lines(self, project, result.text)
        self.assertFalse(any(d.pending for d in result.decisions))
        data = tomllib.loads(result.text)
        self.assertEqual(data["techdocs"]["documents"], ["architecture"])
        self.assertEqual(data["projects"], {"app": "app"})

    def test_effective_config_is_unchanged(self):
        project = "version = 1\n\n[modules]\ntodo = true\ndevelopment = true\n\n[docs]\nlanguage = \"de\"\n"
        choices = {k: v for k, v in ALL_OFF.items() if k not in ("modules.todo", "modules.development")}
        choices |= {"todo.backend": "api", "harness.repo": "[]"}
        result = complete(project, TEMPLATE, choices=choices)
        before = parse_config(tomllib.loads(project))
        after = parse_config(tomllib.loads(result.text))
        for name in KNOWN_MODULES:
            self.assertEqual(before.enabled(name), after.enabled(name), name)
        for part in DEVELOPMENT_PARTS:
            self.assertEqual(before.part_enabled(part), after.part_enabled(part), part)
        neutral = {"modules": {}, "development_parts": {}}
        self.assertEqual(dataclasses.replace(before, **neutral), dataclasses.replace(after, **neutral))

    def test_second_run_changes_nothing(self):
        project = "version = 1\n\n[modules]\ntodo = true\n"
        choices = {k: v for k, v in ALL_OFF.items() if k != "modules.todo"}
        choices |= {"todo.backend": "files", "harness.repo": "[]"}
        first = complete(project, TEMPLATE, choices=choices)
        second = complete(first.text, TEMPLATE)
        self.assertEqual(second.text, first.text)
        self.assertEqual(second.decisions, ())

    def test_invalid_choices_are_errors(self):
        project = TEMPLATE.replace("daily = false\n", "")
        for choices in ({"modules.daily": "maybe"}, {"todo.backend": "api"}, {"comment:daily": "replace"}):
            with self.subTest(choices=choices), self.assertRaises(ConfigError):
                complete(project, TEMPLATE, choices=choices)

    def test_invalid_project_config_is_an_error(self):
        with self.assertRaises(ConfigError):
            complete("version = 1\n[modules]\nnope = true\n", TEMPLATE)


if __name__ == "__main__":
    unittest.main()
