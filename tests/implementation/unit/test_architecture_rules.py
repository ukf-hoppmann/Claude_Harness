"""Tests enforcing rules of docs/development/architecture.md."""

import ast
import sys
import unittest

from helpers import REPO_ROOT, SCRIPTS
from harness_config import KNOWN_MODULES, TABLE_KEYS


class RuntimeRuleTest(unittest.TestCase):
    """Rule 2: plugin scripts use only the Python standard library."""

    def test_scripts_import_only_stdlib_and_local_modules(self):
        local = {path.stem for path in SCRIPTS.glob("*.py")}
        allowed = set(sys.stdlib_module_names) | local | {"__future__"}
        for path in sorted(SCRIPTS.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.level == 0:
                    names = [node.module]
                else:
                    continue
                for name in names:
                    with self.subTest(script=path.name, module=name):
                        self.assertTrue(name.split(".")[0] in allowed, f"{name} is not in the standard library")


class ConfigurationRuleTest(unittest.TestCase):
    """Rule 4: every configuration key is documented in configuration.md."""

    def test_every_key_is_documented(self):
        doc = (REPO_ROOT / "docs/techdocs/configuration.md").read_text(encoding="utf-8")
        keys = ["version"] + [f"modules.{name}" for name in KNOWN_MODULES]
        keys += [f"{table}.{key}" for table, table_keys in TABLE_KEYS.items() for key in sorted(table_keys)]
        keys.append("projects.<Name>")
        for key in keys:
            with self.subTest(key=key):
                self.assertTrue(f"`{key}`" in doc, f"{key} is missing in configuration.md")


if __name__ == "__main__":
    unittest.main()
