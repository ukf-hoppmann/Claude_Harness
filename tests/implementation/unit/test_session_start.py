import unittest
from pathlib import Path
from unittest import mock

import helpers  # noqa: F401  (adds plugin/scripts to sys.path)
from harness_config import ConfigOutdated, parse_config
from session_start import cloud_sync_lines, outdated_message


class OutdatedMessageTest(unittest.TestCase):
    def test_names_versions_and_pending_changes(self):
        exc = ConfigOutdated(1, 2, ("add [widgets] table",))
        message = outdated_message(exc)
        self.assertIn(str(exc), message)
        self.assertIn("/claude-harness:update", message)

    def test_pending_change_count_is_visible(self):
        exc = ConfigOutdated(1, 3, ("step one", "step two"))
        self.assertIn("2 pending change(s)", outdated_message(exc))


class CloudSyncLinesTest(unittest.TestCase):
    """The branch sync runs only at the start of a cloud session with cloud.sync on."""

    ROOT = Path("/project")

    def _lines(self, *, remote="true", source="startup", cloud=None, result="Git: fast-forwarded main."):
        config = parse_config({"version": 1, **({"cloud": cloud} if cloud is not None else {})})
        sync = mock.Mock(return_value=result)
        env = {"CLAUDE_CODE_REMOTE": remote} if remote is not None else {}
        with mock.patch.dict("os.environ", env, clear=True):
            lines = cloud_sync_lines({"source": source}, config, self.ROOT, sync=sync)
        return lines, sync

    def test_runs_at_cloud_startup(self):
        lines, sync = self._lines()
        sync.assert_called_once_with(self.ROOT)
        self.assertEqual(lines, ["Git: fast-forwarded main."])

    def test_nothing_to_say(self):
        lines, sync = self._lines(result=None)
        sync.assert_called_once()
        self.assertEqual(lines, [])

    def test_not_in_local_sessions(self):
        for remote in (None, "false", ""):
            with self.subTest(remote=remote):
                lines, sync = self._lines(remote=remote)
                sync.assert_not_called()
                self.assertEqual(lines, [])

    def test_only_at_startup(self):
        for source in ("resume", "clear", "compact", None):
            with self.subTest(source=source):
                lines, sync = self._lines(source=source)
                sync.assert_not_called()
                self.assertEqual(lines, [])

    def test_switched_off(self):
        lines, sync = self._lines(cloud={"export": True, "sync": False})
        sync.assert_not_called()
        self.assertEqual(lines, [])


if __name__ == "__main__":
    unittest.main()
