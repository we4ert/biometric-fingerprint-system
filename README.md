# Système d'authentification par empreinte digitale

Ce projet est une démonstration Python d'un système d'authentification biométrique par empreinte digitale. Il ne s'appuie pas sur un capteur physique réel, mais simule le comportement d'un capteur d'empreinte et d'un système de comparaison de templates.

## Objectif

Le projet permet de :
- enregistrer un utilisateur avec une empreinte numérique simulée,
- comparer un scan avec un template enregistré,
- accepter ou rejeter l'authentification selon un seuil de similarité,
- gérer les données dans un fichier JSON local.

## Structure du projet

- `app.py` : point d'entrée CLI
- `fingerprint_system.py` : logique de détection, stockage et comparaison
- `tests/test_fingerprint_system.py` : tests automatisés
- `data/fingerprints.json` : stockage local des utilisateurs et de leurs templates

## Prérequis

- Python 3.10 ou supérieur
- `pytest` si vous voulez lancer les tests

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
# ou .venv\Scripts\activate  # Windows
pip install pytest
```

## Utilisation

### 1. Enregistrer un utilisateur

```bash
python app.py register --user-id user001 --sample "empreinte-01"
```

### 2. Vérifier une empreinte

```bash
python app.py verify --user-id user001 --sample "empreinte-01" --threshold 0.90
```

### 3. Lister les utilisateurs enregistrés

```bash
python app.py list
```

## Exemple de sortie

```bash
$ python app.py register --user-id user001 --sample "empreinte-01"
Utilisateur user001 enregistré avec succès.

$ python app.py verify --user-id user001 --sample "empreinte-01" --threshold 0.90
Authentification acceptée.
Score de similarité : 1.0000
```

## Sécurité et limitations

Ce projet est un prototype pédagogique. En production, il faudrait :
- utiliser un vrai capteur d'empreinte,
- ne pas stocker les images brutes,
- conserver uniquement des templates chiffrés,
- sécuriser les accès avec un stockage chiffré,
- utiliser des mécanismes de conformité (RGPD, sécurité des données biométriques).

## Licence

MIT
