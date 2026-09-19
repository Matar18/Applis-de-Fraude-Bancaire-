# 🏦 BankSafe

Application web de **détection de fraude bancaire** combinant un modèle de machine learning et une interface Django. Chaque transaction saisie est analysée en temps réel pour estimer sa probabilité d'être frauduleuse.

## Pourquoi ce projet

Avec l'essor des paiements numériques, les banques doivent identifier les transactions suspectes rapidement, sans pénaliser les clients légitimes. BankSafe illustre comment intégrer un modèle de machine learning entraîné (scikit-learn) dans une vraie application web exploitable — au-delà d'un simple notebook — avec une interface d'analyse, un historique consultable et un dashboard de suivi.

## Fonctionnalités

- **Analyse d'une transaction** : formulaire (montant, heure, nombre de transactions sur 24h, distance du domicile, pays étranger, nouvelle carte) → prédiction de fraude avec probabilité et niveau de risque.
- **Historique** : liste des transactions analysées, filtrable par statut (toutes / fraudes / légitimes).
- **Dashboard** : statistiques globales (taux de fraude, montants moyens) et graphiques (répartition fraude/légitime, comparaison des montants moyens) via Chart.js.

## Stack technique

| Composant | Technologie |
|---|---|
| Backend | Django 6.1 |
| Machine Learning | scikit-learn 1.8 (Pipeline avec `StandardScaler` + `RandomForestClassifier`/`DecisionTreeClassifier`), chargé via `joblib` |
| Frontend | Bootstrap 5, Bootstrap Icons, Chart.js |
| Base de données | SQLite (dev) |

## Structure du projet

```
APP_Fraud/
├── manage.py
├── APP_Fraud/              # Configuration Django (settings, urls, wsgi/asgi)
├── detector/                # App principale
│   ├── models.py            # Modèle Transaction
│   ├── forms.py             # Formulaire d'analyse
│   ├── views.py             # Vues : analyse, historique, dashboard
│   └── urls.py
├── ml_model/
│   └── fraud_model.pkl      # Pipeline scikit-learn entraîné
└── templates/detector/      # Templates (predict, history, dashboard, base)
```

## Installation et lancement

```bash
cd APP_Fraud
pip install django scikit-learn joblib numpy
python manage.py migrate
python manage.py runserver
```

L'application est ensuite accessible sur http://127.0.0.1:8000/ (ou un autre port via `python manage.py runserver 127.0.0.1:8001`).

## Modèle de machine learning

Le pipeline est chargé une seule fois au démarrage (`detector/views.py`) depuis `ml_model/fraud_model.pkl` et prend en entrée 6 variables :

1. `montant`
2. `heure`
3. `nb_transactions_24h`
4. `distance_domicile`
5. `pays_etranger` (0/1)
6. `nouvelle_carte` (0/1)

> **Note** : le modèle a été entraîné avec scikit-learn 1.6.1. Un avertissement `InconsistentVersionWarning` peut apparaître si l'environnement utilise une version différente (ex. 1.8.0) — cela n'empêche pas le fonctionnement, mais il est recommandé de ré-entraîner ou de pinner la version pour garantir des résultats strictement identiques.

## Limites connues

- Base de données SQLite : adaptée au développement, pas à la production.
- Pas d'authentification : toutes les pages sont publiques en l'état.
