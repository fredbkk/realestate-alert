import json
import os
from datetime import datetime
from send_whatsapp import send_whatsapp_message

ALERT_FILE = "new_ads_pending.json"
TO = "+41784050450"

def load_new_ads():
    try:
        with open(ALERT_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def format_alert(ads):
    msg_lines = [f"📬 *{len(ads)} nouvelle(s) annonce(s) à Dallaz ou Potteilaz*"]
    for ad in ads:
        title = ad.get("title", "Sans titre")
        url = ad.get("url", "")
        msg_lines.append(f"• {title}\n{url}")
    msg_lines.append(f"\n🕓 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    return "\n\n".join(msg_lines)

def main():
    ads = load_new_ads()
    if ads:
        msg = format_alert(ads)
        send_whatsapp_message(TO, msg)

if __name__ == "__main__":
    main()
