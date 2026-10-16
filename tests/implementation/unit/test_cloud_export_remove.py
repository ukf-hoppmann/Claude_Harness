import json
import unittest
from pathlib import Path

from cloud_export import ExportError, apply_changes, export_status, plan_export, plan_remove, read_manifest

from . import test_cloud_export_plan as base

FOREIGN = {"type": "command", "command": "echo mine"}
# Deliberately not in the format the export writes, so that only an exact restore reproduces it.
ORIGINAL_SETTINGS = '{"worktree": { "baseRef": "head" },\n  "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo mine"}]}]}}\n'


class RemoveTestCase(base.PlanTestCase):
    def remove(self):
        changes, kept = plan_remove(self.project)
        apply_changes(self.project, changes)
        return changes, kept

    def write(self, relative: str, content: str) -> Path:
        path = self.project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path


class RoundTripTest(RemoveTestCase):
    def test_export_then_removal_restores_the_project_exactly(self):
        self.write(".claude/skills/own/SKILL.md", "my own skill\n")
        self.write("README.md", "readme\n")
        before = base.tree(self.project)
        self.export()
        self.assertNotEqual(base.tree(self.project), before)
        self.remove()
        self.assertEqual(base.tree(self.project), before)

    def test_a_settings_file_that_existed_comes_back_byte_for_byte(self):
        self.write(".claude/settings.json", ORIGINAL_SETTINGS)
        before = base.tree(self.project)
        self.export()
        self.remove()
        self.assertEqual(base.tree(self.project), before)

    def test_the_original_survives_an_update_in_between(self):
        self.write(".claude/settings.json", ORIGINAL_SETTINGS)
        before = base.tree(self.project)
        self.export()
        base.make_plugin(self.plugin, version="2.0.0")
        (self.plugin / "scripts/check.py").write_text("print('v2')\n", encoding="utf-8")
        self.export()
        self.remove()
        self.assertEqual(base.tree(self.project), before)

    def test_the_status_after_the_removal_is_missing(self):
        self.export()
        self.remove()
        self.assertEqual(export_status(self.plugin, self.project), "missing")
        self.assertIsNone(read_manifest(self.project))


class PlanTest(RemoveTestCase):
    def test_planning_writes_nothing(self):
        self.export()
        before = base.tree(self.project)
        plan_remove(self.project)
        self.assertEqual(base.tree(self.project), before)

    def test_everything_the_manifest_lists_is_deleted_together_with_the_manifest(self):
        self.export()
        changes, kept = plan_remove(self.project)
        paths = {c.path for c in changes if c.kind == "delete"}
        self.assertEqual(kept, [])
        self.assertEqual(paths, {
            ".claude-harness/runtime/manifest.json",
            ".claude-harness/runtime/scripts/check.py",
            ".claude-harness/runtime/templates/config.toml",
            ".claude/settings.json",
            ".claude/skills/harness-daily/SKILL.md",
            ".claude/skills/harness-todo/SKILL.md",
        })

    def test_the_config_and_the_runtime_folder_leave_no_leftovers(self):
        self.export()
        self.remove()
        self.assertEqual(sorted(base.tree(self.project)), [".claude-harness/config.toml"])
        self.assertFalse((self.project / ".claude-harness/runtime").exists())

    def test_without_a_copy_there_is_nothing_to_remove(self):
        with self.assertRaises(ExportError):
            plan_remove(self.project)


class HandEditedTest(RemoveTestCase):
    def test_a_file_edited_by_hand_stays_and_is_reported(self):
        self.export()
        edited = self.project / ".claude/skills/harness-todo/SKILL.md"
        edited.write_text("my version\n", encoding="utf-8")
        changes, kept = self.remove()
        self.assertEqual(kept, [".claude/skills/harness-todo/SKILL.md"])
        self.assertEqual(edited.read_text(encoding="utf-8"), "my version\n")
        self.assertFalse((self.project / ".claude/skills/harness-daily").exists())
        self.assertNotIn(".claude/skills/harness-todo/SKILL.md", {c.path for c in changes})

    def test_a_settings_file_edited_after_the_export_keeps_the_new_content(self):
        self.write(".claude/settings.json", ORIGINAL_SETTINGS)
        self.export()
        path = self.project / ".claude/settings.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["hooks"]["Notification"] = [{"hooks": [FOREIGN]}]
        data["model"] = "x"
        path.write_text(json.dumps(data), encoding="utf-8")
        changes, _ = self.remove()
        settings = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(settings["model"], "x")
        self.assertEqual(settings["hooks"]["Notification"], [{"hooks": [FOREIGN]}])
        self.assertEqual(settings["hooks"]["Stop"], [{"hooks": [FOREIGN]}])
        self.assertNotIn("runtime/scripts", path.read_text(encoding="utf-8"))
        change = next(c for c in changes if c.path == ".claude/settings.json")
        self.assertTrue(change.edited)

    def test_an_edited_settings_file_that_holds_nothing_else_is_deleted_when_the_export_created_it(self):
        self.export()
        path = self.project / ".claude/settings.json"
        path.write_text(path.read_text(encoding="utf-8") + "\n\n", encoding="utf-8")
        self.remove()
        self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
