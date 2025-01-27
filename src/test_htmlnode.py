import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode()
        self.assertEqual(
            "HTMLNode(tag: None, value: None, children: None, props: None)", repr(
                node)
        )

    def test_none_values(self):
        prop = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=prop)
        self.assertEqual(
            "HTMLNode(tag: None, value: None, children: None, props: {'href': 'https://www.google.com', 'target': '_blank'})", repr(
                node)
        )

    def test_props_to_html(self):
        prop = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=prop)
        html = node.props_to_html()
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', html
        )


class TestLeafNode(unittest.TestCase):
    def test_raises_value_err(self):
        node = LeafNode(tag=None, value=None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_paragraph(self):
        node = LeafNode("p", "This is a paragraph of text.")
        html = node.to_html()
        self.assertEqual(
            "<p>This is a paragraph of text.</p>", html
        )

    def test_to_html_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        html = node.to_html()
        self.assertEqual(
            '<a href="https://www.google.com">Click me!</a>', html
        )

    def test_repr(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            "LeafNode(a, Click me!, {'href': 'https://www.google.com'})", repr(
                node)
        )


class TestParentNode(unittest.TestCase):
    def test_repr(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            "ParentNode(p, [LeafNode(b, Bold text, None), LeafNode(None, Normal text, None), LeafNode(i, italic text, None), LeafNode(None, Normal text, None)], None)", repr(
                node)
        )

    def test_tag_none(self):
        node = ParentNode(None, [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),],)
        self.assertRaises(ValueError, node.to_html)

    def test_children_none(self):
        node = ParentNode("p", None,)
        self.assertRaises(ValueError, node.to_html)

    def test_children_empty(self):
        node = ParentNode("p", [],)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        html = node.to_html()
        self.assertEqual(
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>", html
        )

    def test_to_html_nested_parent(self):
        node = ParentNode(
            "b",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                )
            ],
        )
        html = node.to_html()
        self.assertEqual(
            "<b><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></b>", html
        )


if __name__ == "__main__":
    unittest.main()
