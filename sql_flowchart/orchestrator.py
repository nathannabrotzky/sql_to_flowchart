import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sql_flowchart.file_loader import load_sql_file
from sql_flowchart.parser import parse_sql_file
from sql_flowchart.modeler import model_sql
from sql_flowchart.diagram_generator import SqlFlowchartGenerator

class SQL:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.content = load_sql_file(self.path)
        self.parsed = parse_sql_file(self.content)
        self.model = model_sql(self.parsed)
        self.generator = SqlFlowchartGenerator(self.model)
        self.output = path.replace(".sql","")
    
    def get_path(self):
        print(self.path)
        return self.path
    
    def get_content(self):
        print(self.content)
        return self.content
    
    def get_parsed(self):
        print(self.parsed)
        return self.parsed
    
    def get_model(self):
        for k, node in self.model.items():
            print(f"{node.id}")
            print(f"{node.type}")
            print(f"{node.content}")
            print(f"{node.parents}")
            print(f"{node.children}\n")
        return self.model
    
    def flowchart(self):
        self.generator.generate_flowchart('output\\' + self.output)
