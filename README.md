# 🗜️ Huffman Coding Compressor

A modern, full-stack web application implementing the Huffman coding algorithm for text compression with real-time analytics and an intuitive user interface.

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Flask Version](https://img.shields.io/badge/flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🌐 Live Demo

**🚀 [Try it live on Render](https://huffman-coding-app.onrender.com)**

## ✨ Features

### 🎯 Core Functionality
- **Real-time Huffman Encoding/Decoding** - Instant text compression and decompression
- **Interactive Web Interface** - Modern, responsive design that works on all devices
- **Copy-to-Input Feature** - Seamless workflow for testing encode/decode cycles
- **Comprehensive Statistics** - Detailed compression metrics and performance analysis

### 📊 Analytics Dashboard
- **Compression Ratio** - Visual representation of space savings
- **Character Frequency Analysis** - Interactive frequency tables
- **Huffman Code Mapping** - Complete binary code assignments for each character
- **File Size Comparison** - Before/after compression statistics

### 🛠️ Technical Excellence
- **Modern Python Architecture** - Type hints, dataclasses, and comprehensive error handling
- **RESTful API Design** - Clean JSON endpoints for encoding/decoding operations
- **Professional Testing Suite** - Comprehensive test coverage with pytest
- **Code Quality Tools** - Black formatting, flake8 linting, mypy type checking
- **Production Ready** - Configured for cloud deployment with proper logging

## 🔬 The Huffman Algorithm

### What is Huffman Coding?
Huffman coding is a lossless data compression algorithm developed by David A. Huffman in 1952. It assigns variable-length codes to characters based on their frequency of occurrence - more frequent characters get shorter codes, resulting in overall compression.

### How It Works
1. **Frequency Analysis** - Count character occurrences in the input text
2. **Priority Queue** - Create nodes for each character, ordered by frequency
3. **Tree Construction** - Build binary tree by merging least frequent nodes
4. **Code Generation** - Assign binary codes based on tree paths (left=0, right=1)
5. **Encoding** - Replace characters with their corresponding binary codes
6. **Decoding** - Use the tree to convert binary codes back to original text

### Algorithm Complexity
- **Time Complexity**: O(n log n) where n = number of unique characters
- **Space Complexity**: O(n) for tree storage and code table
- **Compression Efficiency**: Optimal for the given character frequencies

## 🏗️ Technology Stack

### Backend Technologies
- **🐍 Python 3.10+** - Core programming language with modern features
- **🌶️ Flask 2.3+** - Lightweight web framework for API development
- **📊 Collections.Counter** - Efficient character frequency analysis
- **🌳 heapq** - Priority queue implementation for tree construction
- **� dataclasses** - Modern Python data structures with type safety

### Frontend Technologies
- **📄 HTML5** - Semantic markup with accessibility features
- **🎨 CSS3** - Modern styling with flexbox/grid layouts and responsive design
- **⚡ JavaScript (ES6+)** - Async/await API calls and dynamic DOM manipulation
- **🔄 Fetch API** - RESTful communication between frontend and backend

### Development & Deployment
- **🧪 pytest** - Comprehensive testing framework with fixtures and coverage
- **🎨 Black** - Uncompromising code formatting for consistency
- **� flake8** - Code linting for style and error detection
- **📝 mypy** - Static type checking for enhanced code reliability
- **☁️ Render** - Cloud platform deployment with automatic CI/CD
- **📦 Git** - Version control with professional branching strategy

### Project Architecture
- **🏗️ Flask Blueprints** - Modular application structure
- **🗂️ Application Factory Pattern** - Scalable app configuration
- **📂 Separation of Concerns** - Clean separation of HTML, CSS, and JavaScript
- **🔧 Configuration Management** - Environment-specific settings
- **📋 RESTful API Design** - Clean JSON endpoints with proper HTTP status codes

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Git (for cloning the repository)

### Installation & Setup

```bash
# Clone the repository
git clone https://github.com/Ofir-Roz/Huffman_code.git
cd Huffman_code

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

Open your browser and navigate to `http://127.0.0.1:5000`

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

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

## 📁 Project Structure

```
Huffman_code/
├── 📱 app/                     # Flask web application
│   ├── __init__.py            # Application factory
│   ├── routes.py              # API endpoints and web routes
│   ├── 🎨 static/             # Frontend assets
│   │   ├── css/style.css      # Responsive styling
│   │   └── js/app.js          # Interactive functionality
│   └── 📄 templates/          # HTML templates
│       └── index.html         # Main application interface
├── 🧮 huffman/               # Core algorithm implementation
│   ├── __init__.py           # Package initialization
│   ├── coding.py             # Huffman coding algorithm
│   └── node.py               # Binary tree node structure
├── 🧪 tests/                 # Comprehensive test suite
│   ├── conftest.py           # Test configuration and fixtures
│   ├── test_huffman.py       # Algorithm unit tests
│   └── test_api.py           # API endpoint tests
├── 📚 docs/                  # Documentation
│   ├── ALGORITHM.md          # Detailed algorithm explanation
│   ├── API.md                # API documentation
│   └── COMMANDS.md           # Development commands reference
├── 💡 examples/              # Usage examples and demonstrations
│   ├── basic_usage.py        # Simple encoding/decoding example
│   ├── file_compression.py   # File processing example
│   ├── performance_test.py   # Benchmarking and performance analysis
│   └── sample.txt            # Sample text for testing
├── 🛠️ scripts/              # Development and deployment scripts
│   ├── setup_dev.py          # Development environment setup
│   └── quality_check.py      # Code quality verification
├── ⚙️ config.py              # Application configuration management
├── 🏃 run.py                 # Development server entry point
├── 🚀 app_production.py      # Production deployment script
├── 📦 requirements.txt       # Python dependencies
├── 📦 requirements-prod.txt  # Production-only dependencies
└── 📄 README.md              # This file
```

## 🔌 API Documentation

### Encode Text
```http
POST /encode
Content-Type: application/json

{
  "text": "Hello, World!"
}
```

**Response:**
```json
{
  "encoded": "110100101001...",
  "frequency_table": [
    {"char": "H", "freq": 1},
    {"char": "e", "freq": 1}
  ],
  "huffman_codes": [
    {"char": "H", "code": "1101"},
    {"char": "e", "code": "001"}
  ],
  "stats": {
    "original_size": 104,
    "compressed_size": 45,
    "compression_ratio": 0.43,
    "space_saved": 56.7
  }
}
```

### Decode Text
```http
POST /decode
Content-Type: application/json

{
  "encoded": "110100101001...",
  "frequency_table": [...]
}
```

**Response:**
```json
{
  "decoded": "Hello, World!"
}
```

## 🧪 Testing

The project includes comprehensive tests covering:

- **Unit Tests** - Algorithm correctness and edge cases
- **Integration Tests** - API endpoint functionality
- **Performance Tests** - Compression efficiency benchmarks
- **Error Handling** - Robust error scenarios

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=huffman --cov=app --cov-report=html

# Run specific test file
pytest tests/test_huffman.py -v
```

## 🚀 Deployment

### Render
This application is optimized for deployment on Render:

1. **Fork/Clone** this repository
2. **Connect** to Render via GitHub
3. **Configure** build settings:
   - Build Command: `pip install -r requirements-prod.txt`
   - Start Command: `python app_production.py`
4. **Deploy** automatically on git push

### Local Production
```bash
# Install production dependencies
pip install -r requirements-prod.txt

# Run in production mode
FLASK_ENV=production python run.py
```

## 📈 Performance

### Compression Efficiency
- **Repetitive Text**: Up to 75% compression
- **English Text**: 40-60% compression typically
- **Random Text**: Minimal compression (as expected)

### Benchmark Results
```
Text Type          | Original Size | Compressed Size | Savings
-------------------|---------------|-----------------|--------
Repetitive         | 1000 bits     | 250 bits        | 75%
English Literature | 8000 bits     | 4800 bits       | 40%
Technical Document | 5000 bits     | 3200 bits       | 36%
```

## 👨‍💻 Author

**Ofir Roz**
- GitHub: [@Ofir-Roz](https://github.com/Ofir-Roz)
- LinkedIn: [Ofir Rozanes](https://linkedin.com/in/ofir-rozanes)

## 🙏 Acknowledgments

- **David A. Huffman** - For the ingenious compression algorithm
- **Flask Community** - For the excellent web framework
- **Python Community** - For the powerful programming language and ecosystem

---

⭐ **Star this repository if you found it helpful!**
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
