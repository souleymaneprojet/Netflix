import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
from streamlit_lottie import st_lottie

# =========================
# 🌈 CONFIGURATION GENERALE
# =========================
st.set_page_config(
    page_title="Analyse Netflix",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# 🎨 FOND VIDEO & STYLE CSS
# =========================
st.markdown(
    """
    <style>
    /* --- FOND VIDEO --- */
    [data-testid="stAppViewContainer"] {
        background: url('https://assets.mixkit.co/videos/preview/mixkit-light-leaks-in-red-and-orange-colors-3447-large.mp4');
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }

    

    /* --- FILTRE SUR LA VIDEO --- */
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-color: #4682b4;
        z-index: 0;
    }

    /* --- TITRES --- */
    h1, h2, h3 {
        font-family: 'Trebuchet MS', sans-serif;
        color: #fff;
        text-align: center;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
    }

    /* --- ONGLET STYLISE --- */
    .stTabs [role="tab"] {
        font-size: 18px;
        color: white;
        background-color: #222;
        padding: 10px;
        border-radius: 8px;
        transition: all 0.3s ease-in-out;
        margin: 3px;
        border: 1px solid #555;
    }
    .stTabs [role="tab"]:hover {
    transform: scale(1.05);
    background-color: #ffb347;  /* Orange clair */
    color: #000;  /* Texte noir pour contraste */
}


    /* --- SIDEBAR STYLISEE --- */
    [data-testid="stSidebar"] {
        background: #111;
        color: white;
        padding: 20px;
    }
    [data-testid="stSidebar"] h2 {
        color: #ff2c55;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #f5f5f5; /* gris clair */
        color: #000; /* texte noir */
    }

    /* --- METRICS --- */
    [data-testid="stMetricValue"] {
        color: #ff2c55;
        font-weight: bold;
        font-size: 28px;
    }

    [data-testid="stAppViewContainer"] {
    background: 255;   /* gris très clair */
    color: green;           /* texte noir pour lisibilité */
}


    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# ✨ FONCTION POUR LOTTIE
# =========================
def load_lottie(url):
   
    r = requests.get(url, verify=False)

    if r.status_code != 200:
        return None
    return r.json()

# Animation Netflix
lottie_url = "https://assets4.lottiefiles.com/packages/lf20_touohxv0.json"
lottie_animation = load_lottie(lottie_url)

# =========================
# 🔄 CHARGEMENT DES DONNEES
# =========================
@st.cache_data
def charger_donnees():
    df = pd.read_csv("Netflix.csv")
    df.dropna(subset=['Title'], inplace=True)
    df['Release_Date'] = pd.to_datetime(df['Release_Date'], errors='coerce')
    df['Année'] = df['Release_Date'].dt.year
    df['Mois'] = df['Release_Date'].dt.month
    df['Durée_num'] = df['Duration'].str.extract(r'(\d+)').astype(float)
    return df

df = charger_donnees()

# =========================
# 🎬 EN-TETE + ANIMATION
# =========================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st_lottie(lottie_animation, height=200, key="netflix_intro")
st.title("SOULEYMANE DAFFE DATA SCIENTIST")
st.title("🎬 Tableau de Bord Netflix - Style Immersif 🎥")

# =========================
# 📌 CREATION DES ONGLETS
# =========================
onglets = st.tabs([
    "📊 Statistiques globales",
    "📈 Évolution Films/Séries",
    "🎭 Contenu Adulte vs Familial",
    "🎬 Réalisateurs & Acteurs",
    "🔍 Analyse des descriptions",
    "🕒 Analyses temporelles"
])

# =========================
# 📊 STATISTIQUES GLOBALES
# =========================
with onglets[0]:
    st.header("📊 Statistiques globales")
    nb_films = df[df['Category'] == 'Movie'].shape[0]
    nb_series = df[df['Category'] == 'TV Show'].shape[0]
    nb_total = df.shape[0]
    nb_pays = df['Country'].nunique()

    fig_cat = px.pie(
        values=[nb_films, nb_series],
        names=["Films", "Séries"],
        title="Répartition Films vs Séries",
        hole=0.5
    )
    fig_cat.update_traces(pull=[0.05, 0.05])
    st.plotly_chart(fig_cat, use_container_width=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎞️ Films", nb_films)
    col2.metric("📺 Séries", nb_series)
    col3.metric("🌍 Pays", nb_pays)
    col4.metric("📚 Total titres", nb_total)

# =========================
# 📈 EVOLUTION FILMS/SERIES
# =========================
with onglets[1]:
    st.header("📈 Évolution des films et séries dans le temps")
    serie_film_par_annee = df.groupby(['Année', 'Category']).size().reset_index(name='Nombre')
    fig_evo = px.area(
        serie_film_par_annee,
        x='Année',
        y='Nombre',
        color='Category',
        title="Évolution Films & Séries",
        line_group='Category'
    )
    fig_evo.update_traces(mode="lines+markers", fill="tonexty")
    st.plotly_chart(fig_evo, use_container_width=True)

# =========================
# 🎭 CONTENU ADULTE VS FAMILIAL
# =========================
with onglets[2]:
    st.header("🎭 Contenu adulte vs familial")
    tags_adultes = ['TV-MA', 'R']
    tags_familial = ['PG', 'PG-13', 'TV-Y', 'TV-G']
    nb_adultes = df[df['Rating'].isin(tags_adultes)].shape[0]
    nb_famille = df[df['Rating'].isin(tags_familial)].shape[0]
    fig_rating = px.bar(
        x=['Contenu Adulte', 'Contenu Familial'],
        y=[nb_adultes, nb_famille],
        title="Répartition Adulte vs Familial",
        color=['Contenu Adulte', 'Contenu Familial']
    )
    st.plotly_chart(fig_rating, use_container_width=True)

# =========================
# 🎬 REALISATEURS & ACTEURS
# =========================
with onglets[3]:
    st.header("🎬 Réalisateurs & Acteurs")
    real_top = df['Director'].dropna().value_counts().head(10)
    fig_real = px.bar(
        real_top,
        x=real_top.index,
        y=real_top.values,
        title="Top 10 Réalisateurs"
    )
    st.plotly_chart(fig_real, use_container_width=True)

    all_cast = df['Cast'].dropna().str.split(',').sum()
    all_cast = [a.strip() for a in all_cast]
    acteur_top = Counter(all_cast).most_common(10)
    acteur_df = pd.DataFrame(acteur_top, columns=["Acteur", "Nombre de films/séries"])
    fig_acteur = px.bar(
        acteur_df,
        x="Acteur",
        y="Nombre de films/séries",
        title="Top 10 Acteurs"
    )
    st.plotly_chart(fig_acteur, use_container_width=True)

# =========================
# 🔍 ANALYSE DESCRIPTIONS
# =========================
with onglets[4]:
    st.header("🔍 Analyse des descriptions")
    all_desc = ' '.join(df['Description'].dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color='black', colormap="inferno").generate(all_desc)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# =========================
# 🕒 ANALYSES TEMPORELLES
# =========================
with onglets[5]:
    st.header("🕒 Nombre de sorties par mois")
    prod_par_mois = df['Mois'].value_counts().sort_index()
    fig_mois = px.bar(
        x=prod_par_mois.index,
        y=prod_par_mois.values,
        labels={'x': 'Mois', 'y': 'Nombre de sorties'},
        title="Nombre de sorties par mois",
        color=prod_par_mois.values,
        color_continuous_scale="pinkyl"
    )
    st.plotly_chart(fig_mois, use_container_width=True)
