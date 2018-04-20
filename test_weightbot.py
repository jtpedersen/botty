import unittest
import weightbot
import re


class TestSession(unittest.TestCase):

    def test_begin(self):
        wb = weightbot.WeightBot("test")
        self.assertTrue(isinstance(wb.questions, list))
        self.assertTrue(isinstance(wb.answers, list))
        self.assertEqual(weightbot.State.creating, wb.state)

    def test_nameStrip(self):
        wb = weightbot.WeightBot("    test     ")
        self.assertEqual("test", wb.name)

    def test_velcome(self):
        wb = weightbot.WeightBot("test")
        self.assertTrue(isinstance(wb.welcome(), str))

    def test_createQuestions(self):
        wb = weightbot.WeightBot("test")
        self.assertEqual(weightbot.State.creating, wb.state)
        resp = wb.handleInput("What is love?")
        self.assertEqual(1, len(wb.questions))
        self.assertEqual(0, len(wb.answers))
        self.assertEqual(resp, weightbot.createResponse)

    def test_changeMode(self):
        wb = weightbot.WeightBot("test")
        wb.handleInput("What is love?")
        resp = wb.handleInput("lets vote")
        self.assertEqual(weightbot.State.asking, wb.state)
        self.assertTrue(weightbot.startVoteRepsonse in resp)
        self.assertTrue("Question 1:" in resp)
        self.assertTrue("What is love?" in resp)

    def test_changeModeDeniedWihtoutQuestions(self):
        wb = weightbot.WeightBot("test")
        resp = wb.handleInput("lets vote")
        self.assertEqual(weightbot.State.creating, wb.state)
        self.assertTrue(weightbot.noQuestions in resp)

    def test_handleAnswers(self):
        wb = weightbot.WeightBot("test")
        wb.handleInput("What is love?")
        wb.handleInput("lets vote")
        resp = wb.handleInput("1 Baby dont hurt me")
        self.assertEqual(1, len(wb.answers))
        self.assertEqual( (1, "Baby dont hurt me"), wb.answers[0])
        self.assertTrue(resp)

    def test_handleAnswersRating(self):
        wb = weightbot.WeightBot("test")
        wb.handleInput("What is love?")
        wb.handleInput("lets vote")
        resp = wb.handleInput("4 why not")
        self.assertEqual(1, len(wb.answers))
        self.assertEqual( (4, "why not"), wb.answers[0])
        self.assertTrue(resp)

    def test_handleWrongAnswersRating(self):
        wb = weightbot.WeightBot("test")
        wb.handleInput("What is love?")
        wb.handleInput("lets vote")
        resp = wb.handleInput("84 why not")
        self.assertEqual(0, len(wb.answers))
        self.assertTrue(resp)

    def test_handleWrongAnswersRating(self):
        wb = weightbot.WeightBot("test")
        wb.handleInput("What is love?")
        wb.handleInput("lets vote")
        resp = wb.handleInput("84 why not")
        self.assertEqual(0, len(wb.answers))
        self.assertTrue(resp)

        
    def test_pattern(self):
        txt =  "1 Baby dont hurt me"
        m = re.match("([1-5])\s(.*)", txt)
        print(m.groups())



if __name__ == '__main__':
    unittest.main()
