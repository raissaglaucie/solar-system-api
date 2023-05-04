from werkzeug.exceptions import HTTPException
from app.routes import validate_model
from app.models.planet import Planet
import pytest

def test_get_all_planets_with_no_records(client):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_planets_with_two_records(client, two_saved_planets):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 1,
        "name": "Mercury",
        "description": "smallest planet",
        "diameter": 3031.9
    }
    assert response_body[1] == {
        "id": 2,
        "name": "Jupiter",
        "description": "biggest planet",
        "diameter": 86881
    }
    
def test_get_all_planets_with_title_query_matching_none(client, two_saved_planets):
    # Act
    data = {'name': 'Dog'}
    response = client.get("/planets", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_planets_with_title_query_matching_one(client, two_saved_planets):
    # Act
    data = {'name': 'Mercury'}
    response = client.get("/planets", query_string = data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0] == {
        "id": 1,
        "name": "Mercury",
        "description": "smallest planet",
        "diameter": 3031.9
    }

def test_get_one_planet_missing_record(client, two_saved_planets):
    # Act
    response = client.get("/planets/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Planet 3 not found"}

def test_get_one_planet_invalid_id(client, two_saved_planets):
    # Act
    response = client.get("/planets/earth")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message":"Planet earth invalid"}

def test_get_one_planet(client, two_saved_planets):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Mercury",
        "description": "smallest planet",
        "diameter": 3031.9
    }

def test_create_one_planet(client):
    # Act
    response = client.post("/planets", json={
        "name": "Pluto",
        "description": "dwarf planet",
        "diameter": 1473
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Planet Pluto successfully created"

def test_create_one_planet_no_name(client):
    # Arrange
    test_data = {"description": "The Best!", "diameter": 1000}
    response = client.post("/planets", json=test_data)
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["message"] == 'missing required values'
    assert response_body["missing_values"] == ['name']

def test_create_one_planet_no_description(client):
    # Arrange
    test_data = {"name": "New planet", "diameter": 1000}
    response = client.post("/planets", json=test_data)
    response_body = response.get_json()

    # Act & Assert
    assert response.status_code == 400
    assert response_body["message"] == 'missing required values'
    assert response_body["missing_values"] == ['description']

def test_create_one_planet_no_diameter(client):
    # Arrange
    test_data = {"name": "New planet", "description": "The Best!"}
    response = client.post("/planets", json=test_data)
    response_body = response.get_json()

    # Act & Assert
    assert response.status_code == 400
    assert response_body["message"] == 'missing required values'
    assert response_body["missing_values"] == ['diameter']

def test_create_one_planet_no_name_and_no_description(client):
    # Arrange
    test_data = {"diameter": 1000}
    response = client.post("/planets", json=test_data)
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["message"] == 'missing required values'
    assert response_body["missing_values"] == ['name', 'description']

def test_create_one_planet_no_name_and_no_diameter(client):
    # Arrange
    test_data = {"description": "The Best!"}
    response = client.post("/planets", json=test_data)
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["message"] == 'missing required values'
    assert response_body["missing_values"] == ['name', 'diameter']

def test_create_one_planet_no_description_and_no_diameter(client):
    # Arrange
    test_data = {"name": "New planet"}
    response = client.post("/planets", json=test_data)
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["message"] == 'missing required values'
    assert response_body["missing_values"] == ['description', 'diameter']

def test_create_one_planet_with_extra_keys(client, two_saved_planets):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "name": "New planet",
        "description": "The Best!",
        "diameter": 1000,
        "another": "last value"
    }

    # Act
    response = client.post("/planets", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Planet New planet successfully created"

def test_create_one_planet_with_invalid_diameter(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "New planet",
        "description": "The Best!",
        "diameter": "dog"
    }

    # Act
    response = client.post("/planets", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["error"]

def test_replace_planet(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "New planet",
        "description": "The Best!",
        "diameter": 1000
    }

    # Act
    response = client.put("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Planet #1 successfully updated"

def test_replace_planet_with_extra_keys(client, two_saved_planets):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "name": "New planet",
        "description": "The Best!",
        "diameter": 1000,
        "another": "last value"
    }

    # Act
    response = client.put("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Planet #1 successfully updated"

def test_replace_planet_missing_record(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "New planet",
        "description": "The Best!",
        "diameter": 1000
    }

    # Act
    response = client.put("/planets/3", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Planet 3 not found"}

def test_replace_planet_no_name(client, two_saved_planets):
    # Arrange
    test_data = {
        "description": "The Best!",
        "diameter": 1000
    }

    # Act
    response = client.put("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["message"] == "missing required values"
    assert response_body["missing_values"] == ["name"]

def test_replace_planet_no_description(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "New planet",
        "diameter": 1000
    }

    # Act
    response = client.put("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["message"] == "missing required values"
    assert response_body["missing_values"] == ["description"]

def test_replace_planet_no_diameter(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "New planet",
        "description": "The Best!"
    }

    # Act
    response = client.put("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["message"] == "missing required values"
    assert response_body["missing_values"] == ["diameter"]

def test_replace_planet_no_name_no_description(client, two_saved_planets):
    # Arrange
    test_data = {
        "diameter": 1000
    }

    # Act
    response = client.put("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["message"] == "missing required values"
    assert response_body["missing_values"] == ["name", "description"]

def test_replace_planet_no_name_no_diameter(client, two_saved_planets):
    # Arrange
    test_data = {
        "description": "The Best!"
    }

    # Act
    response = client.put("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["message"] == "missing required values"
    assert response_body["missing_values"] == ["name", "diameter"]

def test_replace_planet_no_description_no_diameter(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "New planet"
    }

    # Act
    response = client.put("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["message"] == "missing required values"
    assert response_body["missing_values"] == ["description", "diameter"]

def test_replace_planet_invalid_id(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "New planet",
        "description": "The Best!",
        "diameter": 1000
    }

    # Act
    response = client.put("/planets/dog", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Planet dog invalid"}

def test_replace_planet_invalid_diameter(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "New planet",
        "description": "The Best!",
        "diameter": "dog"
    }

    # Act
    response = client.put("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body['error']

def test_update_planet_name_only(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "New planet"
    }

    # Act
    response = client.patch("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Planet #1 successfully updated"

def test_update_planet_description_only(client, two_saved_planets):
    # Arrange
    test_data = {
        "description": "The Best!"
    }

    # Act
    response = client.patch("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Planet #1 successfully updated"

def test_update_planet_diameter_only(client, two_saved_planets):
    # Arrange
    test_data = {
        "diameter": 1000
    }

    # Act
    response = client.patch("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Planet #1 successfully updated"

def test_update_planet_name_and_description(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "New planet",
        "description": "The Best!"
    }

    # Act
    response = client.patch("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Planet #1 successfully updated"

def test_update_planet_name_and_diameter(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "New planet",
        "diameter": 1000
    }

    # Act
    response = client.patch("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Planet #1 successfully updated"

def test_update_planet_description_and_diameter(client, two_saved_planets):
    # Arrange
    test_data = {
        "description": "The Best!",
        "diameter": 1000
    }

    # Act
    response = client.patch("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Planet #1 successfully updated"

def test_update_planet_name_description_and_diameter(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "New planet",
        "description": "The Best!",
        "diameter": 1000
    }

    # Act
    response = client.patch("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Planet #1 successfully updated"

def test_update_planet_with_extra_keys(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "New planet",
        "description": "The Best!",
        "diameter": 1000,
        "another": "last value"
    }

    # Act
    response = client.patch("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Planet #1 successfully updated"

def test_update_planet_missing_record(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "New planet",
        "description": "The Best!",
        "diameter": 1000
    }

    # Act
    response = client.patch("/planets/3", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Planet 3 not found"}

def test_update_planet_invalid_id(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "New planet",
        "description": "The Best!",
        "diameter": 1000
    }

    # Act
    response = client.patch("/planets/dog", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Planet dog invalid"}

def test_update_planet_invalid_diameter(client, two_saved_planets):
    # Arrange
    test_data = {
        "name": "New planet",
        "description": "The Best!",
        "diameter": "dog"
    }

    # Act
    response = client.patch("/planets/1", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["message"] == "Invalid request body"
    assert response_body["error"]

def test_delete_planet(client, two_saved_planets):
    # Act
    response = client.delete("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Planet #1 Mercury successfully deleted"

def test_delete_planet_missing_record(client, two_saved_planets):
    # Act
    response = client.delete("/planets/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Planet 3 not found"}

def test_delete_planet_invalid_id(client, two_saved_planets):
    # Act
    response = client.delete("/planets/dog")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Planet dog invalid"}

def test_validate_model(two_saved_planets):
    # Act
    result_planet = validate_model(Planet, 1)

    # Assert
    assert result_planet.id == 1
    assert result_planet.name == "Mercury"
    assert result_planet.description == "smallest planet"
    assert result_planet.diameter == 3031.9

def test_validate_model_missing_record(two_saved_planets):
    # Act & Assert
    with pytest.raises(HTTPException):
        result_planet = validate_model(Planet, "3")
    
def test_validate_model_invalid_id(two_saved_planets):
    # Act & Assert
    with pytest.raises(HTTPException):
        result_planet = validate_model(Planet, "dog")