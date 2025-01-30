import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node


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


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraph(self):
        markdown = """
I am a paragraph with some **bold** text
Here are some more words in the same
paragraph

"""

        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>I am a paragraph with some <b>bold</b> text Here are some more words in the same paragraph</p></div>",
        )

    def test_paragraphs(self):
        markdown = """
I am a paragraph with some **bold** text
Here are some more words in the same
paragraph

I am a different paragraph with *italic* text

"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>I am a paragraph with some <b>bold</b> text Here are some more words in the same paragraph</p><p>I am a different paragraph with <i>italic</i> text</p></div>"
        )

    def test_quotes(self):
        markdown = """
> This is a quote
> with multiple lines
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines</blockquote></div>"
        )

    def test_unordered_list(self):
        markdown = """
- List one item one
- List one item two
- List one item three

* List two item one
* List two item two
* List two item three
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>List one item one</li><li>List one item two</li><li>List one item three</li></ul><ul><li>List two item one</li><li>List two item two</li><li>List two item three</li></ul></div>"
        )

    def test_ordered_list(self):
        markdown = """
1. First
2. Second
3. Third
4. Fourth

1. First
2. Second
2. Third
3. Fourth
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li><li>Fourth</li></ol><p>1. First 2. Second 2. Third 3. Fourth</p></div>"
        )

    def test_code(self):
        markdown = """
```
I am a code block
Here is some code:
code
```
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>I am a code block\nHere is some code:\ncode\n</code></pre></div>"
        )

    def test_headings(self):
        markdown = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

####### Heading 7
"""
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6><p>####### Heading 7</p></div>"
        )


if __name__ == "__main__":
    unittest.main()
