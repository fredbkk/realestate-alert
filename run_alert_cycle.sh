#!/bin/bash

cd "$(dirname "$0")"
source venv/bin/activate

LOG_DATE=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$LOG_DATE] 🏠 Lancement du cycle de surveillance..." >> cronlog.log

# Vider le fichier de résultats
> new_ads_pending.json

# Exécuter tous les scrapers
for scraper in scrapers/*.py; do
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ▶️ $scraper" >> cronlog.log
  python "$scraper" >> cronlog.log 2>&1
done

# Si des annonces ont été trouvées
if [ -s new_ads_pending.json ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📲 Envoi de l'alerte WhatsApp..." >> cronlog.log
  python alert/send_alert.py
else
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❎ Aucun résultat, aucune notification envoyée." >> cronlog.log
fi
