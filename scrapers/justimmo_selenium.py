import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

KEYWORDS = ["dallaz", "potteilaz"]
BASE_URL = "https://www.justimmo.ch/fr/recherche?transaction_type=sale&type%5B%5D=house&location=Bussigny"
SEEN_FILE = "seen_justimmo.json"
MAX_SEEN = 1000
OUTPUT = "../realestate-alert/new_ads_pending.json"

def log(msg):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen)[-MAX_SEEN:], f)

def fetch_with_selenium():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--lang=fr")

    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)
    time.sleep(5)

    ads = driver.find_elements(By.CSS_SELECTOR, "a.property-link")
    seen = load_seen()
    new_ads = []

    for ad in ads:
        title = ad.text.strip().lower()
        href = ad.get_attribute("href")
        if not href or not title:
            continue
        ad_id = href.split("-")[-1]

        if ad_id not in seen and any(k in title for k in KEYWORDS):
            new_ads.append({"title": title, "url": href})
            seen.add(ad_id)

    driver.quit()
    save_seen(seen)
    if new_ads:
        with open(OUTPUT, "w") as f:
            json.dump(new_ads, f)
    return new_ads

if __name__ == "__main__":
    log("🧭 Lancement surveillance Justimmo (via Selenium)...")
    results = fetch_with_selenium()
    if results:
        print("\n📢 Nouvelles annonces trouvées :\n")
        for ad in results:
            print(f"• {ad['title'].capitalize()}\n  🔗 {ad['url']}\n")
    else:
        print("\nAucune nouvelle annonce trouvée.\n")
