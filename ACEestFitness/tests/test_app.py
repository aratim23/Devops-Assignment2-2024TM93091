import pytest
import sys
import os

# Add the ACEestFitness folder to sys.path dynamically
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test loading the home page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"ACEestFitness Tracker" in response.data

def test_add_workout_success(client):
    """Test adding a workout successfully."""
    response = client.post('/add', data={'workout': 'Running', 'duration': '30'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Running" in response.data

def test_add_workout_missing_fields(client):
    """Test adding a workout with missing fields returns error."""
    response = client.post('/add', data={'workout': '', 'duration': ''})
    assert response.status_code == 200
    assert b"Please fill all fields" in response.data

def test_add_workout_invalid_duration(client):
    """Test adding a workout with invalid duration returns error."""
    response = client.post('/add', data={'workout': 'Yoga', 'duration': 'abc'})
    assert response.status_code == 200
    assert b"Duration must be a number" in response.data

def test_view_workouts_empty(client):
    """Test viewing workouts when none are added."""
    # Clear workouts list if needed
    from app import workouts
    workouts.clear()
    response = client.get('/view')
    assert response.status_code == 200
    assert b"No workouts logged yet." in response.data
