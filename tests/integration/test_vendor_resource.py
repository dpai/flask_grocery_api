from grocery_api.resources.vendor_resource import VENDOR_ENDPOINT

def test_get_all_vendors(client):
    response = client.get(f"{VENDOR_ENDPOINT}")
    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_one_vendor(client):
    response = client.get(f"{VENDOR_ENDPOINT}/1")
    assert response.status_code == 200
    assert len(response.json) == 3
    assert response.json["name"] == "Vendor1"
    assert len(response.json["products"]) == 3
    assert response.json["products"] == ["Product1", "Product2", "Product3"]

def test_get_one_vendor_by_name(client):
    response = client.get(f"{VENDOR_ENDPOINT}/Vendor1")
    assert response.status_code == 200
    assert len(response.json) == 3
    assert response.json["name"] == "Vendor1"
    assert len(response.json["products"]) == 3
    assert response.json["products"] == ["Product1", "Product2", "Product3"]

def test_post_one_vendor(client):
    new_vendor_json = {"name": "Vendor3"}
    response = client.post(f"{VENDOR_ENDPOINT}", json=new_vendor_json)
    assert response.status_code == 201
    assert response.json == 3

def test_post_one_vendor_empty_name(client):
    new_vendor_json = {"name": ""}
    response = client.post(f"{VENDOR_ENDPOINT}", json=new_vendor_json)
    assert response.status_code == 500
    assert response.json["message"]["name"] == ['Vendor Name cannot be empty']

def test_post_one_vendor_name_None(client):
    new_vendor_json = {"name": None}
    response = client.post(f"{VENDOR_ENDPOINT}", json=new_vendor_json)
    assert response.status_code == 500
    assert response.json["message"]["name"] == ['Field may not be null.']


def test_post_one_vendor_duplicate(client):
    new_vendor_json = {"name": "Vendor2"}
    response = client.post(f"{VENDOR_ENDPOINT}", json=new_vendor_json)
    assert response.status_code == 500
    assert response.json["message"] == "Unexpected Error!"

def test_get_vendor_not_found(client):
    response = client.get(f"{VENDOR_ENDPOINT}/100")
    assert response.status_code == 404

def test_get_vendor_name_not_found(client):
    response = client.get(f"{VENDOR_ENDPOINT}/Vendor100")
    assert response.status_code == 404

def test_delete_one_vendor(client):
    new_vendor_json = {"name": "Vendor10"}
    response = client.post(f"{VENDOR_ENDPOINT}", json=new_vendor_json)
    assert response.status_code == 201
    response = client.delete(f"{VENDOR_ENDPOINT}/Vendor10")
    assert response.status_code == 200

def test_delete_one_vendor_not_found(client):
    response = client.delete(f"{VENDOR_ENDPOINT}/Vendor10")
    assert response.status_code == 404

def test_delete_one_vendor_by_id(client):
    new_vendor_json = {"name": "Vendor6"}
    response = client.post(f"{VENDOR_ENDPOINT}", json=new_vendor_json)
    assert response.status_code == 201
    response = client.delete(f"{VENDOR_ENDPOINT}/{response.json}")
    assert response.status_code == 200

def test_delete_one_vendor_id_not_found(client):
    response = client.delete(f"{VENDOR_ENDPOINT}/4")
    assert response.status_code == 404

def test_delete_one_vendor_wrong_URI(client):
    response = client.delete(f"{VENDOR_ENDPOINT}")
    assert response.status_code == 405

def test_put_by_vendor_id(client):
    new_vendor_json = {"name": "Vendor20"}
    response = client.post(f"{VENDOR_ENDPOINT}", json=new_vendor_json)
    assert response.status_code == 201
    update_vendor_json = {"name": "Vendor21"}
    response = client.put(f"{VENDOR_ENDPOINT}/{response.json}", json=update_vendor_json)
    assert response.status_code == 200
    response = client.get(f"{VENDOR_ENDPOINT}/{response.json}")
    assert response.status_code == 200
    assert response.json["name"] == "Vendor21"

def test_put_no_vendor_id(client):
    new_vendor_json = {"name": "Vendor21"}
    response = client.put(f"{VENDOR_ENDPOINT}", json=new_vendor_json)
    assert response.status_code == 405

def test_delete_vendor_with_product_reference(client):
    response = client.delete(f"{VENDOR_ENDPOINT}/2")
    assert response.status_code == 500