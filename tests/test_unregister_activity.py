def test_unregister_success_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/participants"

    # Act
    unregister_response = client.delete(endpoint, params={"email": email})
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in participants


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"
    endpoint = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_non_enrolled_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "notenrolled@mergington.edu"
    endpoint = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_activity_data_is_isolated_between_tests(client):
    # Arrange
    activity_name = "Chess Club"
    baseline_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    endpoint = f"/activities/{activity_name}"

    # Act
    response = client.get("/activities")
    participants = response.json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert participants == baseline_participants
