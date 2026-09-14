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
    # Ungaloda Telegram Details
    TOKEN = '8596237137:AAECX8V2uoegggsNHDMiI5e943Dd6WADdGg'
    CHAT_ID = '-1003717180891'
    REFER_LINK = 'https://tirangaclub.top/#/register?invitationCode=5554419196155'
    WIN_GIF_URL = 'https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExeWcwd3d5cWRkdWJjdzN5bzZ2NzY1c2F6cHI1cmZ0YzY0eHllMXIyMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ToMjGpyO2OVfPLpoxu8/giphy.gif' 

    PROMO_IMAGE_LOCAL_PATH = 'refer.jpg'
    ALERT_CHAT_ID = '@my_bot_alerts_123' 

    # Betting Levels & Counters
    betting_levels = [1, 3, 7, 15, 31, 63, 127, 255]
    current_bet_index = 0  
    consecutive_wins = 0  

    last_promo_time = time.time()

    def send_telegram_message(text):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        try:
            response = requests.post(url, json={'chat_id': CHAT_ID, 'text': text})
            print(f"✅ Text Sent: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Text error: {e}")

    def send_win_gif():
        url = f"https://api.telegram.org/bot{TOKEN}/sendAnimation"
        caption = f"✅ WIN WIN WIN! ✅\n\n🎯 Play Now and Earn: {REFER_LINK}"
        try:
            requests.post(url, json={'chat_id': CHAT_ID, 'animation': WIN_GIF_URL, 'caption': caption})
            print(f"🎁 WIN GIF Sent!")
        except Exception as e:
             print(f"⚠️ GIF error: {e}")

    def send_promo_image():
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        caption = f"✨ Use the Trick and play and Eran Now 💯\n\n⚡️ Resister Now : {REFER_LINK}\n\n🔥 It's Your own Risk 🏹"
        if not os.path.exists(PROMO_IMAGE_LOCAL_PATH):
            return 
        try:
            with open(PROMO_IMAGE_LOCAL_PATH, 'rb') as photo:
                requests.post(url, data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': photo})
        except Exception:
            pass

    def send_alert_message(text):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        try:
            requests.post(url, json={'chat_id': ALERT_CHAT_ID, 'text': text})
            print(f"🚨 ALERT Sent!")
        except Exception:
            pass

    # Headless Chrome Options for Render Server
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new') 
    options.add_argument('--no-sandbox') 
    options.add_argument('--disable-dev-shm-usage') 

    print("🌐 Website open aagudhu...")
    # Selenium 4-ன் புதிய முறைப்படி webdriver_manager தேவையில்லை
    driver = webdriver.Chrome(options=options)
    driver.get('https://tirangaprediction.ai/prediction.html')
    print("⏳ Page load aagudhu wait pannunga...")
    time.sleep(5)

    last_period_number = None
    last_predicted_size = None

    print("🚀 Bot started! ULTRA FAST mode-la thedudhu...")

    while True:
        try:
            current_time = time.time()
            if (current_time - last_promo_time) >= 300: 
                send_promo_image()
                last_promo_time = current_time

            current_period = driver.find_element(By.ID, "nextIssue").text 
            
            if current_period != last_period_number and current_period != "":
                time.sleep(0.3) 
                
                try:
                    current_prediction = driver.find_element(By.ID, "currentPrediction").text 
                    actual_last_result = driver.find_element(By.XPATH, "(//div[contains(@class, 'result-type')])[1]").text 
                except Exception:
                    time.sleep(0.2)
                    continue 
                
                print(f"⚡ FAST UPDATE -> Period: {current_period} | Predict: {current_prediction} | Last Result: {actual_last_result}")

                # ⚡ MODHALLA PALAYA RESULT-A CHECK PANNI GIF ANUPPUROM ⚡
                if last_period_number is not None:
                    if last_predicted_size and last_predicted_size.lower() in actual_last_result.lower():
                        send_win_gif()
                        current_bet_index = 0  
                        consecutive_wins += 1  
                        
                        if consecutive_wins == 5:
                            send_alert_message("🎉 SUPER: 5 Continuous WINS! 🎉\n\n✅ Thodarndhu 5 period WIN aagiduchu!\n🔥 Bot is performing great!")
                            consecutive_wins = 0  
                    else:
                        current_bet_index += 1
                        consecutive_wins = 0  
                        
                        if current_bet_index == 5:
                            send_alert_message(f"🚨 WARNING: 5 Continuous Losses! 🚨\n\n❌ Last 5 periods failed.\n⚠️ Next bet multiplier: {betting_levels[current_bet_index]}X\n👀 Please check the game manually!")
                        
                        if current_bet_index >= len(betting_levels):
                            current_bet_index = 0

                # ⚡ ADHUKKU APRAM PUDHU PREDICTION-A ANUPPUROM ⚡
                bet_amount = betting_levels[current_bet_index]
                msg = f"🔮 LIVE PREDICTION 🔮\n\n📌 Issue: {current_period}\n👉 Predict: {current_prediction}\n💰 Betting amount: {bet_amount}X\n\n⏳ Bet Open..."
                send_telegram_message(msg)
                
                last_period_number = current_period
                last_predicted_size = current_prediction
                
        except Exception:
            pass 
        
        time.sleep(0.2)

# ==========================================
# 3. RUN BOTH FLASK SERVER & BOT
# ==========================================
if __name__ == '__main__':
    # Bot-ஐ Background-ல் ரன் செய்ய
    bot_thread = threading.Thread(target=run_telegram_bot)
    bot_thread.start()
    
    # Flask Server-ஐ ரன் செய்ய (Render-க்காக)
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)