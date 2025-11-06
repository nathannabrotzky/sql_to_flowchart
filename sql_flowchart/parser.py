import re

def parse_sql_file(sql: str) -> str:
    cleaned_content = sql
    cleaned_content = re.sub(r'--.*?(\n|$)', ' ', cleaned_content)
    cleaned_content = re.sub(r'/\*.*?\*/', ' ', cleaned_content, flags=re.DOTALL)
    cleaned_content = cleaned_content.replace('\n', ' ').replace('\t', ' ')
    cleaned_content = ' '.join(cleaned_content.split())
    cleaned_content = cleaned_content.lower()
    return cleaned_content