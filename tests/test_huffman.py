"""Tests for the Huffman coding core functionality"""

import pytest
from huffman.coding import HuffmanCoding, EncodingError, DecodingError
from huffman.node import Node


class TestNode:
    """Test the Node class"""
    
    def test_node_creation(self):
        """Test basic node creation"""
        node = Node(char='A', freq=5)
        assert node.char == 'A'
        assert node.freq == 5
        assert node.left is None
        assert node.right is None
    
    def test_node_comparison(self):
        """Test node comparison for priority queue"""
        node1 = Node(char='A', freq=5)
        node2 = Node(char='B', freq=10)
        assert node1 < node2
        assert not node2 < node1
    
    def test_node_properties(self):
        """Test node properties"""
        leaf = Node(char='A', freq=5)
        internal = Node(freq=10, left=leaf, right=None)
        
        assert leaf.is_leaf
        assert not leaf.is_internal
        
        assert not internal.is_leaf
        assert internal.is_internal
    
    def test_node_validation(self):
        """Test node validation"""
        with pytest.raises(ValueError):
            Node(char='A', freq=-1)


class TestHuffmanCoding:
    """Test the HuffmanCoding class"""
    
    def test_frequency_table(self, sample_text):
        """Test frequency table generation"""
        huffman = HuffmanCoding()
        freq_table = huffman.build_frequency_table(sample_text)
        
        assert freq_table['l'] == 3  # 'l' appears 3 times in "Hello World..."
        assert freq_table['o'] == 2  # 'o' appears 2 times
        assert freq_table[' '] == 4  # space appears 4 times
    
    def test_empty_text_encoding(self):
        """Test encoding empty text raises error"""
        huffman = HuffmanCoding()
        with pytest.raises(ValueError):
            huffman.encode("")
    
    def test_single_character_encoding(self):
        """Test encoding single character"""
        huffman = HuffmanCoding()
        encoded, freq_table = huffman.encode("AAAA")
        
        assert encoded == "0000"
        assert freq_table == {'A': 4}
        assert huffman.codes == {'A': '0'}
    
    def test_encoding_decoding_roundtrip(self, sample_text):
        """Test that encoding then decoding returns original text"""
        huffman = HuffmanCoding()
        encoded, freq_table = huffman.encode(sample_text)
        decoded = huffman.decode(encoded, freq_table)
        
        assert decoded == sample_text
    
    def test_invalid_binary_decoding(self, sample_frequency_table):
        """Test decoding invalid binary string"""
        huffman = HuffmanCoding()
        with pytest.raises(DecodingError):
            huffman.decode("abc123", sample_frequency_table)
    
    def test_empty_frequency_table_decoding(self):
        """Test decoding with empty frequency table"""
        huffman = HuffmanCoding()
        with pytest.raises(ValueError):
            huffman.decode("0101", {})
    
    def test_compression_stats(self, sample_text):
        """Test compression statistics calculation"""
        huffman = HuffmanCoding()
        encoded, _ = huffman.encode(sample_text)
        stats = huffman.get_compression_stats(sample_text, encoded)
        
        assert stats.original_size == len(sample_text) * 8
        assert stats.compressed_size == len(encoded)
        assert 0 <= stats.compression_ratio <= 1
        assert 0 <= stats.space_saved <= 100
    
    def test_codes_property(self, sample_text):
        """Test that codes property returns a copy"""
        huffman = HuffmanCoding()
        huffman.encode(sample_text)
        
        codes1 = huffman.codes
        codes2 = huffman.codes
        
        # Should be equal but not the same object
        assert codes1 == codes2
        assert codes1 is not codes2
    
    def test_incomplete_binary_sequence(self, sample_text):
        """Test decoding incomplete binary sequence"""
        huffman = HuffmanCoding()
        encoded, freq_table = huffman.encode(sample_text)
        
        # Remove last bit to make it incomplete
        incomplete = encoded[:-1]
        
        with pytest.raises(DecodingError):
            huffman.decode(incomplete, freq_table)
