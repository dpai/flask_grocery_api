import logging

import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import datetime
import pandas as pd
import altair as alt

from flask import Flask, render_template, jsonify
from flask_restful import Api
from grocery_api.database import db_session
from grocery_api.resources.product_resource import ProductResource, ProductByNameResource, PRODUCT_ENDPOINT
from grocery_api.resources.vendor_resource import VendorResource, VendorByNameResource, VENDOR_ENDPOINT
from grocery_api.resources.shop_resource import ShopResource, ShopByNameResource, SHOP_ENDPOINT
from grocery_api.resources.grocery_resource import GroceryResource, GroceryByProductNameResource, GROCERY_ENDPOINT

logger = logging.getLogger('pythonLogger')

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
        nearest = alt.selection_point(nearest=True, on='mouseover', fields=['date_bought'])

        lines = (
            alt.Chart()
            .mark_line(point=True)
            .encode(x="date_bought", y="price_per_pound", color="shop")
        )

        # Transparent selectors across the chart. This is what tells us
        # the x-value of the cursor
        selectors = alt.Chart().mark_point().encode(
            x='date_bought:O',
            opacity=alt.value(0),
        ).add_params(
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
            lines, selectors, points, text, data=product_df
        ).properties(
            width=450, height=500
        )
        chart_json = chart.to_json()

        payload = { "data": pydict[0], "plot": chart_json}

        return payload

    return app