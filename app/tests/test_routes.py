from app.models.planet import Planet


def test_get_all_planets_with_no_records(client):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_one_planet(client, one_saved_planet):
    # Act
    response = client.get(f"/planets/{one_saved_planet.id}")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": one_saved_planet.id,
        "name": one_saved_planet.name,
        "description": one_saved_planet.description,
        "diameter": one_saved_planet.diameter
    }



def test_create_one_planet(client):
    # Act
    response = client.post("/planets", json={
        "name": "Jupiter",
        "description": "biggest planet",
        "diameter": 86881
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Planet Jupiter successfully created"


def test_get_one_that_dont_exist_and_returns_error_message(client):
    response = client.get("/planets/1")
    response_body = response.get_json()

    assert response.status_code == 404 
    assert response_body["message"] == "Planet 1 not found"
