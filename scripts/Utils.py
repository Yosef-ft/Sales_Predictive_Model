import os
import logging

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import holidays

# ANSI Escape code to make the printing more appealing
ANSI_ESC = {
    "PURPLE": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "ITALICS" :"\033[3m"
}


log_dir = os.path.join(os.path.split(os.getcwd())[0], 'logs')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file_info = os.path.join(log_dir, 'Info.log')
log_file_error = os.path.join(log_dir, 'Error.log')

info_handler = logging.FileHandler(log_file_info)
info_handler.setLevel(logging.INFO)

error_handler = logging.FileHandler(log_file_error)
error_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(levelname)s :: %(message)s',
                              datefmt="%Y-%m-%d %H:%M")
info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)



class DataUtils:
    # def __init__(self, data):
    #     self.data = data


    def load_data(self, file_name: str)->pd.DataFrame:
        '''
        Load the file name from the data directory

        Parameters:
            file_name(str): name of the file

        Returns:
            pd.DataFrame
        '''
        logger.debug("Loading data from file...")
        try:
            data = pd.read_csv(f"../data/{file_name}")
            return data

        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None
        


    def data_info(self, data) -> pd.DataFrame:
        '''
        Provides detailed information about the data, including:
            - Percentage of missing values per column
            - Number of missing values per column
            - Data types of the columns
        It also highlights:
            - The total number of rows and columns in the dataset
            - Columns with the most missing values
            - Columns with more than 50% missing values

        Parameters:
            data(pd.DataFrame): The dataset 
        
        Returns:
            info_df(pd.DataFrame)
        '''
        
        missing_values = data.isna().sum()
        missing_percent = round(data.isna().mean() * 100, 2)
        data_types = data.dtypes
        
        info_df = pd.DataFrame({
            "Missing Values": missing_values,
            "Missing Percentage": missing_percent,
            "Data Types": data_types
        })


        info_df = info_df[missing_percent > 0]
        info_df = info_df.sort_values(by='Missing Percentage', ascending=False)

        max_na_col = list(info_df.loc[info_df['Missing Values'] == info_df['Missing Values'].max()].index)
        more_than_half_na = list(info_df.loc[info_df['Missing Percentage'] > 50].index)
        

        print(f"\n{ANSI_ESC['BOLD']}Dataset Overview{ANSI_ESC['ENDC']}")
        print(f"---------------------")
        print(f"- {ANSI_ESC['ITALICS']}Total rows{ANSI_ESC['ENDC']}: {data.shape[0]}")
        print(f"- {ANSI_ESC['ITALICS']}Total columns{ANSI_ESC['ENDC']}: {data.shape[1]}\n")

        duplicated_rows = int(data.duplicated().sum())
        if duplicated_rows == 0:
            print(f"{ANSI_ESC['GREEN']}No Duplicated data found in the dataset.{ANSI_ESC['ENDC']}\n")
        else:
             print(f"- {ANSI_ESC['RED']}Number of duplicated rows are{ANSI_ESC['ENDC']}: {duplicated_rows}")
        
        if info_df.shape[0] > 0:
            print(f"{ANSI_ESC['BOLD']}Missing Data Summary{ANSI_ESC['ENDC']}")
            print(f"------------------------")
            print(f"- {ANSI_ESC['ITALICS']}Columns with missing values{ANSI_ESC['ENDC']}: {info_df.shape[0]}\n")
            
            print(f"- {ANSI_ESC['ITALICS']}Column(s) with the most missing values{ANSI_ESC['ENDC']}: `{', '.join(max_na_col)}`")
            print(f"- {ANSI_ESC['RED']}Number of columns with more than 50% missing values{ANSI_ESC['ENDC']}: `{len(more_than_half_na)}`\n")


            if more_than_half_na:
                print(f"{ANSI_ESC['BOLD']}Columns with more than 50% missing values:{ANSI_ESC['ENDC']}")
                for column in more_than_half_na:
                    print(f"   - `{column}`")
            else:
                print(f"{ANSI_ESC['GREEN']}No columns with more than 50% missing values.{ANSI_ESC['ENDC']}")
        else:
            print(f"{ANSI_ESC['GREEN']}No missing data found in the dataset.{ANSI_ESC['ENDC']}")

        print(f"\n{ANSI_ESC['BOLD']}Detailed Missing Data Information{ANSI_ESC['ENDC']}")
        print(info_df)

        return info_df
    

    def holiday_generator(self, data):
        logger.debug("Adding holiday column...")
        try:
            us_holidays = holidays.US()
            data['Holiday'] = data['Date'].apply(lambda x: us_holidays[x] if x in us_holidays else 'Not Holiday')
            return data
        
        except Exception as e:
            logger.error(f"Error in adding holiday column: {e}")
            return data

class EDA:

    def distribution(self, df1: pd.DataFrame, df2: pd.DataFrame, col: str, similarity_threshold: float):
        '''
        This funcion checks the distribution of column in two dataframes 

        Parameter:
        ----------
            df1(pd.DataFrame): DataFrame 1
            df2(pd.DataFrmae): DataFrame 2
            col(str): the column you want to check the distribution
            similarity_threshold(float): The allowed percentage difference between the two dataframes to be classified as similar

        Returns:
        -------
            change_pct(float): Returns the percent change of distribution between datasets
        '''
        logger.debug("Checking for column distribution in different dataframes....")

        shape1 = df1[col].shape[0]
        val1 = int(df1[col].value_counts().sort_index().values[0])
        index1 = df1[col].value_counts().index[0]

        shape2 = df2[col].shape[0]
        val2 = int(df2[col].value_counts().sort_index().values[0])
        index2 = df2[col].value_counts().index[0]

        pct1 = round(val1 * 100 / shape1, 2)
        pct2 = round(val2 * 100 / shape2, 2)

        change_pct = round(np.abs(pct1 - pct2), 2)

        print(f"{ANSI_ESC['BOLD']}Similarity Overview{ANSI_ESC['ENDC']}\n")
        print(f"- The first dataset has {pct1}% of the `{index1}` value")
        print(f"- The second dataset has {pct2}% of the `{index2}` value")

        if change_pct > similarity_threshold:
            print(f"{ANSI_ESC['RED']} The distribution of the column {col} are not similar{ANSI_ESC['ENDC']}\n")
            print(f"{ANSI_ESC['ITALICS']} The percent change between the two dataset's value is {change_pct}% ")
            
            

        else:
            print(f"{ANSI_ESC['GREEN']} The distribution of the column {col} are similar{ANSI_ESC['ENDC']}\n")
            print(f"{ANSI_ESC['ITALICS']} The percent change between the two dataset's value is {change_pct}% ")

        return change_pct
            
        
    def stores_promo(self, data)->pd.DataFrame:
        '''
        This function helps with identify which stores need Pormo and which stores perform better without Promo

        Parameters:
        ----------
            data(pd.DataFrame)

        Returns:
        -------
            store_promo_relation(pd.DataFrame): A ratio of sales between stores with promotions and those without promotions.
        '''

        store_with_promo = data[data['Promo'] == 1].groupby(by='Store')['Sales'].sum()
        store_no_promo = data[data['Promo'] == 0].groupby(by='Store')['Sales'].sum()

        ratios_of_sales = round(store_no_promo * 100 / store_with_promo, 2)
        store_Promo_relation = (pd.DataFrame(ratios_of_sales)).rename({'Sales' : '(No Promo / with Promo)%'}, axis =1).sort_values(by='(No Promo / with Promo)%')
        store_Promo_relation['store no promo'] = store_no_promo
        store_Promo_relation['store with promo'] = store_with_promo

        # Stores that will benefit from Promo. 
        top_stores_need_promo = store_Promo_relation[store_Promo_relation['(No Promo / with Promo)%'] < 60]
        
        no_promo = store_Promo_relation.tail()

        print(f'{ANSI_ESC["BOLD"]}Sales and Promo Overview{ANSI_ESC['ENDC']}\n')
        print(f'{ANSI_ESC['RED']} The top three columns that experience more than a 40% increase in total sales when using promotions.{ANSI_ESC['ENDC']}')
        if not top_stores_need_promo.empty:
            for i in range(0, 3):
                print(f'{ANSI_ESC["ITALICS"]} - Store number {top_stores_need_promo.index[i]} has experienced a boost in sales of {100 - top_stores_need_promo.values[i][0]}% when using Promo{ANSI_ESC['ENDC']}')

        print('\n\n')
        print(f'{ANSI_ESC['GREEN']} The top three columns that are better off without Promos.{ANSI_ESC['ENDC']}')
        for i in range(0,3):
            print(f'{ANSI_ESC["ITALICS"]} - Store number {no_promo.index[4 - i]} has experienced a boost in sales of {round(no_promo.values[4 - i][0] - 100, 2)}% without using Promo{ANSI_ESC['ENDC']}')


        return store_Promo_relation
        