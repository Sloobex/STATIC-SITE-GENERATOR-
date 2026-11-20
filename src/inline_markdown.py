import re
from src.textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        split_nodes = []
        sections = old_node.text.split(delimiter)
        
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid markdown, unclosed delimiter: {delimiter}")
            
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
                
        new_nodes.extend(split_nodes)
        
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(old_node)
            continue
            
        for alt, url in images:
            sections = text.split(f"![{alt}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not properly closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = sections[1]
            
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
            
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        text = old_node.text
        links = extract_markdown_links(text)
        if not links:
            new_nodes.append(old_node)
            continue
            
        for anchor, url in links:
            sections = text.split(f"[{anchor}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not properly closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            text = sections[1]
            
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
            
    return new_nodes