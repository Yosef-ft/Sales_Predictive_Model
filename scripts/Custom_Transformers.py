import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer

class MissingDataHandler(BaseEstimator, TransformerMixin):
    '''
    Custom Trnasformer for handling missing data
    '''
    def __init__(self, strategy, fill_value = None ,missing_values = np.nan):
        self.missing_values= missing_values
        self.strategy= strategy
        self.fill_value= fill_value
        self.imputer = None

    def fit(self, X, y=None):
    
        self.imputer = SimpleImputer(strategy=self.strategy, fill_value=self.fill_value, missing_values=self.missing_values)
        self.imputer.fit(X)
        return self
    
    def transform(self, X, y=None):
        
        if self.imputer == None:
            raise ValueError("The imputer has not been fitted yet. Call fit() before transform().")
        
        X_transformed = self.imputer.transform(X)

        return pd.DataFrame(X_transformed, columns=X.columns)
    

class OutlierHandler(BaseEstimator, TransformerMixin):
    '''
    Custom transformer to handle Outliers 

    Parameters
    ----------
        method(str): IQR, z_score
        factor(float): Factor for calculating IQR
        threshold(float): Threshold for determining Z-score 
        cols(list): A list of columns that we don't need to remove the outlier, like unique identifiers

    Returns:
    --------
        pd.Dataframe
    '''

    def __init__(self, method: str, factor: float = 1.5, threshold: float = 3, cols = None):
        self.method = method
        self.factor = factor
        self.threshold = threshold
        self.cols = cols


    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        
        numeric_col = X.select_dtypes(include='float64').columns
        if self.cols:
            fix_cols = [col for col in numeric_col if col not in self.cols]
        else:
            fix_cols = numeric_col

        if self.method == 'IQR':

            Q1 = X[fix_cols].quantile(0.25)
            Q3 = X[fix_cols].quantile(0.75)

            IQ = Q3 - Q1

            lower_bound = Q1 - self.factor * IQ
            upper_bound = Q3 + self.factor * IQ

            X[fix_cols] = X[fix_cols].clip(lower=lower_bound, upper=upper_bound, axis=1)

            return X  
        
        elif self.method == 'z_score':

            z_scores = np.abs(zscore(X[numeric_col]))

            return X[(z_scores < self.threshold).all(axis = 1)]

