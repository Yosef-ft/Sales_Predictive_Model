import sys
import os
import unittest

import pandas as pd

sys.path.append(os.path.abspath('scripts'))
from Utils import EDA


class TestEDA(unittest.TestCase):

    def setUp(self):

        self.data = pd.DataFrame({
            'A' : ['Dog', 'Dog', 'Dog', 'Cat' , 'Cat', 'Cat'],
            'B' : [1, 1, 1, 2, 2, 2]
        })

        self.data2 = pd.DataFrame({
            'A' : ['Dog', 'Dog', 'Dog', 'Cat' , 'Cat', 'Cat'],
            'B' : [1, 1, 2, 2, 2, 2]
        })

        self.store_data = pd.DataFrame({
            'Store': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
            'Promo': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            'Sales': [1000, 600, 2000, 1800, 1500, 1100, 500, 500, 3000, 2400]
        })



    def test_distribution_similar(self):
        '''
        This function tests the distribution when the  values are similar
        '''

        eda = EDA()
        result = eda.distribution(self.data, self.data2, 'A', 0)

        self.assertEqual(result, 0.00)

    
    def test_distribution_not_similar(self):
        '''
        This function tests the distribution when the  values are not similar
        '''        

        eda = EDA()
        result = eda.distribution(self.data, self.data2, 'B', 5)

        self.assertAlmostEqual(result, 16.67)


    def test_stores_promo(self):
        '''
        This function tets the stores promo function by checking the columns
        '''

        eda = EDA()
        result = eda.stores_promo(self.store_data)
        cols = list(result.columns)

        self.assertTrue(isinstance(result.index, pd.Index))
        
        expected_columns = ['(No Promo / with Promo)%', 'store no promo', 'store with promo']
        self.assertListEqual(list(result.columns), expected_columns)

if __name__ == '__main__':
    unittest.main()



