# Trombinoscope Orange

Outil de génération d'un trombinoscope à partir de l'Annuaire Groupe Orange.
Ce script récupère automatiquement les informations des collaborateurs (nom, prénom, photo, fonction, entité) depuis l'annuaire interne.

## Prérequis

- Python 3.10+
- Accès au réseau interne Orange (VPN ou poste connecté)
- Accès à l'Annuaire Groupe (`annuaire-sec.sso.infra.ftgroup`)

## Installation

1. Cloner le projet :
```bash
git clone <url-du-repo>
cd trompinoscope_orange
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation
```bash
python main.py
```

## Structure du projet
```
trompinoscope_orange/
├── main.py          # Script principal
├── People.py        # Modèle de données People
├── requirements.txt
├── pages            # Mettre les pages récupérées 
└── README.md
```