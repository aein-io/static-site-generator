import unittest

from textnode import TextNode, TextType, text_node_to_html
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_uneq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("I am a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_uneq_text_and_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("I am a text node", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_none_url(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT,
                        "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


class TestTextNodeToHTML(unittest.TestCase):
    def test_text_node_to_html(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html(text_node)
        node = LeafNode(None, "This is a text node",)
        self.assertEqual(
            repr(node), repr(html_node)
        )

    def test_text_node_to_html_link(self):
        text_node = TextNode("This is a text node", TextType.LINK,
                             "https://www.boot.dev")
        html_node = text_node_to_html(text_node)
        node = LeafNode("a", "This is a text node", {
                        "href": "https://www.boot.dev"})
        self.assertEqual(
            repr(node), repr(html_node)
        )


if __name__ == "__main__":
    unittest.main()
