from slackclient import SlackClient
import os


class SlackHelper:
    """
    A class that returns a slack communication interface to post messages to Slack Channel
    """
    def initializeSlackHelper(self):
        # get Slack bot token from terminal command 
        self.slack_client = SlackClient(os.environ["SLACK_BOT_TOKEN"])
        self.mybot_id = None

        # check if the slack bot is connected succesfully 
        if self.slack_client.rtm_connect(with_team_state=False):
            print("slack bot is connected and running")
            self.mybot_id = self.slack_client.api_call("auth.test")["user_id"]
        else:
            print("connection failed")

    # post string message to Slack channel 
    def postMessage(self, message):
        self.slack_client.api_call(
            "chat.postMessage",
            channel="general",
            text=message
            )

# some testing commands to ensure slackHelper works proeprly 
if __name__ == "__main__":
    newHelper = SlackHelper()
    newHelper.initializeSlackHelper()
    newHelper.postMessage("hello")
