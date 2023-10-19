import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
import os

from src.exception import CustomException
from src.logger import logging
from src.utils.common import save_object

from sklearn.preprocessing import StandardScaler
from category_encoders import TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file = os.path.join('artifacts','preprocessor.pkl')

    def __init__(self):

        self.data_transformation_config = DataTransformationConfig()


    def feature_extraction(self,data):
         
        """
        This function is responsible for extracting the new feature from existing one
        """
        try:
            logging.info("Entered in feature extraction method")
            data['total_stays'] = data['stays_in_weekend_nights'] + data['stays_in_week_nights']

            logging.info("new feature total_stay is extracted from stays_in_weekend_nights and stays_in_week_nights")

            return data
        except Exception as e:
             raise CustomException(e,sys)




    
    def outlier_removal(self, data):
          
        """
        This function will return the data after outliers removal
        """
        try:

            logging.info("Entered Removing Outliers function") 
            data = self.feature_extraction(data)

            columns_for_outlier_removal = [
                        'adults', 'children', 'babies', 'total_of_special_requests',
                        'lead_time',
                        'average_price_rooms',
                        'total_stays',
                    ]
            
            for column in columns_for_outlier_removal:
                q_low = data[column].quantile(0.25) # Calculate percentiles
                q_hi  = data[column].quantile(0.75)
                
                IQR=q_hi-q_low

                # Filter out outliers
                data=data[~((data[column]<(q_low-1.5*IQR)) | (data[column]>(q_hi+1.5*IQR)))]
            logging.info("Outliers removed")
            return data
        except Exception as e:
             raise CustomException(e,sys)




    def get_data_transformation_object(self):
        '''
        This function would return the transformed columns'''

        try:

    def initiate_data_transformation(self, train_path, test_path):
                """
        This function is responisble for data transformation
        """

        try:
          train_df = pd.read_csv(train_path)
          test_df = pd.read_csv(test_path)

          logging.info("Read test and train data competed")

          logging.info("Obtaining preprocessing object")

          target_column_name='is_canceled'











