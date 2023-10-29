import os
import yaml
import logging
import time
import pandas as pd
import json
import pickle
import sys
from src.logger import logging
from src.exception import CustomException
from sklearn.model_selection import GridSearchCV
from src.config import mongo_client
from sklearn.metrics import r2_score,accuracy_score




def read_yaml(path_to_yaml: str) -> dict:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    logging.info(f"yaml file: {path_to_yaml} loaded successfully")
    return content

def create_directories(path_to_directories: list) -> None:
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        logging.info(f"created directory at: {path}")


def save_json(path: str, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logging.info(f"json file saved at: {path}")

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=2)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)


            #train_model_score = model.score(y_train, y_train_pred)

            #test_model_score = model.score(X_test, y_test_pred)
            test_model_score = accuracy_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score
            

        return report
    
    except Exception as e:
        raise CustomException(e, sys)
    

def get_collection_as_dataframe(database_name, collection_name):
    """
    Description: This function returns collection as dataframe
    ==========================================================
    params:
    database-name: database_name
    collection_name: collection_name
    ===========================================================
    returns Pandas dataframe of a collection"""

    try:
        logging.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")
        if 'Booking_ID' in df.columns:
            logging.info(f"Dropping column: Booking_ID")
            df = df.drop("Booking_ID", axis=1)
            df = df.reset_index(drop=True)
        logging.info(f"Row and columns in df: {df.shape}")
        return df
    except Exception as e:
        raise CustomException(e, sys)
