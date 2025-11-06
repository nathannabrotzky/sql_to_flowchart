import os

def export_html(html_content: str, output_path: str) -> None:
    """
    Writes the given HTML content to the specified output path.
    Creates directories if they don't exist.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Flowchart exported to: {output_path}")