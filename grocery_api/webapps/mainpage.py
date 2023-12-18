from flask import Blueprint, render_template
import altair as alt
import pandas as pd
from grocery_api.resources.product_resource import ProductResource
from grocery_api.resources.grocery_resource import GroceryByProductNameResource

mainbp = Blueprint('mainpage', __name__)

@mainbp.route('/app')
@mainbp.route('/')
def hello():
    ## Get all the products from the database and generate a list to consue for pywebio
    
    pydict = ProductResource().get()
    product_list = {x['name']:x['id'] for x in pydict[0]}
    return render_template('starter.html', products=product_list)

@mainbp.route('/app/compareProduct/<product_name>', methods=['GET'])
def compareProduct(product_name):
    pydict = GroceryByProductNameResource().get(product_name)

    product_df = pd.DataFrame(pydict[0])
    product_df.rename(columns={"shop.shop_name":"shop"}, inplace = True)
    product_df['price_per_pound'] = round(product_df['price']/product_df['quantity']/product_df['weight_in_pounds'], 2)

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection_point(nearest=True, on='mouseover', fields=['date_bought'], value=' ')

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