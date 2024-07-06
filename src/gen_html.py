from block_markdown import markdown_to_html
from htmlnode import (LeafNode, ParentNode)
import os

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.strip("# ")
    raise Exception("no h1 header in text")

def generate_page(from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"{from_path} doesn't exist")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"{template_path} doesn't exist")
    if not os.path.exists(dest_path):
        raise FileNotFoundError(f"{dest_path} doesn't exist")
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown_contents = f.read()
    title = extract_title(markdown_contents)
    html_nodes = markdown_to_html(markdown_contents)
    html_contents = html_nodes.to_html()
    with open(template_path, 'r') as f:
        template = f.read()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_contents)
    path = os.path.dirname(dest_path)
    os.makedirs(path, exist_ok = True)
    with open(dest_path, 'w') as f:
        f.write(template)

    
    
