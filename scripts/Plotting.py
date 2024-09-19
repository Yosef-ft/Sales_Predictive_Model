import math

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
from Utils import logger

class Plots:
    # def __init__(self, data):
    #     self.data = data


    def visualize_missing_values(self, data):
        '''
        This method generates a heatmap to visually represent the missing values in the dataset.
        '''
        logger.debug("Plotting missing values...")
        try:
            missing_cols = data.columns[data.isna().any()]

            missing_data = data[missing_cols]

            msno.bar(missing_data)    
        except Exception as e:
            logger.error(f"Error in plotting missing values: {e}")

    
    
    def visualize_outliers(self, data):
        '''
        This funcions helps in visualizing outliers using boxplot
        '''
        logger.debug("Plotting Outliers...")

        try:
            numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns
            num_columns = len(numerical_cols) # length of numerical columns
            n_cols = int(math.sqrt(num_columns))

            nrows = num_columns // n_cols + num_columns % n_cols

            fig, axes = plt.subplots(nrows=nrows, ncols=n_cols, figsize=(20,12))
            axes = axes.flatten()

            for i, col in enumerate(numerical_cols):
                sns.boxplot(y=data[col], ax=axes[i])
                axes[i].set_title(col)

            for j in range(i + 1, len(axes)):
                fig.delaxes(axes[j])            

            plt.tight_layout()
            plt.show()

        except Exception as e:
            logger.error(f"Error in plotting Outliers: {e}")            