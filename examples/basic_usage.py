# Example: Basic Usage

from huffman.coding import HuffmanCoding

def basic_example():
    """Basic encoding and decoding example"""
    # Create Huffman coding instance
    huffman = HuffmanCoding()
    
    # Text to compress
    text = "Hello, World! This is a simple example."
    print(f"Original text: {text}")
    print(f"Original length: {len(text)} characters")
    
    # Encode the text
    encoded, freq_table = huffman.encode(text)
    print(f"\nEncoded (binary): {encoded}")
    print(f"Encoded length: {len(encoded)} bits")
    
    # Get compression statistics
    stats = huffman.get_compression_stats(text, encoded)
    print(f"\nCompression Statistics:")
    print(f"- Original size: {stats.original_size} bits")
    print(f"- Compressed size: {stats.compressed_size} bits")
    print(f"- Compression ratio: {stats.compression_ratio:.2f}")
    print(f"- Space saved: {stats.space_saved:.1f}%")
    
    # Show Huffman codes
    print(f"\nHuffman Codes:")
    for char, code in sorted(huffman.codes.items()):
        display_char = repr(char) if char in [' ', '\n', '\t'] else char
        print(f"  {display_char}: {code}")
    
    # Decode back to original
    decoded = huffman.decode(encoded, freq_table)
    print(f"\nDecoded text: {decoded}")
    print(f"Matches original: {decoded == text}")

if __name__ == "__main__":
    basic_example()
