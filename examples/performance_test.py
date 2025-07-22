# Example: Performance Comparison

import time
import random
import string
from huffman.coding import HuffmanCoding

def generate_text(length: int, char_distribution: str = "uniform") -> str:
    """Generate test text with different character distributions"""
    
    if char_distribution == "uniform":
        # Uniform distribution - all characters equally likely
        return ''.join(random.choices(string.ascii_lowercase + ' ', k=length))
    
    elif char_distribution == "english":
        # Simulate English text frequency
        chars = 'etaoinshrdlcumwfgypbvkjxqz '
        weights = [12.7, 9.1, 8.2, 7.5, 7.0, 6.3, 6.1, 6.0, 5.9, 4.3, 4.0, 2.8, 2.8, 2.4, 2.4, 2.0, 2.0, 1.9, 1.5, 1.3, 1.0, 0.15, 0.15, 0.10, 18.0]
        return ''.join(random.choices(chars, weights=weights, k=length))
    
    elif char_distribution == "repetitive":
        # Very repetitive text
        base = "AAAAAABBBBCCCDDE"
        return (base * (length // len(base) + 1))[:length]
    
    else:
        raise ValueError("Unknown distribution type")

def benchmark_compression(text: str, description: str) -> dict:
    """Benchmark compression performance"""
    
    huffman = HuffmanCoding()
    
    # Measure encoding time
    start_time = time.time()
    encoded, freq_table = huffman.encode(text)
    encoding_time = time.time() - start_time
    
    # Measure decoding time
    start_time = time.time()
    decoded = huffman.decode(encoded, freq_table)
    decoding_time = time.time() - start_time
    
    # Calculate statistics
    stats = huffman.get_compression_stats(text, encoded)
    
    # Verify correctness
    is_correct = decoded == text
    
    result = {
        'description': description,
        'text_length': len(text),
        'unique_chars': len(freq_table),
        'original_bits': stats.original_size,
        'compressed_bits': stats.compressed_size,
        'compression_ratio': stats.compression_ratio,
        'space_saved': stats.space_saved,
        'encoding_time': encoding_time,
        'decoding_time': decoding_time,
        'total_time': encoding_time + decoding_time,
        'is_correct': is_correct
    }
    
    return result

def run_performance_tests():
    """Run comprehensive performance tests"""
    
    print("🚀 Huffman Coding Performance Benchmark")
    print("=" * 50)
    
    test_cases = [
        (1000, "uniform", "Uniform Distribution (1K chars)"),
        (1000, "english", "English-like Distribution (1K chars)"),
        (1000, "repetitive", "Repetitive Text (1K chars)"),
        (10000, "english", "English-like Distribution (10K chars)"),
        (50000, "english", "English-like Distribution (50K chars)"),
    ]
    
    results = []
    
    for length, distribution, description in test_cases:
        print(f"\n📊 Testing: {description}")
        
        # Generate test text
        text = generate_text(length, distribution)
        
        # Run benchmark
        result = benchmark_compression(text, description)
        results.append(result)
        
        # Display results
        print(f"   Original size: {result['original_bits']:,} bits ({result['original_bits']//8:,} bytes)")
        print(f"   Compressed size: {result['compressed_bits']:,} bits ({result['compressed_bits']//8:,} bytes)")
        print(f"   Compression ratio: {result['compression_ratio']:.3f}")
        print(f"   Space saved: {result['space_saved']:.1f}%")
        print(f"   Unique characters: {result['unique_chars']}")
        print(f"   Encoding time: {result['encoding_time']:.4f} seconds")
        print(f"   Decoding time: {result['decoding_time']:.4f} seconds")
        print(f"   Correctness: {'✅ PASS' if result['is_correct'] else '❌ FAIL'}")
    
    # Summary
    print(f"\n📈 Summary")
    print("=" * 50)
    
    best_compression = min(results, key=lambda x: x['compression_ratio'])
    fastest_encoding = min(results, key=lambda x: x['encoding_time'])
    
    print(f"🏆 Best compression: {best_compression['description']}")
    print(f"   Saved {best_compression['space_saved']:.1f}% space")
    
    print(f"⚡ Fastest encoding: {fastest_encoding['description']}")
    print(f"   Completed in {fastest_encoding['encoding_time']:.4f} seconds")
    
    print(f"\n💡 Insights:")
    print(f"   • Repetitive text compresses best (predictable)")
    print(f"   • Uniform distribution compresses worst (random)")
    print(f"   • English-like text has moderate compression")
    print(f"   • Larger texts generally have better compression ratios")

if __name__ == "__main__":
    run_performance_tests()
