import unittest

from cloud_export import copy_problem

from . import test_cloud_export_plan as base


class CopyProblemTest(base.PlanTestCase):
    def problem(self, wanted: bool, plugin_root=None):
        return copy_problem(self.project, wanted, plugin_root or self.plugin)

    def test_wanted_but_missing(self):
        message = self.problem(True)
        self.assertIn("no copy", message)
        self.assertIn("/claude-harness:update", message)

    def test_wanted_and_current_is_quiet(self):
        self.export()
        self.assertIsNone(self.problem(True))

    def test_wanted_but_outdated_names_both_versions(self):
        self.export()
        base.make_plugin(self.plugin, version="1.1.0")
        message = self.problem(True)
        self.assertIn("outdated", message)
        self.assertIn("copy 1.0.0", message)
        self.assertIn("plugin 1.1.0", message)

    def test_not_wanted_and_no_copy_is_quiet(self):
        self.assertIsNone(self.problem(False))

    def test_not_wanted_but_present(self):
        self.export()
        message = self.problem(False)
        self.assertIn("cloud.export is off", message)
        self.assertIn("/claude-harness:update", message)

    def test_code_running_from_a_copy_cannot_check_itself(self):
        self.export()
        runtime = self.project / ".claude-harness/runtime"  # no skills folder, no plugin manifest
        self.assertIsNone(copy_problem(self.project, True, runtime))
        self.assertIsNone(copy_problem(self.project, False, runtime))

    def test_unusable_settings_are_reported_not_raised(self):
        self.export()
        (self.project / ".claude/settings.json").write_text("{broken", encoding="utf-8")
        self.assertIn("cannot be checked", self.problem(True))
        self.assertIn("cloud.export is off", self.problem(False))  # the manifest alone is enough here


if __name__ == "__main__":
    unittest.main()
