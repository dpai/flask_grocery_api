from grocery_api.resources.product_resource import PRODUCT_ENDPOINT

def test_get_all_products(client):
    response = client.get(f"{PRODUCT_ENDPOINT}")
    assert response.status_code == 200
    assert len(response.json) == 4

def test_get_one_product(client):
    response = client.get(f"{PRODUCT_ENDPOINT}/1")
    assert response.status_code == 200
    assert len(response.json) == 4
    assert response.json["name"] == "Product1"
    assert response.json["vendor_id"] == 1
    assert response.json["vendor.name"] == "Vendor1"

def test_post_one_product(client):
    new_product_json = {"name": "Product5", "vendor_id": "2", "id": "5"}
    response = client.post(f"{PRODUCT_ENDPOINT}", json=new_product_json)
    assert response.status_code == 201
    assert response.json == 5

def test_post_one_product_empty_name(client):
    new_product_json = {"name": ""}
    response = client.post(f"{PRODUCT_ENDPOINT}", json=new_product_json)
    assert response.status_code == 500
    assert response.json["message"]["name"] == ['Product Name cannot be empty']

def test_post_one_product_nonexistent_vendor(client):
    new_product_json = {"name": "Product6", "vendor_id": "10", "id": "6"}
    response = client.post(f"{PRODUCT_ENDPOINT}", json=new_product_json)
    assert response.status_code == 500
    assert response.json["message"] == "Unexpected Error!"

def test_delete_one_product_by_id(client):
    new_product_json = {"name": "Product7", "vendor_id": "2", "id": "7"}
    response = client.post(f"{PRODUCT_ENDPOINT}", json=new_product_json)
    assert response.status_code == 201
    assert response.json == 7
    response = client.delete(f"{PRODUCT_ENDPOINT}/{response.json}")
    assert response.status_code == 200

def test_delete_one_product_id_not_found(client):
    response = client.delete(f"{PRODUCT_ENDPOINT}/7")
    assert response.status_code == 404

def test_delete_one_product_by_name(client):
    new_product_json = {"name": "Product8", "vendor_id": "2", "id": "8"}
    response = client.post(f"{PRODUCT_ENDPOINT}", json=new_product_json)
    assert response.status_code == 201
    response = client.delete(f"{PRODUCT_ENDPOINT}/Product8")
    assert response.status_code == 200

def test_delete_one_product_by_name_not_found(client):
    response = client.delete(f"{PRODUCT_ENDPOINT}/Product8")
    assert response.status_code == 404

def test_delete_one_product_wrong_URI(client):
    response = client.delete(f"{PRODUCT_ENDPOINT}")
    assert response.status_code == 405
