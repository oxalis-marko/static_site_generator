import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_ulist,
    block_type_olist,
    markdown_to_html
)



class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_block(self):
        markdown = ("# This is a heading\n\n"
                    "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n"
                    "* This is a list item\n"
                    "* This is another list item")
        self.assertListEqual(markdown_to_blocks(markdown),
        [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n"
            "* This is another list item",
        ])
    
    def test_empty_blocks(self):
        markdown = ("\n\n"
                       "some whitespace     \n\n"
                       "      \n\n"
                       "\n\n"
                       "block"
        )
        self.assertListEqual(markdown_to_blocks(markdown),
        [
            "some whitespace",
            "block"
        ]
        )

    def test_block_types(self):
        blocks = [
            "this is a paragraph",
            "# this is header",
            "#this is not header",
            "####### this is not header",
            "> this is a quote",
            ("> this is a quote\n"
            "> too"),
            ">this is not a quote",
            ("> this is not\n"
            "another quote"),
            ("```\n"
            "this is code\n"
            "```"),
            ("```\n"
            "this is not a code```"),
            ("- this is an \n"
            "- unordered list"),
            ("* This is not an\n"
            "*unordered list"),
            ("1. This is an\n"
            "2. ordered list"),
            "1. This is a list too",
            "- another list",
            ("1. This is not\n"
            "2.an ordered list")

        ]
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        
        self.assertListEqual(block_types,
        [
            block_type_paragraph,
            block_type_heading,
            block_type_paragraph,
            block_type_paragraph,
            block_type_quote,
            block_type_quote,
            block_type_paragraph,
            block_type_paragraph,
            block_type_code,
            block_type_paragraph,
            block_type_ulist,
            block_type_paragraph,
            block_type_olist,
            block_type_olist,
            block_type_ulist,
            block_type_paragraph
        ])

    def test_markdown_to_html(self):
        markdown = '''# Title

This is a paragraph.
'''
# * List item 1
# * List item 2

# > A blockquote

# 1. First ordered item
# 2. Second ordered item
        print(markdown_to_html(markdown))
#         self.assertEqual(markdown_to_html(markdown),
# '''<div>
#     <h1>Title</h1>
#     <p>This is a paragraph.</p>
#     <ul>
#         <li>List item 1</li>
#         <li>List item 2</li>
#     </ul>
#     <blockquote>A blockquote</blockquote>
#     <ol>
#         <li>First ordered item</li>
#         <li>Second ordered item</li>
# </div>''')

if __name__ == "__main__":
    unittest.main()