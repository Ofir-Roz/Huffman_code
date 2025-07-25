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
        assert freq_table[' '] == 5  # space appears 5 times
    
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


class TestHuffmanTreeVisualization:
    """Test the Huffman tree visualization functionality"""
    
    def test_tree_structure_basic(self):
        """Test basic tree structure generation"""
        huffman = HuffmanCoding()
        encoded, freq_table = huffman.encode("ABC")
        tree_structure = huffman.get_tree_structure()
        
        # Should have tree structure
        assert tree_structure is not None
        assert isinstance(tree_structure, dict)
        assert 'id' in tree_structure
        assert 'x' in tree_structure
        assert 'y' in tree_structure
        assert 'frequency' in tree_structure
        assert 'is_leaf' in tree_structure
        assert 'children' in tree_structure
    
    def test_tree_structure_single_character(self):
        """Test tree structure for single character"""
        huffman = HuffmanCoding()
        encoded, freq_table = huffman.encode("AAAA")
        tree_structure = huffman.get_tree_structure()
        
        # Single character should create a leaf node
        assert tree_structure is not None
        assert tree_structure != {}
        assert tree_structure['is_leaf'] is True
        assert tree_structure['char'] == 'A'
        assert tree_structure['frequency'] == 4
        assert len(tree_structure['children']) == 0
    
    def test_tree_structure_coordinates(self):
        """Test that tree coordinates are reasonable"""
        huffman = HuffmanCoding()
        encoded, freq_table = huffman.encode("ABC")
        tree_structure = huffman.get_tree_structure()
        
        # Root should be centered
        assert tree_structure['x'] > 0
        assert tree_structure['y'] > 0
        assert tree_structure['level'] == 0
        
        # Check children have different coordinates
        if tree_structure['children']:
            child1 = tree_structure['children'][0]
            child2 = tree_structure['children'][1]
            
            assert child1['x'] != child2['x']  # Different x positions
            assert child1['y'] == child2['y']  # Same level
            assert child1['level'] == child2['level'] == 1
    
    def test_tree_structure_leaf_nodes(self):
        """Test that leaf nodes contain character information"""
        huffman = HuffmanCoding()
        encoded, freq_table = huffman.encode("HELLO")
        tree_structure = huffman.get_tree_structure()
        
        # Find all leaf nodes
        leaf_nodes = self._find_leaf_nodes(tree_structure)
        
        # Should have leaf nodes for each unique character
        unique_chars = set("HELLO")
        assert len(leaf_nodes) == len(unique_chars)
        
        # Each leaf should have character and code
        for leaf in leaf_nodes:
            assert leaf['is_leaf'] is True
            assert leaf['char'] is not None
            assert leaf['code'] != ''
            assert leaf['frequency'] > 0
    
    def test_tree_structure_internal_nodes(self):
        """Test that internal nodes have correct properties"""
        huffman = HuffmanCoding()
        encoded, freq_table = huffman.encode("HELLO")
        tree_structure = huffman.get_tree_structure()
        
        # Find all internal nodes
        internal_nodes = self._find_internal_nodes(tree_structure)
        
        for node in internal_nodes:
            assert node['is_leaf'] is False
            assert node['char'] is None
            assert node['code'] == ''
            assert len(node['children']) > 0
            assert node['frequency'] > 0
    
    def test_tree_structure_frequency_consistency(self):
        """Test that frequencies in tree match original text"""
        text = "HELLO WORLD"
        huffman = HuffmanCoding()
        encoded, freq_table = huffman.encode(text)
        tree_structure = huffman.get_tree_structure()
        
        # Check that root frequency equals text length
        assert tree_structure['frequency'] == len(text)
        
        # Check that leaf frequencies match character counts
        leaf_nodes = self._find_leaf_nodes(tree_structure)
        for leaf in leaf_nodes:
            char = leaf['char']
            expected_freq = text.count(char)
            assert leaf['frequency'] == expected_freq
    
    def test_tree_structure_code_consistency(self):
        """Test that tree codes match generated Huffman codes"""
        huffman = HuffmanCoding()
        encoded, freq_table = huffman.encode("HELLO")
        tree_structure = huffman.get_tree_structure()
        
        # Get codes from tree
        leaf_nodes = self._find_leaf_nodes(tree_structure)
        tree_codes = {leaf['char']: leaf['code'] for leaf in leaf_nodes}
        
        # Get codes from huffman object
        huffman_codes = huffman.codes
        
        # Should match
        assert tree_codes == huffman_codes
    
    def test_tree_structure_path_validation(self):
        """Test that tree paths correctly represent binary codes"""
        huffman = HuffmanCoding()
        encoded, freq_table = huffman.encode("ABC")
        tree_structure = huffman.get_tree_structure()
        
        # Verify that following tree paths gives correct codes
        leaf_nodes = self._find_leaf_nodes(tree_structure)
        
        for leaf in leaf_nodes:
            # Find path from root to this leaf
            path = self._find_path_to_node(tree_structure, leaf['id'])
            expected_code = leaf['code']
            
            # Path should match the code
            if expected_code and len(path) > 0:  # Not empty code
                path_code = ''.join(path)
                assert path_code == expected_code, f"Path {path_code} != Code {expected_code} for char {leaf['char']}"
    
    def test_tree_count_leaf_nodes(self):
        """Test the leaf node counting method"""
        huffman = HuffmanCoding()
        encoded, freq_table = huffman.encode("HELLO")
        
        # Test private method through tree structure
        tree_structure = huffman.get_tree_structure()
        leaf_nodes = self._find_leaf_nodes(tree_structure)
        
        # Should match unique character count
        unique_chars = set("HELLO")
        assert len(leaf_nodes) == len(unique_chars)
    
    def test_empty_tree_structure(self):
        """Test tree structure when no encoding has been done"""
        huffman = HuffmanCoding()
        tree_structure = huffman.get_tree_structure()
        
        # Should return empty dict
        assert tree_structure == {}
    
    # Helper methods for tree traversal and analysis
    def _find_leaf_nodes(self, node):
        """Recursively find all leaf nodes in the tree"""
        if not node:
            return []
        
        if node.get('is_leaf', False):
            return [node]
        
        leaves = []
        for child in node.get('children', []):
            leaves.extend(self._find_leaf_nodes(child))
        
        return leaves
    
    def _find_internal_nodes(self, node):
        """Recursively find all internal nodes in the tree"""
        if not node:
            return []
        
        internals = []
        if not node.get('is_leaf', False):
            internals.append(node)
        
        for child in node.get('children', []):
            internals.extend(self._find_internal_nodes(child))
        
        return internals
    
    def _find_path_to_node(self, root, target_id, path=None):
        """Find path from root to target node by ID"""
        if path is None:
            path = []
        
        if root['id'] == target_id:
            return path
        
        for child in root.get('children', []):
            side = '0' if child.get('side') == 'left' else '1'
            result = self._find_path_to_node(child, target_id, path + [side])
            if result is not None:
                return result
        
        return None
