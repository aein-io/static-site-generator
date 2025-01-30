import unittest
from generate_content import extract_title


class ExtractTitle(unittest.TestCase):

    def test_title(self):
        markdown = """
        # Hello

        This has a title
        """
        title = extract_title(markdown)
        self.assertEqual(
            title, "Hello"
        )

    def test_no_title(self):
        markdown = """
        I am but a humble paragraph
        """
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
