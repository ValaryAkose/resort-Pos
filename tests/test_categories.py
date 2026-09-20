def test_create_category(client):
    response = client.post(
        "/categories/",
        json={
            "name": "Breakfast",
            "description": "Breakfast menu",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Breakfast"
    assert data["description"] == "Breakfast menu"
    assert "id" in data


def test_list_categories(client):
    client.post(
        "/categories/",
        json={
            "name": "Lunch",
            "description": "Lunch menu",
        },
    )

    client.post(
        "/categories/",
        json={
            "name": "Dinner",
            "description": "Dinner menu",
        },
    )

    response = client.get("/categories/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Lunch"
    assert data[1]["name"] == "Dinner"


def test_get_category(client):
    create_response = client.post(
        "/categories/",
        json={
            "name": "Desserts",
            "description": "Dessert menu",
        },
    )

    category_id = create_response.json()["id"]

    response = client.get(f"/categories/{category_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Desserts"
    assert data["description"] == "Dessert menu"


def test_get_missing_category(client):
    response = client.get("/categories/9999")

    assert response.status_code == 404


def test_update_category(client):
    create_response = client.post(
        "/categories/",
        json={
            "name": "Old Category",
            "description": "Old description",
        },
    )

    category_id = create_response.json()["id"]

    response = client.put(
        f"/categories/{category_id}",
        json={
            "name": "Updated Category",
            "description": "Updated description",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Category"
    assert data["description"] == "Updated description"
