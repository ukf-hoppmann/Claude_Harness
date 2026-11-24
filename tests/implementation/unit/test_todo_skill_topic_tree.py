import re
import unittest

from helpers import REPO_ROOT

SKILL = REPO_ROOT / "plugin" / "skills" / "todo"
TOOLS = [
    "mindmap_get_tree",
    "mindmap_create_item_at_node",
    "mindmap_assign_item",
    "mindmap_create_node",
    "backlog_create_item",
]


class TopicTreeRuleTest(unittest.TestCase):
    def setUp(self):
        self.skill = (SKILL / "SKILL.md").read_text()
        self.api = (SKILL / "api.md").read_text()

    def test_every_tool_is_named_in_the_rule_and_in_the_table(self):
        for tool in TOOLS:
            with self.subTest(tool=tool):
                self.assertIn(f"`{tool}`", self.skill)
                self.assertRegex(self.api, rf"(?m)^\| `{tool}` \|")

    def test_skill_and_table_name_the_same_tools(self):
        in_table = set(re.findall(r"^\| `((?:mindmap|backlog)_\w+)` \|", self.api, re.M))
        self.assertEqual(in_table, set(TOOLS))
        in_rule = set(re.findall(r"`((?:mindmap_get_tree|mindmap_create_\w+|mindmap_assign_item|backlog_create_item))`", self.skill))
        self.assertEqual(in_rule, set(TOOLS))

    def test_rule_needs_the_owners_yes_for_a_new_node(self):
        self.assertIn("only after the owner's yes", self.skill)

    def test_file_mode_has_its_own_rule(self):
        self.assertNotIn("does not apply yet", self.skill)
        self.assertIn("Files mode, creating an item", self.skill)
        self.assertIn("mindmap/project.md", self.skill)
        self.assertIn("do not create it", self.skill)

    def test_format_describes_the_mindmap_files_and_rules(self):
        fmt = (SKILL / "format.md").read_text()
        self.assertIn("## Mindmap (files mode)", fmt)
        for text in ("mindmap/project.md", "new-<shortname>", "Delete nothing", "# NEW", "Items:", "Memos:"):
            with self.subTest(text=text):
                self.assertIn(text, fmt)

    def test_link_target_exists(self):
        self.assertIn("## Topic tree (MCP tools of the viewer)", self.api)
        self.assertIn("api.md#topic-tree-mcp-tools-of-the-viewer", self.skill)


if __name__ == "__main__":
    unittest.main()
