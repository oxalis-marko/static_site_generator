import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("tag", "value", None ,{"href": "https://google.com", "target": "_blank"})
        self.assertEqual("HTMLNode(tag, value, None, {'href': 'https://google.com', 'target': '_blank'})", repr(node))

    def test_prop_html(self):
        node = HTMLNode("tag", "value", None,{"href": "https://google.com", "target": "_blank"})
        self.assertEqual(" href=\"https://google.com\" target=\"_blank\"", node.props_to_html())

    def test_leaf_to_html(self):
        node = LeafNode("p", "This is a paragraph of text")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text</p>")
    
    def test_leaf_no_tag(self):
        node = LeafNode(None, "baba")
        self.assertEqual("baba", node.to_html())

    def test_parent_bin(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(),"<p><b>Bold text</b><i>Italic text</i>Normal text</p>")

    def test_nested_parent(self):
        node = ParentNode(
            "p1",
            [
                ParentNode(
                    "p2",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
            ],
        )
        self.assertEqual(node.to_html(), "<p1><p2><b>Bold text</b>Normal text</p2></p1>")
    def test_parent_nnn(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, "Normal text"),
                LeafNode(None, "Normal text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(),"<p>Normal textNormal textNormal text</p>")

    def test_parent_bnb(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("b", "Bold text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<b>Bold text</b></p>")

    def test_parent_bbn(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b><b>Bold text</b>Normal text</p>")

    def test_parent_nbb(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, "Normal text"),
                LeafNode("b", "Bold text"),
                LeafNode("b", "Bold text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p>Normal text<b>Bold text</b><b>Bold text</b></p>")
