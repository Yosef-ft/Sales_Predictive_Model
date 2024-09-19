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


if __name__ == '__main__':
    unittest.main()



