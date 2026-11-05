import tempfile
import unittest
from pathlib import Path

from helpers import REPO_ROOT
import cloud_export
from cloud_export import RUNTIME_DIR, SKILL_PREFIX, rewrite_skill_text, skill_files

PLUGIN = REPO_ROOT / "plugin"
EXPECTED_SKILLS = {
    "architecture",
    "conflicts",
    "daily",
    "decomposition",
    "interfaces",
    "semver",
    "techdocs",
    "testing",
    "todo",
}
FRONT = "---\nname: todo\ndescription: Rules for the backlog.\n---\n"


class RewriteSkillTextTest(unittest.TestCase):
    def test_prefixes_the_skill_name_only(self):
        result = rewrite_skill_text(FRONT + "# Todo\n", frozenset({"todo"}))
        self.assertIn("name: harness-todo\n", result)
        self.assertIn("description: Rules for the backlog.\n", result)

    def test_only_the_frontmatter_name_is_changed(self):
        text = FRONT + "# Todo\n\nname: not-a-skill-name\n"
        result = rewrite_skill_text(text, frozenset({"todo"}))
        self.assertIn("\nname: not-a-skill-name\n", result)

    def test_text_without_frontmatter_keeps_its_name_lines(self):
        result = rewrite_skill_text("name: todo\n", frozenset({"todo"}))
        self.assertEqual(result, "name: todo\n")

    def test_reference_to_an_exported_skill_is_prefixed(self):
        text = FRONT + "Load skill `claude-harness:daily` and `claude-harness:todo`.\n"
        result = rewrite_skill_text(text, frozenset({"todo", "daily"}))
        self.assertIn("`harness-daily`", result)
        self.assertIn("`harness-todo`", result)
        self.assertNotIn("claude-harness:", result)

    def test_reference_to_a_skill_that_is_not_exported_stays(self):
        text = FRONT + "Run `/claude-harness:init` or load `claude-harness:worktree`.\n"
        result = rewrite_skill_text(text, frozenset({"todo"}))
        self.assertIn("`/claude-harness:init`", result)
        self.assertIn("`claude-harness:worktree`", result)

    def test_plugin_root_becomes_a_project_relative_runtime_path(self):
        text = FRONT + 'Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/backlog.py" docs/todo`.\n'
        result = rewrite_skill_text(text, frozenset({"todo"}))
        self.assertIn('python3 ".claude-harness/runtime/scripts/backlog.py" docs/todo', result)
        self.assertNotIn("CLAUDE_PLUGIN_ROOT", result)

    def test_line_endings_are_kept(self):
        text = "---\r\nname: todo\r\n---\r\nBody ${CLAUDE_PLUGIN_ROOT}/x\r\n"
        result = rewrite_skill_text(text, frozenset({"todo"}))
        self.assertEqual(result, "---\r\nname: harness-todo\r\n---\r\nBody .claude-harness/runtime/x\r\n")


def write_skill(root: Path, name: str, files: dict[str, str]) -> None:
    for relative, content in files.items():
        path = root / "skills" / name / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


class SkillFilesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.plugin = Path(self.tmp.name)
        write_skill(self.plugin, "todo", {
            "SKILL.md": "---\nname: todo\ndescription: d\n---\nSee `claude-harness:daily`.\n",
            "api.md": "Run ${CLAUDE_PLUGIN_ROOT}/scripts/backlog_api.py\n",
        })
        write_skill(self.plugin, "daily", {"SKILL.md": "---\nname: daily\ndescription: d\n---\nBody\n"})
        for local_only in ("init", "update", "worktree"):
            write_skill(self.plugin, local_only, {"SKILL.md": f"---\nname: {local_only}\ndescription: d\n---\n"})
        (self.plugin / "skills" / "todo" / "__pycache__").mkdir()
        (self.plugin / "skills" / "todo" / "__pycache__" / "x.pyc").write_bytes(b"\x00")

    def test_exports_every_file_of_the_exported_skills_below_the_prefixed_folder(self):
        files = skill_files(self.plugin)
        self.assertEqual(
            sorted(files),
            [
                ".claude/skills/harness-daily/SKILL.md",
                ".claude/skills/harness-todo/SKILL.md",
                ".claude/skills/harness-todo/api.md",
            ],
        )

    def test_init_update_and_worktree_stay_local(self):
        names = cloud_export.exported_skill_names(self.plugin)
        self.assertEqual(names, ["daily", "todo"])

    def test_texts_are_rewritten_with_the_exported_set(self):
        files = skill_files(self.plugin)
        skill = files[".claude/skills/harness-todo/SKILL.md"].decode("utf-8")
        self.assertIn("name: harness-todo", skill)
        self.assertIn("`harness-daily`", skill)
        api = files[".claude/skills/harness-todo/api.md"].decode("utf-8")
        self.assertIn(".claude-harness/runtime/scripts/backlog_api.py", api)

    def test_result_is_deterministic(self):
        self.assertEqual(list(skill_files(self.plugin)), list(skill_files(self.plugin)))


class RealPluginTest(unittest.TestCase):
    def test_the_expected_skills_are_exported(self):
        self.assertEqual(set(cloud_export.exported_skill_names(PLUGIN)), EXPECTED_SKILLS)

    def test_no_placeholder_and_no_unprefixed_skill_name_remains(self):
        files = skill_files(PLUGIN)
        self.assertTrue(files)
        for path, data in files.items():
            text = data.decode("utf-8")
            self.assertNotIn("CLAUDE_PLUGIN_ROOT", text, path)
            for name in EXPECTED_SKILLS:
                self.assertNotIn(f"claude-harness:{name}", text, path)

    def test_every_skill_name_carries_the_prefix(self):
        files = skill_files(PLUGIN)
        for name in EXPECTED_SKILLS:
            skill = files[f".claude/skills/{SKILL_PREFIX}{name}/SKILL.md"].decode("utf-8")
            self.assertIn(f"\nname: {SKILL_PREFIX}{name}\n", skill)

    def test_runtime_dir_is_the_project_relative_copy_folder(self):
        self.assertEqual(RUNTIME_DIR.as_posix(), ".claude-harness/runtime")


if __name__ == "__main__":
    unittest.main()


class RealPluginExportTest(unittest.TestCase):
    """The cloud copy carries the interfaces skill and the development templates of the real plugin."""

    def test_interfaces_skill_and_development_templates_are_exported(self):
        plugin = PLUGIN
        self.assertIn("interfaces", cloud_export.exported_skill_names(plugin))
        self.assertIn(".claude/skills/harness-interfaces/SKILL.md", skill_files(plugin))
        runtime = cloud_export.runtime_files(plugin)
        for name in ("architecture", "scope", "interfaces", "interface", "catalog"):
            self.assertIn(f".claude-harness/runtime/templates/development/{name}.md", runtime)
