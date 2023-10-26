from src.logger import logging
from src.exception import CustomException
import sys


from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer



class TrainingPipeline:
    def start_model_training(self):
        """
        start_model_training function will return the best model with score
        """

        try:
            logging.info("Model training has started!!")

            logging.info("Data ingestion has started!!")
            data_ingestion = DataIngestion()
            train_data_path, test_data_path=data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion has finished!!")

            logging.info("Data transformation has started.")
            data_transformation=DataTransformation()
            train_arr,test_arr=data_transformation.initiate_data_transformation(train_data_path, test_data_path)

            logging.info("Data transformation has completed")

            logging.info("Model training has started")
            model_trainer=ModelTrainer()
            print(model_trainer.initiate_model_trainer(train_arr, test_arr))
            logging.info("Model training has completed!! ")

        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":

    training_pipeline = TrainingPipeline()
    training_pipeline.start_model_training()

