import os

class SQL:
    def __init__(self, path, content):
        self.path = path
        self.content = load_sql_file(path)
    
    def get_path(self):
        return self.path
    
    def get_content(self):
        return self.content

MAX_FILE_SIZE_MB = 5
SQL_KEYWORDS = ['select', 'insert', 'update', 'delete', 'with']

def load_sql_file(file_path: str) -> str:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.lower().endswith('.sql'):
        raise ValueError("Invalid file type. Expected a .sql file.")

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(f"File too large ({file_size_mb:.2f} MB). Max allowed is {MAX_FILE_SIZE_MB} MB.")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()

    if not content.strip():
        raise ValueError("SQL file is empty.")

    if not any(keyword in content.lower() for keyword in SQL_KEYWORDS):
        raise ValueError("File does not appear to contain valid SQL statements.")

    return content