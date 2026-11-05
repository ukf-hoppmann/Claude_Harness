import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath

from helpers import SCRIPTS
from architecture import load_uses, parse_uses
from harness_config import load_config

USES_TABLE = (
    "## Required on use\n\n| Uses | Read |\n|---|---|\n"
    "| `reportError`, `modals.alert` | `docs/errors.md` |\n"
)
RULES = (
    "# Rules\n\n- Code MUST be tidy.\n\n## Scopes\n\n| Scope | Paths | Covers |\n|---|---|---|\n"
    "| ui | `src/ui/**` | UI |\n\n" + USES_TABLE
)
UI_SCOPE = "# UI\n\n## Required on use\n\n| Uses | Read |\n|---|---|\n| `showToast` | `docs/toast.md` |\n"


class ParseUsesTest(unittest.TestCase):
    def test_parses_table(self):
        usages, errors = parse_uses(USES_TABLE)
        self.assertEqual(errors, [])
        self.assertEqual(len(usages), 1)
        self.assertEqual(usages[0].uses, ("reportError", "modals.alert"))
        self.assertEqual(usages[0].read, ("docs/errors.md",))

    def test_no_section_or_empty_table(self):
        self.assertEqual(parse_uses("# Rules\n"), ([], []))
        self.assertEqual(parse_uses("## Required on use\n\n| Uses | Read |\n|---|---|\n"), ([], []))

    def test_several_files_and_rows(self):
        text = ("## Required on use\n\n| Uses | Read |\n|---|---|\n"
                "| `a1` | `x.md`, `y/z.md` |\n| `$b`, `c_d.e` | `x.md` |\n")
        usages, errors = parse_uses(text)
        self.assertEqual(errors, [])
        self.assertEqual([u.read for u in usages], [("x.md", "y/z.md"), ("x.md",)])
        self.assertEqual(usages[1].uses, ("$b", "c_d.e"))

    def test_invalid_rows(self):
        head = "## Required on use\n\n| Uses | Read |\n|---|---|\n"
        for row in ("| `1234` | `x.md` |", "| `foo-bar` | `x.md` |", "| `a b` | `x.md` |", "| plain | `x.md` |",
                    "| `a` | x.md |", "| `a` | `/abs.md` |", "| `a` | `../x.md` |", "| `a` | `*.md` |",
                    "| `a` |", "| `a` | |"):
            usages, errors = parse_uses(head + row + "\n")
            self.assertEqual(usages, [], row)
            self.assertEqual(len(errors), 1, row)

    def test_valid_entries_survive_invalid_neighbours(self):
        usages, errors = parse_uses("## Required on use\n\n| Uses | Read |\n|---|---|\n| `ok`, `1` | `x.md`, `/y.md` |\n")
        self.assertEqual((usages[0].uses, usages[0].read), (("ok",), ("x.md",)))
        self.assertEqual(len(errors), 2)

    def test_ignored_in_comment(self):
        self.assertEqual(parse_uses("<!--\n" + USES_TABLE + "-->\n"), ([], []))


class HookBase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name).resolve()
        self.project = base / "project"
        self.data = base / "data"
        self.write(self.project / ".claude-harness/config.toml", "version = 1\n[modules]\ndevelopment = true\n")
        self.rules = self.write(self.project / "docs/development/architecture.md", RULES)
        self.scope = self.write(self.project / "docs/development/architecture/ui.md", UI_SCOPE)
        self.errors_doc = self.write(self.project / "docs/errors.md", "# Errors\n\nOne\nTwo\n")
        self.toast_doc = self.write(self.project / "docs/toast.md", "# Toast\n")

    def tearDown(self):
        self._tmp.cleanup()

    @staticmethod
    def write(path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def run_hook(self, script, payload):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project), CLAUDE_PLUGIN_DATA=str(self.data))
        return subprocess.run([sys.executable, str(SCRIPTS / script)], input=json.dumps(payload),
                              capture_output=True, text=True, env=env)

    def read(self, path, session="s1", **extra):
        self.run_hook("mark_architecture_read.py",
                      {"session_id": session, "tool_name": "Read", "tool_input": {"file_path": str(path), **extra}})

    def deny(self, tool, tool_input, session="s1"):
        result = self.run_hook("check_architecture.py",
                               {"session_id": session, "tool_name": tool, "tool_input": tool_input})
        self.assertEqual(result.returncode, 0, result.stderr)
        if not result.stdout.strip():
            return None
        return json.loads(result.stdout)["hookSpecificOutput"]["permissionDecisionReason"]

    def write_tool(self, rel, content, session="s1"):
        return self.deny("Write", {"file_path": str(self.project / rel), "content": content}, session)


class RequiredOnUseHookTest(HookBase):
    def setUp(self):
        super().setUp()
        self.read(self.rules)

    def test_hit_blocks_until_doc_is_read_in_full(self):
        reason = self.write_tool("src/app.py", "reportError(e)")
        self.assertIn("reportError", reason)
        self.assertIn("src/app.py", reason)
        self.assertIn("docs/errors.md", reason)
        self.read(self.errors_doc, limit=1)
        self.assertIsNotNone(self.write_tool("src/app.py", "reportError(e)"))
        self.read(self.errors_doc, offset=2)
        self.assertIsNotNone(self.write_tool("src/app.py", "reportError(e)"))
        self.read(self.errors_doc)
        self.assertIsNone(self.write_tool("src/app.py", "reportError(e)"))
        self.assertIsNotNone(self.write_tool("src/app.py", "reportError(e)", session="s2"))

    def test_no_identifier_no_block(self):
        self.assertIsNone(self.write_tool("src/app.py", "print('hello')"))

    def test_word_boundaries(self):
        for text in ("reportErrorX(e)", "myreportError(e)", "_reportError", "$reportError", "reportError2",
                     "xmodals.alert()", "modals.alerts()", "modalsXalert()", "modals.\nalert"):
            self.assertIsNone(self.write_tool("src/app.py", text), text)
        for text in ("reportError", "x = reportError;", "this.reportError(e)", "(reportError)", "modals.alert('x')",
                     "core.modals.alert(1)", "a\nreportError"):
            self.assertIsNotNone(self.write_tool("src/app.py", text), text)

    def test_all_tools_check_new_text(self):
        path = str(self.project / "src/app.py")
        self.assertIsNotNone(self.deny("Edit", {"file_path": path, "old_string": "a", "new_string": "reportError"}))
        self.assertIsNone(self.deny("Edit", {"file_path": path, "old_string": "reportError", "new_string": "a"}))
        edits = [{"old_string": "a", "new_string": "b"}, {"old_string": "c", "new_string": "modals.alert"}]
        self.assertIn("modals.alert", self.deny("MultiEdit", {"file_path": path, "edits": edits}))
        self.assertIsNone(self.deny("MultiEdit", {"file_path": path, "edits": edits[:1]}))
        nb = str(self.project / "src/n.ipynb")
        self.assertIsNotNone(self.deny("NotebookEdit", {"notebook_path": nb, "new_source": "reportError()"}))
        self.assertIsNone(self.deny("NotebookEdit", {"notebook_path": nb, "new_source": "x = 1"}))
        self.assertIsNone(self.deny("NotebookEdit", {"notebook_path": nb}))

    def test_scope_table_applies_only_to_scope_paths(self):
        self.read(self.scope)
        self.assertIsNone(self.write_tool("src/app.py", "showToast()"))
        reason = self.write_tool("src/ui/view.js", "showToast()")
        self.assertIn("showToast", reason)
        self.assertIn("docs/toast.md", reason)
        self.read(self.toast_doc)
        self.assertIsNone(self.write_tool("src/ui/view.js", "showToast()"))
        # the project-wide table also applies inside the scope
        self.assertIn("docs/errors.md", self.write_tool("src/ui/view.js", "reportError()"))

    def test_several_missing_docs_are_summarized(self):
        self.read(self.scope)
        reason = self.write_tool("src/ui/view.js", "showToast(); reportError()")
        for part in ("showToast", "reportError", "docs/toast.md", "docs/errors.md"):
            self.assertIn(part, reason)
        self.read(self.errors_doc)
        reason = self.write_tool("src/ui/view.js", "showToast(); reportError()")
        self.assertIn("docs/toast.md", reason)
        self.assertNotIn("docs/errors.md", reason)

    def test_missing_doc_is_named(self):
        self.errors_doc.unlink()
        self.assertIn("docs/errors.md (missing)", self.write_tool("src/app.py", "reportError()"))

    def test_mandatory_check_comes_first(self):
        # the ui scope file is still unread
        reason = self.write_tool("src/ui/view.js", "reportError()")
        self.assertIn("read the binding architecture rules", reason)
        self.assertNotIn("before using", reason)

    def test_harness_files_are_not_checked(self):
        self.assertIsNone(self.write_tool("docs/todo/notes.md", "reportError"))

    def test_other_files_are_not_marked(self):
        other = self.write(self.project / "docs/other.md", "# Other\n")
        self.read(other)
        state = [f for f in self.data.rglob("*") if f.is_file()] if self.data.exists() else []
        self.assertFalse(any("other.md" in f.read_text() for f in state))

    def test_suite_off_blocks_nothing(self):
        self.write(self.project / ".claude-harness/config.toml", "version = 1\n[modules]\ndevelopment = false\n")
        self.assertIsNone(self.write_tool("src/app.py", "reportError"))

    def test_load_uses_by_path(self):
        config = load_config(self.project)
        every, errors = load_uses(self.project, config)
        self.assertEqual((len(every), errors), (2, []))
        only_rules, _ = load_uses(self.project, config, PurePosixPath("src/app.py"))
        self.assertEqual(len(only_rules), 1)
        in_scope, _ = load_uses(self.project, config, PurePosixPath("src/ui/a.js"))
        self.assertEqual(len(in_scope), 2)

    def test_session_start_reports_errors(self):
        self.write(self.rules, RULES.replace("`docs/errors.md`", "`docs/nope.md`").replace("`reportError`, ", "`1`, "))
        out = self.run_hook("session_start.py", {"session_id": "s1", "source": "startup"}).stdout
        self.assertIn("Required on use", out)
        self.assertIn("docs/nope.md", out)
        self.assertIn("1", out)

    def test_session_start_is_quiet_when_valid(self):
        out = self.run_hook("session_start.py", {"session_id": "s1", "source": "startup"}).stdout
        self.assertNotIn("Required on use", out)


class InheritedRequiredOnUseTest(HookBase):
    def setUp(self):
        super().setUp()
        self.plugin = self.project / "Plugins/A"
        self.write(self.project / ".claude-harness/config.toml",
                   'version = 1\n[modules]\ndevelopment = true\n[projects]\nA = "Plugins/A"\n')
        self.write(self.plugin / ".claude-harness/config.toml", "version = 1\n[modules]\ndevelopment = true\n")
        self.plugin_rules = self.write(self.plugin / "docs/development/architecture.md",
                                       "# Plugin rules\n\n## Inherited rules\n\n| Project | Rules |\n|---|---|\n"
                                       "| root | `architecture.md`, `ui` |\n")

    def test_inherited_tables_apply_to_the_inheriting_project(self):
        self.read(self.plugin_rules)
        self.read(self.rules)
        self.read(self.scope)
        reason = self.write_tool("Plugins/A/src/x.js", "reportError(); showToast()")
        self.assertIn("docs/errors.md", reason)
        self.assertIn("docs/toast.md", reason)  # inherited scope applies regardless of its paths
        self.read(self.errors_doc)
        self.read(self.toast_doc)
        self.assertIsNone(self.write_tool("Plugins/A/src/x.js", "reportError(); showToast()"))

    def test_inherited_paths_are_relative_to_defining_project(self):
        self.write(self.project / "docs/development/architecture.md",
                   "# Core\n\n## Inherited rules\n\n| Project | Rules |\n|---|---|\n| A | `architecture.md` |\n")
        self.write(self.plugin / "docs/development/architecture.md",
                   "# Plugin\n\n## Required on use\n\n| Uses | Read |\n|---|---|\n| `plug` | `docs/p.md` |\n")
        doc = self.write(self.plugin / "docs/p.md", "# P\n")
        self.read(self.project / "docs/development/architecture.md")
        self.read(self.plugin / "docs/development/architecture.md")
        reason = self.write_tool("src/app.py", "plug()")
        self.assertIn("Plugins/A/docs/p.md", reason)
        self.read(doc)
        self.assertIsNone(self.write_tool("src/app.py", "plug()"))

    def test_session_start_reports_inherited_table_errors(self):
        self.write(self.rules, RULES.replace("`docs/errors.md`", "`docs/nope.md`"))
        out = self.run_hook("session_start.py", {"session_id": "s1", "source": "startup"}).stdout
        self.assertIn("Inherited rules", out)
        self.assertIn("docs/nope.md", out)


if __name__ == "__main__":
    unittest.main()
