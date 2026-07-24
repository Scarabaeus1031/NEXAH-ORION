"""Freeze tests for the Version 1 repository package boundary."""

import unittest

import orion


class VersionOnePublicSurfaceTests(unittest.TestCase):
    def test_root_reports_the_release_version(self) -> None:
        self.assertEqual(orion.__version__, "1.0.0")

    def test_earlier_aggregate_imports_remain_compatible(self) -> None:
        for name in (
            "FakeBackend",
            "OllamaBackend",
            "OperatorRegistry",
            "OrientationExecutor",
            "TransformationEngine",
        ):
            self.assertIn(name, orion.__all__)
            self.assertTrue(hasattr(orion, name))


if __name__ == "__main__":
    unittest.main()
