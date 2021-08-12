from grocery_api.resources.grocery_resource import GROCERY_ENDPOINT

def test_get_all_groceries(client):
    response = client.get(f"{GROCERY_ENDPOINT}")
    assert response.status_code == 200
    assert len(response.json) == 6

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

def test_post_one_grocery(client):
    new_grocery_json = {"shop_id": "1", "vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 201
    assert response.json == 7
    response = client.get(f"{GROCERY_ENDPOINT}/{response.json}")
    assert response.json["date_bought"] == "2021-08-30"

def test_post_one_product_empty_shop_id(client):
    new_grocery_json = {"shop_id": "", "vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["shop_id"] == ['Shop field cannot be empty']

def test_post_one_product_missing_shop_id(client):
    new_grocery_json = {"vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["shop_id"] == ['Shop field cannot be empty']

def test_post_one_product_shop_id_None(client):
    new_grocery_json = {"shop_id": None, "vendor_id": "1", "product_id": "1", "date_bought": "2021-08-30", "weight_in_pounds": "1", "quantity": "1", "price": "2.99"}
    response = client.post(f"{GROCERY_ENDPOINT}", json=new_grocery_json)
    assert response.status_code == 500
    assert response.json["message"]["shop_id"] == ['Field may not be null.']