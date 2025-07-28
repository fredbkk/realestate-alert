import json
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

KEYWORDS = ["dallaz", "potteilaz"]
BASE_URL = "https://www.anibis.ch/fr/immobilier--1/maison--36/bussigny-près-lausanne--6438"
SEEN_FILE = "seen_anibis.json"
MAX_SEEN = 1000

def log(msg):
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] {msg}")

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
    time.sleep(5)  # Laisse le JS charger

    ads = driver.find_elements(By.CSS_SELECTOR, "a[href^='/fr/d-maison-a-vendre']")
    seen = load_seen()
    new_ads = []

    for ad in ads:
        title = ad.text.strip().lower()
        href = ad.get_attribute("href")
        if not href or not title:
            continue
        ad_id = href.split("/")[-1]
        if ad_id not in seen and any(k in title for k in KEYWORDS):
            new_ads.append((title, href))
            seen.add(ad_id)

    driver.quit()
    save_seen(seen)
    if new_ads:
        with open("../realestate-alert/new_ads_pending.json", "w") as f:
            json.dump([{"title": t, "url": u} for t, u in new_ads], f)
    return new_ads

if __name__ == "__main__":
    log("🧭 Lancement de la surveillance Anibis (via Selenium)...")
    results = fetch_with_selenium()
    if results:
        print("\n📢 Nouvelles annonces trouvées :\n")
        for title, url in results:
            print(f"• {title.capitalize()}\n  🔗 {url}\n")
    else:
        print("\nAucune nouvelle annonce trouvée.\n")
