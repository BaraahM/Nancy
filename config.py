import os

PELOSI_URL = "https://www.quiverquant.com/congresstrading/politician/Nancy%20Pelosi-P000197"
PUSHCUT_URL = "https://api.pushcut.io/your_key/notifications/yourname(inpushcut)"

DATA_FILE = os.path.expanduser("~/pelosi_trades.json")
LOG_FILE = os.path.expanduser("~/pelosi_tracker.log")

# how often it scrapes
CHECK_INTERVAL = 14400  # 4 hours in seconds
REQUEST_TIMEOUT = 30    # seconds

NOTIFICATION_TITLE = "Pelosi Trade Alert"