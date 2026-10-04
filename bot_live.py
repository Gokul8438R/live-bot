import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import threading
from flask import Flask
import random

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

    def send_win_message():
        msg = "You Are WIN! ✅\nGo to Next Step"
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

    # ==========================================
    # SMART TREND PREDICTOR LOGIC
    # ==========================================
    def get_trend_prediction(history_results):
        try:
            if not history_results:
                return random.choice(["BIG", "SMALL"])
                
            # கடைசியாக வந்த 3 ரிசல்ட்களை எடுக்கிறோம்
            recent_trends = history_results[:3]
            big_count = sum(1 for res in recent_trends if "big" in res.lower())
            small_count = sum(1 for res in recent_trends if "small" in res.lower())
            
            # எது அதிகமாக வந்துள்ளதோ அதையே கணிக்கிறோம் (Trend following)
            if big_count > small_count:
                return "BIG"
            elif small_count > big_count:
                return "SMALL"
            else:
                return random.choice(["BIG", "SMALL"])
        except Exception:
            return random.choice(["BIG", "SMALL"])

    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new') 
    options.add_argument('--no-sandbox') 
    options.add_argument('--disable-dev-shm-usage') 

    driver = webdriver.Chrome(options=options)
    driver.get('https://tirangaprediction.ai/prediction.html')
    time.sleep(5)

    last_period_number = None
    last_predicted_size = None
    history_list = [] # முந்தைய முடிவுகளை சேமிக்க

    while True:
        try:
            current_time = time.time()
            if (current_time - last_promo_time) >= 900: 
                send_promo_message()
                last_promo_time = current_time

            current_period = driver.find_element(By.ID, "nextIssue").text 
            
            if current_period != last_period_number and current_period != "":
                time.sleep(0.1) 
                
                try:
                    # கடைசியாக வந்த முடிவை எடுக்கிறோம்
                    actual_last_result = driver.find_element(By.XPATH, "(//div[contains(@class, 'result-type')])[1]").text 
                    
                    # வரலாற்றில் சேமிக்கிறோம் (Trend கணிக்க)
                    if actual_last_result:
                        history_list.insert(0, actual_last_result)
                        if len(history_list) > 10:
                            history_list.pop()
                            
                    current_prediction = get_trend_prediction(history_list)
                except Exception:
                    time.sleep(0.1)
                    continue 

                if last_period_number is not None:
                    if last_predicted_size and last_predicted_size.lower() in actual_last_result.lower():
                        send_win_message()
                        current_bet_index = 0  
                        consecutive_wins += 1  
                        
                        if consecutive_wins == 6:
                            send_alert_message("🎉 SUPER: 6 Continuous WINS! 🎉")
                            consecutive_wins = 0  
                    else:
                        current_bet_index += 1
                        consecutive_wins = 0  
                        
                        if current_bet_index == 6:
                            send_alert_message(f"🚨 WARNING: 6 Continuous Losses! 🚨\n⚠️ Next bet multiplier: {betting_levels[current_bet_index]}X")
                        
                        if current_bet_index >= len(betting_levels):
                            current_bet_index = 0

                bet_amount = betting_levels[current_bet_index]
                
                msg = f"⚡ 𝗟𝗜𝗩𝗘 ⚡\n📌 : {current_period}\n🎯 : {current_prediction}\n💰 : {bet_amount}X"
                send_telegram_message(msg)
                
                last_period_number = current_period
                last_predicted_size = current_prediction
                
        except Exception:
            pass 
        
        time.sleep(0.05)

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_telegram_bot)
    bot_thread.start()
    
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)