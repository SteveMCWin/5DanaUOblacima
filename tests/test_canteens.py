def test_create_canteen_as_admin(client, admin_student):
    """Test creating a canteen as an admin"""
    response = client.post(
        "/canteens",
        headers={"studentId": str(admin_student["id"])},
        json={
            "name": "New Canteen",
            "location": "Location 1",
            "capacity": 20,
            "workingHours": [
                {"meal": "breakfast", "from": "08:00", "to": "10:00"},
                {"meal": "lunch", "from": "11:00", "to": "14:00"}
            ]
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Canteen"
    assert data["capacity"] == 20


def test_create_canteen_as_regular_user(client, regular_student):
    """Test that regular users cannot create canteens"""
    response = client.post(
        "/canteens",
        headers={"studentId": str(regular_student["id"])},
        json={
            "name": "Unauthorized Canteen",
            "location": "Location 2",
            "capacity": 15,
            "workingHours": [
                {"meal": "lunch", "from": "11:00", "to": "14:00"}
            ]
        }
    )
    
    assert response.status_code == 418


def test_get_canteen_by_id(client, sample_canteen):
    """Test getting a specific canteen by ID"""
    response = client.get(f"/canteens/{sample_canteen['id']}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_canteen["id"]
    assert data["name"] == sample_canteen["name"]


def test_update_canteen_name(client, admin_student, sample_canteen):
    """Test updating canteen name"""
    response = client.put(
        f"/canteens/{sample_canteen['id']}",
        headers={"studentId": str(admin_student["id"])},
        json={"name": "Updated Canteen Name"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Canteen Name"


def test_delete_canteen_as_admin(client, admin_student, sample_canteen):
    """Test deleting a canteen as admin"""
    response = client.delete(
        f"/canteens/{sample_canteen['id']}",
        headers={"studentId": str(admin_student["id"])}
    )
    
    assert response.status_code == 204
