# Development Commands

This file contains common development commands for easy reference.

## Setup Commands

```bash
# Setup development environment
python scripts/setup_dev.py

# Install dependencies only
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy pre-commit
```

## Running the Application

```bash
# Start development server
python run.py

# Start with specific environment
FLASK_ENV=development python run.py
FLASK_ENV=production python run.py
```

## Testing Commands

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=huffman --cov=app

# Run tests with HTML coverage report
pytest --cov=huffman --cov=app --cov-report=html

# Run specific test file
pytest tests/test_huffman.py

# Run tests in verbose mode
pytest -v

# Run tests and stop at first failure
pytest -x
```

## Code Quality Commands

```bash
# Run all quality checks
python scripts/quality_check.py

# Format code with Black
black .

# Check formatting (don't modify)
black --check .

# Lint with flake8
flake8

# Type checking with mypy
mypy .

# Fix import sorting
isort .
```

## Example Commands

```bash
# Run basic example
python examples/basic_usage.py

# Run file compression example
python examples/file_compression.py

# Run performance benchmark
python examples/performance_test.py
```

## Git Commands

```bash
# Setup pre-commit hooks
pre-commit install

# Run pre-commit on all files
pre-commit run --all-files

# Add all changes and commit
git add .
git commit -m "Your commit message"

# Push to remote
git push origin main
```

## Project Management

```bash
# Check project structure
tree /f

# Clean up cache files
Remove-Item -Recurse -Force __pycache__, .pytest_cache, .mypy_cache, htmlcov

# Generate requirements.txt
pip freeze > requirements.txt

# Check package versions
pip list
```

## Docker Commands (if implemented)

```bash
# Build Docker image
docker build -t huffman-coding .

# Run container
docker run -p 5000:5000 huffman-coding

# Run with environment variables
docker run -p 5000:5000 -e FLASK_ENV=production huffman-coding
```

## Production Deployment

```bash
# Install production dependencies only
pip install -r requirements.txt --no-dev

# Run with Gunicorn (production WSGI server)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"

# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
```
