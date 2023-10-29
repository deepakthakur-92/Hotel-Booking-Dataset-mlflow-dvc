from src.logger import logging
from src.exception import CustomException
import sys
import warnings


from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
import mlflow



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
            best_model,accuracy, prec, recall = model_trainer.initiate_model_trainer(train_arr, test_arr)
            logging.info("Model training has completed!! ")
            return best_model,accuracy, prec, recall


        except Exception as e:
            raise CustomException(e,sys)

    def create_experiment(self,experiment_name,run_name, accuracy, precision, recall, model, confusion_matrix_path = None, 
                      roc_auc_plot_path = None, run_params=None):
     
        #mlflow.set_tracking_uri("http://localhost:5000") #uncomment this line if you want to use any database like sqlite as backend storage for model
        mlflow.set_experiment(experiment_name)
        
        with mlflow.start_run():
            # if not run_params == None:
            #     for param in run_params:
            #         mlflow.log_param(param, run_params[param])

            
            mlflow.log_metric('accuracy', accuracy)
            mlflow.log_metric('precision', precision)
            mlflow.log_metric('recall', recall)
            
            mlflow.sklearn.log_model(model, "model")
            
            if not confusion_matrix_path == None:
                mlflow.log_artifact(confusion_matrix_path, 'confusion_matrix')
                
            if not roc_auc_plot_path == None:
                mlflow.log_artifact(roc_auc_plot_path, "roc_auc_plot")
            
            mlflow.set_tag("tag1", "Decision Tree")
            mlflow.set_tags({"tag2":"RandomForestClassifier", "tag3":"Production"})

            ## For Remote server only(DAGShub)
            remote_server_uri="https://dagshub.com/deepak2009thakur/Hotel-Booking-Dataset-mlflow-dvc.mlflow"
            mlflow.set_tracking_uri(remote_server_uri)

            

            # Suppress the specific warning
            warnings.filterwarnings("ignore", message="Setuptools is replacing distutils.")

                
        print('Run - %s is logged to Experiment - %s' %(run_name, experiment_name))
        
if __name__=="__main__":

    training_pipeline = TrainingPipeline()
    best_model, accuracy, prec, recall = training_pipeline.start_model_training()

    #experiment - 1
    training_pipeline.create_experiment("Optimized_model","Random_Forest_classifier", accuracy, prec, recall, best_model, 'confusion_matrix.png', 
                     'roc_auc_plot.png')

