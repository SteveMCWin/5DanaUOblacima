def test_create_reservation_30min(client, regular_student, sample_canteen):
    """Test creating a 30-minute reservation"""
    response = client.post(
        "/reservations",
        json={
            "studentId": regular_student["id"],
            "canteenId": sample_canteen["id"],
            "date": "2025-12-15",
            "time": "12:00",
            "duration": 30
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["duration"] == 30
    assert data["status"] == "Active"


def test_create_reservation_outside_working_hours(client, regular_student, sample_canteen):
    """Test that reservations outside working hours are rejected"""
    response = client.post(
        "/reservations",
        json={
            "studentId": regular_student["id"],
            "canteenId": sample_canteen["id"],
            "date": "2025-12-15",
            "time": "22:00",
            "duration": 30
        }
    )
    
    assert response.status_code == 418


def test_create_overlapping_reservations(client, regular_student, sample_canteen):
    """Test that overlapping reservations are rejected"""
    client.post(
        "/reservations",
        json={
            "studentId": regular_student["id"],
            "canteenId": sample_canteen["id"],
            "date": "2025-12-15",
            "time": "12:00",
            "duration": 30
        }
    )
    
    response = client.post(
        "/reservations",
        json={
            "studentId": regular_student["id"],
            "canteenId": sample_canteen["id"],
            "date": "2025-12-15",
            "time": "12:00",
            "duration": 30
        }
    )
    
    assert response.status_code == 418


def test_delete_own_reservation(client, regular_student, sample_reservation):
    """Test that a student can delete their own reservation"""
    response = client.delete(
        f"/reservations/{sample_reservation['id']}",
        headers={"studentId": str(regular_student["id"])}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Cancelled"


def test_delete_other_student_reservation(client, sample_reservation):
    """Test that a student cannot delete another student's reservation"""
    other_student = client.post(
        "/students",
        json={
            "name": "Other Student",
            "email": "other@test.com",
            "isAdmin": False
        }
    ).json()
    
    response = client.delete(
        f"/reservations/{sample_reservation['id']}",
        headers={"studentId": str(other_student["id"])}
    )
    
    assert response.status_code == 418
