class Session(object):

    def __init__(self, name,  questions=None):
        self.q = 0;
        self.name = name;
        self.answers = []
        self.qs = questions if questions else ["QA", "QB", "QC"]

    def handleAnswer(self, a):
        print("{} --- {}".format(self.name, a))
        self.answers.append(a)

    def nextQuestion(self):
        if len(self.qs) == self.q:
            return None

        resp = self.qs[self.q]
        print("{} --- {}".format(self.name, resp))
        self.q += 1
        return resp

    def finalize(self):
        lines = []
        lines.append("You have answered:");
        for i in range(len(self.qs)):
            lines.append("{} --> {}".format(self.qs[i], self.answers[i]))
        return "\n".join(lines)
