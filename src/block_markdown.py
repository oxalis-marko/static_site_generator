import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)
from inline_markdown import text_to_textnodes
from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
)

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "ulist"
block_type_olist = "olist"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        if block == "":
            continue
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    match block[0]:
        case "#":
            if re.match("#{1,6} ", block):
                return block_type_heading
            else:
                return block_type_paragraph
        case "`":
            if re.match("```", block) and re.search("\n```$", block):
                return block_type_code
            else:
                return block_type_paragraph
        case ">":
            for line in block.split("\n"):
                if re.match("> ", line):
                    continue
                else:
                    return block_type_paragraph
            return block_type_quote
        case "-":
            for line in block.split("\n"):
                if re.match("- ", line):
                    continue
                else:
                    return block_type_paragraph
            return block_type_ulist            
        case "1":
            count = 1
            for line in block.split("\n"):
                if line.startswith(f"{count}. "):
                    count += 1
                    continue
                else:
                    return block_type_paragraph
            return block_type_olist
        case _:
            return block_type_paragraph


def block_to_paragraph(block):
    lines = block.split("\n")
    text = []
    for line in lines:
        textnodes = text_to_textnodes(line)
        for node in textnodes:
            text.append(TextNode.text_node_to_html_node(node))
    return ParentNode("p", text)

def block_to_heading(block):
    header = re.match("#*# ", block)
    text_only = block[header.end():]
    print(text_only)
    lines = text_only.split("\n")
    text = []
    for line in lines:
        textnodes = text_to_textnodes(line)
        for node in textnodes:
            text.append(TextNode.text_node_to_html_node(node))
    return ParentNode(f"h{header.end() - 1}", text)

def block_to_quote(block):
    lines = block.split("\n")
    text = []
    for line in lines:
        textnodes = text_to_textnodes(line.strip("> "))
        for node in textnodes:
            text.append(TextNode.text_node_to_html_node(node))
    return ParentNode("blockquote", text)

def block_to_code(block):
    text = block[4:-4]
    code = LeafNode("code", text)
    return ParentNode("pre", [code])

def block_to_ulist(block):
    text = []
    lines = block.split("\n")
    for line in lines:
        textnodes = text_to_textnodes(line.strip("- "))
        html_nodes = []
        for node in textnodes:
            html_nodes.append(TextNode.text_node_to_html_node(node))
        text.append(ParentNode("li", html_nodes))
    return ParentNode("ul", text)

def block_to_olist(block):
    lines = block.split("\n")
    text = []
    count = 1
    for line in lines:
        textnodes = text_to_textnodes(line.strip(f"{count}."))
        html_nodes = []
        for node in textnodes:
            html_nodes.append(TextNode.text_node_to_html_node(node))
        text.append(ParentNode("li", html_nodes))
        count+=1
    return ParentNode("ol", text)

def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in blocks:
        if (block_to_block_type(block) == block_type_paragraph):
            html_blocks.append(block_to_paragraph(block))
        elif (block_to_block_type(block) == block_type_heading):
            html_blocks.append(block_to_heading(block))
        elif(block_to_block_type(block) == block_type_quote):
            html_blocks.append(block_to_quote(block))
        elif(block_to_block_type(block) == block_type_code):
            html_blocks.append(block_to_code(block))
        elif(block_to_block_type(block) == block_type_ulist):
            html_blocks.append(block_to_ulist(block))
        elif(block_to_block_type(block) == block_type_olist):
            html_blocks.append(block_to_olist(block))
    return ParentNode("div", html_blocks)

