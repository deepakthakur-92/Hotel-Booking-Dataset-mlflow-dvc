import os
import sys
from dataclasses import dataclass


from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score,precision_score, recall_score,log_loss

from src.exception import CustomException
from src.logger import logging

from src.utils.common import save_object,evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()


    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Split training and test input data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            print("x_train shape", X_train.shape)
            print("x_test", X_test.shape)
            models = {
                "Random Forest": RandomForestClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "Logistic Regression": LogisticRegression(),
                "XGBRegressor": XGBClassifier(),
            }
            params={
                "Decision Tree": {
                   # 'criterion':['gini','entropy],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                   'n_estimators' : [100],
                #    'n_jobs' : [-1],
                 #  'max_features':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
                #   'max_depth':[3, 4, 5, 6, 7, 9, 11],
                #    'min_samples_split':[2,3]
                },

                "Logistic Regression":{},
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }

            model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,
                                             models=models,param=params)
            
            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found",sys)
            logging.info(f"Best found model on both training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)
            predicted=best_model.predict(X_test)
            acc = accuracy_score(y_test, predicted)
            prec = precision_score(y_test, predicted)
            recall = recall_score(y_test, predicted)
            return acc
            return prec
            return recall
            print(acc)
            print(prec)
            print(recall)
            logging.log(acc,prec,recall)
                     
        except Exception as e:
            raise CustomException(e,sys)