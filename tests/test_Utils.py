import sys
import os

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

sys.path.append(os.path.abspath('scripts'))
from Utils import DataUtils


class TestUtils(unittest.TestCase):

    def setUp(self):

        self.data_with_missing = pd.DataFrame({
            'col1': [1, 2, 3, 4],
            'col2': [1, 2, None, 4],
            'col3': [None, None, 3, 4],
            'col4': [None, None, None, None]
        })

        self.data_no_missing = pd.DataFrame({
            'col1': [1, 2, 3, 4],
            'col2': [1, 2, 3, 4],
            'col3': [1, 2, 3, 4]
        })       


    @patch('pandas.read_csv')
    def test_load_data_success(self, mock_read_csv):
        '''
        Tests the success of loading data
        '''

        mock_data = self.data_no_missing

        mock_read_csv.return_value = mock_data

        data_utils = DataUtils()
        result = data_utils.load_data('test.csv')

        self.assertIsNotNone(result)
        self.assertEqual(result.shape, mock_data.shape)
        self.assertTrue((result == mock_data).all().all())

    
    @patch('pandas.read_csv')
    def test_load_data_faliure(self, mock_read_csv):
        '''
        Tests the failure of loading data 
        '''

        mock_read_csv.side_effect = IOError('File Not Found')

        data_utils = DataUtils()
        result = data_utils.load_data('None.csv')

        self.assertIsNone(result)


    def test_data_info_with_missing_data(self):
        '''
        Tests the funcion data_info with missing data
        '''

        data_utils = DataUtils()
        result = data_utils.data_info(self.data_with_missing)

        self.assertEqual(result.shape[0], 3) # 3 missing cols
        self.assertListEqual(list(result.columns) , ['Missing Values', 'Missing Percentage', 'Data Types'])

        self.assertEqual(result.iloc[0]['Missing Percentage'], 100.00)


    def test_data_info_without_missing(self):
        '''
        Tests the funcion data_info without missing data
        '''

        data_utils = DataUtils()
        result = data_utils.data_info(self.data_no_missing)

        self.assertTrue(result.empty)


if __name__ == '__main__':
    unittest.main()