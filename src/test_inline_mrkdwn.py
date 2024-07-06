import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)

from inline_markdown import(
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        nodes = [
            TextNode("This is text with **bolded** word", text_type_text),
            TextNode("This is text with **bolded** word", text_type_text),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
                TextNode("This is text with ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_double_bold(self):
        node = TextNode("This is text with **bolded** word and another **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and another ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text)
            ],
            new_nodes,
        )

    def test_delim_multi_bold(self):
        node = TextNode("This is text with **double bolded**, word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with ", text_type_text),
                TextNode("double bolded", text_type_bold),
                TextNode(", word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes2 = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("bold", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("italic", text_type_italic),
            ],
            new_nodes2,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with `code` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with ", text_type_text),
                TextNode("code", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )


    def test_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(extract_markdown_images(text), [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])
        
    def test_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(extract_markdown_links(text), [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])
    

    def test_split_two_image(self):
        node = TextNode(
        "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
        text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes,
        [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode("second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
        ])

    def test_split_one_image(self):
        node = TextNode(
        "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another !",
        text_type_text)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes,
        [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another !", text_type_text),
        ])

    def test_split_no_image(self):
        node = TextNode("There is no image", text_type_text)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes,[TextNode("There is no image", text_type_text)])
    
    def test_corner_image(self):
        node = TextNode("![image](http) text ![another image](h)", text_type_text)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes,
            [
                TextNode("image", text_type_image, "http"),
                TextNode(" text ", text_type_text),
                TextNode("another image", text_type_image, "h")
            ])

    def test_split_two_link(self):
        node = TextNode(
            "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes,
        [
            TextNode("This is text with an ", text_type_text),
            TextNode("link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode("second link", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
        ])

    def test_text_to_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(new_nodes,
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ]
        )
if __name__ == "__main__":
    unittest.main()