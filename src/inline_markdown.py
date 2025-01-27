import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimeter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        texts = node.text.split(delimeter)

        if len(texts) == 2:
            raise Exception("Split node error: no matching closing delimeter")

        for i, text in enumerate(texts):
            if i == 1:
                new_nodes.append(TextNode(text, text_type))
            else:
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images


def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)

        if len(images) == 0:
            if node.text:
                new_nodes.append(node)
                continue

        for image in images:
            splits = node.text.split(f"![{image[0]}]({image[1]})", 1)
            if len(splits) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if len(splits[0]) != 0:
                new_nodes.append(TextNode(splits[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            node.text = "".join(splits[1:])

        if len(node.text) != 0:
            new_nodes.append(TextNode(node.text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)

        if len(links) == 0:
            if node.text:
                new_nodes.append(node)
                continue

        for link in links:
            splits = node.text.split(f"[{link[0]}]({link[1]})", 1)
            if len(splits) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if len(splits[0]) != 0:
                new_nodes.append(TextNode(splits[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            node.text = "".join(splits[1:])

        if len(node.text) != 0:
            new_nodes.append(TextNode(node.text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    return split_nodes_link((split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(
        [node], "**", TextType.BOLD), "*", TextType.ITALIC), "`", TextType.CODE))))
