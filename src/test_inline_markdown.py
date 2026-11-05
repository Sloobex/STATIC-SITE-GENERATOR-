import unittest

from src.textnode import TextNode, TextType
from src.inline_markdown import split_nodes_delimiter


class TestInlineMarkdown(unittest.TestCase):
    
    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode("This is text with **two** bolded **words**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
                TextNode(" bolded ", TextType.TEXT),
                TextNode("words", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_unclosed(self):
        node = TextNode("This is text with an *unclosed italic word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC)

    def test_non_text_nodes_passed_through(self):
        # Čvorovi koji nisu TEXT tipa trebaju ostati netaknuti
        node = TextNode("https://example.com", TextType.LINK)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("https://example.com", TextType.LINK),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()