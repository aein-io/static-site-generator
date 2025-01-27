import unittest
from block_markdown import markdown_to_blocks, block_to_block_type


class TestMarkdownToBlocks(unittest.TestCase):
    def test_functionality(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        blocks = markdown_to_blocks(markdown)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertEqual(blocks, expected)

    def test_excess_space(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.



* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        blocks = markdown_to_blocks(markdown)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertEqual(blocks, expected)


class BlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a paragraph."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_heading(self):
        block = "### This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "heading")

    def test_seven_heading(self):
        block = "####### This is an invalid heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_no_space_heading(self):
        block = "#This is an invalid heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_code(self):
        block = "```\nThis is a code block\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "code")

    def test_invalid_code(self):
        block = "```\nThis is an invalid code block\n``"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_quote(self):
        block = "> I am a quote\n> And there's more of me!"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "quote")

    def test_unordered_list(self):
        block = "- List\n- of\n- items"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "unordered_list")

    def test_invalid_unordered_list(self):
        block = "*Invalid\n *List"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_ordered_list_one_item(self):
        block = "1. One item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "ordered_list")

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "ordered_list")

    def test_invalid_ordered_list(self):
        block = "1. First\n2. Second\n2. Third\n4. Fourth"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")
