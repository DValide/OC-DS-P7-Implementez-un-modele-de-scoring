import streamlit as st
import numpy as np
from PIL import Image
import pickle
import pandas as pd
import plotly.express as px
import plotly.offline as py
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
#import matplotlib.lines as mlines
#import seaborn as sns
import shap
import requests
import json
import urllib.request

st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(
    page_title= "Analyse globale ", 
    page_icon= "🧐🔎",
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
        <title>Application Dashboard Crédit Score - Analyse Globale</title> <center>
        <meta charset="utf-8">
        <meta name="description" content="Analyse générale">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>             
    <h1 style="font-size:300%; color:Crimson; font-family:Arial"> Prêt à dépenser <br>
        <h2 style="color:Gray; font-family:Georgia"> Dashboard global</h2>
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




#Chargement des données 

#shap_values_test = pickle.load( open( "../credit_score_app/static/data/shap_values_test.p", "rb" ) )
#df_shap_test = pickle.load( open( "../credit_score_app/static/data/df_shap_test.p", "rb" ) )
best_model = pickle.load( open( "./static/data/best_model.pickle", "rb" ) )
test_origin = pickle.load( open( "./static/data/test_prediction.pickle", "rb" ) )
#test = pickle.load( open( "../credit_score_app/static/data/test_preprocess.p","rb") )
#test = pd.read_csv('../credit_score_app/static/data/test_preprocess_sample.csv')
#test = test.set_index('SK_ID_CURR')

#url = "http://127.0.0.1:5000/prediction_complete"
url=  "https://dash-scoring.herokuapp.com/prediction_complete"
with urllib.request.urlopen(url) as url:
    data = json.loads(url.read())
    #st.write(data)
    df =pd.DataFrame.from_dict(data)
df = df.T

st.write(df)

st.sidebar.markdown("# 🧐🔎Analyse globale 🧐🔎")
st.markdown("#  <center> 🧐🔎 Analyse globale 🧐🔎 </center> ", unsafe_allow_html=True)


st.sidebar.markdown("Analyse globale, le client est comparé à l'ensemble des clients. ")

liste_clients=list(df.SK_ID_CURR.values)

ID_client = st.selectbox(
     "Merci de saisir l'identifiant du client:",
     (liste_clients))

st.write("Exemple d'ID : 100172, 100013, 455955")

 #Récupération des informations du client

data_client=test_origin[test_origin.SK_ID_CURR==int(ID_client)]
col1, col2 = st.columns(2)
with col1:
    st.write('__Info crédit__')
    st.write('Type de contrat:', data_client['NAME_CONTRACT_TYPE'].values[0])
    st.write('Montant:', data_client['AMT_CREDIT'].values[0],"$")
    st.write('Montant annuel:', data_client['AMT_ANNUITY'].values[0],"$")
    st.write('Ratio credit sur revenus:', data_client['INCOME_TO_CREDIT_RATIO'].values[0],"$")
with col2:
    st.write('__Info Client__')
    st.write('Genre:', data_client['CODE_GENDER'].values[0])
    st.write('Age :', round(abs(data_client['DAYS_BIRTH'].values[0]/365)))
    st.write('Status :', data_client['NAME_FAMILY_STATUS'].values[0])
    st.write('Education:', data_client['NAME_EDUCATION_TYPE'].values[0])
    st.write('Occupation:', data_client['OCCUPATION_TYPE'].values[0])
    st.write(
        'Employé:', data_client['ORGANIZATION_TYPE'].values[0],
        ', depuis', round(abs(data_client['DAYS_EMPLOYED'].values[0]/365)),
        'années')
    st.write("Type d'habitation:", data_client['NAME_HOUSING_TYPE'].values[0])
    st.write('Voiture :', data_client['FLAG_OWN_CAR'].values[0])
    st.write("Patrimoine total :",data_client.AMT_INCOME_TOTAL.values[0],"$")


 #Récupération des informations de solvabilité
ligne_pret = df[df.SK_ID_CURR == int(ID_client)][["Proba", "PREDICTION"]]
if ligne_pret.PREDICTION.values == 0:
    st.write('Ce client est solvable avec un taux de risque de '+ str(round(ligne_pret.Proba.iloc[0],2))+'%')
    pred = ligne_pret.PREDICTION.values[0]

    if pred == 1 :
        pred = "Risque de défaut"
    else :
        pred = "Crédit accordé"

    st.write('La prédiction donne ', pred)

        
elif ligne_pret.PREDICTION.values == 1:
    st.write('Ce client est non solvable avec un taux de risque de '+ str(round(ligne_pret.Proba.iloc[0],2))+'%')
    pred = ligne_pret.PREDICTION.values[0]

    if pred == 1 :
        pred = "Risque de défaut"
    else :
        pred = "Crédit accordé"

    st.write('La prédiction donne ', pred)



## Récupération des features clients
test = df.drop(columns =["Proba", "PREDICTION", "SK_ID_CURR"])
explainer_shap = shap.TreeExplainer(best_model)
shap_value = explainer_shap.shap_values(test)
#shap_id = df[df["SK_ID_CURR"]== ID_client].copy().T

st.markdown("# ANALYSE GLOBALE ")

fig,ax=plt.subplots( figsize=(10,4))
ax = shap.summary_plot(shap_value, test)
st.pyplot(fig)

def application_samples_component():
    st.write('Sample size:')
    nb_clients_sample = st.number_input(
        label='Number of clients', 
        min_value=1,
        max_value=df.shape[0],
        format='%i')
    if st.button('Generate sample'):
        st.write(df.sample(nb_clients_sample))

application_samples_component()
# Recupération des indicateurs impliqués dans le calcul




df_type=test_origin.drop(columns =['SK_ID_CURR','PREDICTION'])
df_num=df_type.select_dtypes(include = 'number')

## Select qualitative columns
st.markdown("<h3 style='text-align: left; color: lightblue;'>Distribution des variables quantitatives</h3>", unsafe_allow_html=True)
Col_num = st.selectbox(
     "Sélectionnez un indicateur pour une analyse analyse intéractive, le client se situe au repère rouge :",
     list(df_num.columns))

st.subheader(Col_num)
#fig,ax=plt.subplots( figsize=(10,4))
    
x0 = test_origin[test_origin['PREDICTION']==0][Col_num]
y0 = test_origin[test_origin['PREDICTION']==1][Col_num]
z0 = test_origin[Col_num]
bins = np.linspace(0, 1, 15)

risque_client=test_origin[test_origin['SK_ID_CURR']==ID_client][Col_num].item()
    

group_labels = ['Solvable', 'Non solvable','Global']

fig = go.Figure()
fig.add_trace(go.Histogram(x=x0, name = 'Crédit accordé'))
fig.add_trace(go.Histogram(x=y0, name = 'Risque de défaut'))
fig.add_trace(go.Histogram(x=z0,name = 'Tous les cients' ))
fig.add_vline(x= risque_client, annotation_text = 'client n° '+ str(ID_client), line_color = "red")
fig.update_layout(barmode='relative')
fig.update_traces(opacity=0.75)
plt.show()
st.plotly_chart(fig, use_container_width=True)

df_object = df_type.select_dtypes(include = 'object')

## Select objects columns
st.markdown("<h3 style='text-align: left; color: lightblue;'>Distribution des variables qualitatives</h3>", unsafe_allow_html=True)
Col = st.selectbox(
     'Sélectionnez un indicateur :',
     list(df_object.columns))

st.subheader(Col)
sizes0 = list(test_origin[Col][test_origin['PREDICTION']==0].value_counts().values)
labels0 =list(test_origin[Col][test_origin['PREDICTION']==0].value_counts().index)

sizes1 = list(test_origin[Col][test_origin['PREDICTION']==1].value_counts().values)
labels1 =list(test_origin[Col][test_origin['PREDICTION']==1].value_counts().index)

size = list(test_origin[Col].value_counts().values)
labels = list(test_origin[Col].value_counts().index)


risque_client=test_origin[test_origin['SK_ID_CURR']== ID_client][Col].item()

fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])

fig.add_trace(go.Pie(labels=labels0, values = sizes0, name = 'Crédit accordé' ), 1,1)
fig.add_trace(go.Pie(labels=labels1, values = sizes1, name ='Risque de défaut' ),1,2)
fig.add_trace(go.Pie(labels=labels, values = size, name = 'Tous les cients'),1,3)
#fig.add_vline(x= risque_client, annotation_text = 'client n° '+ str(id_client), line_color = "red")

fig.update_traces(hole=.45, hoverinfo="label+percent+name")

fig.update_layout(
    title_text="Répartition des clients",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='Solvable', x=0.1, y=0.5, font_size=10, showarrow=False),
                 dict(text='Non Solvable', x=0.5, y=0.5, font_size=10, showarrow=False),
                dict(text='Global', x=0.89, y=0.5, font_size=10, showarrow=False)])
st.plotly_chart(fig, use_container_width=False, sharing="streamlit",)

## Analyse dépendance des 3 features les plus importantes
st.markdown("<h3 style='text-align: left; color: lightblue;'>Analyse des 3 indicateurs les plus importants </h3>", unsafe_allow_html=True)
shap.dependence_plot("EXT_SOURCE_3", shap_value[0], test)
st.pyplot()

fig,ax=plt.subplots( figsize=(10,4))
ax =shap.dependence_plot("CREDIT_TO_ANNUITY_RATIO", shap_value[0],test)
st.pyplot()

fig,ax=plt.subplots( figsize=(10,4))
ax = shap.dependence_plot("EXT_SOURCE_2", shap_value[0], test)
st.pyplot()

ax =shap.dependence_plot("DAYS_BIRTH", shap_value[0],test)
st.pyplot()