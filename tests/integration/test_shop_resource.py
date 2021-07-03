from grocery_api.resources.shop_resource import SHOP_ENDPOINT

def test_get_all_shops(client):
    response = client.get(f"{SHOP_ENDPOINT}")
    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_one_shop(client):
    response = client.get(f"{SHOP_ENDPOINT}/1")
    assert response.status_code == 200
    assert len(response.json) == 3
    assert response.json["shop_name"] == "Test1"
    assert response.json["location"] == "Wisonsin"

def test_post_one_shop(client):
    new_shop_json = {"shop_name": "Test3", "location": "PA"}
    response = client.post(f"{SHOP_ENDPOINT}", json=new_shop_json)
    assert response.status_code == 201
    assert response.json == 3

def test_post_one_shop_empty_name(client):
    new_shop_json = {"shop_name": "", "location": "XYZ"}
    response = client.post(f"{SHOP_ENDPOINT}", json=new_shop_json)
    assert response.status_code == 500
    assert response.json["message"]["shop_name"] == ['Shop Name cannot be empty']

def test_post_one_shop_name_None(client):
    new_shop_json = {"shop_name": None, "location": "XYZ"}
    response = client.post(f"{SHOP_ENDPOINT}", json=new_shop_json)
    assert response.status_code == 500
    assert response.json["message"]["shop_name"] == ['Field may not be null.']

def test_post_one_shop_empty_location(client):
    new_shop_json = {"shop_name": "Test5", "location": ""}
    response = client.post(f"{SHOP_ENDPOINT}", json=new_shop_json)
    assert response.status_code == 500
    assert response.json["message"]["location"] == ['Location cannot be empty']

def test_post_one_shop_location_None(client):
    new_shop_json = {"shop_name": "Test5", "location": None}
    response = client.post(f"{SHOP_ENDPOINT}", json=new_shop_json)
    assert response.status_code == 500
    assert response.json["message"]["location"] == ['Field may not be null.']

def test_get_shop_not_found(client):
    response = client.get(f"{SHOP_ENDPOINT}/100")
    assert response.status_code == 404

def test_get_shop_name_not_found(client):
    response = client.get(f"{SHOP_ENDPOINT}/Test100")
    assert response.status_code == 404

def test_delete_one_shop(client):
    new_shop_json = {"shop_name": "Test10", "location": "WA"}
    response = client.post(f"{SHOP_ENDPOINT}", json=new_shop_json)
    assert response.status_code == 201
    response = client.delete(f"{SHOP_ENDPOINT}/Test10")
    assert response.status_code == 200

def test_delete_one_shop_not_found(client):
    response = client.delete(f"{SHOP_ENDPOINT}/Test10")
    assert response.status_code == 404

def test_delete_one_shop_by_id(client):
    new_shop_json = {"shop_name": "Test6", "location": "FL"}
    response = client.post(f"{SHOP_ENDPOINT}", json=new_shop_json)
    assert response.status_code == 201
    response = client.delete(f"{SHOP_ENDPOINT}/{response.json}")
    assert response.status_code == 200

def test_delete_one_shop_id_not_found(client):
    response = client.delete(f"{SHOP_ENDPOINT}/4")
    assert response.status_code == 404

def test_delete_one_shop_wrong_URI(client):
    response = client.delete(f"{SHOP_ENDPOINT}")
    assert response.status_code == 405

def test_put_by_shop_id(client):
    new_shop_json = {"shop_name": "Test20", "location": "PS"}
    response = client.post(f"{SHOP_ENDPOINT}", json=new_shop_json)
    assert response.status_code == 201
    update_shop_json = {"shop_name": "Test21", "location": "PA"}
    response = client.put(f"{SHOP_ENDPOINT}/{response.json}", json=update_shop_json)
    assert response.status_code == 200
    response = client.get(f"{SHOP_ENDPOINT}/{response.json}")
    assert response.status_code == 200
    assert response.json["shop_name"] == "Test21"
    assert response.json["location"] == "PA"