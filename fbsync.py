from __future__ import print_function

#https://www.twilio.com/blog/2017/12/facebook-messenger-bot-python.html
#Python libraries that we need to import for our bot
import datetime
import random
import pychromecast
import urllib.request
import job_run
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAAOsSV4ZBtScBAHA4vkMa8l0ffs9JmyDc6ApWkd58smyvV92FTDgZCpWcx4MkRPzBNB4voDr1Ay7Tu2sZAHZB7R8RYzoRA7duh3I0A1fXvkOqfuZAswNW9Nd86G9NcKpTmbTYyg1tKFbZBtSzZAqdXlZBNcTEJkr1c9vkr46oGxuGRt1YYhgZCtpw'
VERIFY_TOKEN = 'DAVYDOV_FAMILY_TOKEN'
bot = Bot(ACCESS_TOKEN)

def processaudiourl(url):
    fname=job_run.createfilename(datetime.datetime.utcnow().isoformat())+".mp3"
    urllib.request.urlretrieve(url, job_run.PATHTOWEB+fname)
    print('   Playback init')
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=['School'])
    cast = chromecasts[0]
    cast.wait()
    mc = cast.media_controller
    mc.status.volume_level = 10
    print('    Emitting media:' + job_run.SELFURL + fname)
    mc.play_media(job_run.SELFURL + fname, 'audio/mp3')


#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        ret = verify_fb_token(token_sent)
        print ('Pairing using code:'+ret)
        #app.make_response(ret,202)
        return ret,200, {'Content-Type': 'application/json'}
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    print(output)
                    if message['message'].get('text'):
                        response_sent_text = message['message'].get('text')
                        send_message(recipient_id, response_sent_text)
                    #if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        for atta in message['message'].get('attachments'):
                            if atta['type'] == 'audio':

                                url=atta['payload'].get('url')
                                #for url in atta.get('payload'):
                                print ('....!'+url)
                                processaudiourl(url)
                        #if message['message'].get('attachments').get('type') = 'audio' :
                        #    print ('!')

                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed",200, {'Content-Type': 'application/json'}


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
