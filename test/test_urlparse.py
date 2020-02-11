"""
Test url path handling
"""

import unittest
from components import url_parser

class TestTemplate(unittest.TestCase):
    """Include test cases on a given url"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_case_1(self):
        """Test urllib.parse with posixpath returns path & query"""
        self.assertEqual(url_parser.parse_url('sampleurl.com/graph/')['path'], ['graph'])
        self.assertEqual(url_parser.parse_url('sampleurl.com/graph/')['query'], dict())
    def test_case_2(self):
        """Test timeline of job"""
        self.assertEqual(url_parser.parse_url('sampleurl.com/graph/timeline/8675309')['path'], ['graph', 'timeline', '8675309'])
    def test_case_3(self):
        """Test boxplot with model"""
        self.assertEqual(url_parser.parse_url('sampleurl.com/graph/boxplot/model_test')['path'], ['graph', 'boxplot', 'model_test'])
    def test_case_4(self):
        """Test query handling"""
        self.assertEqual(url_parser.parse_url('sampleurl.com/graph/timeline?start_date=jan.1.1992&end_date=jan.20.1992&feature=duration')['query'], dict(start_date=['jan.1.1992'],end_date=['jan.20.1992'],feature=['duration']))
        self.assertEqual(url_parser.parse_url('sampleurl.com/graph/boxplot/model_test?jobid=8675309')['query'], dict(jobid=['8675309']))
    def test_case_5(self):
        """Check path and query for url with added arguments"""
        self.assertEqual(url_parser.parse_url('localhost'), {'path': [], 'query': {}})
        self.assertEqual(url_parser.parse_url('localhost/route1'), {'path': ['route1'], 'query': {}})
        self.assertEqual(url_parser.parse_url('localhost/route1/'), {'path': ['route1'], 'query': {}})
    def test_case_6(self):
        """Test with port"""
        self.assertEqual(url_parser.parse_url('localhost:8080'), {'path': [], 'query': {}})
        self.assertEqual(url_parser.parse_url('localhost:8080/route1'), {'path': ['route1'], 'query': {}})
        self.assertEqual(url_parser.parse_url('localhost:8080/route1/'), {'path': ['route1'], 'query': {}})
    def test_case_7(self):
        """Test path,query with incomplete port"""
        self.assertEqual(url_parser.parse_url('localhost:'), {'path': [], 'query': {}})
        self.assertEqual(url_parser.parse_url('localhost:/'), {'path': [], 'query': {}})
        self.assertEqual(url_parser.parse_url('localhost:/route1'), {'path': ['route1'], 'query': {}})
    def test_case_8(self):
        """Test path,query with username"""
        self.assertEqual(url_parser.parse_url('admin@localhost'), {'path': [], 'query': {}})
        self.assertEqual(url_parser.parse_url('admin@localhost/'), {'path': [], 'query': {}})
        self.assertEqual(url_parser.parse_url('admin@localhost/route1'), {'path': ['route1'], 'query': {}})
    def test_case_9(self):
        """Test path,query with www without http"""
        self.assertEqual(url_parser.parse_url('www.localhost'), {'path': [], 'query': {}})
        self.assertEqual(url_parser.parse_url('www.localhost/'), {'path': [], 'query': {}})
        self.assertEqual(url_parser.parse_url('www.localhost/route1'), {'path': ['route1'], 'query': {}})

if __name__ == '__main__':
    unittest.main()
