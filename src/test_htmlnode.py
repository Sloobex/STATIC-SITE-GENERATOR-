import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Click here",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_none(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty(self):
        node = HTMLNode("div", "Content", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), 
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_no_tag(self):
        # Test bez taga (sirovi tekst)
        node = LeafNode(None, "Samo običan tekst")
        self.assertEqual(node.to_html(), "Samo običan tekst")

    def test_leaf_to_html_no_value(self):
        # Test koji proverava da li baca ValueError ako nema vrednosti
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        parent_node = ParentNode(
            "div",
            [LeafNode("p", "Hello")],
            {"class": "container", "id": "main"}
        )
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><p>Hello</p></div>'
        )

    def test_parent_node_without_tag(self):
        parent_node = ParentNode(None, [LeafNode("p", "Hello")])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_node_without_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_node_with_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")


if __name__ == "__main__":
    unittest.main()
