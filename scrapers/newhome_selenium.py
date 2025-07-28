import json, os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

KEYWORDS = ["dallaz", "potteilaz"]
BASE_URL = "https://www.newhome.ch/fr/acheter-maison/lieu-bussigny-pres-lausanne/liste"
SEEN_FILE = "seen_newhome.json"
OUTPUT = "../realestate-alert/new_ads_pending.json"
MAX_SEEN = 1000

def log(msg): print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}")
def load_seen(): return set(json.load(open(SEEN_FILE))) if os.path.exists(SEEN_FILE) else set()
def save_seen(seen): json.dump(list(seen)[-MAX_SEEN:], open(SEEN_FILE, "w"))

def fetch():
    opts = Options(); opts.add_argument("--headless"); opts.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=opts)
    driver.get(BASE_URL); time.sleep(5)
    ads = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='listing-result']")
    seen, new_ads = load_seen(), []
    for ad in ads:
        title = ad.text.strip().lower()
        url = ad.get_attribute("href")
        ad_id = url.split("/")[-1]
        if ad_id not in seen and any(k in title for k in KEYWORDS):
            new_ads.append({"title": title, "url": url}); seen.add(ad_id)
    driver.quit(); save_seen(seen)
    if new_ads: json.dump(new_ads, open(OUTPUT, "w"))
    return new_ads

if __name__ == "__main__":
    log("🧭 Surveillance Newhome...")
    r = fetch()
    print("\n📢 Annonces trouvées :\n" + "\n".join(f"• {a['title']}\n  🔗 {a['url']}" for a in r) if r else "\nAucune nouvelle annonce.")
