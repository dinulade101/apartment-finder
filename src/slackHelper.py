from slackclient import SlackClient
import os

class SlackHelper:

  def initializeSlackHelper(self):
    self.slack_client = SlackClient("xoxb-340116437617-mgDrlObfZ0AKJtFm3YsMAqs4")
    self.mybot_id = None

    #print(self.slack_client.rtm_connect())
    if self.slack_client.rtm_connect(with_team_state=False):
      print("slack bot is connected and running")
      self.mybot_id = self.slack_client.api_call("auth.test")["user_id"]
    else:
      print("connection failed")
    
    
  def postMessage(self, message):
    self.slack_client.api_call(
      "chat.postMessage",
      channel="general",
      text=message
    )

if __name__ == "__main__":
  newHelper = SlackHelper()
  newHelper.initializeSlackHelper()
  newHelper.postMessage("hello")
  
