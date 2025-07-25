"""
API routes for the Huffman coding application
"""

from flask import Blueprint, render_template, request, jsonify
from typing import Dict, Any

from huffman.coding import HuffmanCoding, EncodingError, DecodingError

# Create blueprint
api_bp = Blueprint('api', __name__)


@api_bp.route('/')
def index() -> str:
    """Main page"""
    return render_template('index.html')


@api_bp.route('/encode', methods=['POST'])
def encode_text() -> tuple[Dict[str, Any], int]:
    """
    Encode text using Huffman coding.
    
    Returns:
        JSON response with encoded data or error
    """
    try:
        # Handle missing or invalid JSON
        if not request.is_json:
            return {'error': 'Content-Type must be application/json'}, 400
            
        data = request.get_json()
        if data is None:
            return {'error': 'No JSON data provided'}, 400
        
        text = data.get('text', '')
        if not text:
            return {'error': 'No text provided'}, 400
        
        huffman = HuffmanCoding()
        encoded, freq_table = huffman.encode(text)
        stats = huffman.get_compression_stats(text, encoded)
        
        # Convert data for JSON serialization
        freq_list = [{'char': char, 'freq': freq} for char, freq in freq_table.items()]
        codes_list = [{'char': char, 'code': code} for char, code in huffman.codes.items()]
        
        return {
            'encoded': encoded,
            'frequency_table': freq_list,
            'huffman_codes': codes_list,
            'stats': {
                'original_size': stats.original_size,
                'compressed_size': stats.compressed_size,
                'compression_ratio': stats.compression_ratio,
                'space_saved': stats.space_saved
            }
        }, 200
    
    except EncodingError as e:
        return {'error': f'Encoding error: {str(e)}'}, 400
    except Exception as e:
        return {'error': f'Internal server error: {str(e)}'}, 500


@api_bp.route('/decode', methods=['POST'])
def decode_text() -> tuple[Dict[str, Any], int]:
    """
    Decode Huffman encoded text.
    
    Returns:
        JSON response with decoded text or error
    """
    try:
        data = request.get_json()
        if not data:
            return {'error': 'No JSON data provided'}, 400
        
        encoded = data.get('encoded', '')
        freq_table_list = data.get('frequency_table', [])
        
        if not encoded:
            return {'error': 'No encoded text provided'}, 400
        
        if not freq_table_list:
            return {'error': 'No frequency table provided'}, 400
        
        # Convert frequency table back to dict
        try:
            freq_dict = {item['char']: item['freq'] for item in freq_table_list}
        except (KeyError, TypeError):
            return {'error': 'Invalid frequency table format'}, 400
        
        huffman = HuffmanCoding()
        decoded = huffman.decode(encoded, freq_dict)
        
        return {'decoded': decoded}, 200
    
    except DecodingError as e:
        return {'error': f'Decoding error: {str(e)}'}, 400
    except Exception as e:
        return {'error': f'Internal server error: {str(e)}'}, 500


@api_bp.errorhandler(404)
def not_found(error) -> tuple[Dict[str, str], int]:
    """Handle 404 errors"""
    return {'error': 'Endpoint not found'}, 404


@api_bp.errorhandler(405)
def method_not_allowed(error) -> tuple[Dict[str, str], int]:
    """Handle 405 errors"""
    return {'error': 'Method not allowed'}, 405
