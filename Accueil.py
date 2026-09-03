import base64
import streamlit as st

st.set_page_config(page_title="Criminalité LA — Accueil", page_icon="🚔", layout="wide")

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

def image_en_base64(chemin):
    """Encode une image en base64 pour l'insérer directement dans du HTML."""
    with open(chemin, "rb") as f:
        return base64.b64encode(f.read()).decode()


# ============================================================
# CSS personnalisé
# ============================================================
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .hero {
        text-align: center;
        padding: 3rem 1rem 1rem 1rem;
    }
    .hero h1 {
        font-size: 3rem;
        font-weight: 800;
        color: #1F3B73;
        margin-bottom: 0.3rem;
    }
    .hero p {
        font-size: 1.3rem;
        color: #555;
        margin-top: 0;
    }
    .hero .mission {
        font-size: 1rem;
        color: #7A88A0;
        max-width: 640px;
        margin: 0.6rem auto 0 auto;
        line-height: 1.5;
    }

    .accent-bar {
        width: 140px;
        height: 6px;
        margin: 1.2rem auto 0 auto;
        border-radius: 3px;
        background: linear-gradient(90deg, #1F3B73, #C0392B, #1F3B73);
        background-size: 200% 100%;
        animation: glisser 3s linear infinite;
    }
    @keyframes glisser {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }

    /* Cartes équipe */
    .team-card {
        background: linear-gradient(180deg, #E8EEF8 0%, #DCE6F5 100%);
        border: 1px solid #C7D6EE;
        border-radius: 16px;
        padding: 1.5rem 1.5rem 1.5rem 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(31, 59, 115, 0.08);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .team-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 24px rgba(31, 59, 115, 0.18);
    }
    .team-card img {
        border-radius: 10px;
        width: 100%;
        height: auto;
        margin-bottom: 0.9rem;
        display: block;
    }
    .team-card .rank {
        font-size: 0.78rem;
        color: #7A88A0;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-style: italic;
        margin-bottom: 0.15rem;
    }
    .team-card .role {
        color: #1F3B73;
        font-weight: 700;
        font-size: 1.15rem;
        margin-bottom: 0.3rem;
    }
    .team-card .desc {
        color: #666;
        font-size: 0.92rem;
    }

    /* Cartes de navigation */
    .nav-card {
        display: block;
        background: linear-gradient(135deg, #1F3B73 0%, #2C4F8C 100%);
        border-radius: 14px;
        padding: 1.6rem 1rem;
        text-align: center;
        text-decoration: none !important;
        box-shadow: 0 3px 10px rgba(31, 59, 115, 0.18);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .nav-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 26px rgba(31, 59, 115, 0.28);
    }
    .nav-card .icon {
        font-size: 2.2rem;
        margin-bottom: 0.4rem;
    }
    .nav-card .title {
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
    }
    .nav-card .sub {
        color: #C9D6EC;
        font-size: 0.85rem;
        margin-top: 0.2rem;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1F3B73;
        margin-top: 2.8rem;
        margin-bottom: 1.2rem;
    }

    .footer-perso {
        text-align: center;
        color: #9AA6BC;
        font-size: 0.85rem;
        margin-top: 3.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #E3E8F0;
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
    <div class="hero">
        <h1>🚔 Criminalité à Los Angeles</h1>
        <p>Analyse de la criminalité (2020-2023) — Formation Data Analyst, Simplon</p>
        <p class="mission">
            Un outil d'aide à la décision pour prioriser les investissements en sécurité
            publique (patrouilles, éclairage, prévention) à Los Angeles.
        </p>
        <div class="accent-bar"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Navigation rapide
# ============================================================
st.markdown('<div class="section-title">Explorer le dashboard</div>', unsafe_allow_html=True)

col_a, col_b, col_c = st.columns(3, gap="large")

with col_a:
    st.markdown(
        """
        <a href="Presentation" target="_self" class="nav-card">
            <div class="icon">📋</div>
            <div class="title">Présentation</div>
            <div class="sub">Contexte et objectifs</div>
        </a>
        """,
        unsafe_allow_html=True,
    )

with col_b:
    st.markdown(
        """
        <a href="Analyse" target="_self" class="nav-card">
            <div class="icon">📊</div>
            <div class="title">Analyse</div>
            <div class="sub">Géographie, temporel, victimes</div>
        </a>
        """,
        unsafe_allow_html=True,
    )

with col_c:
    st.markdown(
        """
        <a href="Recommandations" target="_self" class="nav-card">
            <div class="icon">✅</div>
            <div class="title">Recommandations</div>
            <div class="sub">Synthèse pour l'élu</div>
        </a>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# Équipe
# ============================================================
st.markdown('<div class="section-title">L\'équipe</div>', unsafe_allow_html=True)

ludivine_b64 = image_en_base64("assets/Ludivine.png")
suz_b64 = image_en_base64("assets/Suz.png")
josephine_b64 = image_en_base64("assets/Josephine.png")

col_marge1, col1, col2, col3, col_marge2 = st.columns([0.5, 1, 1, 1, 0.5], gap="large")

with col1:
    st.markdown(
        f"""
        <div class="team-card">
            <img src="data:image/png;base64,{ludivine_b64}">
            <div class="rank">Capitaine</div>
            <div class="role">Ludivine</div>
            <div class="desc">Type de crime, victimes et circonstances</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="team-card">
            <img src="data:image/png;base64,{suz_b64}">
            <div class="rank">Sergent</div>
            <div class="role">Suz</div>
            <div class="desc">Analyse temporelle</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="team-card">
            <img src="data:image/png;base64,{josephine_b64}">
            <div class="rank">Inspecteur</div>
            <div class="role">Joséphine</div>
            <div class="desc">Analyse géographique</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# Pied de page
# ============================================================
st.markdown(
    """
    <div class="footer-perso">
        Données : LAPD, « Crime Data from 2020 to Present » · Période analysée : 2020-2023<br>
        Projet réalisé dans le cadre de la formation Data Analyst — Simplon
    </div>
    """,
    unsafe_allow_html=True,
)