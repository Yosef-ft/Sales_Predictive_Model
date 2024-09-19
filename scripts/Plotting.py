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


    def seasonal_purchase_behavior(self, data):
        '''
        Creates a bar plot for seasonal purchase behaviour
        '''
        try: 
            logger.debug('Plotting seasonal purchase behaviour of customers...')
            holiday_sales = data[data['Holiday'] != 'Not Holiday'].groupby(by='Holiday')['Sales'].sum().reset_index().sort_values(by = 'Sales', ascending=False)

            sns.barplot(data=holiday_sales, x='Holiday', y='Sales', hue='Holiday', palette='coolwarm', legend=False)
            plt.xticks(rotation = 90)
            plt.title('Sales volume by Holiday')
            plt.xlabel('Holidays')
            plt.ylabel('Sales Volume')     
            plt.show();   
        except Exception as e:
             logger.error(f"Error in plotting bar plot for seasonal purchase behaviour: {e}")  


    def customer_sales_corr(self, data):
        '''
        Scatter plot between sales and customer
        '''
        logger.debug('Scatter plot between sales and customer')
        try: 
            scatter = plt.scatter(data['Customers'], data['Sales'], c=data.index, cmap='viridis')
            plt.colorbar(scatter, label='Date')
            plt.title('Sales vs Customers Over Time')
            plt.xlabel('Number of Customers')
            plt.ylabel('Sales')
            plt.show()  
        except Exception as e:
            logger.error(f'Error while plotting scatter plot {e}')      

    def effect_of_promo(self, data, col: str):
        '''
        Line plot of the effect of Promo on differnet columns

        Parameters:
        ----------
            data(pd.DataFrame)
            col(str): the column you want to compare with the Promo
        '''
        logger.debug(f'line plot between Promo and {col}')
        try: 
            sns.lineplot(
                x=data[data['Promo'] == 1]['Date'].dt.month,
                y=data[data['Promo'] == 1][col],
                label='With Promo', 
                color='darkblue', 
                linestyle='-', 
                linewidth=2,
                marker='o'
            )

            sns.lineplot(
                x=data[data['Promo'] == 0]['Date'].dt.month,
                y=data[data['Promo'] == 0][col],
                label='Without Promo', 
                color='salmon', 
                linestyle='--', 
                linewidth=2,
                marker='x'
            )        
        except Exception as e:
            logger.error(f'Error while plotting line plot {e}')    
