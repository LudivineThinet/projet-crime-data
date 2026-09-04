import streamlit as st
import pandas as pd

from modules import geographie, temporel, victimes_typologie

st.set_page_config(page_title="Analyse - Criminalité LA", layout="wide")

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

    button[data-baseweb="tab"] {
        font-size: 1.05rem;
        font-weight: 600;
        padding: 0.6rem 1.4rem;
        color: #555;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #1F3B73 !important;
        border-bottom: 3px solid #1F3B73 !important;
    }
    button[data-baseweb="tab"]:hover {
        color: #1F3B73 !important;
        background-color: #F0F4FA;
    }
    button[data-baseweb="tab"] p {
        font-size: 1.05rem;
        font-weight: 600;
    }
    [data-baseweb="tab-highlight"] {
        background-color: #1F3B73 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def charger_donnees():
    """Charge et prépare les données une seule fois (mise en cache Streamlit)."""
    df_clean = pd.read_csv("data/df_clean.csv")
    df_mocodes = pd.read_csv("data/df_mocodes.csv")
    mo_codes_df = pd.read_csv("data/mo_codes.csv", dtype={"mocode": str})

    df_clean["date_survenue"] = pd.to_datetime(df_clean["date_survenue"])
    df_clean["date_signalement"] = pd.to_datetime(df_clean["date_signalement"])
    df_mocodes["Mocodes"] = df_mocodes["Mocodes"].astype(str).str.zfill(4)
    df_clean = df_clean[df_clean["date_survenue"].dt.year.isin([2020, 2021, 2022, 2023])]

    mo_codes_dict = dict(zip(mo_codes_df["mocode"], mo_codes_df["description_mocode"]))
    df_mocodes["description_mocode"] = df_mocodes["Mocodes"].map(mo_codes_dict)

    return df_clean, df_mocodes, mo_codes_dict


df_clean, df_mocodes, mo_codes_dict = charger_donnees()

st.title("Analyse de la criminalité à Los Angeles (2020-2023)")

onglet_geo, onglet_temporel, onglet_victimes = st.tabs([
    "🗺️ Géographie",
    "📅 Temporel",
    "🔎 Type de crime & Victimes"
])

with onglet_geo:
    geographie.afficher()

with onglet_temporel:
    temporel.afficher(df_clean)

with onglet_victimes:
    victimes_typologie.afficher(df_clean, df_mocodes, mo_codes_dict)