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