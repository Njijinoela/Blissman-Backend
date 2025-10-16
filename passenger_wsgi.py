import sys
import os

# Add your project directory to the sys.path
project_home = '/home3/blissma1/Blissman_Backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application
