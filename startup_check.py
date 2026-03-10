#!/usr/bin/env python
"""
Startup helper for Face Recognition System
Run this to test dependencies and get started
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required. Current:", f"{version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor} OK")
    return True


def check_venv():
    """Check if virtual environment is activated."""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is active")
        return True
    print("⚠️  Virtual environment not detected")
    print("   Run: python -m venv venv")
    print("   Then activate it:")
    print("   Windows: venv\\Scripts\\activate")
    print("   macOS/Linux: source venv/bin/activate")
    return False


def check_dependencies():
    """Check if required packages are installed."""
    packages = [
        'django',
        'PIL',
        'cv2',
        'face_recognition',
        'numpy',
    ]
    
    all_ok = True
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Run: pip install -r requirements.txt")
            all_ok = False
    
    return all_ok


def check_database():
    """Check if database is initialized."""
    db_path = Path('db.sqlite3')
    if db_path.exists():
        print("✅ Database exists")
        return True
    print("⚠️  Database not found")
    print("   Run: python manage.py migrate")
    return False


def main():
    """Run startup checks."""
    print("\n" + "="*50)
    print("Face Recognition System - Startup Check")
    print("="*50 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_venv),
        ("Dependencies", check_dependencies),
        ("Database", check_database),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n[{name}]")
        result = check_func()
        results.append((name, result))
        print()
    
    # Summary
    print("="*50)
    print("SUMMARY")
    print("="*50)
    
    ok_count = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\nStatus: {ok_count}/{total} checks passed")
    
    if ok_count == total:
        print("\n🎉 All checks passed! Ready to run:")
        print("→ python manage.py runserver")
        print("→ Visit: http://localhost:8000/")
    else:
        print("\n⚠️  Some checks failed. See above for fixes.")
    
    print("\n" + "="*50 + "\n")


if __name__ == '__main__':
    main()
