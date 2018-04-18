import os
import time
import re
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

reviewbot_id = None

#constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


class Session(object):

    def __init__(self, name):
        self.q = 0;
        self.name = name;
        self.answers = []
        self.qs = ["rating", "weight", "sight"]

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

session = None

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    global session
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            txt = event["text"]
            channel = event["channel"]
            print(txt)
            if session:
                return txt, channel

            user_id, message = parse_direct_mention(txt)
            if user_id == starterbot_id:
                return message, channel
        elif event['type'] == 'user_typing':
            print('Event text')
            for k,v in event.items():
                print("\t{}:{}".format(k,v))
        else:
            print(event["type"])
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    print("parse_direct_mention: {}".format(message_text))
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    global session
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    if session:
        session.handleAnswer(command)
        response = session.nextQuestion()
        if not response:
            response = session.finalize()
            session = None
    else:
        # This is where you start to implement more commands!
        if command.startswith(EXAMPLE_COMMAND):
            session = Session(command.replace(EXAMPLE_COMMAND, ""))
            response = session.nextQuestion()

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")