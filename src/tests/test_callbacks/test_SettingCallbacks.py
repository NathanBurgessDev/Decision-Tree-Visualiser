import os, sys, unittest

# This allows python to find modules stored in parent directories
# specifically in this case the src directory as it is 2 parent folders
# up from this directory
fpath = os.path.join(os.path.dirname(__file__), '..\\..')
sys.path.append(fpath)

# The path had to be changed so app.py cpould be imported
# This is important as it will initialise AppInstance.app,
# which is needed for callbacks to work
from app import app

# All callbacks from SettingCallbacks.py can then be imported
import callbacks.callbacks.SettingCallbacks as SettingCallbacks

class test_readDataframe(unittest.TestCase):

    # setUp and can initialise resources to be used in test cases
    # I think it has to be named setUp so it doesnt get run as a test
    def setUp(self):
        self.uploadMessage = "Drag and drop or click to upload a dataset (.csv) "

    def test_readDataframe_000(self):
        # Specific callbacks in SettingCallbacks can be accesed
        # and you can provide varies input values as tests
        result = SettingCallbacks.readDataframe(["hello"], [])
        # Function return values are tuples so should be contained
        # in () to check for equivilance 
        self.assertEqual(result,
                         (False,"No Contents!", self.uploadMessage, [], [], [], []))
        
    def test_readDataframe_001(self):
        result = SettingCallbacks.readDataframe(["hello.pdf"], ["abc"])
        self.assertEqual(result,
                         (True, "Wrong File Type!", self.uploadMessage, [], [], [], []))
        
if __name__ == '__main__':
    unittest.main()