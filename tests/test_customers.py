def test_create_customer(client):
    response = client.post(
        "/customers/",
        json={
            "name": "Jane Doe",
            "room_number": "305",
            "phone": "0700000000",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Jane Doe"
    assert data["room_number"] == "305"
    assert data["phone"] == "0700000000"
    assert "id" in data


def test_list_customers(client):
    client.post(
        "/customers/",
        json={
            "name": "Guest One",
            "room_number": "101",
            "phone": "0711111111",
        },
    )

    client.post(
        "/customers/",
        json={
            "name": "Guest Two",
            "room_number": "102",
            "phone": "0722222222",
        },
    )

    response = client.get("/customers/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Guest One"
    assert data[1]["name"] == "Guest Two"


def test_get_customer(client):
    create_response = client.post(
        "/customers/",
        json={
            "name": "Room Guest",
            "room_number": "204",
            "phone": "0733333333",
        },
    )

    customer_id = create_response.json()["id"]

    response = client.get(f"/customers/{customer_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Room Guest"
    assert response.json()["room_number"] == "204"


def test_get_missing_customer(client):
    response = client.get("/customers/9999")

    assert response.status_code == 404


def test_update_customer(client):
    create_response = client.post(
        "/customers/",
        json={
            "name": "Old Name",
            "room_number": "201",
            "phone": "0744444444",
        },
    )

    customer_id = create_response.json()["id"]

    response = client.put(
        f"/customers/{customer_id}",
        json={
            "name": "Updated Name",
            "room_number": "202",
            "phone": "0755555555",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Name"
    assert data["room_number"] == "202"
    assert data["phone"] == "0755555555"
