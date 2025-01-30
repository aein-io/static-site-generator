import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestSplitNodesDelimeter(unittest.TestCase):
    def test_delimeter_err(self):
        node = TextNode("This is text with a code block` word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(
            expected, new_nodes
        )

    def test_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(
            expected, new_nodes
        )

    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(
            expected, new_nodes
        )


class TestExtractMarkdownImages(unittest.TestCase):
    def test_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text), [(
                "rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

    def test_empty(self):
        text = "This text has no images at all."
        self.assertEqual(
            extract_markdown_images(text), []
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text), [(
                "to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

    def test_empty(self):
        text = "This text has no links at all."
        self.assertEqual(
            extract_markdown_links(text), []
        )


class TestSplitNodeImage(unittest.TestCase):
    def test_text_with_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) for real", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE,
                     "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" for real", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)

    def test_text_with_images(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE,
                     "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_text_with_no_images(self):
        node = TextNode(
            "There are no images here bud.", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    def test_text_with_image_first(self):
        node = TextNode(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) I just rick rolled you", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("rick roll", TextType.IMAGE,
                     "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" I just rick rolled you", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)


class TestSplitNodeLink(unittest.TestCase):
    def test_text_with_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_text_with_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) visit them!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(" visit them!", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_text_with_no_links(self):
        node = TextNode(
            "There are no links here bud.", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_text_with_link_first(self):
        node = TextNode(
            "[Boot dev](https://www.boot.dev) is the best course for backend!", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" is the best course for backend!", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_node(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_nodes, expected)


if __name__ == "__main__":
    unittest.main()
