"""
Modern Huffman Coding Implementation with type hints and error handling
"""

import heapq
from collections import Counter
from typing import Dict, Tuple, Optional, Any
from dataclasses import dataclass

from .node import Node


@dataclass
class CompressionStats:
    """Statistics about compression performance"""
    original_size: int
    compressed_size: int
    compression_ratio: float
    space_saved: float
    
    def __post_init__(self) -> None:
        """Calculate derived values"""
        if self.original_size > 0:
            self.compression_ratio = self.compressed_size / self.original_size
            self.space_saved = (1 - self.compression_ratio) * 100
        else:
            self.compression_ratio = 0
            self.space_saved = 0


class HuffmanCodingError(Exception):
    """Base exception for Huffman coding errors"""
    pass


class EncodingError(HuffmanCodingError):
    """Raised when encoding fails"""
    pass


class DecodingError(HuffmanCodingError):
    """Raised when decoding fails"""
    pass


class HuffmanCoding:
    """
    Modern implementation of Huffman coding algorithm.
    
    Features:
    - Type hints for better code clarity
    - Comprehensive error handling
    - Performance optimizations
    - Clean API design
    """
    
    def __init__(self) -> None:
        self._codes: Dict[str, str] = {}
        self._root: Optional[Node] = None
    
    @property
    def codes(self) -> Dict[str, str]:
        """Get the generated Huffman codes"""
        return self._codes.copy()
    
    @property
    def root(self) -> Optional[Node]:
        """Get the root of the Huffman tree"""
        return self._root
    
    def build_frequency_table(self, text: str) -> Dict[str, int]:
        """
        Count character frequencies in the text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary mapping characters to their frequencies
            
        Raises:
            ValueError: If text is empty
        """
        if not text:
            raise ValueError("Text cannot be empty")
        
        return dict(Counter(text))
    
    def _build_huffman_tree(self, freq_table: Dict[str, int]) -> Optional[Node]:
        """
        Build Huffman tree using priority queue.
        
        Args:
            freq_table: Character frequency mapping
            
        Returns:
            Root node of the Huffman tree
        """
        if not freq_table:
            return None
        
        # Create heap with leaf nodes
        heap = [Node(char=char, freq=freq) for char, freq in freq_table.items()]
        heapq.heapify(heap)
        
        # Build tree bottom-up
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            merged = Node(
                freq=left.freq + right.freq,
                left=left,
                right=right
            )
            heapq.heappush(heap, merged)
        
        return heap[0] if heap else None
    
    def _generate_codes(self, node: Optional[Node], code: str = "") -> None:
        """
        Generate binary codes for each character recursively.
        
        Args:
            node: Current node in the tree
            code: Current binary code path
        """
        if not node:
            return
        
        if node.is_leaf:
            # Leaf node - assign code (handle single character case)
            self._codes[node.char] = code if code else "0"
        else:
            # Internal node - recurse
            self._generate_codes(node.left, code + "0")
            self._generate_codes(node.right, code + "1")
    
    def _serialize_tree(self, node: Optional[Node], x: float = 0, y: float = 0, 
                       level: int = 0, side: str = "", width_factor: float = 200) -> Dict[str, Any]:
        """
        Serialize tree structure for visualization.
        
        Args:
            node: Current node to serialize
            x: X coordinate for positioning
            y: Y coordinate for positioning
            level: Current tree level (depth)
            side: Which side of parent ('left' or 'right')
            width_factor: Spacing factor for horizontal positioning
            
        Returns:
            Dictionary representation of the tree structure
        """
        if not node:
            return {}
        
        # Calculate horizontal spacing for more compact, cubic layout
        spacing = width_factor / (2.2 ** (level + 1))
        spacing = max(spacing, 30)  # Reduced minimum spacing for more compact layout
        
        result = {
            'id': f"node_{id(node)}",
            'x': x,
            'y': y,
            'level': level,
            'side': side,
            'frequency': node.freq,
            'is_leaf': node.is_leaf,
            'char': node.char if node.is_leaf else None,
            'code': self._codes.get(node.char, '') if node.is_leaf else '',
            'children': []
        }
        
        # Add children if internal node
        if not node.is_leaf:
            left_x = x - spacing
            right_x = x + spacing
            child_y = y + 75  # Slightly reduced for more cubic proportions
            
            if node.left:
                left_child = self._serialize_tree(node.left, left_x, child_y, 
                                                level + 1, 'left', width_factor)
                if left_child:
                    result['children'].append(left_child)
            
            if node.right:
                right_child = self._serialize_tree(node.right, right_x, child_y, 
                                                 level + 1, 'right', width_factor)
                if right_child:
                    result['children'].append(right_child)
        
        return result

    def get_tree_structure(self) -> Dict[str, Any]:
        """
        Get the tree structure for visualization.
        
        Returns:
            Dictionary containing the complete tree structure
        """
        if not hasattr(self, '_root') or not self._root:
            return {}
        
        # Calculate tree width for more cubic layout - less wide, more proportional
        leaf_count = self._count_leaf_nodes(self._root)
        tree_width = min(1000, max(600, leaf_count * 60))
        
        return self._serialize_tree(self._root, tree_width / 2, 50, 0, "", tree_width * 0.6)
    
    def _count_leaf_nodes(self, node: Optional[Node]) -> int:
        """Count the number of leaf nodes in the tree."""
        if not node:
            return 0
        if node.is_leaf:
            return 1
        
        left_count = self._count_leaf_nodes(node.left) if node.left else 0
        right_count = self._count_leaf_nodes(node.right) if node.right else 0
        return left_count + right_count
    
    def encode(self, text: str) -> Tuple[str, Dict[str, int]]:
        """
        Encode text using Huffman coding.
        
        Args:
            text: Text to encode
            
        Returns:
            Tuple of (encoded_binary_string, frequency_table)
            
        Raises:
            EncodingError: If encoding fails
        """
        try:
            if not text:
                raise ValueError("Text cannot be empty")
            
            # Build frequency table
            freq_table = self.build_frequency_table(text)
            
            # Handle single character case
            if len(freq_table) == 1:
                char = next(iter(freq_table))
                freq = freq_table[char]
                # Create a single leaf node as root for visualization
                from .node import Node
                self._root = Node(char=char, freq=freq)
                self._codes = {char: "0"}
                return "0" * len(text), freq_table
            
            # Build tree and generate codes
            self._root = self._build_huffman_tree(freq_table)
            if not self._root:
                raise EncodingError("Failed to build Huffman tree")
            
            self._codes = {}
            self._generate_codes(self._root)
            
            # Encode the text
            try:
                encoded = "".join(self._codes[char] for char in text)
            except KeyError as e:
                raise EncodingError(f"Character not found in codes: {e}")
            
            return encoded, freq_table
            
        except Exception as e:
            if isinstance(e, (ValueError, EncodingError)):
                raise
            raise EncodingError(f"Encoding failed: {str(e)}") from e
    
    def decode(self, encoded_text: str, freq_table: Dict[str, int]) -> str:
        """
        Decode binary text using frequency table.
        
        Args:
            encoded_text: Binary string to decode
            freq_table: Character frequency mapping
            
        Returns:
            Decoded text
            
        Raises:
            DecodingError: If decoding fails
        """
        try:
            if not encoded_text:
                return ""
            
            if not freq_table:
                raise ValueError("Frequency table cannot be empty")
            
            # Validate binary string
            if not all(bit in '01' for bit in encoded_text):
                raise DecodingError("Encoded text must contain only 0s and 1s")
            
            # Handle single character case
            if len(freq_table) == 1:
                char = next(iter(freq_table))
                return char * len(encoded_text)
            
            # Rebuild tree
            root = self._build_huffman_tree(freq_table)
            if not root:
                raise DecodingError("Failed to rebuild Huffman tree")
            
            # Decode bit by bit
            decoded = []
            current = root
            
            for bit in encoded_text:
                if bit == "0":
                    current = current.left
                else:
                    current = current.right
                
                if not current:
                    raise DecodingError("Invalid binary sequence")
                
                # If we reach a leaf node
                if current.is_leaf:
                    decoded.append(current.char)
                    current = root
            
            # Check if we ended at root (complete decode)
            if current != root:
                raise DecodingError("Incomplete binary sequence")
            
            return "".join(decoded)
            
        except Exception as e:
            if isinstance(e, (ValueError, DecodingError)):
                raise
            raise DecodingError(f"Decoding failed: {str(e)}") from e
    
    def get_compression_stats(self, original_text: str, encoded_text: str) -> CompressionStats:
        """
        Calculate compression statistics.
        
        Args:
            original_text: Original input text
            encoded_text: Encoded binary string
            
        Returns:
            CompressionStats object with detailed metrics
        """
        original_bits = len(original_text) * 8  # ASCII = 8 bits per char
        compressed_bits = len(encoded_text)
        
        return CompressionStats(
            original_size=original_bits,
            compressed_size=compressed_bits,
            compression_ratio=0,  # Will be calculated in __post_init__
            space_saved=0  # Will be calculated in __post_init__
        )
