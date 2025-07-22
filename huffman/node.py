"""
Node class for Huffman Tree with modern Python features
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    """
    Represents a node in the Huffman tree.
    
    Attributes:
        char: Character stored in leaf nodes, None for internal nodes
        freq: Frequency of the character or sum of child frequencies
        left: Left child node
        right: Right child node
    """
    char: Optional[str] = None
    freq: int = 0
    left: Optional[Node] = None
    right: Optional[Node] = None
    
    def __lt__(self, other: Node) -> bool:
        """Less than operator for priority queue comparison"""
        return self.freq < other.freq
    
    def __post_init__(self) -> None:
        """Validate node after initialization"""
        if self.freq < 0:
            raise ValueError("Frequency cannot be negative")
    
    @property
    def is_leaf(self) -> bool:
        """Check if this is a leaf node"""
        return self.char is not None
    
    @property
    def is_internal(self) -> bool:
        """Check if this is an internal node"""
        return self.char is None and (self.left is not None or self.right is not None)
    
    def __repr__(self) -> str:
        """String representation for debugging"""
        if self.is_leaf:
            return f"Node('{self.char}', {self.freq})"
        return f"Node(internal, {self.freq})"
