import os
import tempfile
import unittest
from unittest import mock
from pathlib import Path, PurePosixPath

import helpers  # noqa: F401  (adds plugin/scripts to sys.path)
import harness_config
from harness_config import ConfigError, ConfigOutdated, Migration, load_config, migrate_data, parse_config, project_root


class ParseConfigTest(unittest.TestCase):
    def test_valid_config(self):
        config = parse_config({
            "version": 1,
            "docs": {"root": "documentation", "language": "de"},
            "modules": {"todo": True, "daily": True},
            "todo": {"path": "planning"},
            "daily": {"path": "log"},
        })
        self.assertTrue(config.enabled("todo"))
        self.assertTrue(config.enabled("daily"))
        self.assertEqual(config.language, "de")
        self.assertEqual(config.docs_root, PurePosixPath("documentation"))
        self.assertEqual(config.todo_path, PurePosixPath("documentation/planning"))
        self.assertEqual(config.daily_path, PurePosixPath("documentation/log"))

    def test_defaults(self):
        config = parse_config({"version": 1})
        self.assertFalse(config.enabled("todo"))
        self.assertFalse(config.enabled("daily"))
        self.assertEqual(config.language, "en")
        self.assertEqual(config.todo_path, PurePosixPath("docs/todo"))
        self.assertEqual(config.daily_path, PurePosixPath("docs/daily"))
        self.assertFalse(config.enabled("techdocs"))
        self.assertEqual(config.techdocs_path, PurePosixPath("docs/techdocs"))
        self.assertEqual(config.techdocs, ("architecture", "interfaces", "configuration"))

    def test_techdocs_documents(self):
        config = parse_config({"version": 1, "techdocs": {"path": "tech", "documents": ["operations"]}})
        self.assertEqual(config.techdocs_path, PurePosixPath("docs/tech"))
        self.assertEqual(config.techdocs, ("operations",))
        self.assertEqual(parse_config({"version": 1, "techdocs": {"documents": []}}).techdocs, ())

    def test_development_suite(self):
        off = parse_config({"version": 1})
        self.assertFalse(off.part_enabled("architecture"))
        self.assertEqual(off.development_path, PurePosixPath("docs/development"))
        on = parse_config({"version": 1, "modules": {"development": True}})
        self.assertTrue(on.part_enabled("architecture"))
        opted_out = parse_config({
            "version": 1,
            "modules": {"development": True},
            "development": {"path": "rules", "architecture": False},
        })
        self.assertFalse(opted_out.part_enabled("architecture"))
        self.assertTrue(opted_out.part_enabled("decomposition"))
        self.assertEqual(opted_out.development_path, PurePosixPath("docs/rules"))
        self.assertFalse(off.part_enabled("decomposition"))
        self.assertTrue(on.part_enabled("decomposition"))
        no_decomposition = parse_config({
            "version": 1,
            "modules": {"development": True},
            "development": {"decomposition": False},
        })
        self.assertFalse(no_decomposition.part_enabled("decomposition"))
        self.assertTrue(no_decomposition.part_enabled("architecture"))
        self.assertTrue(on.part_enabled("worktree"))
        self.assertFalse(off.part_enabled("worktree"))
        no_worktree = parse_config({
            "version": 1,
            "modules": {"development": True},
            "development": {"worktree": False},
        })
        self.assertFalse(no_worktree.part_enabled("worktree"))
        self.assertTrue(no_worktree.part_enabled("decomposition"))

    def test_harness_repo(self):
        self.assertEqual(parse_config({"version": 1}).harness_repos, ())
        config = parse_config({"version": 1, "harness": {"repo": ["/abs/harness", "~/code/harness"]}})
        self.assertEqual(config.harness_repos, ("/abs/harness", "~/code/harness"))
        self.assertEqual(parse_config({"version": 1, "harness": {"repo": []}}).harness_repos, ())

    def test_semver(self):
        config = parse_config({"version": 1})
        self.assertFalse(config.enabled("semver"))
        self.assertEqual(config.semver_file, PurePosixPath("docs/VERSION"))
        self.assertEqual(config.semver_sync, ())
        self.assertEqual(config.semver_paths, (PurePosixPath("."),))
        config = parse_config({
            "version": 1,
            "docs": {"root": "documentation"},
            "modules": {"semver": True},
            "semver": {"file": "release/VERSION.txt", "sync": ["package.json", "sub/Cargo.toml"], "paths": ["src", "lib/"]},
        })
        self.assertTrue(config.enabled("semver"))
        self.assertEqual(config.semver_file, PurePosixPath("documentation/release/VERSION.txt"))
        self.assertEqual(config.semver_sync, (PurePosixPath("package.json"), PurePosixPath("sub/Cargo.toml")))
        self.assertEqual(config.semver_paths, (PurePosixPath("src"), PurePosixPath("lib")))

    def test_version_file_is_a_harness_file(self):
        config = parse_config({"version": 1, "semver": {"file": "VERSION"}})
        self.assertTrue(config.is_harness_file(PurePosixPath("docs/VERSION")))
        self.assertFalse(config.is_harness_file(PurePosixPath("package.json")))

    def test_projects(self):
        self.assertEqual(parse_config({"version": 1}).projects, ())
        config = parse_config({
            "version": 1,
            "projects": {"VariantFilter": "Plugins/VariantFilter", "other_2": "Plugins/Other/"},
        })
        self.assertEqual(config.projects, (
            ("VariantFilter", PurePosixPath("Plugins/VariantFilter")),
            ("other_2", PurePosixPath("Plugins/Other")),
        ))

    def test_rejects_invalid_projects(self):
        cases = [
            {"projects": "Plugins/A"},
            {"projects": {"root": "Plugins/A"}},
            {"projects": {"1st": "Plugins/A"}},
            {"projects": {"a b": "Plugins/A"}},
            {"projects": {"A": "/abs"}},
            {"projects": {"A": "../outside"}},
            {"projects": {"A": "."}},
            {"projects": {"A": ""}},
            {"projects": {"A": 1}},
            {"projects": {"A": "Plugins/A", "B": "Plugins/A"}},
            {"projects": {"A": "Plugins", "B": "Plugins/B"}},
        ]
        for extra in cases:
            with self.subTest(data=extra), self.assertRaises(ConfigError):
                parse_config({"version": 1, **extra})

    def test_subproject_rejects_registry_and_harness(self):
        self.assertEqual(parse_config({"version": 1}, subproject=True).projects, ())
        for extra in ({"projects": {"A": "Plugins/A"}}, {"harness": {"repo": []}}):
            with self.subTest(data=extra), self.assertRaises(ConfigError):
                parse_config({"version": 1, **extra}, subproject=True)

    def test_rejects_invalid_values(self):
        cases = [
            {"version": 2},
            {"version": 1, "extra": 1},
            {"version": 1, "modules": {"unknown": True}},
            {"version": 1, "modules": {"todo": "yes"}},
            {"version": 1, "todo": {"path": "/abs"}},
            {"version": 1, "todo": {"path": "../outside"}},
            {"version": 1, "todo": {"path": "docs", "other": 1}},
            {"version": 1, "docs": {"root": "/abs"}},
            {"version": 1, "docs": {"language": "deu"}},
            {"version": 1, "docs": {"language": "DE"}},
            {"version": 1, "docs": {"other": 1}},
            {"version": 1, "docs": "docs"},
            {"version": 1, "daily": {"path": "../x"}},
            {"version": 1, "techdocs": {"documents": ["unknown"]}},
            {"version": 1, "techdocs": {"documents": ["interfaces", "interfaces"]}},
            {"version": 1, "techdocs": {"documents": "interfaces"}},
            {"version": 1, "techdocs": {"path": "/abs"}},
            {"version": 1, "development": {"architecture": "yes"}},
            {"version": 1, "development": {"decomposition": 1}},
            {"version": 1, "development": {"worktree": "on"}},
            {"version": 1, "development": {"unknown": True}},
            {"version": 1, "development": {"path": "../x"}},
            {"version": 1, "harness": {"repo": "/abs/harness"}},
            {"version": 1, "harness": {"repo": ["relative/harness"]}},
            {"version": 1, "harness": {"repo": [""]}},
            {"version": 1, "harness": {"repo": [1]}},
            {"version": 1, "harness": {"other": 1}},
            {"version": 1, "harness": "x"},
            {"version": 1, "modules": {"semver": "on"}},
            {"version": 1, "semver": {"file": "/abs"}},
            {"version": 1, "semver": {"file": "../VERSION"}},
            {"version": 1, "semver": {"sync": "package.json"}},
            {"version": 1, "semver": {"sync": ["../package.json"]}},
            {"version": 1, "semver": {"sync": [""]}},
            {"version": 1, "semver": {"paths": []}},
            {"version": 1, "semver": {"paths": ["/abs"]}},
            {"version": 1, "semver": {"other": 1}},
        ]
        for data in cases:
            with self.subTest(data=data), self.assertRaises(ConfigError):
                parse_config(data)


class MigrationTest(unittest.TestCase):
    def _add_widget_module(self, data):
        return {**data, "modules": {**data.get("modules", {}), "todo": True}}

    def test_outdated_config_raises_config_outdated(self):
        migration = Migration(1, 2, "turn todo on by default", self._add_widget_module)
        with mock.patch.object(harness_config, "MIGRATIONS", (migration,)), \
                mock.patch.object(harness_config, "CONFIG_VERSION", 2):
            with self.assertRaises(ConfigOutdated) as ctx:
                parse_config({"version": 1})
        self.assertEqual(ctx.exception.current_version, 1)
        self.assertEqual(ctx.exception.target_version, 2)
        self.assertEqual(ctx.exception.steps, ("turn todo on by default",))

    def test_migrate_data_applies_chain_and_result_parses(self):
        migration = Migration(1, 2, "turn todo on by default", self._add_widget_module)
        with mock.patch.object(harness_config, "MIGRATIONS", (migration,)), \
                mock.patch.object(harness_config, "CONFIG_VERSION", 2):
            migrated = migrate_data({"version": 1})
            self.assertEqual(migrated["version"], 2)
            self.assertEqual(migrated["modules"], {"todo": True})
            self.assertTrue(parse_config(migrated).enabled("todo"))

    def test_multi_step_chain_is_applied_in_order(self):
        step_one = Migration(1, 2, "step one", self._add_widget_module)
        step_two = Migration(2, 3, "step two", lambda data: {**data, "docs": {"language": "de"}})
        with mock.patch.object(harness_config, "MIGRATIONS", (step_one, step_two)), \
                mock.patch.object(harness_config, "CONFIG_VERSION", 3):
            with self.assertRaises(ConfigOutdated) as ctx:
                parse_config({"version": 1})
            self.assertEqual(ctx.exception.steps, ("step one", "step two"))
            migrated = migrate_data({"version": 1})
            self.assertEqual(migrated["version"], 3)
            self.assertEqual(migrated["modules"], {"todo": True})
            self.assertEqual(migrated["docs"], {"language": "de"})

    def test_version_without_migration_path_stays_a_plain_config_error(self):
        migration = Migration(2, 3, "unrelated step", lambda data: data)
        with mock.patch.object(harness_config, "MIGRATIONS", (migration,)), \
                mock.patch.object(harness_config, "CONFIG_VERSION", 3):
            with self.assertRaises(ConfigError) as ctx:
                parse_config({"version": 1})
            self.assertNotIsInstance(ctx.exception, ConfigOutdated)
            with self.assertRaises(ConfigError) as ctx:
                migrate_data({"version": 1})
            self.assertNotIsInstance(ctx.exception, ConfigOutdated)

    def test_version_greater_than_current_is_still_invalid(self):
        # Regression: unrelated to migrations, must not become ConfigOutdated.
        migration = Migration(1, 2, "step", self._add_widget_module)
        with mock.patch.object(harness_config, "MIGRATIONS", (migration,)), \
                mock.patch.object(harness_config, "CONFIG_VERSION", 2):
            with self.assertRaises(ConfigError) as ctx:
                parse_config({"version": 7})
            self.assertNotIsInstance(ctx.exception, ConfigOutdated)


class ProjectRootTest(unittest.TestCase):
    def test_worktree_of_the_project_becomes_the_root(self):
        base = Path("/work/repo")
        worktree = base / ".claude/worktrees/TASK-1"
        with mock.patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(base)}):
            self.assertEqual(project_root({}), base)
            self.assertEqual(project_root({"cwd": str(worktree / "tests")}), worktree)
            self.assertEqual(
                project_root({"cwd": str(base), "tool_input": {"file_path": str(worktree / "src/x.py")}}),
                worktree,
            )
            self.assertEqual(
                project_root({"tool_input": {"notebook_path": str(worktree / "n.ipynb")}}), worktree
            )
            self.assertEqual(project_root({"cwd": str(base / ".claude/worktrees")}), base)
            self.assertEqual(project_root({"tool_input": {"file_path": "/elsewhere/.claude/worktrees/x/y"}}), base)

    def test_without_project_dir_uses_cwd(self):
        env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(project_root({"cwd": "/work/repo"}), Path("/work/repo"))
            self.assertEqual(
                project_root({"cwd": "/work/repo/.claude/worktrees/a/b"}), Path("/work/repo/.claude/worktrees/a")
            )


class LoadConfigTest(unittest.TestCase):
    def test_missing_config_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(load_config(Path(tmp)))

    def test_invalid_toml(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".claude-harness" / "config.toml"
            path.parent.mkdir()
            path.write_text("version = ")
            with self.assertRaises(ConfigError):
                load_config(Path(tmp))

    def test_template_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".claude-harness" / "config.toml"
            path.parent.mkdir()
            path.write_text((helpers.REPO_ROOT / "plugin/templates/config.toml").read_text())
            self.assertTrue(load_config(Path(tmp)).enabled("todo"))


if __name__ == "__main__":
    unittest.main()
