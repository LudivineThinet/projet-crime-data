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

    .hero-presentation {
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
    }
    .hero-presentation h1 {
        font-size: 2.6rem;
        font-weight: 800;
        color: #1F3B73;
        margin-bottom: 0.3rem;
    }
    .accent-bar {
        width: 120px;
        height: 5px;
        margin: 1rem auto 0 auto;
        border-radius: 3px;
        background: linear-gradient(90deg, #1F3B73, #C0392B, #1F3B73);
        background-size: 200% 100%;
        animation: glisser 3s linear infinite;
    }
    @keyframes glisser {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1F3B73;
        margin-top: 2.5rem;
        margin-bottom: 1.2rem;
    }

    .info-card {
        background: linear-gradient(180deg, #F7F9FC 0%, #EEF3FA 100%);
        border-left: 4px solid #1F3B73;
        border-radius: 10px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
        color: #333;
        line-height: 1.6;
    }
    .info-card b { color: #1F3B73; }

    .metric-card {
        background: linear-gradient(180deg, #E8EEF8 0%, #DCE6F5 100%);
        border: 1px solid #C7D6EE;
        border-radius: 14px;
        padding: 1.2rem 0.8rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(31, 59, 115, 0.08);
    }
    .metric-card .valeur {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1F3B73;
    }
    .metric-card .label {
        font-size: 0.85rem;
        color: #555;
        margin-top: 0.2rem;
    }

    .axe-card {
        background: linear-gradient(135deg, #1F3B73 0%, #2C4F8C 100%);
        border-radius: 14px;
        padding: 1.6rem 1.3rem;
        color: white;
        height: 100%;
    }
    .axe-card h4 {
        margin-top: 0;
        margin-bottom: 0.6rem;
    }
    .axe-card p {
        color: #C9D6EC;
        font-size: 0.92rem;
        font-style: italic;
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Hero
# ============================================================
st.markdown(
    """
    <div class="hero-presentation">
        <h1>📋 Présentation du projet</h1>
        <div class="accent-bar"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Contexte & mission
# ============================================================
st.markdown(
    """
    <div class="info-card">
        <b>Le contexte.</b> Un élu municipal de Los Angeles doit arbitrer un budget de
        sécurité publique entre patrouilles, éclairage et prévention. Faute d'une vue
        d'ensemble sur la criminalité de la ville, ces décisions reposent aujourd'hui
        largement sur des impressions locales plutôt que sur des données consolidées.
    </div>
    <div class="info-card">
        <b>La mission.</b> Ce projet répond à une question simple : où, quand et sur
        quoi concentrer les moyens ? Pour y répondre, l'analyse s'appuie sur le dataset
        officiel du LAPD (<i>Crime Data from 2020 to Present</i>), plus d'un million de
        faits enregistrés.
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Chiffres clés
# ============================================================
st.markdown('<div class="section-title">Le projet en chiffres</div>', unsafe_allow_html=True)

chiffres = [
    ("877 330", "Crimes analysés"),
    ("4", "Années analysées"),
    ("21", "Zones géographiques"),
    ("735 536", "Victimes identifiées"),
]

cols = st.columns(4)
for col, (valeur, label) in zip(cols, chiffres):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="valeur">{valeur}</div>
                <div class="label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.caption("Chiffres sur la période 2020-2023 (2024 et 2025 exclues, incomplètes).")

# ============================================================
# Méthodologie
# ============================================================
st.markdown('<div class="section-title">La méthodologie</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="info-card">
        <b>Le dataset.</b> Plus d'1 million de crimes enregistrés par le LAPD entre 2020
        et aujourd'hui. Après nettoyage (doublons, valeurs aberrantes, colonnes
        incohérentes), l'analyse porte sur la période 2020-2023 : 2024 et 2025 sont
        exclues car incomplètes dans le dataset source (le nombre de dossiers
        enregistrés chute progressivement à partir d'avril 2024, un artefact de
        collecte et non une vraie baisse de la criminalité).
    </div>
    <div class="info-card">
        <b>Les outils.</b> Les calculs statistiques s'appuient prioritairement sur
        NumPy (comptages, agrégations, calculs vectorisés), la structuration et le
        nettoyage des données sur pandas. Les visualisations sont construites avec
        Plotly, Matplotlib et Seaborn, et restituées dans ce dashboard Streamlit.
    </div>
    <div class="info-card">
        <b>La répartition du travail.</b> Chaque membre de l'équipe a traité un axe de
        façon indépendante à partir du même jeu de données nettoyé, avant assemblage
        dans ce dashboard commun.
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Les trois axes
# ============================================================
st.markdown('<div class="section-title">Les trois axes d\'analyse</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(
        """
        <div class="axe-card">
            <h4>🗺️ Géographie</h4>
            <p>Quelles zones concentrent le plus de crimes, comment évoluent-elles,
            et où sont les points chauds précis ?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="axe-card">
            <h4>📅 Temporel</h4>
            <p>La criminalité augmente-t-elle ? À quelles heures et quels jours
            le risque est-il le plus élevé ?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="axe-card">
            <h4>🔎 Type de crime & victimes</h4>
            <p>Quels crimes dominent, qui sont les victimes, et dans quelles
            circonstances les faits se produisent-ils ?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )