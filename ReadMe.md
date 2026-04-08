# Trombinoscope

Outil de génération d'un trombinoscope à partir de l'Annuaire.
Ce script récupère automatiquement les informations des collaborateurs (nom, prénom, photo, fonction, entité) depuis l'annuaire interne.

## Prérequis

- Python 3.10+
- Accès au réseau interne entreprise (VPN ou poste connecté)
- Accès à l'Annuaire Groupe (`annuaire-sec.sso.infra.ftgroup`)
- Remplir les dossiers 'pages' et 'detailsPages' avec les pages html.

## Installation

1. Cloner le projet :
```bash
git clone <url-du-repo>
cd trombinoscope
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
Dans le cas où vous avez beaucoup de personne sur les pages
```bash
python main.py
```
Dans le cas ou vous avez que une personne
```bash
python main.py 1 
```

## Structure du projet
```
trombinoscope/
├── main.py          # Script principal
├── photos           # Dossier pour stocker les photos récupérer
├── People.py        # Modèle de données People
├── requirements.txt 
├── pages            # Mettre les pages récupérées 
└── README.md
```
