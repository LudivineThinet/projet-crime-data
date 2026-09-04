# Analyse de la criminalité à Los Angeles (2020-2023)

Dashboard Streamlit réalisé dans le cadre de la formation Data Analyst, Simplon.

Ce projet analyse plus d'1 million de faits enregistrés par le LAPD (*Crime Data
from 2020 to Present*) pour aider un élu municipal à prioriser son budget de
sécurité publique (patrouilles, éclairage, prévention), selon trois axes :
géographie, temporalité, et type de crime & victimes.

🔗 **Dashboard en ligne :** [projet-crime-data-simplon.streamlit.app](https://projet-crime-data-simplon.streamlit.app/)

## Les trois axes d'analyse

- **Géographie** : quelles zones concentrent le plus de crimes, comment évoluent-elles
- **Temporalité** : la criminalité augmente-t-elle, quels créneaux sont les plus à risque
- **Type de crime & victimes** : quels crimes dominent, qui sont les victimes, dans
  quelles circonstances

## Structure du projet

```
Accueil.py                     Page d'accueil (équipe, navigation)
requirements.txt
README.md

pages/
  1_Presentation.py             Contexte, méthodologie, chiffres clés
  2_Analyse.py                  Charge les données, affiche les 3 onglets d'analyse
  3_Recommandations.py          Synthèse et recommandations pour l'élu

data/
  df_clean.csv                  Dataset principal nettoyé (via Git LFS, ~185 Mo)
  df_mocodes.csv                Circonstances (mocodes), un code par ligne
  mo_codes.csv                  Table de traduction des codes mocodes (LAPD)
  crimes_by_zone.csv            Agrégats géographiques
  zone_evolution.csv
  crimes_by_secteur.csv
  crimes_by_position.csv
  top10_hotspots.csv

modules/
  geographie.py                 Onglet Géographie
  temporel.py                   Onglet Temporel
  victimes_typologie.py         Onglet Type de crime & Victimes

assets/                         Photos affichées sur la page d'accueil
```

## Installation

```bash
pip install -r requirements.txt
```

`df_clean.csv` est suivi via **Git LFS** (trop volumineux pour Git classique).
Si le fichier ne se télécharge pas correctement après un `git clone` :

```bash
git lfs install
git lfs pull
```

## Lancement (en local)

```bash
streamlit run Accueil.py
```

## Période analysée

L'analyse porte sur **2020-2023** (4 années complètes). 2024 et 2025 sont
exclues : le nombre de dossiers enregistrés chute progressivement à partir
d'avril 2024 dans le dataset source, un artefact de collecte et non une
vraie baisse de la criminalité.

## Méthodologie

- **NumPy** en priorité pour les calculs (comptages, agrégations, calculs
  vectorisés)
- **pandas** pour le nettoyage et la structuration des données
- **Plotly, Matplotlib, Seaborn** pour les visualisations
- Chaque axe a été traité indépendamment à partir du même jeu de données
  nettoyé, avant assemblage dans ce dashboard commun

## Déploiement en ligne

Le projet est prévu pour Streamlit Community Cloud (connecté à ce repo
GitHub). ⚠️ Le plan gratuit (1 Go de RAM) peut ne pas suffire pour ce
dataset volumineux selon la charge ; en cas d'instabilité en ligne, une
présentation en local reste la solution la plus fiable.

## Limites connues

- `type_arme` : les catégories « Arme inconnue/autre » regroupent à la fois
  les armes non précisées au moment du rapport et celles qui ne correspondent
  à aucune catégorie prédéfinie du LAPD (le dataset ne distingue pas les deux)
- `code_secteur` n'a pas de nom associé dans le dataset source ; la
  correspondance secteur → zone a été reconstruite à partir des données
  (chaque secteur appartient à une seule zone)
- Les mocodes (circonstances) sont traduits à partir du PDF officiel du LAPD
  (révision 06/2018) ; quelques codes plus récents restent non traduits
  (poids négligeable, < 0,5 % des occurrences)