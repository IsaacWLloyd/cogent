#!/usr/bin/env python3
"""
Test runner script that sets up proper Python path for imports.
"""

import os
import sys
import subprocess

# Add backend and parent directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(backend_dir)

sys.path.insert(0, backend_dir)
sys.path.insert(0, parent_dir)

# Set environment variable for imports
os.environ['PYTHONPATH'] = f"{backend_dir}:{parent_dir}:{os.environ.get('PYTHONPATH', '')}"

# Run pytest
result = subprocess.run([sys.executable, '-m', 'pytest', 'tests/', '-v'], cwd=backend_dir)
sys.exit(result.returncode)