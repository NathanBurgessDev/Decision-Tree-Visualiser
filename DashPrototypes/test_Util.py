import unittest
import pandas as pd
import csv
from Util import ImportUtil as iu

class TestImportUtil(unittest.TestCase):
    #Testing that the csv to dataframe function returns the same dataframe as if it were imported directly.
    def test_CSV_To_Dataframe(self):
        with open('CSVs/iris.csv', newline='') as irisCSV:
            csvStr = ""
            irisReader = csv.reader(irisCSV, delimiter=',')
            for row in irisReader:
                csvStr += (', '.join(row))
                    
            df = iu.csvToDataFrame(csvStr)
            pandasDF = pd.read_csv('CSVs/iris.csv')
            self.assertEqual(df.columns[0], pandasDF.columns[0], "The first column labels do not match.")


if __name__ == '__main__':
    unittest.main()
