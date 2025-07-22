# Huffman Coding Project

A Python implementation of Huffman coding algorithm for text compression.

## Project Structure

- `huffman_coding.py` - Main Huffman coding class
- `node.py` - Tree node class for building Huffman tree
- `main.py` - Command-line interface
- `test_huffman.py` - Unit tests
- `file_utils.py` - File I/O utilities

## How to Run

```bash
python main.py encode input.txt output.huff
python main.py decode output.huff decoded.txt
```

## Features

- Text compression using Huffman algorithm
- Binary file output for maximum compression
- Command-line interface for easy use
- Complete test suite

## Algorithm Overview

1. Count character frequencies in input text
2. Build Huffman tree using priority queue
3. Generate binary codes for each character
4. Encode text using generated codes
5. Save compressed data to file
