import unittest
from session import Session


class TestSession(unittest.TestCase):

    def test_begin(self):
        qs = ["a", "b"]
        s = Session("hest", qs)
        self.assertEquals(s.nextQuestion(), "a")
        self.assertEquals(s.nextQuestion(), "b")
        self.assertEquals(s.nextQuestion(), None)

if __name__ == '__main__':
    unittest.main()
