import json
import re
import unittest

from helpers import REPO_ROOT
from cloud_export import (
    MANAGED_MARK,
    ExportError,
    dump_settings,
    hook_entries,
    merge_hooks,
    parse_settings,
    remove_hooks,
)

PLUGIN_HOOKS = json.loads((REPO_ROOT / "plugin/hooks/hooks.json").read_text(encoding="utf-8"))
GUARD = '[ "$CLAUDE_CODE_REMOTE" != "true" ] || '
SESSION_START = (
    GUARD + 'python3 "${CLAUDE_PROJECT_DIR:-.}/.claude-harness/runtime/scripts/session_start.py"'
)
FOREIGN = {"type": "command", "command": "echo foreign"}


def commands(hooks: dict) -> list[str]:
    return [h["command"] for groups in hooks.values() for g in groups for h in g["hooks"]]


class HookEntriesTest(unittest.TestCase):
    def setUp(self):
        self.entries = hook_entries(PLUGIN_HOOKS)

    def test_same_events_matchers_and_timeouts_as_the_plugin(self):
        self.assertEqual(self.entries.keys(), PLUGIN_HOOKS["hooks"].keys())
        for event, groups in PLUGIN_HOOKS["hooks"].items():
            self.assertEqual([g.get("matcher") for g in groups], [g.get("matcher") for g in self.entries[event]])
            self.assertEqual(
                [h["timeout"] for g in groups for h in g["hooks"]],
                [h["timeout"] for g in self.entries[event] for h in g["hooks"]],
            )

    def test_session_start_command_is_exact(self):
        self.assertEqual(self.entries["SessionStart"][0]["hooks"][0]["command"], SESSION_START)

    def test_every_command_is_guarded_marked_and_free_of_the_plugin_variable(self):
        for command in commands(self.entries):
            self.assertTrue(command.startswith(GUARD), command)
            self.assertIn(MANAGED_MARK, command)
            self.assertNotIn("CLAUDE_PLUGIN_ROOT", command)

    def test_the_same_scripts_are_called(self):
        def scripts(hooks):
            return [re.search(r"scripts/(\w+\.py)", c).group(1) for c in commands(hooks)]

        self.assertEqual(scripts(self.entries), scripts(PLUGIN_HOOKS["hooks"]))

    def test_the_plugin_data_is_not_modified(self):
        before = json.dumps(PLUGIN_HOOKS, sort_keys=True)
        hook_entries(PLUGIN_HOOKS)
        self.assertEqual(json.dumps(PLUGIN_HOOKS, sort_keys=True), before)


class MergeHooksTest(unittest.TestCase):
    def setUp(self):
        self.entries = hook_entries(PLUGIN_HOOKS)

    def test_into_empty_settings(self):
        result = merge_hooks({}, self.entries)
        self.assertEqual(result["hooks"], self.entries)

    def test_other_keys_stay(self):
        settings = {"worktree": {"baseRef": "head"}, "enabledPlugins": {"x@y": True}}
        result = merge_hooks(settings, self.entries)
        self.assertEqual(result["worktree"], {"baseRef": "head"})
        self.assertEqual(result["enabledPlugins"], {"x@y": True})

    def test_foreign_hooks_stay_and_come_first(self):
        settings = {"hooks": {"Stop": [{"hooks": [FOREIGN]}], "Notification": [{"hooks": [FOREIGN]}]}}
        result = merge_hooks(settings, self.entries)
        self.assertEqual(result["hooks"]["Stop"][0], {"hooks": [FOREIGN]})
        self.assertEqual(len(result["hooks"]["Stop"]), 1 + len(self.entries["Stop"]))
        self.assertEqual(result["hooks"]["Notification"], [{"hooks": [FOREIGN]}])

    def test_merging_twice_gives_the_same_result(self):
        once = merge_hooks({"hooks": {"Stop": [{"hooks": [FOREIGN]}]}}, self.entries)
        self.assertEqual(merge_hooks(once, self.entries), once)

    def test_an_old_managed_entry_is_replaced_not_duplicated(self):
        old = {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": f"python3 {MANAGED_MARK}old.py"}]}]}}
        result = merge_hooks(old, self.entries)
        self.assertNotIn("old.py", " ".join(commands(result["hooks"])))

    def test_a_mixed_group_keeps_only_the_foreign_hook(self):
        managed = {"type": "command", "command": f"python3 {MANAGED_MARK}old.py"}
        settings = {"hooks": {"Stop": [{"matcher": "x", "hooks": [FOREIGN, managed]}]}}
        result = merge_hooks(settings, {})
        self.assertEqual(result["hooks"]["Stop"], [{"matcher": "x", "hooks": [FOREIGN]}])

    def test_the_input_is_not_modified(self):
        settings = {"hooks": {"Stop": [{"hooks": [FOREIGN]}]}}
        before = json.dumps(settings)
        merge_hooks(settings, self.entries)
        self.assertEqual(json.dumps(settings), before)

    def test_hooks_that_is_no_object_is_an_error(self):
        with self.assertRaises(ExportError):
            merge_hooks({"hooks": []}, self.entries)


class RemoveHooksTest(unittest.TestCase):
    def test_removes_only_the_managed_entries(self):
        settings = {"worktree": {"baseRef": "head"}, "hooks": {"Stop": [{"hooks": [FOREIGN]}]}}
        merged = merge_hooks(settings, hook_entries(PLUGIN_HOOKS))
        self.assertEqual(remove_hooks(merged), settings)

    def test_round_trip_of_empty_settings_leaves_no_hooks_key(self):
        merged = merge_hooks({}, hook_entries(PLUGIN_HOOKS))
        self.assertEqual(remove_hooks(merged), {})

    def test_hooks_without_managed_entries_are_untouched(self):
        settings = {"hooks": {"Stop": [{"hooks": [FOREIGN]}]}}
        self.assertEqual(remove_hooks(settings), settings)


class ParseSettingsTest(unittest.TestCase):
    def test_empty_text_is_empty_settings(self):
        self.assertEqual(parse_settings(""), {})
        self.assertEqual(parse_settings("  \n"), {})

    def test_object_is_parsed(self):
        self.assertEqual(parse_settings('{"a": 1}'), {"a": 1})

    def test_invalid_json_is_an_error(self):
        with self.assertRaises(ExportError):
            parse_settings("{not json")

    def test_a_list_is_an_error(self):
        with self.assertRaises(ExportError):
            parse_settings("[1]")

    def test_dump_is_stable_and_ends_with_a_newline(self):
        text = dump_settings({"b": 1, "a": {"ä": 2}})
        self.assertEqual(text, '{\n  "b": 1,\n  "a": {\n    "ä": 2\n  }\n}\n')
        self.assertEqual(parse_settings(text), {"b": 1, "a": {"ä": 2}})


if __name__ == "__main__":
    unittest.main()
