# Google calendar notification script with audio playback

Simple application that can be at Cron. That voices over notifications from the Google calendar to your Google Home devices.

Uses GCP service account to access specific shared GSuite calendar.
Loads events from it. Creates media message using GCP test-to-speech API.
In order to playback media to Google Home devices media must be available over HTTP.
Meaning, that in addition to this scrip you will need to run a simple web server, for example Nginx. 
Setting it up, in combination with script you will be able to play back 
notification media on specific speaker group in your Google Home.

Will gladly extend this documentation as I see any interest to it. Feel free to reach out with requests.
