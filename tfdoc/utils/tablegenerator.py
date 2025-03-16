def generate_markdown_table(headers, rows, file_path):
    """Generate Markdown table output."""
    with open(file_path, "w") as file:
        file.write("| " + " | ".join(headers) + " |\n") 
        file.write("|-" + "-|-".join(["-" * len(header) for header in headers]) + "- |\n")
        for row in rows:
            file.write("| " + " | ".join(map(str,row)) + " |\n")

def generate_confluence_table(headers, rows, file_path):
    """Generate Confluence wiki markup table output."""
    with open(file_path, "w") as file:
        file.write("|| " + " || ".join(headers) + " ||\n")
        for row in rows:
            file.write("| " + " | ".join(map(str, row)) + " |\n")