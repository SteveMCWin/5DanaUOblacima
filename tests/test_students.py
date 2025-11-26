def test_create_regular_student(client):
    """Test creating a regular student"""
    response = client.post(
        "/students",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "isAdmin": False
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["isAdmin"] is False


def test_create_student_duplicate_email(client):
    """Test that duplicate emails are rejected"""
    client.post(
        "/students",
        json={
            "name": "First Student",
            "email": "duplicate@example.com",
            "isAdmin": False
        }
    )
    
    response = client.post(
        "/students",
        json={
            "name": "Second Student",
            "email": "duplicate@example.com",
            "isAdmin": False
        }
    )
    
    assert response.status_code == 418


def test_create_student_missing_field(client):
    """Test that missing required field is rejected"""
    response = client.post(
        "/students",
        json={
            "email": "noname@example.com",
            "isAdmin": False
        }
    )
    
    assert response.status_code == 422


def test_retrieve_existing_student(client, regular_student):
    """Test retrieving an existing student"""
    response = client.get(f"/students/{regular_student['id']}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == regular_student["id"]
    assert data["name"] == regular_student["name"]


def test_retrieve_nonexistent_student(client):
    """Test retrieving a student that doesn't exist"""
    response = client.get("/students/999")
    
    assert response.status_code == 404
