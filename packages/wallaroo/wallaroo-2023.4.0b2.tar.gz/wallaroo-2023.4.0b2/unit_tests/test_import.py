import os
import sys
import unittest


class TestImports(unittest.TestCase):
    def assert_import_ok(self, str):
        try:
            exec(str)
        except:
            self.fail(str)

    def test_imports(self):
        self.assert_import_ok("import wallaroo")


if __name__ == "__main__":
    unittest.main()
