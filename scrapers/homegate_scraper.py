import requests
from bs4 import BeautifulSoup
import json
import time
import os

BASE_URL = "https://www.homegate.ch/acheter/immobilier/lieu-bussigny-pres-lausanne/match/maison"
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

def fetch_ads():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "fr-FR,fr;q=0.9"
    }
    resp = requests.get(BASE_URL, headers=headers)
    if resp.status_code != 200:
        log(f"❌ Erreur HTTP {resp.status_code}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    cards = soup.select("article a")
    seen = load_seen()
    new_ads = []

    for a in cards:
        url = a.get("href")
        if not url or not url.startswith("/acheter/"):
            continue
        full_url = "https://www.homegate.ch" + url
        if full_url in seen:
            continue
        text = a.text.lower()
        if any(k in text for k in KEYWORDS):
            new_ads.append({"source": "Homegate", "url": full_url})
            seen.add(full_url)

    if new_ads:
        log(f"✅ {len(new_ads)} nouvelle(s) annonce(s) trouvée(s) sur Homegate.")
        save_seen(seen)
    else:
        log("Aucune nouvelle annonce trouvée.")

    return new_ads

if __name__ == "__main__":
    ads = fetch_ads()
    if ads:
        if os.path.exists(OUTPUT):
            with open(OUTPUT, "r") as f:
                current = json.load(f)
        else:
            current = []
        current.extend(ads)
        with open(OUTPUT, "w") as f:
            json.dump(current, f, indent=2)
