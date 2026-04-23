def test_signup_success_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    signup_response = client.post(endpoint, params={"email": email})
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert signup_response.status_code == 200
    assert signup_response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in participants


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_email_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"
    before_response = client.get("/activities")
    before_count = len(before_response.json()[activity_name]["participants"])

    # Act
    response = client.post(endpoint, params={"email": existing_email})
    after_response = client.get("/activities")
    after_count = len(after_response.json()[activity_name]["participants"])

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"
    assert before_count == after_count


def test_signup_with_url_encoded_activity_name_works(client):
    # Arrange
    encoded_activity_name = "Chess%20Club"
    decoded_activity_name = "Chess Club"
    email = "encoded@mergington.edu"
    endpoint = f"/activities/{encoded_activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})
    activities_response = client.get("/activities")
    participants = activities_response.json()[decoded_activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert email in participants
