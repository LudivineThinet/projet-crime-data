import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter


# ======================================================================
# TRADUCTIONS (constantes)
# ======================================================================

TRADUCTION_CRIMES = {
    "VEHICLE - STOLEN": "Vol de véhicule",
    "BATTERY - SIMPLE ASSAULT": "Coups et blessures simples",
    "BURGLARY FROM VEHICLE": "Vol dans un véhicule",
    "THEFT OF IDENTITY": "Usurpation d'identité",
    "VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)": "Vandalisme grave (400$ et +)",
    "BURGLARY": "Cambriolage",
    "THEFT PLAIN - PETTY ($950 & UNDER)": "Vol simple (moins de 950$)",
    "ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT": "Agression avec arme",
    "INTIMATE PARTNER - SIMPLE ASSAULT": "Violence conjugale simple",
    "THEFT FROM MOTOR VEHICLE - PETTY ($950 & UNDER)": "Vol dans véhicule (moins de 950$)"
}

TRADUCTION_STATUTS = {
    "Invest Cont": "Enquête en cours",
    "Adult Other": "Autre issue (adulte)",
    "Adult Arrest": "Arrestation (adulte)",
    "Juv Arrest": "Arrestation (mineur)",
    "Juv Other": "Autre issue (mineur)",
    "UNK": "Inconnu"
}

TRADUCTION_ARMES = {
    "STRONG-ARM (HANDS, FIST, FEET OR BODILY FORCE)": "Force physique (mains, poings, pieds)",
    "UNKNOWN WEAPON/OTHER WEAPON": "Arme inconnue/autre",
    "VERBAL THREAT": "Menace verbale",
    "HAND GUN": "Arme de poing",
    "SEMI-AUTOMATIC PISTOL": "Pistolet semi-automatique",
    "KNIFE WITH BLADE 6INCHES OR LESS": "Couteau (lame ≤ 15cm)",
    "UNKNOWN FIREARM": "Arme à feu inconnue",
    "OTHER KNIFE": "Autre couteau",
    "MACE/PEPPER SPRAY": "Spray au poivre",
    "VEHICLE": "Véhicule"
}

TRADUCTION_CRIMES_ARMES = {
    "BATTERY - SIMPLE ASSAULT": "Coups et blessures simples",
    "ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT": "Agression avec arme",
    "INTIMATE PARTNER - SIMPLE ASSAULT": "Violence conjugale simple",
    "ROBBERY": "Vol qualifié",
    "CRIMINAL THREATS - NO WEAPON DISPLAYED": "Menaces (sans arme visible)",
    "BRANDISH WEAPON": "Exhibition d'arme",
    "INTIMATE PARTNER - AGGRAVATED ASSAULT": "Violence conjugale aggravée",
    "BURGLARY": "Cambriolage",
    "VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)": "Vandalisme grave (400$ et +)",
    "ATTEMPTED ROBBERY": "Tentative de vol qualifié",
    "OTHER ASSAULT": "Autre agression",
    "BATTERY WITH SEXUAL CONTACT": "Agression sexuelle avec contact",
    "RAPE, FORCIBLE": "Viol",
    "CHILD ABUSE (PHYSICAL) - SIMPLE ASSAULT": "Maltraitance infantile (physique) simple",
    "BURGLARY FROM VEHICLE": "Vol dans un véhicule"
}

TRADUCTION_MOCODES = {
    "1822": "Suspect inconnu de la victime",
    "0344": "Vol des biens de la victime",
    "0913": "Victime connaissait le suspect",
    "0329": "Vandalisme",
    "0416": "Coup(s) porté(s) avec une arme",
    "1300": "Véhicule impliqué",
    "0400": "Usage de la force",
    "2000": "Violence conjugale",
    "1402": "Preuves enregistrées",
    "2004": "Suspect sans domicile fixe"
}

ORDRE_ORIGINES_DEFAUT = ["Autre", "Blanc", "Hispanique", "Noir", "Asiatique", "Origines minoritaires", "Non renseignée"]
MAPPING_ORIGINE = {"H": "Hispanique", "W": "Blanc", "B": "Noir", "A": "Asiatique", "O": "Autre", "X": "Non renseignée"}


def separateur():
    st.markdown("<div style='margin-top: 60px; margin-bottom: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("---")


# ======================================================================
# CALCULS LOURDS, MIS EN CACHE
# (paramètres préfixés _ pour éviter le hash coûteux des gros dataframes)
# ======================================================================

@st.cache_data
def calculer_crimes_dominants(_df_clean):
    crimes_array = _df_clean["crime_principal"].to_numpy()
    types_crimes, counts = np.unique(crimes_array, return_counts=True)
    tri_index = np.argsort(counts)[::-1]
    types_crimes_tries = types_crimes[tri_index]
    counts_tries = counts[tri_index]

    top10_crimes = types_crimes_tries[:10]
    top10_crimes_fr = [TRADUCTION_CRIMES[c] for c in top10_crimes]
    top10_counts = counts_tries[:10]
    total_crimes = counts_tries.sum()
    part_crime_1 = (counts_tries[0] / total_crimes) * 100

    mask_top10 = _df_clean["crime_principal"].isin(top10_crimes)
    df_top10 = _df_clean[mask_top10]
    zones_uniques = _df_clean["nom_zone"].unique()
    zones_array = df_top10["nom_zone"].to_numpy()
    crimes_array_top10 = df_top10["crime_principal"].to_numpy()

    matrice = np.zeros((len(zones_uniques), 10))
    for i, zone in enumerate(zones_uniques):
        for j, crime in enumerate(top10_crimes):
            matrice[i, j] = np.sum((zones_array == zone) & (crimes_array_top10 == crime))

    return top10_crimes, top10_crimes_fr, top10_counts, part_crime_1, matrice, zones_uniques


@st.cache_data
def calculer_profil_victimes(_df_clean):
    mask_victimes_completes = (
        _df_clean["age_victime"].notna()
        & _df_clean["sexe_victime"].notna()
        & _df_clean["origine_victime"].notna()
    )
    df_victimes = _df_clean.loc[
        mask_victimes_completes,
        ["id_dossier", "age_victime", "sexe_victime", "origine_victime", "crime_principal"]
    ].copy()
    df_victimes["age_victime"] = df_victimes["age_victime"].astype(int)
    df_victimes["origine_categorisee"] = (
        df_victimes["origine_victime"].map(MAPPING_ORIGINE).fillna("Origines minoritaires")
    )

    mask_sexe = df_victimes["sexe_victime"].isin(["M", "F"])
    df_violin = df_victimes[mask_sexe]
    effectifs_sexe = df_violin.groupby(["origine_categorisee", "sexe_victime"])["age_victime"].count()

    # Ordre décroissant : le plus de victimes à gauche
    totaux_par_origine = {
        o: effectifs_sexe.get((o, "F"), 0) + effectifs_sexe.get((o, "M"), 0)
        for o in ORDRE_ORIGINES_DEFAUT
    }
    ordre_decroissant = sorted(totaux_par_origine, key=lambda o: totaux_par_origine[o], reverse=True)

    return df_violin, effectifs_sexe, ordre_decroissant


@st.cache_data
def calculer_gravite(_df_clean):
    gravite_array = _df_clean["categorie_gravite"].to_numpy()
    valeurs, comptages = np.unique(gravite_array, return_counts=True)
    part_graves = (comptages[valeurs == 1][0] / comptages.sum()) * 100

    annees_array = _df_clean["date_survenue"].dt.year.to_numpy()
    annees_uniques = np.unique(annees_array)
    nb_graves_par_annee = np.array([(gravite_array[annees_array == a] == 1).sum() for a in annees_uniques])
    nb_mineurs_par_annee = np.array([(gravite_array[annees_array == a] == 2).sum() for a in annees_uniques])

    return part_graves, annees_uniques, nb_graves_par_annee, nb_mineurs_par_annee


@st.cache_data
def calculer_statuts(_df_clean):
    statuts_array = _df_clean["description_statut"].to_numpy()
    statuts_uniques, comptages_statuts = np.unique(statuts_array, return_counts=True)
    tri_statuts = np.argsort(comptages_statuts)[::-1]
    statuts_tries_fr = [TRADUCTION_STATUTS[s] for s in statuts_uniques[tri_statuts]]
    comptages_statuts_tries = comptages_statuts[tri_statuts]

    total_dossiers = comptages_statuts_tries.sum()
    n_enquete = comptages_statuts_tries[statuts_tries_fr.index("Enquête en cours")]
    n_clos = total_dossiers - n_enquete
    n_arrest_adulte = comptages_statuts_tries[statuts_tries_fr.index("Arrestation (adulte)")]
    n_autre_adulte = comptages_statuts_tries[statuts_tries_fr.index("Autre issue (adulte)")]
    n_arrest_mineur = comptages_statuts_tries[statuts_tries_fr.index("Arrestation (mineur)")]
    n_autre_mineur = comptages_statuts_tries[statuts_tries_fr.index("Autre issue (mineur)")]

    return n_enquete, n_clos, n_arrest_adulte, n_autre_adulte, n_arrest_mineur, n_autre_mineur


@st.cache_data
def calculer_armes(_df_clean):
    armes_array = _df_clean["type_arme"].dropna().to_numpy()
    armes_uniques, comptages_armes = np.unique(armes_array, return_counts=True)
    tri_armes = np.argsort(comptages_armes)[::-1]
    armes_triees = armes_uniques[tri_armes]
    comptages_armes_tries = comptages_armes[tri_armes]

    top10_armes = armes_triees[:10]
    top10_comptages_armes = comptages_armes_tries[:10]
    top10_armes_fr = [TRADUCTION_ARMES[a] for a in top10_armes]

    return top10_armes, top10_armes_fr, top10_comptages_armes


@st.cache_data
def calculer_sankey_armes(_df_clean, top10_armes, top10_armes_fr):
    df_avec_arme = _df_clean[_df_clean["type_arme"].notna()]
    crimes_avec_arme_array = df_avec_arme["crime_principal"].to_numpy()
    types_crimes_arme, counts_crimes_arme = np.unique(crimes_avec_arme_array, return_counts=True)
    top15_crimes_armes = types_crimes_arme[np.argsort(counts_crimes_arme)[::-1]][:15]
    top15_crimes_armes_fr = [TRADUCTION_CRIMES_ARMES[c] for c in top15_crimes_armes]

    noeuds = top15_crimes_armes_fr + top10_armes_fr
    index_crimes = {crime: i for i, crime in enumerate(top15_crimes_armes_fr)}
    index_armes = {arme: i + len(top15_crimes_armes_fr) for i, arme in enumerate(top10_armes_fr)}

    mask_sankey = _df_clean["crime_principal"].isin(top15_crimes_armes) & _df_clean["type_arme"].isin(top10_armes)
    df_sankey = _df_clean[mask_sankey]
    crimes_arr = df_sankey["crime_principal"].to_numpy()
    armes_arr = df_sankey["type_arme"].to_numpy()

    sources, cibles, valeurs = [], [], []
    for i, crime in enumerate(top15_crimes_armes):
        for j, arme in enumerate(top10_armes):
            n = np.sum((crimes_arr == crime) & (armes_arr == arme))
            if n > 0:
                sources.append(index_crimes[top15_crimes_armes_fr[i]])
                cibles.append(index_armes[top10_armes_fr[j]])
                valeurs.append(n)

    tri_flux = np.argsort(valeurs)[::-1]
    s_top, c_top, v_top = [], [], []
    for i in tri_flux:
        if not (noeuds[sources[i]] == "Menaces (sans arme visible)" and noeuds[cibles[i]] == "Menace verbale"):
            s_top.append(sources[i]); c_top.append(cibles[i]); v_top.append(valeurs[i])
        if len(s_top) == 10:
            break

    noeuds_utilises = sorted(set(s_top) | set(c_top))
    reindex = {a: n for n, a in enumerate(noeuds_utilises)}
    s_final = [reindex[s] for s in s_top]
    c_final = [reindex[c] for c in c_top]
    noeuds_final = [noeuds[i] for i in noeuds_utilises]

    crimes_utilises = [i for i in noeuds_utilises if i < len(top15_crimes_armes_fr)]
    palette_pastel = ["#6FA8DC", "#F6B26B", "#93C47D", "#E06666", "#8E7CC3", "#76A5AF"]
    couleur_crime_ancien_index = {c: palette_pastel[i % len(palette_pastel)] for i, c in enumerate(crimes_utilises)}
    couleur_crime = {reindex[k]: v for k, v in couleur_crime_ancien_index.items()}
    couleurs_noeuds = [couleur_crime[i] if i in couleur_crime else "#D9D9D9" for i in range(len(noeuds_final))]
    couleurs_liens = [couleur_crime[s] for s in s_final]

    return s_final, c_final, v_top, noeuds_final, couleurs_noeuds, couleurs_liens


@st.cache_data
def calculer_mocodes(_df_clean, _df_mocodes):
    mocodes_array = _df_mocodes["Mocodes"].to_numpy()
    mocodes_uniques, comptages_mocodes = np.unique(mocodes_array, return_counts=True)
    tri_mocodes = np.argsort(comptages_mocodes)[::-1]
    mocodes_tries = mocodes_uniques[tri_mocodes]
    comptages_mocodes_tries = comptages_mocodes[tri_mocodes]

    top10_mocodes = mocodes_tries[:10]
    top10_comptages_mocodes = comptages_mocodes_tries[:10]
    top10_mocodes_fr = [TRADUCTION_MOCODES[m] for m in top10_mocodes]

    return top10_mocodes, top10_mocodes_fr, top10_comptages_mocodes


@st.cache_data
def calculer_cooccurrence_mocodes(_df_mocodes, top10_mocodes, top10_mocodes_fr):
    """Matrice de coocurrence : combien de dossiers partagent chaque paire de mocodes (diagonale exclue).

    Version optimisée mémoire : on filtre d'abord sur le top 10 (au lieu de
    combiner tous les mocodes de tous les dossiers, ~5,5M paires en mémoire
    en même temps que le compteur -> dépassement de RAM sur Streamlit Cloud).
    """
    top10_set = set(top10_mocodes)
    df_filtre = _df_mocodes[_df_mocodes["Mocodes"].isin(top10_set)]
    mocodes_par_dossier = df_filtre.groupby("DR_NO")["Mocodes"].apply(list)

    compteur_paires = Counter()
    for liste_mocodes in mocodes_par_dossier:
        codes_uniques = sorted(set(liste_mocodes))
        if len(codes_uniques) >= 2:
            compteur_paires.update(combinations(codes_uniques, 2))

    n = len(top10_mocodes)
    xs, ys, tailles, textes = [], [], [], []
    for i in range(n):
        for j in range(n):
            if j >= i:
                continue  # ne garde qu'un seul triangle (l'autre moitié), chaque paire une seule fois
            paire = tuple(sorted([top10_mocodes[i], top10_mocodes[j]]))
            valeur = compteur_paires.get(paire, 0)
            if valeur > 0:
                xs.append(top10_mocodes_fr[j])
                ys.append(top10_mocodes_fr[i])
                tailles.append(valeur)
                textes.append(f"{top10_mocodes_fr[i]} + {top10_mocodes_fr[j]} : {valeur} dossiers")

    return xs, ys, tailles, textes


# ======================================================================
# AFFICHAGE — STORYTELLING
# ======================================================================

def afficher(df_clean, df_mocodes, mo_codes_dict):

    # ---------------- Section 1 : les crimes qui dominent ----------------
    st.markdown("## Quels crimes touchent le plus Los Angeles ?")
    top10_crimes, top10_crimes_fr, top10_counts, part_crime_1, matrice, zones_uniques = calculer_crimes_dominants(df_clean)

    st.markdown(
        f"Sur la période 2020-2023, **{top10_crimes_fr[0]}** est de loin le crime le plus fréquent, "
        f"représentant à lui seul **{part_crime_1:.1f}%** de l'ensemble des crimes enregistrés."
    )

    col1, col2 = st.columns(2)
    col1.metric("Crime le plus fréquent", top10_crimes_fr[0])
    col2.metric("Part sur le total", f"{part_crime_1:.2f}%")

    fig_treemap = px.treemap(
        names=top10_crimes_fr, parents=[""] * 10, values=top10_counts,
        title="Top 10 des types de crimes les plus fréquents",
        color=top10_counts, color_continuous_scale="Reds", hover_name=top10_crimes
    )
    fig_treemap.update_layout(template="plotly_white")
    st.plotly_chart(fig_treemap, use_container_width=True)

    st.markdown("Mais la répartition de ces crimes n'est pas uniforme selon les zones de la ville :")

    fig_heatmap = px.imshow(
        matrice.T, x=zones_uniques, y=top10_crimes_fr,
        color_continuous_scale="Reds",
        labels=dict(x="Zone", y="Type de crime", color="Nombre de crimes"),
        title="Répartition des crimes du top 10 par zone"
    )
    fig_heatmap.update_layout(width=1400, height=650)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    separateur()

    # ---------------- Section 2 : qui sont les victimes ----------------
    st.markdown("## Qui sont les victimes ?")
    st.markdown(
        "En croisant l'âge, le sexe et l'origine déclarée des victimes, un profil démographique se dessine, "
        "avec des variations selon les communautés."
    )

    df_violin, effectifs_sexe, ordre_decroissant = calculer_profil_victimes(df_clean)

    plt.figure(figsize=(16, 8))
    sns.violinplot(
        data=df_violin, x="origine_categorisee", y="age_victime", hue="sexe_victime",
        split=True, inner=None, order=ordre_decroissant,
        palette={"F": "#E45756", "M": "#4C78A8"}
    )
    plt.title("Distribution de l'âge des victimes par origine et sexe (du plus au moins représenté)")
    plt.xlabel("Origine")
    plt.ylabel("Âge de la victime")
    plt.legend(loc="upper left", bbox_to_anchor=(1.02, 1), title="Sexe")

    for x, origine in enumerate(ordre_decroissant):
        n_f = effectifs_sexe.get((origine, "F"), 0)
        n_m = effectifs_sexe.get((origine, "M"), 0)
        plt.text(x, -11, f"{n_f + n_m}", ha="center", fontsize=11, color="black")
        plt.text(x, -15, f"F: {n_f}", ha="center", fontsize=10, color="#E45756")
        plt.text(x, -19, f"M: {n_m}", ha="center", fontsize=10, color="#4C78A8")

    plt.ylim(bottom=-25)
    plt.subplots_adjust(bottom=0.2)
    st.pyplot(plt.gcf())
    plt.clf()

    separateur()

    # ---------------- Section 3 : gravité et évolution ----------------
    st.markdown("## La criminalité s'aggrave-t-elle ?")

    part_graves, annees_uniques, nb_graves_par_annee, nb_mineurs_par_annee = calculer_gravite(df_clean)

    st.markdown(
        f"Près de **{part_graves:.0f}%** des crimes enregistrés à Los Angeles sont classés comme graves "
        f"(catégorie « Part 1 » du FBI)."
    )

    col_don1, col_don2, col_don3 = st.columns([0.5, 2, 0.5])
    with col_don2:
        fig_donut = go.Figure(go.Pie(
            labels=["Crimes graves", "Crimes mineurs"],
            values=[part_graves, 100 - part_graves],
            hole=0.55,
            marker_colors=["#B98080", "#7FA6C9"]
        ))
        fig_donut.update_traces(
            textinfo="percent",
            textfont=dict(size=20, color="white"),
            insidetextorientation="horizontal"
        )
        fig_donut.update_layout(
            title="Répartition graves / mineurs", width=650, height=550,
            showlegend=True, legend=dict(orientation="v", x=1, y=0.5, font=dict(size=14)),
            template="plotly_white"
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("Et cette part progresse d'année en année :")

    fig_lignes = px.line(
        x=annees_uniques, y=[nb_graves_par_annee, nb_mineurs_par_annee], markers=True,
        labels=dict(x="Année", value="Nombre de crimes", variable="Catégorie")
    )
    fig_lignes.data[0].name = "Crimes graves (Part 1)"
    fig_lignes.data[1].name = "Crimes mineurs (Part 2)"
    fig_lignes.update_xaxes(tickmode="array", tickvals=annees_uniques, ticktext=[str(a) for a in annees_uniques])
    fig_lignes.update_layout(
        width=1000, height=600, template="plotly_white",
        title="Évolution du nombre de crimes graves et mineurs (2020-2023)"
    )
    st.plotly_chart(fig_lignes, use_container_width=True)

    separateur()

    # ---------------- Section 4 : que deviennent les dossiers ----------------
    st.markdown("## Que deviennent les dossiers une fois signalés ?")

    n_enquete, n_clos, n_arrest_adulte, n_autre_adulte, n_arrest_mineur, n_autre_mineur = calculer_statuts(df_clean)

    total_adultes = n_arrest_adulte + n_autre_adulte
    total_mineurs = n_arrest_mineur + n_autre_mineur
    pct_adultes_clos = total_adultes / (total_adultes + total_mineurs) * 100
    pct_mineurs_clos = total_mineurs / (total_adultes + total_mineurs) * 100

    st.markdown(
        "Une grande partie des dossiers reste encore en cours d'investigation. Parmi ceux qui ont "
        "abouti, le sort réservé aux adultes et aux mineurs mérite d'être regardé séparément."
    )

    col_gauche, col_droite = st.columns([2, 1])

    with col_gauche:
        fig_global = go.Figure(go.Pie(
            labels=["Enquête en cours", "Dossiers clôturés"],
            values=[n_enquete, n_clos],
            hole=0.4,
            marker_colors=["#2E7D32", "#A5D6A7"]
        ))
        fig_global.update_traces(textinfo="percent+value", textfont=dict(color="white"))
        fig_global.update_layout(
            title="Statut global des dossiers", height=500, template="plotly_white",
            legend=dict(orientation="h", y=-0.1)
        )
        st.plotly_chart(fig_global, use_container_width=True)

    with col_droite:
        fig_adultes = go.Figure(go.Pie(
            labels=["Arrestation", "Autre issue"], values=[n_arrest_adulte, n_autre_adulte],
            marker_colors=["#1F3B73", "#A9C6E8"]
        ))
        fig_adultes.update_traces(textinfo="percent")
        fig_adultes.update_layout(title="Adultes", height=200, template="plotly_white", margin=dict(t=40, b=10))
        st.plotly_chart(fig_adultes, use_container_width=True)
        st.caption(f"{pct_adultes_clos:.1f}% des dossiers clôturés")

        fig_mineurs = go.Figure(go.Pie(
            labels=["Arrestation", "Autre issue"], values=[n_arrest_mineur, n_autre_mineur],
            marker_colors=["#1F3B73", "#A9C6E8"]
        ))
        fig_mineurs.update_traces(textinfo="percent")
        fig_mineurs.update_layout(title="Mineurs", height=200, template="plotly_white", margin=dict(t=40, b=10))
        st.plotly_chart(fig_mineurs, use_container_width=True)
        st.caption(f"{pct_mineurs_clos:.1f}% des dossiers clôturés")

    separateur()

    # ---------------- Section 5 : les armes utilisées ----------------
    st.markdown("## Quelles armes sont utilisées ?")

    top10_armes, top10_armes_fr, top10_comptages_armes = calculer_armes(df_clean)

    st.markdown(
        f"Contrairement à une idée reçue, **{top10_armes_fr[0].lower()}** est de loin le moyen le plus utilisé "
        f"dans les crimes impliquant une arme, bien avant les armes à feu."
    )

    fig_armes = go.Figure()
    fig_armes.add_trace(go.Scatter(
        x=top10_comptages_armes, y=top10_armes_fr,
        mode="markers", marker=dict(size=14, color="#1F3B73")
    ))
    for arme, compte in zip(top10_armes_fr, top10_comptages_armes):
        fig_armes.add_shape(type="line", x0=0, x1=compte, y0=arme, y1=arme, line=dict(color="#A9C6E8", width=3))
    fig_armes.update_layout(
        title="Top 10 des armes utilisées",
        xaxis_title="Nombre de crimes", yaxis_title="Type d'arme",
        yaxis=dict(categoryorder="total ascending"),
        width=1000, height=600, template="plotly_white"
    )
    st.plotly_chart(fig_armes, use_container_width=True)

    st.markdown("Certaines armes sont aussi fortement associées à des types de crimes précis :")

    s_final, c_final, v_top, noeuds_final, couleurs_noeuds, couleurs_liens = calculer_sankey_armes(
        df_clean, top10_armes, top10_armes_fr
    )

    fig_sankey_final = go.Figure(go.Sankey(
        node=dict(
            pad=20, thickness=20, line=dict(color="black", width=0.5),
            label=noeuds_final, color=couleurs_noeuds
        ),
        link=dict(source=s_final, target=c_final, value=v_top, color=couleurs_liens),
        textfont=dict(color="#1A1A1A", size=13)
    ))
    fig_sankey_final.update_layout(
        title="Les associations crime-arme les plus fréquentes",
        width=1100, height=650
    )
    st.plotly_chart(fig_sankey_final, use_container_width=True)

    separateur()

    # ---------------- Section 6 : les circonstances (mocodes) ----------------
    st.markdown("## Dans quelles circonstances ces crimes se produisent-ils ?")

    st.markdown(
        "Chaque rapport de police du LAPD peut être accompagné d'un ou plusieurs **codes de circonstances** "
        "(*mocodes*, pour *modus operandi codes*). Ce ne sont pas des types de crime, mais des détails sur "
        "la manière dont les faits se sont déroulés : le suspect était-il un inconnu ? une arme a-t-elle été "
        "brandie ? la victime connaissait-elle son agresseur ? Un même dossier peut cumuler plusieurs de ces codes."
    )

    top10_mocodes, top10_mocodes_fr, top10_comptages_mocodes = calculer_mocodes(df_clean, df_mocodes)

    fig_mocodes = go.Figure()
    fig_mocodes.add_trace(go.Scatter(
        x=top10_comptages_mocodes, y=top10_mocodes_fr,
        mode="markers", marker=dict(size=14, color="#1F3B73")
    ))
    for m, compte in zip(top10_mocodes_fr, top10_comptages_mocodes):
        fig_mocodes.add_shape(type="line", x0=0, x1=compte, y0=m, y1=m, line=dict(color="#A9C6E8", width=3))
    fig_mocodes.update_layout(
        title="Les 10 circonstances les plus fréquentes",
        xaxis_title="Nombre d'occurrences", yaxis_title="Circonstance",
        yaxis=dict(categoryorder="total ascending"),
        width=1100, height=600, template="plotly_white"
    )
    st.plotly_chart(fig_mocodes, use_container_width=True)

    st.markdown("Ces circonstances ne sont pas isolées : certaines reviennent souvent ensemble sur un même dossier.")

    xs, ys, tailles, textes = calculer_cooccurrence_mocodes(df_mocodes, top10_mocodes, top10_mocodes_fr)

    fig_bubble = go.Figure(go.Scatter(
        x=xs, y=ys, mode="markers",
        marker=dict(
            size=tailles, sizemode="area",
            sizeref=2. * max(tailles) / (60. ** 2), sizemin=4,
            color="#1F3B73", opacity=0.7
        ),
        text=textes, hoverinfo="text"
    ))
    fig_bubble.update_layout(
        title="Circonstances qui apparaissent ensemble sur un même dossier",
        xaxis_title="Circonstance", yaxis_title="Circonstance",
        width=1300, height=900, template="plotly_white",
        xaxis=dict(tickangle=45, categoryorder="array", categoryarray=top10_mocodes_fr),
        yaxis=dict(categoryorder="array", categoryarray=top10_mocodes_fr)
    )
    st.plotly_chart(fig_bubble, use_container_width=True)