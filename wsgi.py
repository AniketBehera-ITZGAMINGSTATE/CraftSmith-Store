import sys
import os

# Add your project directory to path
path = '/home/yourusername/mysite'
if path not in sys.path:
    sys.path.append(path)

from app import app as application