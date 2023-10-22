import os
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.utils.common import save_object, load_object



class PredictPipeline:
    def __init__(self):
        pass


    def predict(self, features):
        try:
            model_path = os.path.join("artifacts","model.pkl")
            preprocessor_path=os.path.join('artifacts','preprocessor.pkl')
            print("Before Loading")
            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            print("After Loading")
            data_scaled=preprocessor.transform(features)
            preds=model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise CustomException(e,sys)
        


class CustomData:
    def __init__(self,
                meal: str,
                required_car_parking_spaces: int,
                assigned_room_type: str,
                lead_time: int,
                market_segment: str,
                reserved_room_type: str,
                is_repeated_guest: int,
                previous_cancellations: int,
                previous_bookings_not_canceled, int,
                total_of_special_requests: int,
                average_price_rooms: int,
                total_stays: int
                ):
        
        self.meal = meal
        self.required_car_parking_spaces = required_car_parking_spaces
        self.assigned_room_type = assigned_room_type
        self.lead_time = lead_time
        self.market_segment = market_segment
        self.reserved_room_type = reserved_room_type
        self.is_repeated_guest = is_repeated_guest
        self.previous_cancellations = previous_cancellations
        self.previous_bookings_not_canceled = previous_bookings_not_canceled
        self.total_of_special_requests = total_of_special_requests
        self.average_price_rooms = average_price_rooms
        self.total_stays = total_stays


    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict={
                
            }
        


