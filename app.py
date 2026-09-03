import streamlit as st

st.set_page_config(page_title="Analyse Criminalité Los Angeles", layout="wide")

st.title("Analyse de la criminalité à Los Angeles (2020-2023)")
st.subheader("Projet réalisé dans le cadre de la formation Data Analyst — Simplon")

st.markdown("---")

st.markdown("### Équipe")
col1, col2, col3 = st.columns(3)
col1.markdown("**Ludivine**\n\nType de crime & Victimes")
col2.markdown("**Suz**\n\nAnalyse temporelle")
col3.markdown("**Joséphine**\n\nAnalyse géographique")

st.markdown("---")

st.markdown("Utilisez le menu à gauche pour naviguer entre les différentes sections.")