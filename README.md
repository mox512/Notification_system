# "Kids it's time to to get to class" automation using Google calendar, GCP and Google Home devices.

Motivation / problem statement: The time I was in school there was a class ring notifying everyone that break is over and it's time to get back to the desks.
Nowadays my kids study remotely. Even though there is a kids friendly calendar that shows when the next class starts, it was not quite useful so far. Notifications is not reliable.
I wanted to leverage the power of the smart devices we have across our homes, and give meaningful scheduled voiced loud notifications to everyone at home.



Here is diagram describing key components,
![alt text](https://github.com/mox512/Notification_system/blob/master/Diagram.png?raw=true)

Uses GCP service account to access specific shared GSuite calendar.
Loads events from it. 
Creates media messages using GCP test-to-speech API.
Stores this media at a local HTTP server. 
And triggers its playback using Cromecast functionality of Google Home.

Recommended use: 
Set this at Cron to run it each minute. 
With the current configuration app will start creating notification 3 minutes before the event.

Will gladly extend this documentation as I see any interest in it. Feel free to reach out with requests.


