# Notification_system

Simple application that can be at Cron. That voices over notifications from the calendar to your Google Home devices.


Uses GCP service account to access specific shared GSuite calendar.
Loads events from it. Creates media messsage usign GCP test-to-speech API.
As addition to this app you will need to run a web server. Setting it up, in combination with script you will be able playback 
notification media on specific speaker group in your Google Home.
