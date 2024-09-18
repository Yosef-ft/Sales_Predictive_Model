import os
import logging

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


log_dir = os.path.join(os.path.split(os.getcwd())[0], 'logs')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file_info = os.path.join(log_dir, 'Info.log')
log_file_error = os.path.join(log_dir, 'Error.log')

info_handler = logging.FileHandler(log_file_info)
info_handler.setLevel(logging.INFO)

error_handler = logging.FileHandler(log_file_error)
error_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(levelname)s :: %(message)s')
info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(info_handler)
logger.addHandler(error_handler)



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
        logger.info("Loading data from file...")
        try:
            data = pd.read_csv(f"../data/{file_name}")
            return data

        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None