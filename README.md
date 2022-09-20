# Google calendar notification script with audio playback

Motivation / problem statement: The time I was in school there were a class ring notifiing everyone that break is over and it's time to get back to the desks.
Now days my kids study remotely. Eventhough there there is kids friendly calendar that shows when next class starts, it was not quite reliable so far.
I wanted to leverage power of the smart devices we have across our homes, and give meningfull scheduled voiced loud notifications to everyone at home.

Here is diagram describing key components,
![alt text](https://github.com/mox512/Notification_system/blob/master/Diagram.png?raw=true)

Uses GCP service account to access specific shared GSuite calendar.
Loads events from it. 
Creates media message using GCP test-to-speech API.
Stores this media at local HTTP server. 
And triggers it playback using Cromecast functionality of Google Home.

Recommended use: Set it at Cron. 
Will gladly extend this documentation as I see any interest to it. Feel free to reach out with requests.
