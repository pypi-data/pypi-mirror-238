import unittest


class TestPackageInstallation(unittest.TestCase):
    def test_dependencies_installed(self):
        all_dependencies_installed = False
        try:
            import numpy
            import scipy
            import torch

            all_dependencies_installed = True
        except Exception:
            pass
        self.assertTrue(all_dependencies_installed)

    def test_active_learn_installed(self):
        active_learn_installed = False
        try:
            from active_learn import ActiveSampler

            active_learn_installed = True
        except Exception:
            pass
        self.assertTrue(active_learn_installed)


if __name__ == "__main__":
    unittest.main()
