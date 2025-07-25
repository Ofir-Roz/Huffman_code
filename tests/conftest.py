"""Test configuration and fixtures"""

import pytest
from app import create_app


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def sample_text():
    """Sample text for testing"""
    return "Hello World! This is a test."


@pytest.fixture
def sample_frequency_table():
    """Sample frequency table for testing"""
    return {
        'H': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 5, 'W': 1, 'r': 1, 'd': 1,
        '!': 1, 'T': 1, 'h': 1, 'i': 2, 's': 4, 'a': 1, 't': 4, '.': 1
    }
