# Example: File Compression

import os
from huffman.coding import HuffmanCoding

def compress_file(input_file: str, output_file: str) -> None:
    """Compress a text file using Huffman coding"""
    
    # Read input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    if not text:
        print("Error: File is empty")
        return
    
    print(f"Read {len(text)} characters from '{input_file}'")
    
    # Compress using Huffman coding
    huffman = HuffmanCoding()
    try:
        encoded, freq_table = huffman.encode(text)
        stats = huffman.get_compression_stats(text, encoded)
        
        print(f"\nCompression Results:")
        print(f"- Original size: {stats.original_size} bits ({stats.original_size // 8} bytes)")
        print(f"- Compressed size: {stats.compressed_size} bits ({stats.compressed_size // 8} bytes)")
        print(f"- Space saved: {stats.space_saved:.1f}%")
        
        # Save compressed data (simplified - in real implementation you'd save binary)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Huffman Compressed File\n")
            f.write(f"# Original size: {len(text)} chars\n")
            f.write(f"# Compressed size: {len(encoded)} bits\n")
            f.write(f"# Frequency table: {freq_table}\n")
            f.write(f"# Encoded data:\n")
            f.write(encoded)
        
        print(f"Compressed data saved to '{output_file}'")
        
    except Exception as e:
        print(f"Compression failed: {e}")

def decompress_file(input_file: str, output_file: str) -> None:
    """Decompress a Huffman compressed file"""
    # This is a simplified example - real implementation would parse binary format
    print("Note: This is a simplified decompression example")
    print("In a real implementation, you'd save/load in binary format")

if __name__ == "__main__":
    # Example usage
    input_file = "sample.txt"
    compressed_file = "sample_compressed.huff"
    
    if os.path.exists(input_file):
        compress_file(input_file, compressed_file)
    else:
        print(f"Sample file '{input_file}' not found")
        print("Creating a sample file for demonstration...")
        
        sample_text = """
        This is a sample text file for demonstrating Huffman coding compression.
        The algorithm works by assigning shorter binary codes to more frequent characters.
        Characters that appear more often get shorter codes, while rare characters get longer codes.
        This results in overall compression of the text data.
        
        Notice how spaces and common letters like 'e', 't', 'a' will get short codes,
        while less common characters will get longer codes.
        
        The compression ratio depends on the character frequency distribution in your text.
        """
        
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(sample_text)
        
        print(f"Created sample file '{input_file}'")
        compress_file(input_file, compressed_file)
