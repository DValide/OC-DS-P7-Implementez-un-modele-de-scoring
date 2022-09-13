import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = "Accueil",
    page_icon = "🔎",
    layout="wide"
    )
# Suppression des marges par défaut
padding = 1
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)
#Titre
html_header="""
    <head> 
    <center>
        <title>Dashboard Scoring client </title> <center>
        <meta charset="utf-8">
        <meta name="description" content="accueil">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>             
    <h1 style="font-size:300%; color:Crimson; font-family:Arial"> Prêt à dépenser <br>
        <h2 style="color:Gray; font-family:Georgia"> Accueil 🔎</h2>
        <hr style= "  display: block;
          margin-top: 0;
          margin-bottom: 0;
          margin-left: auto;
          margin-right: auto;
          border-style: inset;
          border-width: 1.5px;"/>
     </h1>
"""
st.markdown('<style>body{background-color: #fbfff0}</style>',unsafe_allow_html=True)
st.markdown(html_header, unsafe_allow_html=True)

#st.markdown("Accueil🔎")

st.sidebar.markdown(" Page d'accueil du dashboard. Ci-dessus le menu principal qui permet de naviguer dans les résultats notre modèle de scoring.")

st.markdown("#  <center>  Dashboard scoring client </center>", unsafe_allow_html=True)

st.sidebar.success("Selectionnez un mode d'analyse.")

logo =  Image.open("../credit_score_app/static/images/logo_entreprise.png") 
logo_home = Image.open("../credit_score_app/static/images/home_credit_logo.png")

col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.write("")

with col2:
    st.image(logo, width= 600)

with col3:
    st.write("")


st.markdown("<h2> Dashboard conçu pour les chargés de relation client à l'attention des clients. Dans un soucis de transparence le process decisionnel d' octroi de crédit est expliqué ici </h2>", unsafe_allow_html=True)
st.sidebar.image(logo_home, width=240, caption=" Origine des données ",
                 use_column_width='always')