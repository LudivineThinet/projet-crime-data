"""
BLOC 1 — GÉOGRAPHIE
Module Streamlit pour l'analyse géographique de la criminalité (Joséphine).

Les CSV pré-agrégés doivent se trouver dans data/ (au même
niveau que le reste de data/, à la racine du projet).
"""

import folium
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# Couleurs harmonisées avec le notebook et le document Word
ROUGE = "#d9534f"
BLEU_NUIT = "#2c3e50"
BLEU_GRIS = "#7f8c8d"
BLEU_ORIGINE = "#1f77b4"
ORANGE = "#eb6834"
VERT = "#0ca30c"


@st.cache_data
def charger_donnees_geo():
    crimes_by_zone = pd.read_csv("data/crimes_by_zone.csv")
    zone_evolution = pd.read_csv("data/zone_evolution.csv")
    crimes_by_secteur = pd.read_csv("data/crimes_by_secteur.csv")
    crimes_by_position = pd.read_csv("data/crimes_by_position.csv")
    top10_hotspots = pd.read_csv("data/top10_hotspots.csv")
    return crimes_by_zone, zone_evolution, crimes_by_secteur, crimes_by_position, top10_hotspots


def afficher(df_clean=None):
    """Onglet Géographie (Joséphine). df_clean n'est pas utilisé ici : ce
    bloc travaille sur ses propres CSV pré-agrégés (data/)."""

    crimes_by_zone, zone_evolution, crimes_by_secteur, crimes_by_position, top10_hotspots = charger_donnees_geo()

    # ============================================================
    # En-tête de section
    # ============================================================
    st.header("📍 Géographie de la criminalité")
    st.caption("Analyse de la criminalité à Los Angeles — LAPD 2020-2025 · Joséphine")
    st.markdown(
        "**Décision pour l'élu :** où concentrer le budget (patrouilles, éclairage, "
        "prévention) entre les 21 zones, et où les résultats des investissements "
        "passés sont visibles ou non."
    )
    st.divider()

    # ============================================================
    # Q1 — Quelles zones concentrent le plus de crimes ?
    # ============================================================
    st.subheader("Q1 — Quelles zones concentrent le plus de crimes ?")

    total_crimes = int(crimes_by_zone["nombre_crimes"].sum())
    zone_1 = crimes_by_zone.iloc[0]
    top3_pct = crimes_by_zone.iloc[2]["part_cumulee_pct"]
    top5_pct = crimes_by_zone.iloc[4]["part_cumulee_pct"]
    top10_noms = crimes_by_zone.head(10)["nom_zone"].tolist()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de crimes", f"{total_crimes:,}".replace(",", " "))
    col2.metric("Zone n°1", zone_1["nom_zone"], f"{zone_1['part_pct']} %")
    col3.metric("Cumul Top 3 zones", f"{top3_pct} %")
    col4.metric("Cumul Top 5 zones", f"{top5_pct} %")

    tab_vol, tab_part, tab_pareto, tab_top, tab_donut = st.tabs(
        ["Volume par zone", "Part de chaque zone", "Diagramme de Pareto", "Top 3 vs Top 5", "Zone n°1"]
    )

    with tab_vol:
        df_sorted = crimes_by_zone.sort_values("nombre_crimes", ascending=True)
        couleurs = [ROUGE if z == "Central" else BLEU_NUIT if z in top10_noms else BLEU_GRIS for z in df_sorted["nom_zone"]]
        fig, ax = plt.subplots(figsize=(6.75, 5.25))
        ax.barh(df_sorted["nom_zone"], df_sorted["nombre_crimes"], color=couleurs)
        ax.set_xlabel("Nombre de crimes")
        ax.set_title("Volume de crimes par zone")
        st.pyplot(fig)

    with tab_part:
        df_sorted = crimes_by_zone.sort_values("part_pct", ascending=True)
        couleurs = [ROUGE if z == "Central" else BLEU_NUIT if z in top10_noms else BLEU_GRIS for z in df_sorted["nom_zone"]]
        fig, ax = plt.subplots(figsize=(6.75, 5.25))
        ax.barh(df_sorted["nom_zone"], df_sorted["part_pct"], color=couleurs)
        min_val, max_val = df_sorted["part_pct"].min(), df_sorted["part_pct"].max()
        ax.axvline(x=min_val, color=BLEU_GRIS, linestyle="--", linewidth=1)
        ax.axvline(x=max_val, color=ROUGE, linestyle="--", linewidth=1)
        ax.set_xlabel("Part du total (%)")
        ax.set_title(f"Part de chaque zone dans le total (Amplitude : {min_val:.2f} % à {max_val:.2f} %)")
        st.pyplot(fig)

    with tab_pareto:
        df_sorted = crimes_by_zone.sort_values("nombre_crimes", ascending=False).reset_index(drop=True)
        fig, ax1 = plt.subplots(figsize=(9, 4.5))
        couleurs = [ROUGE if z == "Central" else BLEU_NUIT if z in top10_noms[:5] else BLEU_ORIGINE for z in df_sorted["nom_zone"]]
        ax1.bar(df_sorted["nom_zone"], df_sorted["nombre_crimes"], color=couleurs, alpha=0.85)
        ax1.set_ylabel("Nombre de crimes", color=BLEU_ORIGINE)
        ax1.tick_params(axis="x", rotation=45, labelsize=8)
        ax2 = ax1.twinx()
        ax2.plot(df_sorted["nom_zone"], df_sorted["part_cumulee_pct"], color="red", marker="o", linewidth=2, markersize=5)
        ax2.set_ylabel("Part cumulée (%)", color="red")
        ax2.set_ylim(0, 105)
        ax2.axhline(y=top5_pct, color="orange", linestyle="--", linewidth=1)
        plt.title("Diagramme de Pareto — Concentration des crimes par zone")
        plt.tight_layout()
        st.pyplot(fig)

    with tab_top:
        fig, ax = plt.subplots(figsize=(4.5, 3.75))
        couleurs = [BLEU_NUIT, ROUGE]
        bars = ax.bar(["Top 3 zones", "Top 5 zones"], [top3_pct, top5_pct], color=couleurs, width=0.45)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 1, f"{h:.2f} %", ha="center", fontweight="bold")
        ax.set_ylabel("Part du total (%)")
        ax.set_title("Concentration de la criminalité dans les principales zones")
        ax.set_ylim(0, top5_pct * 1.25)
        st.pyplot(fig)

    with tab_donut:
        part_central = zone_1["part_pct"]
        part_reste = round(100 - part_central, 2)
        fig, ax = plt.subplots(figsize=(3.75, 3.75))
        ax.pie(
            [part_central, part_reste], autopct="%1.2f%%", pctdistance=0.82, startangle=90,
            colors=[ROUGE, BLEU_NUIT], wedgeprops=dict(width=0.35, edgecolor="white", linewidth=2),
        )
        ax.legend([f"Central ({part_central} %)", f"Autres zones ({part_reste} %)"], loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
        ax.set_title("Poids de la zone n°1 (Central) dans la criminalité totale")
        st.pyplot(fig)

    with st.expander("Voir le tableau complet des 21 zones"):
        st.dataframe(crimes_by_zone, use_container_width=True, hide_index=True)

    st.info(
        f"**Constat :** {zone_1['nom_zone']} concentre {zone_1['part_pct']} % des crimes "
        f"— la zone n°1, avec près du double de la part moyenne. Le Top 5 des zones "
        f"représente {top5_pct} % du total."
    )

    st.divider()

    # ============================================================
    # Q2 — Quelles zones se dégradent ou s'améliorent dans le temps ?
    # ============================================================
    st.subheader("Q2 — Quelles zones se dégradent ou s'améliorent dans le temps ?")
    st.caption("Comparaison 2021 → 2023 — années complètes uniquement")

    with st.expander("ℹ️ Pourquoi 2021-2023 et pas 2021-2024 ?"):
        st.write(
            "2024 est incomplète dans ce dataset : le nombre de dossiers enregistrés "
            "chute progressivement à partir d'avril (délai d'enregistrement), et non "
            "parce que la criminalité baisse réellement. Comparer 2021 à 2024 brut "
            "ferait apparaître une fausse baisse sur les 21 zones. L'analyse porte donc "
            "sur les 4 années complètes du dataset : 2020, 2021, 2022 et 2023."
        )

    zone_degradation = zone_evolution.loc[zone_evolution["variation_2020_2023_pct"].idxmax()]
    zone_moins_degradee = zone_evolution.loc[zone_evolution["variation_2020_2023_pct"].idxmin()]
    zones_alerte = zone_evolution[zone_evolution["variation_2020_2023_pct"] > 15].sort_values(
        "variation_2020_2023_pct", ascending=False
    )
    aucune_amelioration = (zone_evolution["variation_2020_2023_pct"] > 0).all()

    col1, col2, col3 = st.columns(3)
    col1.metric("Se dégrade le plus", zone_degradation["nom_zone"], f"+{zone_degradation['variation_2020_2023_pct']:.1f} %", delta_color="inverse")
    col2.metric("Zone la moins dégradée", zone_moins_degradee["nom_zone"], f"+{zone_moins_degradee['variation_2020_2023_pct']:.1f} %", delta_color="inverse")
    col3.metric("Zones en alerte (> +15 %)", f"{len(zones_alerte)} / 21")

    if aucune_amelioration:
        st.warning(
            "**Aucune zone ne s'améliore réellement sur 2020-2023** : les 21 zones affichent "
            "toutes une hausse, de +0,75 % (Foothill, la plus stable) à "
            f"+{zone_degradation['variation_2020_2023_pct']:.1f} % ({zone_degradation['nom_zone']})."
        )

    tab_evo, tab_traj, tab_annuel, tab_alerte = st.tabs(
        ["Évolution 2020→2023", "Trajectoire", "Évolution annuelle (5 zones)", "Zones en alerte"]
    )

    with tab_evo:
        df_sorted2 = zone_evolution.sort_values("variation_2020_2023_pct", ascending=True)
        couleurs2 = [ROUGE if z == zone_degradation["nom_zone"] else BLEU_NUIT if z == zone_moins_degradee["nom_zone"] else BLEU_ORIGINE for z in df_sorted2["nom_zone"]]
        fig, ax = plt.subplots(figsize=(6.75, 5.25))
        ax.barh(df_sorted2["nom_zone"], df_sorted2["variation_2020_2023_pct"], color=couleurs2)
        ax.axvline(x=15, color=ROUGE, linestyle="--", linewidth=1.2, label="Seuil d'alerte (+15 %)")
        ax.set_xlabel("Variation du nombre de crimes, 2020 → 2023 (%)")
        ax.set_title(
            f"Évolution 2020-2023 : Focus sur {zone_degradation['nom_zone']} "
            f"({zone_degradation['variation_2020_2023_pct']:+.1f} %) et "
            f"{zone_moins_degradee['nom_zone']} ({zone_moins_degradee['variation_2020_2023_pct']:+.1f} %)"
        )
        ax.legend()
        st.pyplot(fig)

    with tab_traj:
        fig, ax = plt.subplots(figsize=(6.75, 5.25))
        for _, row in zone_evolution.iterrows():
            if row["nom_zone"] == zone_degradation["nom_zone"]:
                couleur, largeur, alpha = ORANGE, 2.5, 1.0
            elif row["nom_zone"] == zone_moins_degradee["nom_zone"]:
                couleur, largeur, alpha = VERT, 2.5, 1.0
            else:
                couleur, largeur, alpha = BLEU_GRIS, 1.0, 0.4
            ax.plot([2020, 2023], [row["crimes_2020"], row["crimes_2023"]], color=couleur, linewidth=largeur, alpha=alpha, marker="o", markersize=5)
            if row["nom_zone"] in [zone_degradation["nom_zone"], zone_moins_degradee["nom_zone"]]:
                ax.text(2023.1, row["crimes_2023"], f"{row['nom_zone']} ({row['variation_2020_2023_pct']:+.1f} %)", va="center", fontsize=9, fontweight="bold", color=couleur)
        ax.set_xticks([2020, 2023])
        ax.set_xticklabels(["2020", "2023"])
        ax.set_xlim(2019.7, 2024.2)
        ax.set_ylabel("Nombre de crimes")
        ax.set_title("Trajectoire des zones entre 2020 et 2023")
        st.pyplot(fig)

    with tab_annuel:
        zones_selection = zone_evolution.sort_values("variation_2020_2023_pct", ascending=False).head(5)["nom_zone"].tolist()
        fig, ax = plt.subplots(figsize=(6.75, 4.5))
        for zone in zones_selection:
            row = zone_evolution[zone_evolution["nom_zone"] == zone]
            if row.empty:
                continue
            row = row.iloc[0]
            ax.plot([2020, 2021, 2022, 2023], [row["crimes_2020"], row["crimes_2021"], row["crimes_2022"], row["crimes_2023"]], marker="o", label=zone)
        ax.set_xticks([2020, 2021, 2022, 2023])
        ax.set_xlabel("Année")
        ax.set_ylabel("Nombre de crimes")
        ax.set_title("Évolution annuelle du nombre de crimes (Top 5 des zones qui se dégradent le plus)")
        ax.legend()
        st.pyplot(fig)

    with tab_alerte:
        alertes = zones_alerte.sort_values("variation_2020_2023_pct", ascending=True)
        couleurs3 = [ROUGE if z == zone_degradation["nom_zone"] else BLEU_ORIGINE for z in alertes["nom_zone"]]
        fig, ax = plt.subplots(figsize=(5.25, 3.75))
        ax.barh(alertes["nom_zone"], alertes["variation_2020_2023_pct"], color=couleurs3, alpha=0.85)
        ax.axvline(x=15, color=ROUGE, linestyle="--", linewidth=1.2, label="Seuil d'alerte (+15 %)")
        ax.set_xlabel("Variation 2020 → 2023 (%)")
        ax.set_title("Zones dépassant le seuil d'alerte (+15 %)")
        ax.legend()
        st.pyplot(fig)

    st.warning(
        "**Zones en alerte (variation > +15 %) :** "
        + ", ".join(f"{row['nom_zone']} ({row['variation_2020_2023_pct']:+.1f} %)" for _, row in zones_alerte.iterrows())
    )

    st.divider()

    # ============================================================
    # Q3 — Où précisément sont les points chauds ?
    # ============================================================
    st.subheader("Q3 — Où précisément sont les points chauds ?")

    col1, col2 = st.columns(2)
    col1.metric("Crimes géolocalisés", f"{int(crimes_by_position['nombre_crimes'].sum()):,}".replace(",", " "))
    col2.metric("Positions GPS uniques", f"{len(crimes_by_position):,}".replace(",", " "))

    tab_heat, tab_bulles, tab_combo = st.tabs(
        ["Carte de densité", "Top 10 points chauds", "Top 10 secteurs"]
    )

    with tab_heat:
        m_heatmap = folium.Map(location=[34.0522, -118.2437], zoom_start=10, tiles="OpenStreetMap")
        heat_data = crimes_by_position[["latitude", "longitude", "nombre_crimes"]].values.tolist()
        HeatMap(heat_data, radius=10, blur=15, max_zoom=13, gradient={0.2: "blue", 0.4: "lime", 0.6: "yellow", 1: "red"}).add_to(m_heatmap)
        st_folium(m_heatmap, width=1100, height=500)

    with tab_bulles:
        m_bubbles = folium.Map(location=[34.0522, -118.2437], zoom_start=12, tiles="OpenStreetMap")
        for _, row in top10_hotspots.iterrows():
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]], radius=row["nombre_crimes"] / 300,
                popup=f"Crimes : {row['nombre_crimes']}", tooltip=f"Crimes : {row['nombre_crimes']}",
                color=ROUGE, fill=True, fill_color=ROUGE, fill_opacity=0.6,
            ).add_to(m_bubbles)
        st_folium(m_bubbles, width=1100, height=500)
        st.dataframe(top10_hotspots, use_container_width=True, hide_index=True)

    with tab_combo:
        # Vrai classement (2020-2023), calculé depuis crimes_by_secteur.csv
        # (code_secteur, nombre_crimes, nom_zone)
        top10_reel = crimes_by_secteur.head(10).copy()
        top10_reel["code_secteur"] = top10_reel["code_secteur"].astype(str) + " (" + top10_reel["nom_zone"] + ")"
        df_top10 = top10_reel.rename(columns={"nombre_crimes": "crimes", "nom_zone": "zone"})

        # Une couleur par zone présente dans ce top 10 (palette cyclique)
        palette_zones = [ROUGE, BLEU_NUIT, BLEU_ORIGINE, ORANGE, VERT, BLEU_GRIS]
        zones_presentes = df_top10["zone"].unique().tolist()
        color_map = {z: palette_zones[i % len(palette_zones)] for i, z in enumerate(zones_presentes)}

        # Tri du plus grand (en haut) au plus petit (en bas) : ordre croissant
        # car un bar chart horizontal Plotly affiche le premier élément de la
        # liste en bas.
        df_sorted = df_top10.sort_values("crimes", ascending=True)

        fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "treemap"}]],
                             subplot_titles=("Classement par secteur", "Répartition zone → secteur"), horizontal_spacing=0.1)

        fig.add_trace(go.Bar(
            x=df_sorted["crimes"], y=df_sorted["code_secteur"], orientation="h",
            marker_color=[color_map[z] for z in df_sorted["zone"]],
            text=df_sorted["crimes"], texttemplate="%{text:,}", textposition="outside",
            cliponaxis=False, showlegend=False
        ), row=1, col=1)

        # Légende manuelle par zone (une barre fictive par couleur, invisible)
        for zone_name, couleur in color_map.items():
            if zone_name in df_top10["zone"].values:
                fig.add_trace(go.Bar(x=[None], y=[None], marker_color=couleur, name=zone_name, showlegend=True), row=1, col=1)

        fig_treemap = px.treemap(df_top10, path=["zone", "code_secteur"], values="crimes", color="zone", color_discrete_map=color_map)
        for trace in fig_treemap.data:
            fig.add_trace(trace, row=1, col=2)
        fig.update_layout(title_text="<b>Top 10 des secteurs les plus touchés</b>", title_x=0.5, height=500,
                           template="plotly_white", legend=dict(title=dict(text="<b>Zone</b>"), orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.25))
        fig.update_xaxes(title_text="<b>Nombre de crimes</b>", range=[0, df_top10["crimes"].max() * 1.18], row=1, col=1)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.caption("Sources : data/*.csv, générés depuis le notebook de Joséphine — Projet Criminalité LA.")