# 🗜️ Huffman Coding Compressor

A modern Python implementation of the Huffman coding algorithm for text compression with a beautiful web interface.

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Flask Version](https://img.shields.io/badge/flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Type Checking](https://img.shields.io/badge/type%20checking-mypy-blue.svg)](http://mypy-lang.org/)

## ✨ Features

- 🎯 **Modern Python**: Type hints, dataclasses, and error handling
- 🌐 **Web Interface**: Beautiful responsive UI with real-time compression
- 📊 **Detailed Analytics**: Compression ratios and character frequency analysis
- 🧪 **Comprehensive Tests**: High test coverage with pytest
- 🔧 **Development Tools**: Black, flake8, mypy for code quality
- 📱 **Mobile Friendly**: Responsive design that works on all devices
- 🚀 **Production Ready**: Proper logging and configuration management

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Ofir-Roz/Huffman_code.git
cd Huffman_code

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

Open your browser and go to `http://127.0.0.1:5000`

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Set up pre-commit hooks (optional)
pip install pre-commit
pre-commit install

# Run tests
pytest

# Run with coverage
pytest --cov=huffman --cov=app

# Format code
black .

# Type checking
mypy .

# Lint code
flake8
```

## 🏗️ Project Structure

```
Huffman_code/
├── app/                    # Flask application package
│   ├── __init__.py        # App factory
│   ├── routes.py          # API endpoints
│   └── templates/         # HTML templates
│       └── index.html
├── huffman/               # Core algorithm package
│   ├── __init__.py
│   ├── coding.py          # Main Huffman implementation
│   └── node.py            # Tree node class
├── tests/                 # Test suite
│   ├── conftest.py        # Test configuration
│   ├── test_huffman.py    # Core algorithm tests
│   └── test_api.py        # API endpoint tests
├── config.py              # Application configuration
├── run.py                 # Application entry point
├── requirements.txt       # Dependencies
├── pyproject.toml         # Tool configuration
├── setup.cfg              # Flake8 configuration
└── .env.example           # Environment variables template
```

## 🎯 Usage

### Web Interface

1. **Open** your browser to `http://127.0.0.1:5000`
2. **Enter text** in the input area
3. **Click "Encode"** to compress the text
4. **View results** including:
   - Binary encoded output
   - Compression statistics
   - Character frequency analysis
   - Huffman codes for each character
5. **Click "Decode"** to decompress back to original text

### API Endpoints

#### Encode Text
```bash
curl -X POST http://127.0.0.1:5000/encode \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World!"}'
```

#### Decode Text
```bash
curl -X POST http://127.0.0.1:5000/decode \
  -H "Content-Type: application/json" \
  -d '{
    "encoded": "110100101...",
    "frequency_table": [{"char": "H", "freq": 1}, ...]
  }'
```

### Python Package

```python
from huffman.coding import HuffmanCoding

# Create instance
huffman = HuffmanCoding()

# Encode text
encoded, freq_table = huffman.encode("Hello World!")
print(f"Encoded: {encoded}")

# Get compression stats
stats = huffman.get_compression_stats("Hello World!", encoded)
print(f"Space saved: {stats.space_saved:.1f}%")

# Decode text
decoded = huffman.decode(encoded, freq_table)
print(f"Decoded: {decoded}")
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=huffman --cov=app --cov-report=html

# Run specific test file
pytest tests/test_huffman.py

# Run with verbose output
pytest -v
```

## 🔧 Development

### Code Quality Tools

```bash
# Format code with Black
black .

# Type checking with mypy
mypy .

# Lint with flake8
flake8

# Run all quality checks
black . && mypy . && flake8 && pytest
```

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
HOST=127.0.0.1
PORT=5000
```

## 📚 Algorithm Overview

The Huffman coding algorithm works in these steps:

1. **Frequency Analysis**: Count character occurrences in input text
2. **Tree Construction**: Build binary tree using priority queue (greedy algorithm)
3. **Code Generation**: Assign shorter codes to more frequent characters
4. **Encoding**: Replace characters with their binary codes
5. **Decoding**: Use tree to convert binary codes back to characters

### Time Complexity
- Building tree: O(n log n) where n is number of unique characters
- Encoding: O(m) where m is text length
- Decoding: O(m) where m is encoded length

### Space Complexity
- Tree storage: O(n) for n unique characters
- Code table: O(n) for n unique characters

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and quality checks
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Huffman coding algorithm by David A. Huffman (1952)
- Flask web framework
- Modern Python development practices
- Beautiful UI inspired by modern web design
