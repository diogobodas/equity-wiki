#!/usr/bin/env python3
"""Backwards compatibility — delegates to file_extract.py."""
import subprocess, sys
sys.exit(subprocess.call([sys.executable, __file__.replace('pdf_extract.py', 'file_extract.py')] + sys.argv[1:]))
