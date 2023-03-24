import os, sys, unittest
fpath = os.path.join(os.path.dirname(__file__), '..\\..')
sys.path.append(fpath)
from app import app
import callbacks.callbacks.DisplayCallbacks as DisplayCallbacks

class test_readDataframe(unittest.TestCase):

    """
    def setUp(self):
        # Set up member variable for tests
    """

    def test_modelSelected_000(self):
        result = DisplayCallbacks.modelSelected(None)
        self.assertEqual(result, [()])
        
if __name__ == '__main__':
    unittest.main()