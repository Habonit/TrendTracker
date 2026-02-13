import unittest
from utils.pdf_generator import create_report_html, generate_pdf_from_html, create_wordcloud_image
import os

class TestPDFGenerator(unittest.TestCase):
    def test_create_wordcloud_image(self):
        """워드클라우드 생성이 base64 문자열을 정상적으로 반환하는지"""
        keywords = {'apple': 10, 'banana': 5, 'cherry': 3}
        image_str = create_wordcloud_image(keywords)
        self.assertTrue(image_str.startswith("data:image/png;base64,"))
        self.assertGreater(len(image_str), 100)

    def test_create_report_html(self):
        """HTML 생성이 정상적으로 되는지"""
        items = [{
            'keyword': 'test_keyword',
            'source': 'auto',
            'date': '2023-10-10 10:00',
            'summary': 'This is a test summary.'
        }]
        html = create_report_html("Test Title", "Exec Summary", "", items)
        self.assertIn("Test Title", html)
        self.assertIn("Exec Summary", html)
        self.assertIn("test_keyword", html)
    
    def test_generate_pdf_from_html(self):
        """PDF bytes가 생성되는지"""
        html = "<html><body><h1>Hello PDF</h1></body></html>"
        pdf_bytes = generate_pdf_from_html(html)
        self.assertIsNotNone(pdf_bytes)
        self.assertTrue(len(pdf_bytes) > 0)
        self.assertTrue(pdf_bytes.startswith(b'%PDF-'))

if __name__ == '__main__':
    unittest.main()
