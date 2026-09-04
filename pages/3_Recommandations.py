import streamlit as st

st.set_page_config(page_title="Recommandations - Criminalité LA", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] {
        background-color: #F0F4FA;
        padding-top: 1rem;
    }
    [data-testid="stSidebarNav"] a {
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        margin: 0.15rem 0.5rem;
        font-weight: 500;
    }
    [data-testid="stSidebarNav"] a:hover {
        background-color: #DCE6F5;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: #1F3B73;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] span {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("✅ Recommandations pour l'élu")

st.markdown(
    "Synthèse des trois analyses (géographie, temporalité, type de crime & victimes), "
    "organisée par priorité d'action."
)

st.markdown("---")

# ============================================================
# Priorité 1 : Central
# ============================================================
st.markdown("## 🔴 Priorité 1 — Central : une double urgence")

st.markdown(
    """
    Central cumule deux signaux indépendants qui en font la priorité absolue :

    - **Déjà la zone la plus touchée en volume** : 59 457 crimes sur 2020-2023, soit
      6,78 % du total — nettement au-dessus de la part moyenne d'une zone
      (100 % / 21 ≈ 4,76 %)
    - **La zone qui se dégrade le plus vite** : +46,2 % entre 2020 et 2023, loin
      devant les 9 autres zones en alerte (Rampart +27,8 %, Wilshire +26,1 %,
      West Valley +22,8 %, Devonshire +22,4 %, Olympic +22,0 %, Newton +19,4 %,
      Pacific +19,1 %, Topanga +18,9 %, Southwest +17,3 %)

    **Recommandation :** déclencher un renforcement prioritaire (patrouilles,
    éclairage) sur Central, en ciblant spécifiquement les secteurs 162, 182 et 111
    qui concentrent l'essentiel des faits de la zone.
    """
)

st.markdown("---")

# ============================================================
# Priorité 2 : Créneau horaire
# ============================================================
st.markdown("## 🟠 Priorité 2 — Le créneau 17h-22h, tous les jours")

st.markdown(
    """
    - L'heure est **le** facteur déterminant, pas le jour de la semaine : l'écart
      week-end vs semaine est quasi nul (≈ 0 %)
    - Le risque grimpe régulièrement au fil de la journée pour culminer entre
      **17h et 21h**, avec un creux marqué entre 4h et 6h
    - **1 crime sur 4** se produit la nuit (22h-5h)

    **Recommandation :** concentrer les renforts de patrouille et d'éclairage
    public sur la tranche 17h-22h, de façon uniforme toute l'année et tous les
    jours de la semaine — pas de logique de « renfort estival » ou de « renfort
    week-end », le sujet est le niveau global et l'heure de la journée.
    """
)

st.markdown("---")

# ============================================================
# Priorité 3 : Zones en alerte
# ============================================================
st.markdown("## 🟡 Priorité 3 — Les 4 autres zones en alerte")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
        Au-delà de Central, neuf autres zones dépassent le seuil d'alerte de
        +15 % de variation sur 2020-2023 :

        - **Rampart** : +27,8 %
        - **Wilshire** : +26,1 %
        - **West Valley** : +22,8 %
        - **Devonshire** : +22,4 %
        - **Olympic** : +22,0 %
        - **Newton** : +19,4 %
        - **Pacific** : +19,1 %
        - **Topanga** : +18,9 %
        - **Southwest** : +17,3 %

        Cette hausse n'est pas un phénomène isolé : **les 21 zones affichent toutes
        une variation positive** sur la période, aucune ne s'améliore réellement
        (la plus stable, Foothill, n'est qu'à +0,8 %). C'est une tendance de fond
        sur toute la ville, pas un problème localisé à une poignée de zones.
        """
    )

with col2:
    st.markdown(
        """
        **⚠️ Pas de zone "succès"**

        Contrairement à une première lecture sur 2021-2023 seule, aucune zone ne
        recule réellement sur la période complète 2020-2023. Il n'y a pas de
        stratégie locale à dupliquer pour l'instant — la priorité reste la
        même partout : contenir la hausse.
        """
    )

st.markdown("---")

# ============================================================
# Priorité 4 : type de crime et victimes
# ============================================================
st.markdown("## 🔵 Priorité 4 — Cibler la nature des faits, pas seulement le lieu")

st.markdown(
    """
    - **Le vol domine largement** le volume global des crimes enregistrés,
      loin devant les crimes violents
    - Parmi les crimes impliquant une arme, c'est la **force physique** (mains,
      poings, pieds) qui domine très largement — bien avant les armes à feu,
      contrairement à une idée reçue
    - **Seuls 9 % des dossiers** aboutissent à une arrestation ; près de 4 dossiers
      sur 5 restent en enquête en cours
    - Les circonstances les plus fréquentes signalées par les enquêteurs sont
      **« suspect inconnu de la victime »** et **« vol des biens de la victime »**,
      souvent associées entre elles

    **Recommandation :** au-delà du renfort de présence, ces constats plaident pour
    un investissement dans la **capacité d'enquête et d'élucidation** (le principal
    point de friction n'est pas l'absence de signalement, mais le faible taux de
    résolution), et pour des mesures de **prévention situationnelle** contre le vol
    de véhicules et les cambriolages, qui dominent le volume.
    """
)

st.markdown("---")

# ============================================================
# Synthèse finale
# ============================================================
st.markdown("## 📌 En une phrase")

st.info(
    "**Priorité immédiate : Central, sur le créneau 17h-22h.** "
    "Priorité secondaire : les 9 autres zones en alerte (Rampart, Wilshire, West "
    "Valley, Devonshire, Olympic, Newton, Pacific, Topanga, Southwest) — la hausse "
    "touche en réalité les 21 zones sans exception, aucune ne recule. "
    "En parallèle, renforcer la capacité d'enquête pour améliorer le taux "
    "d'élucidation, aujourd'hui très bas (≈ 9 %)."
)

st.caption(
    "Sources : analyses Géographie (Joséphine), Temporalité (Suz) et Type de crime "
    "& Victimes (Ludivine) — dataset LAPD, période 2020-2023 (2024-2025 exclues, "
    "incomplètes)."
)