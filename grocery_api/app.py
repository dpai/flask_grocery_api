import logging

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import datetime
import pandas as pd
import altair as alt
import time
import cv2
import os
import numpy as np

from flask import Flask, render_template, Response
from flask_restful import Api
from grocery_api.database import db_session
from grocery_api.resources.product_resource import ProductResource, ProductByNameResource, PRODUCT_ENDPOINT
from grocery_api.resources.vendor_resource import VendorResource, VendorByNameResource, VENDOR_ENDPOINT
from grocery_api.resources.shop_resource import ShopResource, ShopByNameResource, SHOP_ENDPOINT
from grocery_api.resources.grocery_resource import GroceryResource, GroceryByProductNameResource, GROCERY_ENDPOINT

from tensorflow.keras.models import Model, load_model

logger = logging.getLogger('pythonLogger')

# Helpers
def checkPathExists(path):
  if not os.path.exists(path):
    logger.info(f"Cannot access path: {path}")
    return False
  else:
    logger.info(f"Path {path} accessible")
    return True
  
def load_currency_model():
    if checkPathExists('full_model.h5'):
        inference_model = load_model('full_model.h5')
        return inference_model
    else:
        logger.info("Inference Model not found")
        return None

def create_app(config_object=None):
    # Init app
    app = Flask(__name__)
    app.config.from_object(config_object)

    logger.info(config_object)

    api = Api(app)

    api.add_resource(ProductResource, PRODUCT_ENDPOINT, f"{PRODUCT_ENDPOINT}/<int:id>")
    api.add_resource(ProductByNameResource, PRODUCT_ENDPOINT, f"{PRODUCT_ENDPOINT}/<string:product_name>")
    api.add_resource(VendorResource, VENDOR_ENDPOINT, f"{VENDOR_ENDPOINT}/<int:id>")
    api.add_resource(VendorByNameResource, VENDOR_ENDPOINT, f"{VENDOR_ENDPOINT}/<string:vendor_name>")
    api.add_resource(ShopResource, SHOP_ENDPOINT, f"{SHOP_ENDPOINT}/<int:id>")
    api.add_resource(ShopByNameResource, SHOP_ENDPOINT, f"{SHOP_ENDPOINT}/<string:shop_name>")
    api.add_resource(GroceryResource, GROCERY_ENDPOINT, f"{GROCERY_ENDPOINT}/<int:id>")
    api.add_resource(GroceryByProductNameResource, GROCERY_ENDPOINT, f"{GROCERY_ENDPOINT}/<string:product_name>")

    inference_model = load_currency_model()
    IMG_SIZE = (224, 224)
    labels = ['100_1', '100_2', '10_1', '10_2', '1_1', '1_2', '20_1', '20_2', '2_1',
       '2_2', '50_1', '50_2', '5_1', '5_2']

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    @app.route('/app')
    @app.route('/')
    def hello():
        ## Get all the products from the database and generate a list to consue for pywebio
        
        pydict = ProductResource().get()
        product_list = {x['name']:x['id'] for x in pydict[0]}
        return render_template('starter.html', products=product_list)

    @app.route('/app/compareProduct/<product_name>', methods=['GET'])
    def compareProduct(product_name):
        pydict = GroceryByProductNameResource().get(product_name)

        product_df = pd.DataFrame(pydict[0])
        product_df.rename(columns={"shop.shop_name":"shop"}, inplace = True)
        product_df['price_per_pound'] = round(product_df['price']/product_df['quantity']/product_df['weight_in_pounds'], 2)

        # Create a selection that chooses the nearest point & selects based on x-value
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                        fields=['date_bought'], empty='none')

        lines = (
            alt.Chart(product_df)
            .mark_line(point=True)
            .encode(x="date_bought", y="price_per_pound", color="shop")
        )

        # Transparent selectors across the chart. This is what tells us
        # the x-value of the cursor
        selectors = alt.Chart(product_df).mark_point().encode(
            x='date_bought:O',
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )

        # Draw points on the line, and highlight based on selection
        points = lines.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )

        # Draw text labels near the points, and highlight based on selection
        text = lines.mark_text(align='left', dx=5, dy=-5).encode(
            text=alt.condition(nearest, 'price_per_pound:Q', alt.value(' '))
        )

        # Put the five layers into a chart and bind the data
        chart = alt.layer(
            lines, selectors, points, text
        ).properties(
            width=450, height=500
        )
        chart_json = chart.to_json()

        payload = { "data": pydict[0], "plot": chart_json}

        return payload
    
    def gen():
        """Video streaming generator function."""
        cap = cv2.VideoCapture('video_usd.mp4')

        # Read until video is completed
        while(cap.isOpened()):
        # Capture frame-by-frame
            ret, img = cap.read()
            if ret == True:
                img_resize = cv2.resize(img, (IMG_SIZE[0], IMG_SIZE[1])) 
                time.sleep(1.0/60)
                img_input = np.array([img_resize/255.0])
                y_pred = inference_model.predict(img_input)
                predictions = np.argmax(y_pred, axis=1)
                predicted_denominations = labels[int(predictions)]
                logger.info(f"{predicted_denominations.split('_')[0]} Dollars")
                cv2.putText(img_resize, f"{predicted_denominations.split('_')[0]} Dollars", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
                frame = cv2.imencode('.jpg', img_resize)[1].tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            else: 
                break
        
    @app.route('/video_feed')
    def video_feed():
        """Video streaming route. Put this in the src attribute of an img tag."""
        return Response(gen(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/usd_detect')
    def detect():
        return render_template('vfeed.html')
    
    return app