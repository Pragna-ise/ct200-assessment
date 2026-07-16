import re
from dataclasses import dataclass

@dataclass
class Node:
    title: str
    level: int
    content: str
    parent: str = None


def parse_markdown(file_path):

    nodes = []

    current_title = None
    current_level = None
    current_content = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:

        line = line.strip()

        heading = re.match(r"^(#+)\s+(.*)", line)

        if heading:

            if current_title:
                nodes.append(
                    Node(
                        title=current_title,
                        level=current_level,
                        content="\n".join(current_content)
                    )
                )

            current_level = len(heading.group(1))
            current_title = heading.group(2).replace("**", "").strip()
            current_content = []

        else:
            current_content.append(line)

    if current_title:
        nodes.append(
            Node(
                title=current_title,
                level=current_level,
                content="\n".join(current_content)
            )
        )

    return nodes