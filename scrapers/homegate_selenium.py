import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_URL = "https://www.homegate.ch/buy/house/zip-1030/matching-list?txt=dallaz%2C%20potteilaz"
KEYWORDS = ["dallaz", "potteilaz"]
SEEN_FILE = "seen_homegate.json"
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

def fetch_new_ads():
    log("🧭 Surveillance Homegate...")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    driver.get(BASE_URL)
    time.sleep(5)

    elems = driver.find_elements(By.CSS_SELECTOR, "a.ListingListItem_link__gf7uP")
    seen = load_seen()
    new_ads = []

    for elem in elems:
        try:
            url = elem.get_attribute("href")
            title = elem.text.lower()
            if any(kw in title for kw in KEYWORDS) and url not in seen:
                new_ads.append({"title": title, "url": url})
                seen.add(url)
        except Exception:
            continue

    driver.quit()
    save_seen(seen)

    if new_ads:
        with open(OUTPUT, "w") as f:
            json.dump(new_ads, f, indent=2)
        log(f"✅ {len(new_ads)} nouvelle(s) annonce(s) détectée(s).")
    else:
        log("Aucune nouvelle annonce.")

if __name__ == "__main__":
    fetch_new_ads()
