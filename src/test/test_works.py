import unittest
from retrieve_orcid.get_works import collect_works, out
from retrieve_orcid.model import Work

class TestWorks(unittest.TestCase):
    def test_collect_works(self):
        works = collect_works("0000-0002-1825-0097")
        self.assertTrue(len(works) > 0)
        self.assertTrue(isinstance(works[0], Work))
    
    def test_out(self):
        works = collect_works("0000-0002-1825-0097")
        self.assertTrue(len(works) > 0)
        self.assertTrue(isinstance(works[0], Work))
        out(works, "test_out.csv")
        
if __name__ == "__main__":
    unittest.main()