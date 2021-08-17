from grocery_api.resources.grocery_resource import GROCERY_ENDPOINT

def test_get_all_groceries(client):
    response = client.get(f"{GROCERY_ENDPOINT}")
    assert response.status_code == 200
    assert len(response.json) == 7

def test_get_one_grocery(client):
    response = client.get(f"{GROCERY_ENDPOINT}/1")
    assert response.status_code == 200
    assert len(response.json) == 7
    assert response.json["product.name"] == "Product1"
    assert response.json["shop.shop_name"] == "Test1"
    assert response.json["product.vendor.name"] == "Vendor1"
    assert response.json["date_bought"] == "2021-04-12"
    assert response.json["price"] == 2.99
    assert response.json["weight_in_pounds"] == 1
    assert response.json["quantity"] == 1

def test_get_grocery_by_product_name(client):
    response = client.get(f"{GROCERY_ENDPOINT}/Product1")
    assert response.status_code == 200
    assert len(response.json) == 3

def test_get_grocery_by_product_name_filter_vendor_name(client):
    response = client.get(f"{GROCERY_ENDPOINT}/Product1", query_string={"vendor_name": "Vendor1"})
    assert response.status_code == 200
    assert len(response.json) == 2

def test_post_one_grocery(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 201
    assert response.json == 8
    response = client.get(f"{GROCERY_ENDPOINT}/{response.json}")
    assert response.json["date_bought"] == "2021-08-30"

def test_post_one_grocery_empty_shop_id(client):
    new_grocery_json = {"shop_id": "", "vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["shop_id"] == ['Shop field cannot be empty']

def test_post_one_grocery_missing_shop_id(client):
    new_grocery_json = {"vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["shop_id"] == ['Shop field cannot be empty']

def test_post_one_grocery_shop_id_None(client):
    new_grocery_json = {"shop_id": None, "vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["shop_id"] == ['Field may not be null.']

def test_post_one_grocery_non_exixtent_shop(client):
    new_grocery_json = {"shop_id": "10", "vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"] == "Unexpected Error!"

def test_post_one_grocery_missing_vendor_id(client):
    new_grocery_json = {"shop_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["vendor_id"] == ['Vendor field cannot be empty']

def test_post_one_grocery_vendor_id_None(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": None, "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["vendor_id"] == ['Field may not be null.']

def test_post_one_grocery_non_exixtent_vendor(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "10", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"] == "Unexpected Error!"

def test_post_one_grocery_missing_product_id(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["product_id"] == ['Product field cannot be empty']

def test_post_one_grocery_product_id_None(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": None, "product_id": None, "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["product_id"] == ['Field may not be null.']

def test_post_one_grocery_non_exixtent_product(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "1", "product_id": "10", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"] == "Unexpected Error!"

def test_post_one_grocery_missing_date_bought(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "1", "product_id": "1", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["date_bought"] == ['Date Bought field cannot be empty']

def test_post_one_grocery_date_bought_None(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "1", "product_id": "1", "date_bought": None, "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["date_bought"] == ['Field may not be null.']

def test_post_one_grocery_date_bought_None(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "1", "product_id": "1", "date_bought": "", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["date_bought"] == ['Date Bought field cannot be empty']

def test_post_one_grocery_missing_weight_in_pounds(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["weight_in_pounds"] == ['Weight in Pounds field cannot be empty']

def test_post_one_grocery_weight_in_pounds_None(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": None, "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["weight_in_pounds"] == ['Field may not be null.']

def test_post_one_grocery_weight_in_pounds_Empty(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["weight_in_pounds"] == ['Weight in Pounds field cannot be empty']

def test_post_one_grocery_missing_quantity(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["quantity"] == ['Quantity field cannot be empty']

def test_post_one_grocery_quantity_None(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": None, "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["quantity"] == ['Field may not be null.']

def test_post_one_grocery_quantity_Empty(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["quantity"] == ['Quantity field cannot be empty']

def test_post_one_grocery_missing_price(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["price"] == ['Price field cannot be empty']

def test_post_one_grocery_price_None(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": None}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["price"] == ['Field may not be null.']

def test_post_one_grocery_price_Empty(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": ""}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["price"] == ['Price field cannot be empty']