import requests
from bs4 import BeautifulSoup
import json
import os
import time

KEYWORDS = ["dallaz", "potteilaz"]
BASE_URL = "https://www.petitesannonces.ch/a/immobilier/ventes-maison"
SEEN_FILE = "seen_petitesannonces.json"
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
    log("🔎 Vérification des nouvelles annonces Petitesannonces...")
    resp = requests.get(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
    if resp.status_code != 200:
        log(f"❌ Erreur HTTP {resp.status_code}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    ads = soup.select("article a[href^='/a/immobilier']")
    seen = load_seen()
    new_ads = []

    for ad in ads:
        href = ad.get("href")
        title = ad.get_text(strip=True).lower()
        full_url = f"https://www.petitesannonces.ch{href}"
        ad_id = href.split("/")[-1]

        if ad_id not in seen and any(k in title for k in KEYWORDS):
            new_ads.append({"title": title, "url": full_url})
            seen.add(ad_id)

    save_seen(seen)
    if new_ads:
        with open(OUTPUT, "w") as f:
            json.dump(new_ads, f)
    return new_ads

if __name__ == "__main__":
    results = fetch_new_ads()
    if results:
        print("\n📢 Nouvelles annonces trouvées :\n")
        for ad in results:
            print(f"• {ad['title'].capitalize()}\n  🔗 {ad['url']}\n")
    else:
        print("\nAucune nouvelle annonce trouvée.\n")
