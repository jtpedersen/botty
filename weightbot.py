from enum import Enum
class State(Enum):
    creating = 0
    asking = 1


startVoteCommand = "lets vote"

noQuestions = "You can not start to vote before you have defined a question. Try with \"Is this a nice bot\""
createResponse = "Do you have anymore topics to add? ( \"{}\" begin)".format(startVoteCommand);
startVoteRepsonse = "Now the voting process begins, answer each question with your rate (1-5) followed by the reason. Ie \"5 that sounds awesome\""




class WeightBot(object):

    def __init__(self, name):
        self.q = 0;
        self.name = name;
        self.answers = []
        self.questions = []
        self.state = State.creating

    def handleInput(self, txt):
        print("{} --- {}".format(self.name, txt))
        if State.creating == self.state:
            if startVoteCommand == txt:
                return self.handleStartVote()
            else:
                return self.handleNewQuestion(txt)
        else:
            self.answers.append((1, "Baby dont hurt me"))

    def handleStartVote(self):
        if len(self.questions) > 0:
            self.state = State.asking
            return "{}\n{}".format(startVoteRepsonse, self.nextQuestion())
        else:
            return noQuestions
    def handleNewQuestion(self, txt):
        self.questions.append(txt);
        return createResponse

    def nextQuestion(self):
        if len(self.questions) == self.q:
            return None

        resp = self.questions[self.q]
        self.q += 1
        return "Question {}: {}?".format(self.q, resp)

    def finalize(self):
        lines = []
        lines.append("You have answered:");
        for i in range(len(self.questions)):
            lines.append("{} --> {}".format(self.questions[i], self.answers[i]))
        return "\n".join(lines)
