import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import threading
from flask import Flask

# ==========================================
# 1. FLASK WEB SERVER SETUP (For Render 24/7)
# ==========================================
app = Flask(__name__)

@app.route('/')
def keep_alive():
    return "Bot is running 24/7 successfully!"

# ==========================================
# 2. MAIN TELEGRAM BOT CODE
# ==========================================
def run_telegram_bot():
    TOKEN = '8596237137:AAECX8V2uoegggsNHDMiI5e943Dd6WADdGg'
    CHAT_ID = '-1003717180891'
    REFER_LINK = 'https://tirangaclub.top/#/register?invitationCode=5554419196155'
    ALERT_CHAT_ID = '@my_bot_alerts_123' 

    betting_levels = [1, 3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191]
    current_bet_index = 0  
    consecutive_wins = 0  

    last_promo_time = time.time()

    def send_telegram_message(text):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        try:
            requests.post(url, json={'chat_id': CHAT_ID, 'text': text})
        except Exception:
            pass

    # Update 1: Removed period numbers from win message
    def send_win_message(prediction):
        pred_upper = str(prediction).upper()
        msg = f"{pred_upper} ✅ WIN WIN WIN! ✅"
        send_telegram_message(msg)

    def send_promo_message():
        msg = f"✨ Use the Trick and play and Earn Now 💯\n\n⚡️ Register Now : {REFER_LINK}\n\n🔥 It's Your own Risk 🏹"
        send_telegram_message(msg)

    def send_alert_message(text):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        try:
            requests.post(url, json={'chat_id': ALERT_CHAT_ID, 'text': text})
        except Exception:
            pass

    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new') 
    options.add_argument('--no-sandbox') 
    options.add_argument('--disable-dev-shm-usage') 

    driver = webdriver.Chrome(options=options)
    driver.get('https://tirangaprediction.ai/prediction.html')
    time.sleep(5)

    last_period_number = None
    last_predicted_size = None

    while True:
        try:
            current_time = time.time()
            if (current_time - last_promo_time) >= 900: 
                send_promo_message()
                last_promo_time = current_time

            current_period = driver.find_element(By.ID, "nextIssue").text 
            
            if current_period != last_period_number and current_period != "":
                # Update 2: Reduced sleep time from 0.3 to 0.1 for faster fetch
                time.sleep(0.1) 
                
                try:
                    current_prediction = driver.find_element(By.ID, "currentPrediction").text 
                    actual_last_result = driver.find_element(By.XPATH, "(//div[contains(@class, 'result-type')])[1]").text 
                except Exception:
                    time.sleep(0.1)
                    continue 

                if last_period_number is not None:
                    if last_predicted_size and last_predicted_size.lower() in actual_last_result.lower():
                        send_win_message(last_predicted_size)
                        current_bet_index = 0  
                        consecutive_wins += 1  
                        
                        if consecutive_wins == 10:
                            send_alert_message("🎉 SUPER: 10 Continuous WINS! 🎉")
                            consecutive_wins = 0  
                    else:
                        current_bet_index += 1
                        consecutive_wins = 0  
                        
                        if current_bet_index == 10:
                            send_alert_message(f"🚨 WARNING: 10 Continuous Losses! 🚨\n⚠️ Next bet multiplier: {betting_levels[current_bet_index]}X")
                        
                        if current_bet_index >= len(betting_levels):
                            current_bet_index = 0

                bet_amount = betting_levels[current_bet_index]
                pred_upper = str(current_prediction).upper()
                
                msg = f"🔮 LIVE : {current_period}\n👉  {pred_upper} : {bet_amount}X"
                send_telegram_message(msg)
                
                last_period_number = current_period
                last_predicted_size = current_prediction
                
        except Exception:
            pass 
        
        # Update 3: Reduced loop sleep time from 0.2 to 0.05 for immediate detection
        time.sleep(0.05)

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_telegram_bot)
    bot_thread.start()
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)