"""Tests for the Flask API endpoints"""

import json
import pytest


class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_index_route(self, client):
        """Test main page loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Huffman Coding' in response.data
    
    def test_encode_endpoint_success(self, client, sample_text):
        """Test successful encoding"""
        response = client.post(
            '/encode',
            data=json.dumps({'text': sample_text}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'encoded' in data
        assert 'frequency_table' in data
        assert 'huffman_codes' in data
        assert 'stats' in data
        
        # Check stats structure
        stats = data['stats']
        assert 'original_size' in stats
        assert 'compressed_size' in stats
        assert 'compression_ratio' in stats
        assert 'space_saved' in stats
    
    def test_encode_endpoint_empty_text(self, client):
        """Test encoding with empty text"""
        response = client.post(
            '/encode',
            data=json.dumps({'text': ''}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_encode_endpoint_no_json(self, client):
        """Test encoding without JSON data"""
        response = client.post('/encode')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_decode_endpoint_success(self, client, sample_text):
        """Test successful decoding"""
        # First encode the text
        encode_response = client.post(
            '/encode',
            data=json.dumps({'text': sample_text}),
            content_type='application/json'
        )
        encode_data = json.loads(encode_response.data)
        
        # Then decode it
        response = client.post(
            '/decode',
            data=json.dumps({
                'encoded': encode_data['encoded'],
                'frequency_table': encode_data['frequency_table']
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['decoded'] == sample_text
    
    def test_decode_endpoint_missing_data(self, client):
        """Test decoding with missing data"""
        response = client.post(
            '/decode',
            data=json.dumps({'encoded': '0101'}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_decode_endpoint_invalid_frequency_table(self, client):
        """Test decoding with invalid frequency table"""
        response = client.post(
            '/decode',
            data=json.dumps({
                'encoded': '0101',
                'frequency_table': 'invalid'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_404_error(self, client):
        """Test 404 error handling"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_method_not_allowed(self, client):
        """Test 405 error handling"""
        response = client.get('/encode')
        assert response.status_code == 405
        data = json.loads(response.data)
        assert 'error' in data
