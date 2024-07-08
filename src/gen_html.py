from block_markdown import markdown_to_html
from htmlnode import (LeafNode, ParentNode)
import os
from pathlib import Path
import re

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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise FileNotFoundError(f"{dir_path_content} doesn't exist")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"{template_path} doesn't exist")
    content_list = os.listdir(dir_path_content)
    pattern = re.compile(r'(.md$)')
    for entry in content_list:
        path = Path(os.path.join(dir_path_content, entry))
        if path.exists():
            if path.is_dir():
                new_dest = os.path.join(dest_dir_path, entry)
                Path(new_dest).mkdir(exist_ok = True)
                generate_pages_recursive(path, template_path, new_dest)
            elif path.is_file():
                if pattern.search(str(path)):
                    new_name = entry.replace('.md', '.html')
                    dest = os.path.join(dest_dir_path, new_name)
                    Path(dest).touch(exist_ok = True)
                    generate_page(path, template_path, dest)
                else:
                    continue
                
        else:
            raise FileNotFoundError(f"{path} doestn't exist")

    
    
