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

    .hero-reco {
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
    }
    .hero-reco h1 {
        font-size: 2.6rem;
        font-weight: 800;
        color: #1F3B73;
        margin-bottom: 0.3rem;
    }
    .hero-reco p {
        font-size: 1.1rem;
        color: #555;
    }
    .accent-bar {
        width: 120px;
        height: 5px;
        margin: 1rem auto 1.5rem auto;
        border-radius: 3px;
        background: linear-gradient(90deg, #1F3B73, #C0392B, #1F3B73);
        background-size: 200% 100%;
        animation: glisser 3s linear infinite;
    }
    @keyframes glisser {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }

    .priorite-titre {
        font-size: 1.3rem;
        font-weight: 700;
        margin-top: 2.2rem;
        margin-bottom: 1rem;
    }

    .priorite-card {
        border-radius: 10px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 0.6rem;
        color: #333;
        line-height: 1.65;
    }
    .priorite-card b { color: #1F3B73; }
    .p1 { background: linear-gradient(180deg, #FBEAEA 0%, #F7DADA 100%); border-left: 5px solid #C0392B; }
    .p2 { background: linear-gradient(180deg, #FDF1E6 0%, #FBE5CC 100%); border-left: 5px solid #E67E22; }
    .p3 { background: linear-gradient(180deg, #FDF8E3 0%, #FBF0C0 100%); border-left: 5px solid #D4AC0D; }
    .p4 { background: linear-gradient(180deg, #E8EEF8 0%, #DCE6F5 100%); border-left: 5px solid #1F3B73; }

    .apart-card {
        background: #FFFFFF;
        border: 1px solid #E3E8F0;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        color: #333;
        line-height: 1.55;
        height: 100%;
    }
    .apart-card b { color: #C0392B; }

    .synthese-card {
        background: linear-gradient(135deg, #1F3B73 0%, #2C4F8C 100%);
        border-radius: 14px;
        padding: 1.8rem 2rem;
        color: white;
        font-size: 1.05rem;
        line-height: 1.7;
        margin-top: 1rem;
    }
    .synthese-card b { color: #FFD966; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Hero
# ============================================================
st.markdown(
    """
    <div class="hero-reco">
        <h1>✅ Recommandations pour l'élu</h1>
        <p>Synthèse des trois analyses (géographie, temporalité, type de crime &amp;
        victimes), organisée par priorité d'action.</p>
        <div class="accent-bar"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Priorité 1 : Central
# ============================================================
st.markdown('<div class="priorite-titre">🔴 Priorité 1 — Central : une double urgence</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="priorite-card p1">
        Central cumule deux signaux indépendants qui en font la priorité absolue :
        <ul>
            <li><b>Déjà la zone la plus touchée en volume</b> : 59 457 crimes sur 2020-2023,
            soit 6,78 % du total — nettement au-dessus de la part moyenne d'une zone
            (100 % / 21 ≈ 4,76 %)</li>
            <li><b>La zone qui se dégrade le plus vite</b> : +46,2 % entre 2020 et 2023,
            loin devant les 9 autres zones en alerte</li>
        </ul>
        <b>Recommandation :</b> déclencher un renforcement prioritaire (patrouilles,
        éclairage) sur Central, en ciblant spécifiquement les secteurs 162, 182 et 111
        qui concentrent l'essentiel des faits de la zone.
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Priorité 2 : Créneau horaire
# ============================================================
st.markdown('<div class="priorite-titre">🟠 Priorité 2 — Le créneau 17h-22h, tous les jours</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="priorite-card p2">
        <ul>
            <li>L'heure est <b>le</b> facteur déterminant, pas le jour de la semaine :
            l'écart week-end vs semaine est quasi nul (≈ 0 %)</li>
            <li>Le risque grimpe régulièrement au fil de la journée pour culminer entre
            <b>17h et 21h</b>, avec un creux marqué entre 4h et 6h</li>
            <li><b>1 crime sur 4</b> se produit la nuit (22h-5h)</li>
        </ul>
        <b>Recommandation :</b> concentrer les renforts de patrouille et d'éclairage
        public sur la tranche 17h-22h, de façon uniforme toute l'année et tous les
        jours de la semaine — pas de logique de « renfort estival » ou de « renfort
        week-end », le sujet est le niveau global et l'heure de la journée.
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Priorité 3 : Zones en alerte
# ============================================================
st.markdown('<div class="priorite-titre">🟡 Priorité 3 — Les 4 zones qui montent le plus vite après Central</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="priorite-card p3">
        Quatre zones se dégradent nettement plus vite que la moyenne, juste derrière
        Central :
        <ul>
            <li><b>Rampart</b> : +27,8 % &nbsp;·&nbsp; <b>Wilshire</b> : +26,1 %
            &nbsp;·&nbsp; <b>West Valley</b> : +22,8 % &nbsp;·&nbsp;
            <b>Devonshire</b> : +22,4 %</li>
        </ul>
        Cinq autres zones dépassent aussi le seuil d'alerte de +15 % (Olympic, Newton,
        Pacific, Topanga, Southwest), mais avec une progression plus modérée. Aucune
        des 21 zones ne recule réellement sur la période — la hausse est une tendance
        de fond sur toute la ville, pas un problème localisé.
        <br><br>
        <b>Recommandation :</b> après Central, programmer un second temps de
        renforcement (patrouilles, éclairage) sur ces 4 zones dès le prochain cycle
        budgétaire, et mettre en place un suivi trimestriel du seuil d'alerte pour
        les 5 zones restantes, afin d'anticiper si elles rejoignent ce groupe
        prioritaire.
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Priorité 4 : type de crime et victimes
# ============================================================
st.markdown('<div class="priorite-titre">🔵 Priorité 4 — Cibler la nature des faits, pas seulement le lieu</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="priorite-card p4">
        <ul>
            <li><b>Le vol domine largement</b> le volume global, loin devant les crimes
            violents → <b>prioriser la prévention situationnelle</b> (parkings
            sécurisés, dispositifs anti-vol) sur les zones à forte densité de vols de
            véhicules et cambriolages.</li>
            <li>Parmi les crimes armés, c'est la <b>force physique</b> qui domine très
            largement, bien avant les armes à feu → l'enjeu n'est pas le désarmement
            mais une <b>présence humaine dissuasive</b> (patrouilles visibles,
            médiation de proximité) sur le créneau 17h-22h déjà identifié.</li>
            <li><b>Seuls 9 % des dossiers</b> aboutissent à une arrestation → investir
            en priorité dans la <b>capacité d'enquête</b> (effectifs, outils
            d'élucidation), plutôt que dans la seule présence terrain.</li>
            <li>Les circonstances les plus fréquentes sont <b>« suspect inconnu »</b>
            et <b>« vol des biens de la victime »</b>, souvent associées → ce profil
            (agresseur inconnu, opportuniste) justifie de renforcer
            <b>vidéosurveillance et éclairage</b> plutôt que des dispositifs ciblant
            les violences entre proches.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Synthèse finale
# ============================================================
st.markdown('<div class="priorite-titre">📌 En une phrase</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="synthese-card">
        <b>Priorité immédiate : Central, sur le créneau 17h-22h.</b><br>
        Priorité secondaire : les 9 autres zones en alerte (Rampart, Wilshire, West
        Valley, Devonshire, Olympic, Newton, Pacific, Topanga, Southwest) — la hausse
        touche en réalité les 21 zones sans exception, aucune ne recule.<br>
        En parallèle, renforcer la capacité d'enquête pour améliorer le taux
        d'élucidation, aujourd'hui très bas (≈ 9 %).
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Sources : analyses Géographie (Joséphine), Temporalité (Suz) et Type de crime "
    "& Victimes (Ludivine) — dataset LAPD, période 2020-2023 (2024-2025 exclues, "
    "incomplètes)."
)