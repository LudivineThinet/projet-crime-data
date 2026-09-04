"""
BLOC 2 — TEMPORALITÉ
Module Streamlit pour l'analyse temporelle de la criminalité (Suz).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


@st.cache_data
def preparer_donnees(_df_clean):
    """Ajoute les colonnes dérivées nécessaires (année, mois, jour, heure)."""
    df = _df_clean.copy()
    df["annee"] = df["date_survenue"].dt.year
    df["mois"] = df["date_survenue"].dt.month
    df["jour_num"] = df["date_survenue"].dt.dayofweek  # 0 = lundi ... 6 = dimanche
    df["heure"] = df["heure_survenue"].str[:2].astype("Int64")  # "21:30" -> 21
    return df


def espace():
    """Espace vertical entre deux graphiques."""
    st.markdown("<div style='margin-top: 2.8rem;'></div>", unsafe_allow_html=True)


def separateur():
    """Séparation nette entre les deux grandes parties du storytelling."""
    st.markdown("<div style='margin-top: 4rem; margin-bottom: 3rem;'></div>", unsafe_allow_html=True)
    st.markdown("---")


def note(texte):
    """Petite analyse sous un graphique, un peu plus grande qu'un st.caption standard."""
    st.markdown(
        f"<p style='font-size: 0.98rem; color: #555; margin-top: 0.4rem;'>{texte}</p>",
        unsafe_allow_html=True,
    )


def afficher(df_clean):
    """Onglet Temporalité (Suz), format storytelling."""
    dfc = preparer_donnees(df_clean)

    # ========================================================================
    # SECTION 1 — La criminalité augmente-t-elle depuis 2020 ?
    # ========================================================================
    st.markdown("## La criminalité augmente-t-elle depuis 2020 ?")
    st.markdown(
        "Le nombre de crimes a augmenté de **16,3 %** entre 2020 et 2023, avec un pic "
        "en 2022 puis une stabilisation. Aucune saisonnalité marquée : la charge reste "
        "constante toute l'année."
    )
    espace()

    # --- Courbe mensuelle + donut annuel ---
    annees = np.arange(2020, 2024)
    serie = dfc.groupby(dfc["date_survenue"].dt.to_period("M")).size()
    serie.index = serie.index.to_timestamp()
    par_an = dfc.groupby("annee").size()
    vals = par_an.to_numpy()
    evol = (vals[-1] / vals[0] - 1) * 100

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.125), gridspec_kw={"width_ratios": [2, 1]})

    ax1.plot(serie.index, serie.values, color="#8B1A1A", lw=2)
    ax1.plot(serie.index, serie.rolling(3, center=True).mean(), "--", color="#333", lw=1)
    ax1.axvspan(pd.Timestamp("2020-03-15"), pd.Timestamp("2020-06-15"), color="grey", alpha=.15)
    for a, v in zip(par_an.index, vals):
        ax1.text(pd.Timestamp(f"{a}-07-01"), serie.max()*1.08, f"{a}\n{v:,}".replace(",", " "),
                 ha="center", fontsize=8, fontweight="bold", color="#8B1A1A")
    ax1.set_title("Crimes par mois", fontsize=10)
    ax1.set_ylim(serie.min()*.88, serie.max()*1.18)
    ax1.spines[["top", "right"]].set_visible(False)
    ax1.grid(axis="y", alpha=.25)

    exp = np.where(vals == vals.max(), .04, 0)
    _, txt, autotxt = ax2.pie(vals, labels=par_an.index.astype(str),
        colors=["#F2C4C4", "#E67E7E", "#C0392B", "#8B1A1A"], explode=exp,
        autopct="%.0f%%", startangle=90, counterclock=False, pctdistance=.75,
        wedgeprops=dict(width=.42, edgecolor="white", lw=2))
    plt.setp(autotxt, color="white", fontweight="bold")
    plt.setp(txt, fontweight="bold")
    ax2.text(0, 0, f"{np.sum(vals)//1000}k\ncrimes", ha="center", va="center", fontsize=10, fontweight="bold")
    ax2.set_title("Poids de chaque annee", fontsize=10)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    note(
        f"Après un creux au printemps 2020 (confinement), la criminalité augmente "
        f"durablement : **+{evol:.0f} %** entre 2020 et 2023, portée par un pic en 2022."
    )
    espace()

    # --- Variation annuelle ---
    par_an = dfc.groupby("annee").size()
    annees = par_an.index.to_numpy()
    vals = par_an.to_numpy()
    variation = np.diff(vals) / vals[:-1] * 100
    labels = ["2020 -> 2021", "2021 -> 2022", "2022 -> 2023"]
    couleurs = np.where(variation > 0, "#C0392B", "#2E7D32")

    fig, ax = plt.subplots(figsize=(7.5, 3.7))
    ax.bar(labels, variation, color=couleurs, width=.5)
    ax.axhline(0, color="black", lw=1)
    for i, v in enumerate(variation):
        va = "bottom" if v > 0 else "top"
        ax.text(i, v + np.sign(v)*0.8, f"{v:+.1f} %", ha="center", va=va, fontweight="bold", color=couleurs[i])
    ax.set_ylim(variation.min() - 4, variation.max() + 5)
    ax.set_title("Variation annuelle du nombre de crimes", fontsize=10)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.tick_params(axis="x", length=0)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)
    note(
        "La hausse est concentrée sur 2020-2022 ; 2023 marque un léger recul de la "
        "croissance d'une année sur l'autre, sans revenir au niveau de 2020."
    )
    espace()

    # --- Saisonnalité ---
    mois_fr = np.array(["Jan", "Fev", "Mar", "Avr", "Mai", "Juin", "Juil", "Aou", "Sep", "Oct", "Nov", "Dec"])
    jours_par_mois = np.array([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    par_mois = dfc.groupby("mois").size().to_numpy() / 4
    par_jour_mois = par_mois / jours_par_mois
    indice = par_jour_mois / np.mean(par_jour_mois)
    mois_fr_list = list(mois_fr)

    fig, ax = plt.subplots(figsize=(5.5, 2.4))
    ax.fill_between(mois_fr_list, indice, 1, color="#4C72B0", alpha=0.2)
    ax.plot(mois_fr_list, indice, color="#4C72B0", linewidth=2.5, marker="o")
    ax.axhline(1, color="grey", linestyle="--", linewidth=1)
    ax.set_ylim(0.90, 1.10)
    for x, v in enumerate(indice):
        ax.text(x, v + 0.007, f"{v:.2f}", ha="center", fontsize=7)
    ax.set_title("Indice de saisonnalité par mois", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    note(
        "Aucune saisonnalité marquée : l'écart entre le mois le plus chargé et le plus "
        "calme reste sous les 7 %."
    )

    separateur()

    # ========================================================================
    # SECTION 2 — Quels créneaux sont les plus à risque ?
    # ========================================================================
    st.markdown("## Quels créneaux horaires et jours sont les plus à risque ?")
    st.markdown(
        "Le jour de la semaine n'a quasi aucun effet. C'est **l'heure** qui compte : "
        "creux entre 4h et 6h, pic entre 17h et 21h. **Un crime sur quatre** a lieu la nuit "
        "(22h-5h)."
    )
    espace()

    # --- Horloge polaire + courbe par heure ---
    h = dfc["heure"].dropna().astype(int).to_numpy()
    par_heure = np.bincount(h, minlength=24)
    heures = np.arange(24)
    sans12 = np.where(heures == 12, np.nan, par_heure)
    pic, calme = np.nanargmax(sans12), np.nanargmin(sans12)
    ang = np.linspace(0, 2*np.pi, 24, endpoint=False)

    fig = plt.figure(figsize=(11.25, 4.125))

    ax1 = fig.add_subplot(1, 2, 1, projection="polar")
    h12 = np.where(heures == 12, 0, par_heure).astype(float)
    ax1.bar(ang, h12, width=2*np.pi/24*0.9, color=plt.cm.Reds(h12 / h12.max()))
    ax1.set_theta_offset(np.pi/2)
    ax1.set_theta_direction(-1)
    ax1.set_xticks(ang)
    ax1.set_xticklabels([f"{i}h" for i in range(24)], fontsize=6)
    ax1.set_yticklabels([])
    ax1.set_title("Vue horloge 24 h", fontsize=10)

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.fill_between(heures, sans12, color="#C0392B", alpha=0.12)
    ax2.plot(heures, sans12, color="#C0392B", linewidth=2.5)
    ax2.plot(12, par_heure[12], "x", color="grey")
    ax2.annotate("12 h exclue", (12, par_heure[12]), (13, par_heure[12]), fontsize=7, color="grey", va="center")
    for i, lab in [(pic, "pic"), (calme, "creux")]:
        ax2.annotate(f"{lab} {i} h", (i, par_heure[i]), (i, par_heure[i] + 5000), ha="center", fontweight="bold", fontsize=8)
    ax2.set_title("Nombre de crimes par heure", fontsize=10)
    ax2.set_xticks(heures)
    ax2.margins(x=0)
    ax2.get_yaxis().set_visible(False)
    ax2.spines[["top", "right", "left"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    note(
        "Le risque grimpe régulièrement au fil de la journée et culmine autour de "
        "17h-21h, avec un creux net entre 4h et 6h."
    )
    espace()

    # --- Part de nuit ---
    nuit = np.isin(heures, [22, 23, 0, 1, 2, 3, 4, 5])
    part_nuit = np.sum(par_heure[nuit]) / np.sum(par_heure) * 100

    fig, ax = plt.subplots(figsize=(6, 2.4))
    ax.bar(heures, par_heure, color=np.where(nuit, "#1F3B73", "#DCE4F2"))
    ax.set_title("Nombre de crimes par heure (nuit en bleu foncé)", fontsize=10)
    ax.set_xlabel("heure de la journee")
    ax.set_xticks(heures)
    ax.get_yaxis().set_visible(False)
    ax.spines[["top", "right", "left"]].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    note(f"**{part_nuit:.0f} %** des crimes se produisent la nuit, entre 22h et 5h.")
    espace()

    # --- Par jour de la semaine ---
    jn = dfc["jour_num"].to_numpy()
    par_jour = np.bincount(jn, minlength=7)
    jours_fr = np.array(["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"])
    o = np.argsort(par_jour)[::-1]
    noms, vals_jour = jours_fr[o], par_jour[o]
    pct = vals_jour / vals_jour.sum() * 100

    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.barh(noms, vals_jour, color=plt.cm.YlGn(np.linspace(.9, .35, 7)))
    ax.invert_yaxis()
    ax.bar_label(ax.containers[0], labels=[f"{v/1000:.0f}k ({p:.1f} %)" for v, p in zip(vals_jour, pct)], padding=4, fontsize=8)
    ax.set_title("Nombre de crimes par jour de la semaine", fontsize=10)
    ax.set_xlim(0, vals_jour.max() * 1.22)
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.get_xaxis().set_visible(False)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)
    note(
        "Le jour de la semaine a très peu d'effet : l'écart entre le jour le plus et le "
        "moins chargé reste faible."
    )
    espace()

    # --- Heatmap jour x heure ---
    matrice = np.zeros((7, 24), dtype=int)
    sub = dfc.dropna(subset=["heure"])
    np.add.at(matrice, (sub["jour_num"].to_numpy(), sub["heure"].astype(int).to_numpy()), 1)

    fig, ax = plt.subplots(figsize=(7, 2.6))
    sns.heatmap(matrice, cmap="Reds", xticklabels=heures, yticklabels=jours_fr, ax=ax)
    ax.set_title("Crimes par jour et par heure", fontsize=10)
    ax.set_xlabel("heure")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    note(
        "La bande la plus sombre est verticale, pas horizontale : c'est bien l'heure qui "
        "structure le risque, pas le jour."
    )