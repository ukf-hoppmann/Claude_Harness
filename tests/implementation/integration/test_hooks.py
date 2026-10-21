import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import SCRIPTS, item, write_backlog


class HookTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name)
        self.project = base / "project"
        self.data = base / "data"
        self.project.mkdir()
        self.todo_dir = self.project / "docs" / "todo"

    def tearDown(self):
        self._tmp.cleanup()

    def write_config(self, todo=True, path="todo", daily=False, backend="files"):
        config = self.project / ".claude-harness" / "config.toml"
        config.parent.mkdir(exist_ok=True)
        config.write_text(
            'version = 1\n[docs]\nroot = "docs"\n'
            f'[modules]\ntodo = {"true" if todo else "false"}\ndaily = {"true" if daily else "false"}\n'
            f'[todo]\npath = "{path}"\nbackend = "{backend}"\n'
        )

    def run_hook(self, script, payload):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project), CLAUDE_PLUGIN_DATA=str(self.data))
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            env=env,
        )

    def edit(self, file_path, session="s1"):
        return self.run_hook(
            "mark_backlog_dirty.py",
            {"session_id": session, "tool_name": "Edit", "tool_input": {"file_path": str(file_path)}},
        )

    def stop(self, session="s1", active=False):
        return self.run_hook("check_backlog.py", {"session_id": session, "stop_hook_active": active})

    def test_session_start_without_config(self):
        result = self.run_hook("session_start.py", {})
        self.assertEqual(result.returncode, 0)
        self.assertIn("/claude-harness:init", result.stdout)

    def test_session_start_reports_missing_backlog(self):
        self.write_config()
        result = self.run_hook("session_start.py", {})
        self.assertIn("does not exist", result.stdout)
        self.assertIn("ask for permission", result.stdout)
        self.assertFalse(self.todo_dir.exists())

    def test_session_start_reports_a_missing_cloud_copy(self):
        self.write_config()
        config = self.project / ".claude-harness" / "config.toml"
        config.write_text(config.read_text() + "[cloud]\nexport = true\n")
        result = self.run_hook("session_start.py", {})
        self.assertIn("Cloud copy:", result.stdout)
        self.assertIn("/claude-harness:update", result.stdout)

    def test_session_start_is_quiet_about_a_current_cloud_copy(self):
        self.write_config()
        config = self.project / ".claude-harness" / "config.toml"
        config.write_text(config.read_text() + "[cloud]\nexport = true\n")
        export = subprocess.run(
            [sys.executable, str(SCRIPTS / "cloud_export.py"), str(self.project), "--write"], capture_output=True, text=True
        )
        self.assertEqual(export.returncode, 0, export.stdout)
        self.assertNotIn("Cloud copy:", self.run_hook("session_start.py", {}).stdout)

    def test_session_start_is_quiet_about_the_cloud_copy_when_the_option_is_off(self):
        self.write_config()
        self.assertNotIn("Cloud copy:", self.run_hook("session_start.py", {}).stdout)

    def test_session_start_reports_a_cloud_copy_that_is_still_there_although_the_option_is_off(self):
        self.write_config()
        export = subprocess.run(
            [sys.executable, str(SCRIPTS / "cloud_export.py"), str(self.project), "--write"], capture_output=True, text=True
        )
        self.assertEqual(export.returncode, 0, export.stdout)
        self.assertIn("cloud.export is off", self.run_hook("session_start.py", {}).stdout)

    def test_the_copys_own_session_start_does_not_check_the_copy(self):
        self.write_config()
        config = self.project / ".claude-harness" / "config.toml"
        config.write_text(config.read_text() + "[cloud]\nexport = true\n")
        subprocess.run([sys.executable, str(SCRIPTS / "cloud_export.py"), str(self.project), "--write"], capture_output=True, text=True)
        copied = self.project / ".claude-harness/runtime/scripts/session_start.py"
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(self.project), CLAUDE_PLUGIN_DATA=str(self.data))
        result = subprocess.run([sys.executable, str(copied)], input="{}", capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Claude_Harness: modules", result.stdout)
        self.assertNotIn("Cloud copy:", result.stdout)

    def test_session_start_reports_module_off(self):
        self.write_config(todo=False)
        result = self.run_hook("session_start.py", {})
        self.assertIn("todo=off", result.stdout)
        self.assertNotIn("Backlog", result.stdout)

    def test_session_start_reports_invalid_config(self):
        config = self.project / ".claude-harness" / "config.toml"
        config.parent.mkdir()
        config.write_text("version = 7\n")
        self.assertIn("invalid configuration", self.run_hook("session_start.py", {}).stdout)

    def test_session_start_reports_backlog_errors(self):
        self.write_config()
        write_backlog(self.todo_dir, [item("STORY-001", Priority="Wrong")])
        self.assertIn("1 errors", self.run_hook("session_start.py", {}).stdout)

    def write_subprojects(self, broken=False, backend_a="files"):
        (self.project / ".claude-harness" / "config.toml").write_text(
            'version = 1\n[docs]\nlanguage = "de"\n[modules]\ntodo = true\n[todo]\nbackend = "files"\n'
            '[projects]\nA = "Plugins/A"\nB = "Plugins/B"\n'
        )
        write_backlog(self.todo_dir, [])
        a = self.project / "Plugins" / "A" / ".claude-harness" / "config.toml"
        a.parent.mkdir(parents=True)
        a.write_text(
            'version = 1\n[docs]\nlanguage = "en"\n[modules]\ntodo = true\ntechdocs = true\n'
            f'[todo]\nbackend = "{backend_a}"\n'
        )
        if not broken:
            b = self.project / "Plugins" / "B" / ".claude-harness" / "config.toml"
            b.parent.mkdir(parents=True)
            b.write_text("version = 1\n")

    def test_session_start_lists_subprojects(self):
        self.write_config()
        self.write_subprojects()
        out = self.run_hook("session_start.py", {}).stdout
        self.assertIn("projects root (.), A (Plugins/A), B (Plugins/B)", out)
        self.assertIn("Project root (.): language de; modules todo; backlog docs/todo/TODO.md", out)
        self.assertIn("Project A (Plugins/A): language en; modules techdocs, todo; backlog Plugins/A/docs/todo/TODO.md", out)
        self.assertIn("Project B (Plugins/B): language en; modules none", out)
        # Skill pointers appear once, however many projects use the module.
        self.assertEqual(out.count("skill claude-harness:todo"), 1)
        self.assertEqual(out.count("skill claude-harness:techdocs"), 1)
        self.assertIn("A: Backlog: Plugins/A/docs/todo/TODO.md does not exist", out)
        self.assertIn("A: Missing technical docs: Plugins/A/README.md", out)
        self.assertNotIn("daily", out)

    def test_session_start_api_backend_names_api_and_skips_check(self):
        self.write_config(backend="api")
        write_backlog(self.todo_dir, [item("STORY-001", Priority="Wrong")])
        out = self.run_hook("session_start.py", {}).stdout
        self.assertIn("Backlog: docs/todo via ToDo-Viewer API (http://localhost:5411/api);", out)
        self.assertNotIn("errors", out)

    def test_session_start_names_notes_module_without_network(self):
        self.write_config(backend="api")
        out = self.run_hook("session_start.py", {}).stdout
        self.assertIn("Notes: via ToDo-Viewer API (http://localhost:5411/api); rules in skill claude-harness:todo", out)
        self.write_config(backend="files")
        out = self.run_hook("session_start.py", {}).stdout
        self.assertNotIn("Notes:", out)

    def test_session_start_api_backend_does_not_require_todo_file(self):
        self.write_config(backend="api")
        out = self.run_hook("session_start.py", {}).stdout
        self.assertNotIn("does not exist", out)
        self.assertIn("via ToDo-Viewer API", out)

    def test_session_start_files_backend_reports_missing_backlog(self):
        self.write_config(backend="files")
        self.assertIn("does not exist", self.run_hook("session_start.py", {}).stdout)

    def test_session_start_subproject_with_api_backend(self):
        self.write_config()
        self.write_subprojects(backend_a="api")
        write_backlog(self.project / "Plugins/A/docs/todo", [item("STORY-001", Priority="Wrong")])
        out = self.run_hook("session_start.py", {}).stdout
        self.assertIn("backlog Plugins/A/docs/todo via API", out)
        self.assertIn("backlog docs/todo/TODO.md", out)
        self.assertNotIn("A: Backlog check", out)

    def test_session_start_reports_broken_subproject(self):
        self.write_config()
        self.write_subprojects(broken=True)
        out = self.run_hook("session_start.py", {}).stdout
        self.assertIn("Project B (Plugins/B): Plugins/B/.claude-harness/config.toml does not exist; its files get no harness rules.", out)
        self.assertIn("Project A (Plugins/A)", out)

    def test_backlog_edit_in_worktree_is_checked(self):
        self.write_config()
        worktree = self.project / ".claude/worktrees/w1"
        (worktree / ".claude-harness").mkdir(parents=True)
        (worktree / ".claude-harness/config.toml").write_text(
            (self.project / ".claude-harness/config.toml").read_text()
        )
        write_backlog(worktree / "docs/todo", [item("STORY-001", Priority="Wrong")])
        self.run_hook("mark_backlog_dirty.py", {
            "session_id": "s1", "cwd": str(worktree), "tool_name": "Edit",
            "tool_input": {"file_path": str(worktree / "docs/todo/TODO.md")},
        })
        result = self.run_hook("check_backlog.py", {"session_id": "s1", "cwd": str(worktree)})
        self.assertEqual(result.returncode, 2)
        self.assertIn("Priority", result.stderr)

    def test_subproject_backlog_is_checked_alone(self):
        self.write_config()
        self.write_subprojects()
        write_backlog(self.todo_dir, [item("STORY-001", Priority="Wrong")])
        plugin_todo = self.project / "Plugins/A/docs/todo"
        write_backlog(plugin_todo, [item("STORY-001", Priority="Wrong")])
        self.edit(plugin_todo / "TODO.md")
        result = self.stop()
        self.assertEqual(result.returncode, 2)
        self.assertIn("after your edits in Plugins/A/docs/todo:", result.stderr)
        self.assertNotIn("in docs/todo:", result.stderr)
        write_backlog(plugin_todo, [item("STORY-001")])
        self.assertEqual(self.stop().returncode, 0)
        # The marker is gone once the plugin backlog is valid.
        self.assertEqual(self.stop().returncode, 0)

    def test_root_and_subproject_backlogs_reported_separately(self):
        self.write_config()
        self.write_subprojects()
        write_backlog(self.todo_dir, [item("STORY-001", Priority="Wrong")])
        plugin_todo = self.project / "Plugins/A/docs/todo"
        write_backlog(plugin_todo, [item("STORY-002", Priority="Wrong")])
        self.edit(self.todo_dir / "TODO.md")
        self.edit(plugin_todo / "TODO.md")
        result = self.stop()
        self.assertIn("after your edits in docs/todo:", result.stderr)
        self.assertIn("after your edits in Plugins/A/docs/todo:", result.stderr)

    def test_stop_without_backlog_edit_does_nothing(self):
        self.write_config()
        write_backlog(self.todo_dir, [item("STORY-001", Priority="Wrong")])
        self.edit(self.project / "src" / "main.py")
        self.assertEqual(self.stop().returncode, 0)

    def test_stop_blocks_invalid_backlog_once(self):
        self.write_config()
        write_backlog(self.todo_dir, [item("STORY-001", Priority="Wrong")])
        self.edit(self.todo_dir / "TODO.md")
        first = self.stop()
        self.assertEqual(first.returncode, 2)
        self.assertIn("Priority must be one of", first.stderr)
        self.assertEqual(self.stop(active=True).returncode, 0)

    def test_stop_clears_marker_when_valid(self):
        self.write_config()
        write_backlog(self.todo_dir, [item("STORY-001", Priority="Wrong")])
        self.edit(self.todo_dir / "TODO.md")
        self.assertEqual(self.stop().returncode, 2)
        write_backlog(self.todo_dir, [item("STORY-001")])
        self.assertEqual(self.stop().returncode, 0)
        write_backlog(self.todo_dir, [item("STORY-001", Priority="Wrong")])
        self.assertEqual(self.stop().returncode, 0)

    def test_stop_delivers_new_notice_once_per_session(self):
        self.write_config()
        write_backlog(self.todo_dir, [
            item("EPIC-001", Type="Epic", Status="In progress"),
            item("STORY-001", Parent="`EPIC-001`", Required_for_parent="Yes",
                 Status="Completed", Resolution="Confirmed."),
        ])
        self.edit(self.todo_dir / "TODO.md")
        first = self.stop()
        self.assertEqual(first.returncode, 2)
        self.assertIn("EPIC-001: all required children are Completed", first.stderr)
        self.edit(self.todo_dir / "TODO.md")
        self.assertEqual(self.stop().returncode, 0)
        self.edit(self.todo_dir / "TODO.md", session="s2")
        self.assertEqual(self.stop(session="s2").returncode, 2)

    def test_module_off_skips_check(self):
        self.write_config(todo=False)
        write_backlog(self.todo_dir, [item("STORY-001", Priority="Wrong")])
        self.edit(self.todo_dir / "TODO.md")
        self.assertEqual(self.stop().returncode, 0)

    def test_api_backend_skips_backlog_check(self):
        self.write_config(backend="api")
        write_backlog(self.todo_dir, [item("STORY-001", Priority="Wrong")])
        self.edit(self.todo_dir / "TODO.md")
        result = self.stop()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")

    NOTES_LOG = "## 2026-10-01 — First\n\n### Discussed\n\n- a\n\n## 2026-10-02 — Second\n\n### Decided\n\n- b\n"

    def write_notes(self, identifier="STORY-001", head=True, decided=1, log=NOTES_LOG):
        path = self.todo_dir / "items" / identifier / f"{identifier}_notes.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        text = f"# {identifier} — Title\n\n"
        if head:
            points = "".join(f"  - d{i}\n" for i in range(decided))
            text += f"## State\n\n- Goal/Status: g\n- Decided:\n{points}- References: none\n\n"
        path.write_text(text + log)
        return path

    def confirm(self, identifier="STORY-001"):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "backlog.py"), str(self.todo_dir), "--confirm-state", identifier],
            capture_output=True, text=True,
        )

    def test_stop_blocks_changed_notes_with_stale_head_until_confirmed(self):
        self.write_config()
        write_backlog(self.todo_dir, [item("STORY-001")])
        self.edit(self.write_notes())
        first = self.stop()
        self.assertEqual(first.returncode, 2)
        self.assertIn("STORY-001_notes.md", first.stderr)
        self.assertIn("stale", first.stderr)
        self.assertIn("--confirm-state STORY-001", first.stderr)
        self.assertEqual(self.stop().returncode, 2)
        self.assertEqual(self.confirm().returncode, 0)
        self.assertEqual(self.stop().returncode, 0)

    def test_stop_blocks_changed_notes_without_head(self):
        self.write_config()
        write_backlog(self.todo_dir, [item("STORY-001")])
        self.edit(self.write_notes(head=False))
        result = self.stop()
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing", result.stderr)

    def test_stop_ignores_old_notes_that_were_not_changed(self):
        self.write_config()
        write_backlog(self.todo_dir, [item("STORY-001")])
        self.write_notes(head=False)
        self.edit(self.todo_dir / "TODO.md")
        self.assertEqual(self.stop().returncode, 0)

    def test_stop_does_not_check_the_head_of_a_spec(self):
        self.write_config()
        write_backlog(self.todo_dir, [item("STORY-001")])
        spec = self.todo_dir / "items" / "STORY-001" / "STORY-001_spec.md"
        spec.parent.mkdir(parents=True)
        spec.write_text("# Spec\n")
        self.edit(spec)
        self.assertEqual(self.stop().returncode, 0)

    def test_stop_does_not_loop_on_a_stale_head(self):
        self.write_config()
        write_backlog(self.todo_dir, [item("STORY-001")])
        self.edit(self.write_notes())
        self.assertEqual(self.stop(active=True).returncode, 0)

    def test_stop_gives_a_long_head_notice_once(self):
        self.write_config()
        write_backlog(self.todo_dir, [item("STORY-001")])
        self.write_notes(decided=16)
        self.assertEqual(self.confirm().returncode, 0)
        self.edit(self.todo_dir / "items" / "STORY-001" / "STORY-001_notes.md")
        first = self.stop()
        self.assertEqual(first.returncode, 2)
        self.assertIn("more than 15 points", first.stderr)
        self.edit(self.todo_dir / "items" / "STORY-001" / "STORY-001_notes.md")
        self.assertEqual(self.stop().returncode, 0)

    def git(self, *args):
        subprocess.run(["git", "-C", str(self.project), *args], check=True, capture_output=True)

    def test_stop_notices_a_rewritten_log_against_git(self):
        self.write_config()
        write_backlog(self.todo_dir, [item("STORY-001")])
        path = self.write_notes()
        self.assertEqual(self.confirm().returncode, 0)
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "init")
        path.write_text(path.read_text().replace("- a\n", "- rewritten\n"))
        self.assertEqual(self.confirm().returncode, 0)
        self.edit(path)
        result = self.stop()
        self.assertEqual(result.returncode, 2)
        self.assertIn("earlier log entry", result.stderr)

    def test_stop_without_git_gives_no_rewrite_notice(self):
        self.write_config()
        write_backlog(self.todo_dir, [item("STORY-001")])
        self.write_notes()
        self.assertEqual(self.confirm().returncode, 0)
        self.edit(self.todo_dir / "items" / "STORY-001" / "STORY-001_notes.md")
        self.assertEqual(self.stop().returncode, 0)

    def test_api_backend_skips_notes_head_check(self):
        self.write_config(backend="api")
        write_backlog(self.todo_dir, [item("STORY-001")])
        self.edit(self.write_notes())
        result = self.stop()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")

    def test_custom_todo_path(self):
        self.write_config(path="planning")
        planning = self.project / "docs" / "planning"
        write_backlog(planning, [item("STORY-001", Priority="Wrong")])
        self.edit(planning / "TODO.md")
        self.assertEqual(self.stop().returncode, 2)


if __name__ == "__main__":
    unittest.main()
