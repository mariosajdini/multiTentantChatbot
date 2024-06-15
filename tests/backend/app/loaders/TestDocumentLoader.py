import unittest
from backend.app.loaders.DocumentLoader import DocumentLoader


class TestDocumentLoader(unittest.TestCase):
    def setUp(self):
        self.file_path = "data/test.pdf"
        self.loader = DocumentLoader(self.file_path)

    def test_load_pdf_document(self):
        documents = self.loader.load()
        self.assertIsNotNone(documents)
        self.assertEqual(len(documents), 8)


if __name__ == '__main__':
    unittest.main()
