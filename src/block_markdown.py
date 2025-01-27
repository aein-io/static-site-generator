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
