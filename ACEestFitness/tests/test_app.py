import pytest
import sys
import os

# Add the ACEestFitness folder to sys.path dynamically
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, workouts

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reset workouts before each test for isolation
        workouts.clear()
        workouts.update({"Warm-up": [], "Workout": [], "Cool-down": []})
        yield client

def test_index_route(client):
    """Test home page renders with correct status."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Warm-up" in response.data  # The category names appear

def test_add_workout_success(client):
    """Valid add workout form redirects to view page."""
    response = client.post('/add', data={
        'category': 'Workout',
        'exercise': 'Push-ups',
        'duration': '15'
    })
    assert response.status_code == 302  # Redirect
    assert len(workouts['Workout']) == 1
    assert workouts['Workout'][0]['exercise'] == 'Push-ups'
    assert workouts['Workout'][0]['duration'] == 15

def test_add_workout_missing_fields(client):
    """Submitting with missing fields returns error on index page."""
    response = client.post('/add', data={
        'category': '',
        'exercise': '',
        'duration': ''
    })
    assert response.status_code == 200
    assert b"Please fill all fields" in response.data

def test_add_workout_invalid_category(client):
    """Submitting an invalid category returns error."""
    response = client.post('/add', data={
        'category': 'Invalid',
        'exercise': 'Pull-ups',
        'duration': '10'
    })
    assert response.status_code == 200
    assert b"Invalid category" in response.data

def test_add_workout_invalid_duration(client):
    """Submitting non-integer duration returns error."""
    response = client.post('/add', data={
        'category': 'Warm-up',
        'exercise': 'Jogging',
        'duration': 'ten'
    })
    assert response.status_code == 200
    assert b"Duration must be an integer" in response.data

def test_view_workouts_route(client):
    """View route renders workouts in categories."""
    # Add a workout first
    client.post('/add', data={
        'category': 'Cool-down',
        'exercise': 'Stretching',
        'duration': '5'
    })
    response = client.get('/view')
    assert response.status_code == 200
    assert b"Stretching" in response.data
