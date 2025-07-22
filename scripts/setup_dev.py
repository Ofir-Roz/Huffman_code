#!/usr/bin/env python3
"""
Development setup script
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr.strip()}")
        return False

def main():
    """Setup development environment"""
    print("🚀 Setting up Huffman Coding development environment")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install dependencies
    commands = [
        ("pip install -r requirements.txt", "Installing dependencies"),
        ("pip install pre-commit", "Installing pre-commit"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            print(f"\n❌ Setup failed at: {description}")
            sys.exit(1)
    
    # Setup pre-commit hooks (optional)
    if os.path.exists(".git"):
        run_command("pre-commit install", "Setting up pre-commit hooks")
    else:
        print("⚠️  Git repository not found, skipping pre-commit setup")
    
    # Run initial tests
    run_command("python -m pytest tests/ -v", "Running initial tests")
    
    print("\n🎉 Development environment setup complete!")
    print("\n📋 Next steps:")
    print("   • Run tests: pytest")
    print("   • Format code: black .")
    print("   • Type check: mypy .")
    print("   • Lint code: flake8")
    print("   • Start app: python run.py")

if __name__ == "__main__":
    main()
