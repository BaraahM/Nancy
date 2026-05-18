## Nancy Pelosi Stocks Trading Tracker

Python script that watches Nancy Pelosi's trades and pings you when she makes a new one.
it:
* Checks QuiverQuant every few hours for new trades
* Sends notifications on Mac and iPhone when something new pops up
* Keeps track of what it's seen before so it doesn't spam, yay lol
* Handles errors instead of crashing

### Setup
1. **Download this repo**
2. **Install the stuff it needs:**
   ```bash
   pip install -r requirements.txt

3. **Optional Setup for iPhone(for getting the notifications):**
Install the Pushcut app, make a shortcut, then update PUSHCUT_URL in config.py with your API key.

### Running 
```
python nancytracker.py
```
It'll check every 4 hours and log everything to ~/pelosi_tracker.log so you can see what's happening.

### Customizing
**Want to change how often it checks? Edit config.py**

__ Important: Replace the placeholder values in config.py with your real API keys:__
1. UR_PUSHCUT_API_KEY - Get this from the Pushcut app
2. OUR_SHORTCUT_NAME - Whatever you named your shortcut

Files
nancytracker.py - The main script
config.py - Settings and API keys
requirements.txt - What Python packages you need

## Heads Up
Because this relies on web scraping QuiverQuant, it depends on their current website structure. If they update their UI or change their tables, the scraper might need a quick tweak to find the right data again.
