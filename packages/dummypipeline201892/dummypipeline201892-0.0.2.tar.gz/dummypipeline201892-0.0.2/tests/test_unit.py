import os
import pytest
from database import firebase
import firebase_admin
from firebase_admin import db, credentials


@pytest.fixture
def firebase_initialized():
    firebase.initialize_firebase()
    yield


# Test per connessione
def test_firebase_connection(firebase_initialized):
    assert True