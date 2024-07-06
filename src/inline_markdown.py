from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)

import re

def split_nodes_delimiter (old_nodes, delimiter, text_type):
        new_nodes = []
        for node in old_nodes:
            if node.text_type != text_type_text:
                new_nodes.append(node)
            else:
                if delimiter in node.text:
                    split_nodes = node.text.split(delimiter)
                    for i in range(len(split_nodes)):
                        if split_nodes[i] != "":
                            if i%2 != 0:
                                new_nodes.append(TextNode(split_nodes[i], text_type))
                            else:
                                new_nodes.append(TextNode(split_nodes[i], text_type_text))
                else:
                    new_nodes.append(node)
        return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        text = node.text
        img_tuples = extract_markdown_images(text)
        if len(img_tuples) == 0:
            new_nodes.append(node)
            continue
        for tupl in img_tuples:
            split = text.split(f"![{tupl[0]}]({tupl[1]})", 1)
            if len(split) == 2:
                if split[0] == "":
                    new_nodes.append(TextNode(tupl[0], text_type_image, tupl[1]))
                    text = split[1]
                else:
                    new_nodes.append(TextNode(split[0], text_type_text))
                    new_nodes.append(TextNode(tupl[0], text_type_image, tupl[1]))
                    text = split[1]
        if text != "":
            new_nodes.append(TextNode(text, text_type_text))
    return new_nodes
          
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        text = node.text
        link_tuples = extract_markdown_links(text)
        if len(link_tuples) == 0:
            new_nodes.append(node)
            continue
        for tupl in link_tuples:
            split = text.split(f"[{tupl[0]}]({tupl[1]})", 1)
            if len(split) == 2:
                if split[0] == "":
                    new_nodes.append(TextNode(tupl[0], text_type_link, tupl[1]))
                    text = split[1]
                else:
                    new_nodes.append(TextNode(split[0], text_type_text))
                    new_nodes.append(TextNode(tupl[0], text_type_link, tupl[1]))
                    text = split[1]
        if text != "":
            new_nodes.append(TextNode(text, text_type_text))
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, text_type_text)
    nodes_img = split_nodes_image([node])
    nodes_l = split_nodes_link(nodes_img)
    nodes_b = split_nodes_delimiter(nodes_l, "**", text_type_bold)
    nodes_it = split_nodes_delimiter(nodes_b, "*", text_type_italic)
    nodes_c = split_nodes_delimiter(nodes_it, "`", text_type_code)
    return nodes_c