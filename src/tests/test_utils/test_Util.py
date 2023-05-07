import unittest, os, sys
import os, sys, unittest
import pandas as pd
import io, pickle
import base64
from pandas.util.testing import assert_frame_equal
from io import StringIO
fpath = os.path.join(os.path.dirname(__file__), '..\\..')
sys.path.append(fpath)
from utils.Util import ImportUtil

class test_ImportUtil(unittest.TestCase):

    # Test case with a valid content
    def test_readContent_0(self):
        file = "test.txt"
        content = "text/plain;base64,SGVsbG8gV29ybGQ="
        expected_output = "Hello World"
        self.assertEqual(ImportUtil.readContent(file, content), expected_output)


    # Test case with a valid content of a different type
    def test_readContent_1(self):
        file = "test.txt"
        content = "application/json;base64,eyJmb28iOiJiYXIifQ=="
        expected_output = '{"foo":"bar"}'
        self.assertEqual(ImportUtil.readContent(file, content), expected_output)

    # Test case with an invalid content
    def test_readContent_2(self):
        file = "test.txt"
        content = "invalid_content"
        with self.assertRaises(ValueError):
            ImportUtil.readContent(file, content)

    # Test case with an empty content
    def test_readContent_3(self):
        file = "test.txt"
        content = ""
        with self.assertRaises(ValueError):
            ImportUtil.readContent(file, content)

    # Test case with a valid CSV
    def test_csvToDataFrame_0(self):
        csv = "Name, Age\nAlice, 25\nBob, 30"
        expected_output = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [25, 30]})
        assert_frame_equal(expected_output,
                         ImportUtil.csvToDataFrame(csv))

    # Test case with an invalid CSV
    def test_csvToDataFrame_1(self):
        csv = "Name, Age\nAlice, 25\nBob, 30, Engineer"
        with self.assertRaises(pd.errors.ParserError):
            ImportUtil.csvToDataFrame(csv)

    # Test case with an empty CSV
    def test_csvToDataFrame_2(self):
        csv = ""
        with self.assertRaises(pd.errors.EmptyDataError):
            ImportUtil.csvToDataFrame(csv)

    # Test case with a valid pickle
    def test_readPickle_0(self):
        test_object = [1, 2, 3]
        pickled_object = pickle.dumps(test_object)
        base64_object = base64.b64encode(pickled_object).decode("utf-8")
        content = f"application/octet-stream;base64,{base64_object}"
        expected_output = test_object
        result = ImportUtil.readPickle("test.pkl", content)
        self.assertEqual(pickle.load(result), expected_output)

    # Test case with an invalid pickle
    def test_readPickle_1(self):
        file = "test.pkl"
        content = "application/octet-stream;base64,invalid_content"
        with self.assertRaises(base64.binascii.Error):
            ImportUtil.readPickle(file, content)

    # Test case with an empty content
    def test_readPickle_2(self):
        file = "test.pkl"
        content = ""
        with self.assertRaises(ValueError):
            ImportUtil.readPickle(file, content)

    # Test case with a valid pickle
    def test_unPickle_0(self):
        data = [1, 2, 3, 4, 5]
        pickled_data = pickle.dumps(data)
        bytes_io = io.BytesIO(pickled_data)
        unpickled_data = ImportUtil.unPickle(bytes_io)
        self.assertEqual(unpickled_data, data)


    # Test case with an invalid pickle
    def test_unPickle_1(self):
        file = io.BytesIO(b'invalid_content')
        with self.assertRaises(pickle.UnpicklingError):
            ImportUtil.unPickle(file)

    # Test case with an empty file
    def test_unPickle_2(self):
        file = io.BytesIO()
        expected_output = None
        self.assertEqual(ImportUtil.unPickle(file), expected_output)

if __name__ == '__main__':
    unittest.main()
