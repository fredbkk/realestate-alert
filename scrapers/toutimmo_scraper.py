import requests, json, os, time
from bs4 import BeautifulSoup

KEYWORDS = ["dallaz", "potteilaz"]
BASE_URL = "https://www.toutimmo.ch/fr/acheter-maison/vaud/bussigny"
SEEN_FILE = "seen_toutimmo.json"
OUTPUT = "../realestate-alert/new_ads_pending.json"
MAX_SEEN = 1000

def log(msg): print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}")
def load_seen(): return set(json.load(open(SEEN_FILE))) if os.path.exists(SEEN_FILE) else set()
def save_seen(seen): json.dump(list(seen)[-MAX_SEEN:], open(SEEN_FILE, "w"))

def fetch():
    r = requests.get(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
    if r.status_code != 200: log(f"❌ HTTP {r.status_code}"); return []
    soup = BeautifulSoup(r.text, "html.parser")
    ads = soup.select("a[href^='/fr/acheter-maison']")
    seen, new_ads = load_seen(), []
    for a in ads:
        title = a.get_text(strip=True).lower()
        href = a.get("href"); ad_id = href.split("-")[-1]
        url = f"https://www.toutimmo.ch{href}"
        if ad_id not in seen and any(k in title for k in KEYWORDS):
            new_ads.append({"title": title, "url": url}); seen.add(ad_id)
    save_seen(seen)
    if new_ads: json.dump(new_ads, open(OUTPUT, "w"))
    return new_ads

if __name__ == "__main__":
    log("🔎 Surveillance ToutImmo...")
    r = fetch()
    print("\n📢 Annonces trouvées :\n" + "\n".join(f"• {a['title']}\n  🔗 {a['url']}" for a in r) if r else "\nAucune nouvelle annonce.")
