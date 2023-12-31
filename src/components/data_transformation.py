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
from imblearn.over_sampling import SMOTE


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file = os.path.join('artifacts','preprocessor.pkl')


class DataTransformation:
        
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



    def feature_selection(self,data):
        """
        This function is responsible to get those feature which is important for the model
        """
        try:
            logging.info("Entered in feature selection method")
            data = data.drop(['adults',
                                'babies',
                                'children', 
                                'Booking_ID', 
                                'stays_in_weekend_nights',
                                'stays_in_week_nights',
                                'arrival_date_year',
                                'arrival_date_month',
                                'arrival_date_day_of_month',
                                'arrival_date_week_number'], axis =1)
            data = data.reset_index(drop=True)

            return data

            logging.info("feature got removed which was not important for model")
        except Exception as e:
             raise CustomException(e,sys)
        


    def features_encoding(self, x, y):
        """
        This function will return encoded data of categorical column based on Target Encoding
        """

        try:
            logging.info("Entered in data encoding method with Target Encoding")
            encoder = TargetEncoder()
            encoder = encoder.fit(x, y)
            #encoded_data = encoder.transform(x)

            logging.info("Encoding completed!!")
            return encoder
        
        except Exception as e:
            raise CustomException(e,sys)
        

    def oversmapling_smote(self, x,y):
        """
        This function is responsible for applying oversmapling technique - SMOTE on training data
        """

        try:

            logging.info("Entered in oversmapling method to fix the issue of imbalanced data")
            smote = SMOTE(sampling_strategy='auto', random_state=42)
            X_train_resampled, y_train_resampled = smote.fit_resample(x, y) 

            logging.info("Oversampling completed!!")
            return X_train_resampled, y_train_resampled
        
        except Exception as e:
            raise CustomException(e,sys)
        

    def standardization(self):
        """
        This function is responsible for scaling the data
        """

        try:
            logging.info("Entered in scaling method to scale the data")
            scaler = StandardScaler()
            
            return scaler
        
        except Exception as e:
            raise CustomException(e,sys)
        

    def get_data_transformation_object(self, x,y):
        """
        This method is responsible for returning the preprocessing object
        """
        try:
            logging.info("Entered in data transformation preprocessing ")
            cat_cols=[
                'meal',
                'assigned_room_type',
                'market_segment',
                'reserved_room_type'
            ]

            num_cols=[
                'required_car_parking_spaces',
                'lead_time',
                'is_repeated_guest',
                'previous_cancellations',
                'previous_bookings_not_canceled',
                'total_of_special_requests',
                'average_price_rooms',
                'total_stays'
            ]

            #steps for target encoding
            encoder = TargetEncoder()
            #encode = encoder.fit(x,y)

            num_pipeline=Pipeline(steps=[
                ('scaler', StandardScaler())
            ])

            cat_pipeline=Pipeline(steps=[
                ('target_encoding',encoder),
                ("StandardScaler", StandardScaler())
            ])

            logging.info(f"Categorical Columns:{cat_cols}")
            logging.info(f"Numerical Columns:{num_cols}")

            preprocessor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,num_cols),
                    ("cat_pipeline",cat_pipeline,cat_cols)
                ]
            )

            preprocessor.fit(x,y)

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
            

    def initiate_data_transformation(self, train_path, test_path):
        """
        This function is responisble for data transformation
        """

        try:
            logging.info("Entered into data transformation method")
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)


            logging.info("Read test and train data completed")
            
            target_column_name='is_canceled'

            # outliers removals in train and test data
            logging.info("Removal of outliers in train and test dataset")
            train_df = self.outlier_removal(train_df)
            test_df =  self.outlier_removal(test_df)
            

            # feature selection in train and test data
            logging.info("Feature selection in train and test dataset")
            train_df = self.feature_selection(train_df)
            test_df = self.feature_selection(test_df)

            # divide the train dataset to independent and dependent feature

            input_features_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]
                   
            # divide the test dataset to independent and dependent feature

            input_features_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info("Applying Target encoding on train and test dataset")
            encoder_train = self.features_encoding(input_features_train_df,target_feature_train_df)
            encoder_test= self.features_encoding(input_features_test_df,target_feature_test_df)
            input_features_encoded_train_df = encoder_train.transform(input_features_train_df)
            input_feature_encoded_test_df = encoder_test.transform(input_features_test_df)

            logging.info("Applying oversampling technique-SMOTE only in training dataset")
            input_features_sampled_train_df, target_feature_sampled_train_df = self.oversmapling_smote(input_features_encoded_train_df,target_feature_train_df)

            logging.info("Scaling of the training and test dataset")
            scaler = self.standardization()
            input_features_scaled_train_arr = scaler.fit_transform(input_features_sampled_train_df)
            input_feature_scaled_test_arr = scaler.transform(input_feature_encoded_test_df)

            #creating preprocessing obj so while prediction we can preprocess
            preprocessing_obj = self.get_data_transformation_object(input_features_train_df,target_feature_train_df)


            train_arr = np.c_[
                input_features_scaled_train_arr, np.array(target_feature_sampled_train_df)
            ]
            test_arr = np.c_[input_feature_scaled_test_arr, np.array(target_feature_test_df)]


            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file,
                obj=preprocessing_obj
            )
            

            logging.info(f"data transformation completed!!")
            return (
                train_arr,
                test_arr,
                #self.data_transformation_config.preprocessor_obj_file
            )
        
        except Exception as e:
            raise CustomException(e,sys)
        