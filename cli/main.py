import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sql_flowchart.orchestrator import SQL

# Iterate over every file in the current folder
for filename in os.listdir('queries'):
    file = SQL('queries\\'+filename)
    file.flowchart()

