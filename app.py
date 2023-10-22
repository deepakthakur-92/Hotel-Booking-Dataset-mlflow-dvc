from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipelines.prediction_pipeline import CustomData,PredictPipeline
import template

application=Flask(__name__)

app=application

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=CustomData(
            meal = request.form.get('meal'),
            required_car_parking_spaces = request.form.get('required_car_parking_spaces'),
            assigned_room_type = request.form.get('assigned_room_type'),
            lead_time = request.form.get('lead_time'),
            market_segment = request.form.get('market_segment'),
            reserved_room_type = request.form.get('reserved_room_type'),
            is_repeated_guest = request.form.get('is_repeated_guest'),
            previous_cancellations = request.form.get('previous_cancellations'),
            previous_bookings_not_canceled = request.form.get('previous_bookings_not_canceled'),
            total_of_special_requests = request.form.get('total_of_special_requests'),
            average_price_rooms = request.form.get('average_price_rooms'),
            total_stays = request.form.get('total_stays'),

        )


        pred_df=data.get_data_as_data_frame()
        print(pred_df)
        print("Before Prediction")

        predict_pipeline=PredictPipeline()
        print("Mid Prediction")
        results=predict_pipeline.predict(pred_df)
        print("after Prediction")
        return render_template('home.html',results=results[0])
    

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
    app.run()        