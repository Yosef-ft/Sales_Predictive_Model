import sys
import os

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

sys.path.append(os.path.abspath('scripts'))
from Utils import DataUtils


class TestUtils(unittest.TestCase):

    @patch('pandas.read_csv')
    def test_load_data_success(self, mock_read_csv):
        '''
        Tests the success of loading data
        '''

        mock_data = pd.DataFrame({"Store" : [1, 2],"StoreType" : ['c', 'a']})

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




if __name__ == '__main__':
    unittest.main()