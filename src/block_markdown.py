from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block_to_block_type(block) == "heading":
            if block.startswith("# "):
                return block[2:]
            continue

    raise Exception("Invalid HTML: No title")


def markdown_to_blocks(markdown):
    blocks = list(
        filter(None, map(lambda x: x.strip(), markdown.split("\n\n"))))
    return blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"

    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code"

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"

    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return "paragraph"
        return "unordered_list"

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return "paragraph"
        return "unordered_list"

    if block.startswith("1. "):
        for i, line in enumerate(lines):
            if not line.startswith(f"{i + 1}. "):
                return "paragraph"
        return "ordered_list"

    return "paragraph"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        children.append(block_to_html_node(block))

    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    match block_type:
        case "heading":
            return heading_to_html(block)
        case "code":
            return code_to_html(block)
        case "quote":
            return quote_to_html(block)
        case "unordered_list":
            return unordered_list_to_html(block)
        case "ordered_list":
            return ordered_list_to_html(block)
        case "paragraph":
            return paragraph_to_html(block)
        case _:
            raise ValueError("Invalid block type")


def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)

    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))

    return children


def heading_to_html(block):
    hashes = block.count("#")

    if hashes >= len(block) or hashes > 6:
        raise ValueError(f"Invalid heading: heading {hashes}")

    tag = f"h{hashes}"
    text = block[hashes + 1:]
    children = text_to_children(text)
    return ParentNode(tag, children)


def code_to_html(block):
    text = block[4:-3]
    children = text_to_children(text)
    code_node = ParentNode("code", children)
    return ParentNode("pre", [code_node])


def quote_to_html(block):
    lines = block.split("\n")
    quote_lines = []

    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        quote_lines.append(line.lstrip(">").strip())

    quote = " ".join(quote_lines)
    children = text_to_children(quote)
    return ParentNode("blockquote", children)


def unordered_list_to_html(block):
    lines = block.split("\n")
    list_items = []

    for line in lines:
        children = text_to_children(line[2:])
        list_items.append(ParentNode("li", children))

    return ParentNode("ul", list_items)


def ordered_list_to_html(block):
    lines = block.split("\n")
    list_items = []

    for line in lines:
        children = text_to_children(line[3:])
        list_items.append(ParentNode("li", children))

    return ParentNode("ol", list_items)


def paragraph_to_html(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)
