import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from cloud_export import (
    MANIFEST_FILE,
    Change,
    ExportError,
    apply_changes,
    export_status,
    plan_export,
    read_manifest,
)

HOOKS = {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": 'python3 "${CLAUDE_PLUGIN_ROOT}/scripts/check.py"', "timeout": 5}]}]}}


def make_plugin(root: Path, version: str = "1.0.0") -> None:
    files = {
        ".claude-plugin/plugin.json": json.dumps({"name": "p", "version": version}),
        "hooks/hooks.json": json.dumps(HOOKS),
        "skills/todo/SKILL.md": "---\nname: todo\ndescription: d\n---\nRun ${CLAUDE_PLUGIN_ROOT}/scripts/check.py\n",
        "skills/daily/SKILL.md": "---\nname: daily\ndescription: d\n---\nBody\n",
        "skills/init/SKILL.md": "---\nname: init\ndescription: d\n---\n",
        "scripts/check.py": "print('check')\n",
        "scripts/__pycache__/check.pyc": "x",
        "templates/config.toml": "version = 1\n",
    }
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def by_path(changes: list[Change]) -> dict[str, Change]:
    return {c.path: c for c in changes}


def tree(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}


class PlanTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.plugin = Path(self.tmp.name) / "plugin"
        self.project = Path(self.tmp.name) / "project"
        make_plugin(self.plugin)
        (self.project / ".claude-harness").mkdir(parents=True)
        (self.project / ".claude-harness/config.toml").write_text("version = 1\n", encoding="utf-8")

    def export(self) -> list[Change]:
        changes = plan_export(self.plugin, self.project)
        apply_changes(self.project, changes)
        return changes


class FirstExportTest(PlanTestCase):
    def test_everything_is_created_and_nothing_else(self):
        changes = by_path(plan_export(self.plugin, self.project))
        self.assertEqual(
            sorted(changes),
            [
                ".claude-harness/runtime/manifest.json",
                ".claude-harness/runtime/scripts/check.py",
                ".claude-harness/runtime/templates/config.toml",
                ".claude/settings.json",
                ".claude/skills/harness-daily/SKILL.md",
                ".claude/skills/harness-todo/SKILL.md",
            ],
        )
        self.assertEqual({c.kind for c in changes.values()}, {"create"})

    def test_planning_writes_nothing(self):
        before = tree(self.project)
        plan_export(self.plugin, self.project)
        self.assertEqual(tree(self.project), before)

    def test_caches_and_local_only_skills_are_not_copied(self):
        paths = by_path(plan_export(self.plugin, self.project))
        self.assertFalse([p for p in paths if "__pycache__" in p or "harness-init" in p])

    def test_files_have_the_rewritten_content(self):
        self.export()
        skill = (self.project / ".claude/skills/harness-todo/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: harness-todo", skill)
        self.assertIn(".claude-harness/runtime/scripts/check.py", skill)
        settings = json.loads((self.project / ".claude/settings.json").read_text(encoding="utf-8"))
        self.assertIn(".claude-harness/runtime/scripts/check.py", settings["hooks"]["Stop"][0]["hooks"][0]["command"])

    def test_manifest_lists_version_and_hashes_of_the_generated_files(self):
        self.export()
        manifest = read_manifest(self.project)
        self.assertEqual(manifest["format"], 1)
        self.assertEqual(manifest["plugin_version"], "1.0.0")
        self.assertNotIn(MANIFEST_FILE.as_posix(), manifest["files"])
        self.assertNotIn(".claude/settings.json", manifest["files"])
        for path, digest in manifest["files"].items():
            self.assertEqual(digest, hashlib.sha256((self.project / path).read_bytes()).hexdigest(), path)
        self.assertEqual(len(manifest["files"]), 4)  # two skills, one script, one template

    def test_manifest_remembers_that_the_settings_file_was_created(self):
        self.export()
        self.assertTrue(read_manifest(self.project)["settings_created"])

    def test_no_manifest_before_the_first_export(self):
        self.assertIsNone(read_manifest(self.project))
        self.assertEqual(export_status(self.plugin, self.project), "missing")


class RepeatedExportTest(PlanTestCase):
    def test_a_second_run_has_nothing_to_do(self):
        self.export()
        self.assertEqual(plan_export(self.plugin, self.project), [])
        self.assertEqual(export_status(self.plugin, self.project), "current")

    def test_a_changed_plugin_file_is_an_update_and_marks_the_copy_outdated(self):
        self.export()
        (self.plugin / "scripts/check.py").write_text("print('new')\n", encoding="utf-8")
        changes = by_path(plan_export(self.plugin, self.project))
        self.assertEqual({p: c.kind for p, c in changes.items()}, {
            ".claude-harness/runtime/scripts/check.py": "update",
            ".claude-harness/runtime/manifest.json": "update",
        })
        self.assertEqual(export_status(self.plugin, self.project), "outdated")

    def test_a_new_plugin_version_updates_the_manifest(self):
        self.export()
        make_plugin(self.plugin, version="1.1.0")
        changes = by_path(plan_export(self.plugin, self.project))
        self.assertEqual(list(changes), [".claude-harness/runtime/manifest.json"])
        apply_changes(self.project, list(changes.values()))
        self.assertEqual(read_manifest(self.project)["plugin_version"], "1.1.0")

    def test_a_skill_that_left_the_plugin_is_deleted_from_the_project(self):
        self.export()
        (self.plugin / "skills/daily/SKILL.md").unlink()
        (self.plugin / "skills/daily").rmdir()
        changes = by_path(self.export())
        self.assertEqual(changes[".claude/skills/harness-daily/SKILL.md"].kind, "delete")
        self.assertFalse((self.project / ".claude/skills/harness-daily").exists())
        self.assertTrue((self.project / ".claude/skills/harness-todo/SKILL.md").exists())

    def test_a_copy_edited_by_hand_is_marked_and_replaced(self):
        self.export()
        target = self.project / ".claude/skills/harness-todo/SKILL.md"
        target.write_text("mine\n", encoding="utf-8")
        change = by_path(plan_export(self.plugin, self.project))[".claude/skills/harness-todo/SKILL.md"]
        self.assertEqual((change.kind, change.edited), ("update", True))
        self.export()
        self.assertIn("name: harness-todo", target.read_text(encoding="utf-8"))

    def test_a_missing_copied_file_is_created_again(self):
        self.export()
        (self.project / ".claude-harness/runtime/scripts/check.py").unlink()
        changes = by_path(plan_export(self.plugin, self.project))
        self.assertEqual(changes[".claude-harness/runtime/scripts/check.py"].kind, "create")


class SettingsTest(PlanTestCase):
    def write_settings(self, data: object, raw: str | None = None) -> Path:
        path = self.project / ".claude/settings.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(raw if raw is not None else json.dumps(data), encoding="utf-8")
        return path

    def test_foreign_settings_and_hooks_are_kept(self):
        foreign = {"type": "command", "command": "echo mine"}
        path = self.write_settings({"worktree": {"baseRef": "head"}, "hooks": {"Stop": [{"hooks": [foreign]}]}})
        change = by_path(plan_export(self.plugin, self.project))[".claude/settings.json"]
        self.assertEqual(change.kind, "update")
        apply_changes(self.project, plan_export(self.plugin, self.project))
        settings = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(settings["worktree"], {"baseRef": "head"})
        self.assertEqual(settings["hooks"]["Stop"][0], {"hooks": [foreign]})
        self.assertEqual(len(settings["hooks"]["Stop"]), 2)
        self.assertFalse(read_manifest(self.project)["settings_created"])

    def test_an_already_merged_file_in_another_format_is_not_touched(self):
        self.export()
        path = self.project / ".claude/settings.json"
        path.write_text(json.dumps(json.loads(path.read_text(encoding="utf-8"))), encoding="utf-8")
        self.assertEqual(plan_export(self.plugin, self.project), [])

    def test_invalid_json_stops_the_plan(self):
        path = self.write_settings(None, raw="{broken")
        with self.assertRaises(ExportError):
            plan_export(self.plugin, self.project)
        self.assertEqual(path.read_text(encoding="utf-8"), "{broken")

    def test_the_created_flag_survives_later_exports(self):
        self.export()
        make_plugin(self.plugin, version="2.0.0")
        self.export()
        self.assertTrue(read_manifest(self.project)["settings_created"])


class ApplyTest(PlanTestCase):
    def test_a_path_outside_the_project_is_refused(self):
        with self.assertRaises(ExportError):
            apply_changes(self.project, [Change("../outside.txt", "create", None, b"x")])
        self.assertFalse((self.project.parent / "outside.txt").exists())

    def test_an_absolute_path_is_refused(self):
        with self.assertRaises(ExportError):
            apply_changes(self.project, [Change("/tmp/x-cloud-export", "create", None, b"x")])

    def test_files_are_written_byte_for_byte(self):
        apply_changes(self.project, [Change("a/b.bin", "create", None, b"\x00\r\nx")])
        self.assertEqual((self.project / "a/b.bin").read_bytes(), b"\x00\r\nx")


if __name__ == "__main__":
    unittest.main()
