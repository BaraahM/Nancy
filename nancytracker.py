import requests
from bs4 import BeautifulSoup
import json
import os
import time
import logging
from datetime import datetime
from config import *


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def fetch_trades():
    """fetching data from QuiverQuant website and error handling"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(PELOSI_URL, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, "html.parser")
        trades = []
        
        table = soup.find("table")
        if table:
            rows = table.find_all("tr")[1:]  # skips the header row
            for row in rows:
                cols = row.find_all("td")
                if len(cols) > 2:
                    trade = {
                        "date": cols[0].text.strip(),
                        "ticker": cols[1].text.strip(),
                        "transaction": cols[2].text.strip(),
                        "amount": cols[3].text.strip(),
                    }
                    trades.append(trade)
        
        logging.info(f"successfully fetched {len(trades)} trades")
        return trades
        
    except requests.exceptions.RequestException as e:
        logging.error(f"network error fetching trades: {e}")
        return []
    except Exception as e:
        logging.error(f"unexpected error fetching trades: {e}")
        return []

def load_previous_trades():
    """load previous trade data from JSON file with error handling"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                trades = json.load(f)
                logging.info(f"loaded {len(trades)} previous trades")
                return trades
        return []
    except (json.JSONDecodeError, IOError) as e:
        logging.error(f"error loading previous trades: {e}")
        return []

def save_trades(trades):
    """save trade data to JSON file with error handling"""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(trades, f, indent=4)
        logging.info(f"saved {len(trades)} trades to file")
    except IOError as e:
        logging.error(f"error saving trades: {e}")

def send_mac_notification(message):
    """send notification to macOS with error handling"""
    try:
        os.system(f'osascript -e \'display notification "{message}" with title "{NOTIFICATION_TITLE}"\'')
        logging.info("Mac notification sent successfully")
    except Exception as e:
        logging.error(f"failed to send Mac notification: {e}")

def send_ios_notification(message):
    """send notification to iOS via Pushcut with error handling"""
    try:
        # PUSHCUT_URL is imported from config
        response = requests.post(PUSHCUT_URL, json={"text": message}, timeout=10)
        if response.status_code == 200:
            logging.info("phone notification sent successfully")
        else:
            logging.warning(f"phone notification failed with status {response.status_code}")
    except Exception as e:
        logging.error(f"failed to send iphone notification: {e}")


def validate_trade(trade):
    """validate trade data structure and content"""
    required_fields = ['date', 'ticker', 'transaction', 'amount']
    return all(field in trade and trade[field].strip() for field in required_fields)

def monitor():
    """main monitoring function with error handling and data validation"""
    try:
        logging.info("starting trade monitoring cycle")
        
        prev_trades = load_previous_trades()
        latest_trades = fetch_trades()
        
        if not latest_trades:
            logging.warning("no trades fetched, skipping this cycle")
            return
        
        # Validate trades before processing
        valid_trades = [trade for trade in latest_trades if validate_trade(trade)]
        if len(valid_trades) != len(latest_trades):
            logging.warning(f"filtered out {len(latest_trades) - len(valid_trades)} invalid trades")
        
        new_trades = [trade for trade in valid_trades if trade not in prev_trades]
        
        if new_trades:
            for trade in new_trades:
                message = f"New Pelosi trade: {trade['ticker']} - {trade['transaction']} (${trade['amount']}) on {trade['date']}"
                logging.info(f"New trade detected: {message}")
                
                send_mac_notification(message)
                send_ios_notification(message)
            
            save_trades(valid_trades)
            logging.info(f"processed {len(new_trades)} new trades")
        else:
            logging.info("no new trades detected")
            
    except Exception as e:
        logging.error(f"error in monitoring cycle: {e}")

if __name__ == "__main__":
    """Main execution block with proper error handling"""
    logging.info("Nancy Pelosi Trade Tracker started")
    
    try:
        while True:
            monitor()
            time.sleep(CHECK_INTERVAL)  # wait before checking again
    except KeyboardInterrupt:
        logging.info("tracker stopped by user")
    except Exception as e:
        logging.error(f"fatal error in main loop: {e}")