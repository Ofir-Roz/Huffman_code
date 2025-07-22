#!/usr/bin/env python3
"""
Code quality check script
"""

import subprocess
import sys

def run_check(command, name, required=True):
    """Run a code quality check"""
    print(f"🔍 Running {name}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {name} passed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {name} failed")
        if e.stdout:
            print(f"   Output: {e.stdout}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return not required

def main():
    """Run all code quality checks"""
    print("🔧 Running code quality checks")
    print("=" * 40)
    
    checks = [
        ("black --check .", "Black (code formatting)", True),
        ("flake8", "Flake8 (linting)", True),
        ("mypy .", "MyPy (type checking)", False),  # Optional for now
        ("python -m pytest tests/ -v --cov=huffman --cov=app", "Tests with coverage", True),
    ]
    
    all_passed = True
    
    for command, name, required in checks:
        passed = run_check(command, name, required)
        if not passed and required:
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All quality checks passed!")
        sys.exit(0)
    else:
        print("❌ Some quality checks failed!")
        print("\n🔧 To fix formatting issues, run:")
        print("   black .")
        sys.exit(1)

if __name__ == "__main__":
    main()
