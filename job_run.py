from __future__ import print_function
import time
import pychromecast
import datetime
import urllib.request
import os
from google.cloud import texttospeech
from datetime import timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = '/home/denis/Documents/Scheduler/token.json'
SELFURL = 'http://192.168.86.111/'
ACCOUNTNAME = 'moxusa512@gmail.com'
PATHTOWEB = "/var/www/web/"

def createfilename(text):
    symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
               u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")
    tr = {ord(a): ord(b) for a, b in zip(*symbols)}
    return text.translate(tr).replace(" ", "_").replace("-", "_").replace(".", "_").replace("/", "_").replace(":", "_")

def url_is_alive(url):
    request = urllib.request.Request(url)
    request.get_method = lambda: 'HEAD'
    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False

def synthesize_text(text):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code='ru-RU',
        name='ru-RU-Standard-E',
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    fname = PATHTOWEB + createfilename(text) + ".mp3"
    #Nginx web server is automatically listing all the files from /var/www/web/ to SELFURL website
    with open(fname, "wb") as out:
        out.write(response.audio_content)
        print('    Media written: ' + fname)

def emittnotifications(param):

    print('   Checking available media')
    for URL in param:
        urlstr = SELFURL + createfilename(URL['summary']) + '.mp3'

        if url_is_alive(urlstr):
            print('    Media found: ' + urlstr + '')
        else:
            print('    Creating media:' + urlstr + ' - file not found')
            synthesize_text(URL['summary'])

    print('   Playback init')
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=['School'])
    # School is name for speaker group that we use for broadcasting
    cast = chromecasts[0]
    cast.wait()
    mc = cast.media_controller
    mc.status.volume_level = 10
    # Play first notification on the list
    fname = SELFURL + 'Ding.mp3'
    print('    Emitting media:' + fname)
    mc.play_media(fname, 'audio/mp3')
    # while cast.media_controller.status.player_state != "PLAYING":
    #    time.sleep(0.1)
    #    print(mc.status)

    while mc.status.player_state != "PLAYING":
        time.sleep(0.1)

    # Queue next items
    for URL in param:   #param[1:]
        fname = SELFURL + createfilename(URL['summary']) + '.mp3'
        print('    Enqueuing media:' + fname)
        mc.play_media(fname, 'audio/mp3', enqueue=True)
    print('   Playback complete')
    pychromecast.discovery.stop_discovery(browser)

def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_FILE
    from google.oauth2 import service_account
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    now = datetime.datetime.utcnow().isoformat()
    infuture = datetime.datetime.utcnow() + timedelta(seconds=(3 * 60))
    # Change here to manage how far in advance you would like to ge notifications
    print('-----', now, '-----')
    print('   Credentials valid:', credentials.valid)

    try:
        service = build('calendar', 'v3', credentials=credentials)
        calendar_list_entry = {'id': ACCOUNTNAME}
        created_calendar_list_entry = service.calendarList().insert(body=calendar_list_entry).execute()
        print('   Inserted calendar: ' + created_calendar_list_entry['summary'])

        print('   Listing calendars:')
        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                print('     ' + calendar_list_entry['summary'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

        print('   Getting the upcoming events')
        events_result = service.events().list(calendarId=ACCOUNTNAME, timeMin=now + 'Z',
                                              timeMax=infuture.isoformat() + 'Z',
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        notifications = []
        for event in events:
            eventstart = datetime.datetime.strptime(event['start'].get('dateTime')[:19], '%Y-%m-%dT%H:%M:%S')
            print('       --TD eve: ' +event['summary'])
            print('       --TD sta: '+eventstart.strftime("%m/%d/%Y, %H:%M:%S"))
            print('       --TD now: '+datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            # next If designed to Skip notifications for the events that already in progress
            if eventstart < datetime.datetime.now():
                print('     ' + eventstart.strftime('%Y-%m-%dT%H:%M:%S') + ' !SKIPPED! ' + event['summary'])
            else:
                print('     ' + eventstart.strftime('%Y-%m-%dT%H:%M:%S') + ' ' + event['summary'])
                notifications.add(event)

        if not notifications:
            print('   No events listed for notification. Exiting. ')
            return

        emittnotifications(notifications)
    except HttpError as error:
        print('An error occurred: %s' % error)

if __name__ == '__main__':
    main()
