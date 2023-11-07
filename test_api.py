import pytest
import requests

# URL of the API (you might need to adjust this depending on your setup)
API_URL = "http://localhost:8912"

# Test cases for GET /translations endpoint
def test_get_translation_success():
    # Test getting a translation that exists
    response = requests.get(f"{API_URL}/translations?word=hello&language=spanish")
    assert response.status_code == 200
    assert "translation" in response.json()

def test_get_translation_no_word():
    # Test the response for missing 'word' parameter
    response = requests.get(f"{API_URL}/translations?language=spanish")
    assert response.status_code == 400

def test_get_translation_no_language():
    # Test the response for missing 'language' parameter
    response = requests.get(f"{API_URL}/translations?word=hello")
    assert response.status_code == 400

# Test cases for POST /translations endpoint
def test_add_translation_success():
    # Test adding a new translation
    response = requests.post(f"{API_URL}/translations", json={
        "word": "test",
        "language": "spanish",
        "translation": "prueba"
    })
    assert response.status_code == 201

def test_add_translation_duplicate():
    # Test adding a translation that already exists
    response = requests.post(f"{API_URL}/translations", json={
        "word": "hello",
        "language": "spanish",
        "translation": "hola"
    })
    assert response.status_code == 409

# Test cases for PUT /translations endpoint
def test_update_translation_success():
    # Test updating an existing translation
    response = requests.put(f"{API_URL}/translations", json={
        "word": "test",
        "language": "spanish",
        "translation": "examen"
    })
    assert response.status_code == 200

def test_update_translation_nonexistent():
    # Test updating a translation that doesn't exist
    response = requests.put(f"{API_URL}/translations", json={
        "word": "nonexistent",
        "language": "spanish",
        "translation": "noexistente"
    })
    assert response.status_code == 200  # If your API does not create a new one for updates

# Test cases for DELETE /translations endpoint
def test_delete_translation_success():
    # Test deleting an existing translation
    response = requests.delete(f"{API_URL}/translations?word=test&language=spanish")
    assert response.status_code == 200

def test_delete_translation_nonexistent():
    # Test deleting a translation that doesn't exist
    response = requests.delete(f"{API_URL}/translations?word=nonexistent&language=spanish")
    assert response.status_code == 404
