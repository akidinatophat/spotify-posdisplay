# spotify-posdisplay
This script will show what you're currently playing on Spotify on your Logic Controls LD9000-series point of sale customer display.

[![](https://akidinatophat.github.io/displayrunner-example.jpg)](https://akidinatophat.github.io/displayrunner-example.jpg)

# Disclaimer
This script is very jank. I wrote this in early 2024 as a proof of concept and for my personal use. I've only tested this on Windows but it should work fine on Linux and such.

# Limitations
- These displays have a 45 character limit in scrolling mode, so song data (artists and song name) greater than 45 characters combined will display `MAX CHARS`.
- Updates are not live, the script queries the API every 5 seconds for any changes.
- Runs slower on newer Python versions (3.12 or later).
