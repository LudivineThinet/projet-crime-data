import streamlit as st

st.set_page_config(page_title="Présentation - Criminalité LA", layout="wide")

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

st.title("📋 Présentation du projet")

st.markdown(
    """
    ## Le contexte

    Un·e élu·e municipal·e de Los Angeles doit arbitrer un budget de sécurité publique
    entre patrouilles, éclairage et prévention. Faute d'une vue d'ensemble sur la
    criminalité de la ville, ces décisions reposent aujourd'hui largement sur des
    impressions locales plutôt que sur des données consolidées.

    ## La mission

    Ce projet répond à une question simple : **où, quand et sur quoi concentrer les
    moyens ?** Pour y répondre, l'analyse s'appuie sur le dataset officiel du LAPD
    (*Crime Data from 2020 to Present*), plus d'un million de faits enregistrés, et
    la découpe en trois angles complémentaires.
    """
)

st.markdown("---")

st.markdown("## Les trois axes d'analyse")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("### 🗺️ Géographie")
    st.markdown(
        "*Quelles zones concentrent le plus de crimes, comment évoluent-elles, "
        "et où sont les points chauds précis ?*"
    )

with col2:
    st.markdown("### 📅 Temporel")
    st.markdown(
        "*La criminalité augmente-t-elle ? À quelles heures et quels jours "
        "le risque est-il le plus élevé ?*"
    )

with col3:
    st.markdown("### 🔎 Type de crime & victimes")
    st.markdown(
        "*Quels crimes dominent, qui sont les victimes, et dans quelles "
        "circonstances les faits se produisent-ils ?*"
    )

st.markdown("---")

st.markdown("## La méthodologie")

st.markdown(
    """
    **Le dataset.** Plus d'1 million de crimes enregistrés par le LAPD entre 2020 et
    aujourd'hui. Après nettoyage (doublons, valeurs aberrantes, colonnes incohérentes),
    l'analyse porte sur la période **2020-2023** : 2024 et 2025 sont exclues car
    incomplètes dans le dataset source (le nombre de dossiers enregistrés chute
    progressivement à partir d'avril 2024, un artefact de collecte et non une
    vraie baisse de la criminalité).

    **Les outils.** Les calculs statistiques s'appuient prioritairement sur **NumPy**
    (comptages, agrégations, calculs vectorisés), la structuration et le nettoyage
    des données sur **pandas**. Les visualisations sont construites avec Plotly,
    Matplotlib et Seaborn, et restituées dans ce dashboard **Streamlit**.

    **La répartition du travail.** Chaque membre de l'équipe a traité un axe de
    façon indépendante à partir du même jeu de données nettoyé, avant assemblage
    dans ce dashboard commun.
    """
)

st.markdown("---")

st.markdown("## Quelques chiffres clés")

col_k1, col_k2, col_k3, col_k4 = st.columns(4)
col_k1.metric("Crimes analysés (2020-2023)", "≈ 877 000")
col_k2.metric("Zones géographiques", "21")
col_k3.metric("Crimes graves (Part 1)", "≈ 60 %")
col_k4.metric("Taux d'arrestation", "≈ 9 %")

st.caption(
    "Chiffres arrondis, issus des trois analyses détaillées dans l'onglet « Analyse »."
)