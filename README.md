# 🏠 RealEstate Alert Bot

Ce bot surveille quotidiennement les annonces immobilières suisses pour détecter les **maisons à vendre** dans les **quartiers de Dallaz** ou **Potteilaz** à **Bussigny (VD, Suisse)**.

---

## 🚀 Fonctionnalités

- Surveillance automatique de **plus de 10 sites immobiliers suisses** :
  - Immoscout24
  - Anibis
  - PetitesAnnonces
  - JustImmo
  - Acheter-Louer.ch
  - ToutImmo
  - Flatfox
  - Newhome
  - Swissproperty
  - JustHome
  - Immobilier.ch
  - Homegate
- Détection des nouvelles annonces mentionnant "Dallaz" ou "Potteilaz"
- Envoi d'une **alerte immédiate sur WhatsApp**
- Cron job journalier pour surveillance automatique
- Système anti-duplicata avec fichier `seen_*.json`

---

## ⚙️ Installation

```bash
git clone https://github.com/fredbkk/realestate-alert.git
cd realestate-alert
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


