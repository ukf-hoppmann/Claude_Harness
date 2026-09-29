import unittest

import helpers  # noqa: F401  (adds plugin/scripts to sys.path)
from harness_config import ConfigOutdated
from session_start import outdated_message


class OutdatedMessageTest(unittest.TestCase):
    def test_names_versions_and_pending_changes(self):
        exc = ConfigOutdated(1, 2, ("add [widgets] table",))
        message = outdated_message(exc)
        self.assertIn(str(exc), message)
        self.assertIn("/claude-harness:update", message)

    def test_pending_change_count_is_visible(self):
        exc = ConfigOutdated(1, 3, ("step one", "step two"))
        self.assertIn("2 pending change(s)", outdated_message(exc))


if __name__ == "__main__":
    unittest.main()
