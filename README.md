# Google calendar notification scrip with audio playback

Simple application that can be at Cron. That voices over notifications from the Google calendar to your Google Home devices.

Uses GCP service account to access specific shared GSuite calendar.
Loads events from it. Creates media messsage usign GCP test-to-speech API.
As addition to this app you will need to run a simple web server, for example Nginx. 
Setting it up, in combination with script you will be able to playback 
notification media on specific speaker group in your Google Home.

Will gladly extend this documentation as I see any interest to it. Feel free to comment
D.
