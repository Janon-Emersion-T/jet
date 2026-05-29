import unittest

import tools.wisdom_transcendence_tools as module
from phase_batch_test_helper import assert_phase_module


class WisdomTranscendenceToolsTests(unittest.TestCase):
    def test_module_render_and_routes(self):
        assert_phase_module(self, module)


if __name__ == "__main__":
    unittest.main()
