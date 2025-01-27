import re
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

text = "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) wow"
links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
splitted = text.split(f"[{links[0][0]}]({links[0][1]})", 1)
splitted_more = "#".join(splitted).split(f"[{links[1][0]}]({links[1][1]})", 1)
final = "".join(splitted_more).split("#")

new_nodes = []
for link in links:
    splits = text.split(f"[{link[0]}]({link[1]})", 1)
    print(f"First Split: {splits}")
    if len(splits[0]) != 0:
        new_nodes.append(TextNode(splits[0], TextType.TEXT))
    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
    print(f"New Nodes: {new_nodes}\n\n")
    text = "".join(splits[1:])

if len(text) != 0:
    new_nodes.append(TextNode(text, TextType.TEXT))

print(f"Final New Nodes: {new_nodes}")
