import requests
from bs4 import BeautifulSoup
import json
import os
import time

KEYWORDS = ["dallaz", "potteilaz"]
BASE_URL = "https://www.anibis.ch/fr/immobilier--1/maison--36/bussigny-près-lausanne--6438"
SEEN_FILE = "seen_anibis.json"
MAX_SEEN_IDS = 1000

def log(msg):
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] {msg}")

def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()
    try:
        with open(SEEN_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return set(data)
            return set()
    except Exception as e:
        log(f"⚠️ Erreur lecture {SEEN_FILE} : {e}")
        return set()

def save_seen(seen_ids):
    trimmed = list(seen_ids)[-MAX_SEEN_IDS:]
    with open(SEEN_FILE, "w") as f:
        json.dump(trimmed, f)

def fetch_new_ads():
    log("🔎 Vérification des nouvelles annonces Anibis...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        resp = requests.get(BASE_URL, headers=headers)
        if resp.status_code != 200:
            log(f"❌ Erreur HTTP {resp.status_code}")
            return []
    except Exception as e:
        log(f"❌ Erreur réseau : {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    links = soup.select("a[href^='/fr/d-maison-a-vendre-']")
    seen = load_seen()
    new_ads = []
    total_checked = 0

    for a in links:
        total_checked += 1
        title = a.get_text(strip=True).lower()
        href = a["href"]
        ad_id = href.split("/")[-1]

        if ad_id not in seen and any(k in title for k in KEYWORDS):
            full_url = f"https://www.anibis.ch{href}"
            new_ads.append((title, full_url))
            seen.add(ad_id)

    save_seen(seen)
    log(f"🔍 {total_checked} annonces vérifiées, {len(new_ads)} nouvelle(s) détectée(s)")
    return new_ads

if __name__ == "__main__":
    results = fetch_new_ads()
    if results:
        print("\n📢 Nouvelles annonces trouvées :\n")
        for title, link in results:
            print(f"• {title.capitalize()}\n  🔗 {link}\n")
    else:
        print("\nAucune nouvelle annonce trouvée.\n")
