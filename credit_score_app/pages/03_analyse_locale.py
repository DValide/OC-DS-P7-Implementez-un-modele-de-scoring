import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import pickle
import plotly.express as px
import plotly.offline as py
import plotly.graph_objects as go
import streamlit.components.v1 as components
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import seaborn as sns
import shap
import requests
import json
import urllib.request
#Options
st.set_option('deprecation.showPyplotGlobalUse', False)

#Nom de la page
st.set_page_config(
    page_title= "Analyse locale", 
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
        <title>Application Dashboard Crédit Score - Analyse Client</title> <center>
        <meta charset="utf-8">
        <meta name="description" content="Analyse client">
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>             
    <h1 style="font-size:300%; color:Crimson; font-family:Arial"> Prêt à dépenser <br>
        <h2 style="color:Gray; font-family:Georgia"> Dashboard local</h2>
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

#st.markdown("# Analyse locale ")
#st.sidebar.markdown("# Analyse locale ")

#Chargement des données 
#shap_values_test = pickle.load( open( "../credit_score_app/static/data/shap_values_test.p", "rb" ) )
df_shap_test = pickle.load( open( "../credit_score_app/static/data/df_shap_test.p", "rb" ) )
best_model = pickle.load( open( "../credit_score_app/static/data/best_model.pickle", "rb" ) )
test_origin = pickle.load( open( "../credit_score_app/static/data/test_prediction.pickle", "rb" ) )
#test = pickle.load( open( "../credit_score_app/static/data/test_preprocess.p","rb") )
#test = pd.read_csv('../credit_score_app/static/data/test_preprocess_sample.csv')
#test = test.set_index('SK_ID_CURR')

url = "http://127.0.0.1:5000/prediction_complete"
#url=  "https://dash-scoring.herokuapp.com/prediction_complete"
with urllib.request.urlopen(url) as url:
    data = json.loads(url.read())
    #st.write(data)
    df =pd.DataFrame.from_dict(data)
df = df.T

st.write(df)



st.sidebar.markdown("# 🎈 Analyse Locale ")


st.sidebar.markdown("Analyse locale rattachée à un client spécifique. On retrouves ses informations et son score crédit justifiée par une interprétabilité locale., Mais également des infor")

#st.sidebar.markdown("<p style='text-align:center;'> <img src='https://cdn.dribbble.com/users/513906/screenshots/5384407/dribbb.gif' width='250' height='200'> </p>", unsafe_allow_html=True)

html_select_client="""
    <div class="card">
      <div class="card-body" style="border-radius: 10px 10px 0px 0px;
                  background: #DEC7CB; padding-top: 5px; width: auto;
                  height: 40px;">
        <h3 class="card-title" style="background-color:#DEC7CB; color:Crimson;
                   font-family:Georgia; text-align: center; padding: 0px 0;">
          Informations sur le client / demande de prêt
        </h3>
      </div>
    </div>
    """

st.markdown(html_select_client, unsafe_allow_html=True)

liste_clients=list(df.SK_ID_CURR.values)

ID_client = st.selectbox(
     "Merci de sélectionner un identifiant du client:",
     (liste_clients))

st.write("Exemple d'ID : 205960, 413756, 344067")
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
    st.write('Ce client est solvable avec un taux de risque de '+ str(round(ligne_pret.Proba.iloc[0]*100,2))+'%')
    pred = ligne_pret.PREDICTION.values[0]

    if pred == 1 :
        pred = "Risque de défaut"
    else :
        pred = "Crédit accordé"

    st.write('La prédiction donne ', pred)

        
elif ligne_pret.PREDICTION.values == 1:
    st.write('Ce client est non solvable avec un taux de risque de '+ str(round(ligne_pret.Proba.iloc[0]*100,2))+'%')
    pred = ligne_pret.PREDICTION.values[0]

    if pred == 1 :
        pred = "Risque de défaut"
    else :
        pred = "Crédit accordé"

    st.write('La prédiction donne ', pred)

score = round(ligne_pret.Proba.iloc[0]*100,2)

#Tracé de la jauge
st.markdown("<h3 style='text-align: left; color: lightblue;'>Score crédit</h3>", unsafe_allow_html=True)
st.spinner('Jauge en cours de chargement')


fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = score,
    mode = "gauge+number",
    title = {'text': "Score crédit du client", 'font': {'size': 24}},
    delta = {'reference': 50},
    gauge = {'axis': {'range': [None, 100],
                      'tickwidth': 3,
                      'tickcolor': 'darkblue'},
             'bar': {'color': 'white', 'thickness' : 0.15},
             'bgcolor': 'white',
             'borderwidth': 2,
             'bordercolor': 'gray',
             'steps': [{'range': [0, 40], 'color': 'Green'},
                       {'range': [40, 67.4], 'color': 'LimeGreen'},
                       {'range': [67.2, 67.8], 'color': 'red'},
                       {'range': [67.6, 80], 'color': 'Orange'},
                       {'range': [80, 100], 'color': 'Crimson'}],
             'threshold': {'line': {'color': 'white', 'width': 5},
                           'thickness': 0.20,
                           # Score du client en %
                           # df_dashboard['SCORE_CLIENT_%']
                           'value': score }}))

fig.update_layout(paper_bgcolor='white',
                        height=400, width=500,
                        font={'color': 'darkblue', 'family': 'Arial'},
                        margin=dict(l=0, r=0, b=0, t=0, pad=0))
st.plotly_chart(fig, use_container_width=True)

st.markdown("<h3 style='text-align: left; color: lightblue;'>Interprétabilité locale</h3>", unsafe_allow_html=True)

shap.initjs()

test = df.drop(columns =["Proba", "PREDICTION", "SK_ID_CURR"])

explainer = shap.TreeExplainer(best_model)
shap_value = explainer(test, check_additivity=False)
#st.markdown(shap_value[1])
#cols= test_origin.columns.to_list()
client_index = df_shap_test[df_shap_test['SK_ID_CURR'] == ID_client].index.item()
X_shap = df_shap_test.set_index('SK_ID_CURR')
X_shap = X_shap.drop(columns = ["Proba","PREDICTION"])
X_test_courant = X_shap.iloc[client_index]
X_test_courant_array = X_test_courant.values.reshape(1, -1)
                

def affiche_facteurs_influence():
    ''' Affiche les facteurs d'influence du client courant
    '''
    html_facteurs_influence="""
        <div class="card">
            <div class="card-body" style="border-radius: 10px 10px 0px 0px;
                  background: #DEC7CB; padding-top: 5px; width: auto;
                  height: 40px;">
                  <h3 class="card-title" style="background-color:#DEC7CB; color:Crimson;
                      font-family:Georgia; text-align: center; padding: 0px 0;">
                      Variables importantes
                  </h3>
            </div>
        </div>
        """
    
    # ====================== GRAPHIQUES COMPARANT CLIENT COURANT / CLIENTS SIMILAIRES =========================== 
    
    if st.checkbox("Voir facteurs d\'influence"):     
        
        st.markdown(html_facteurs_influence, unsafe_allow_html=True)

        with st.spinner('**Affiche les facteurs d\'influence du client courant...**'):                 
                       
            #with st.expander('Facteurs d\'influence du client courant',
            #                  expanded=True):
                
            


            client_index = df[df['SK_ID_CURR'] == ID_client].index.item()
            st.write(client_index)
            X_shap = test_origin.set_index('SK_ID_CURR')
            X_shap = X_shap.drop(columns = ["Proba","PREDICTION"])
            X_test_courant = X_shap.iloc[client_index]
            X_test_courant_array = X_test_courant.values.reshape(1, -1)
                
            shap_values_courant = explainer.shap_values(X_test_courant_array)
                
                
                # Forceplot du client courant
                # BarPlot du client courant
                
            st.pyplot(shap.plots.force(explainer.expected_value[1],shap_values_courant[1],X_test_courant, matplotlib=True))  
               
                
                    # Plot the graph on the dashboard
                
     
                # Décision plot du client courant
                    # Décision Plot
            shap.decision_plot(explainer.expected_value[1], shap_values_courant[1], X_test_courant)
               
                    # Plot the graph on the dashboard
            st.pyplot()
affiche_facteurs_influence()

st.markdown("<h3 style='text-align: left; color: lightblue;'>Voir les clients voisins</h3>", unsafe_allow_html=True)


test_origin['AGE']=round(abs(test_origin['DAYS_BIRTH']/365),1)
  #ID_c=int(ID)

#INFO CLIENT SHAP
info_client=test_origin[test_origin['SK_ID_CURR']==ID_client]
enfant_c=info_client['CNT_CHILDREN'].item()
age_c=info_client['AGE'].item()
genre_c=info_client['CODE_GENDER'].item()
region_c=info_client['REGION_RATING_CLIENT'].item()
     
  #PROCHE VOISIN
enfant_v=test_origin[test_origin['CNT_CHILDREN']==enfant_c]
age_v=enfant_v[enfant_v['AGE']==age_c]
genre_v=age_v[age_v['CODE_GENDER']==genre_c]
region_v=genre_v[genre_v['REGION_RATING_CLIENT']==region_c]

if len(region_v) < 15:
  shap_values=region_v.sample(len(region_v),random_state=42)
if len(region_v) >= 15:
  shap_values=region_v.sample(15,random_state=42)

fig,ax=plt.subplots( figsize=(10,4))
plt.barh(range(len(shap_values)),shap_values['Proba'])
risque_client=info_client['Proba'].item()
plt.axhline(y=risque_client,linewidth=8, color='#d62728')
plt.xlabel('% de risque')
plt.ylabel('N° profils similaires')
plt.figtext(0.755,0.855,'-',fontsize = 60,fontweight = 'bold',color = '#d62728')
plt.figtext(0.797,0.9,'Client '+str(ID_client))
st.pyplot(fig)

moy_vois=shap_values['Proba'].mean()
diff_proba=round(abs(risque_client-moy_vois)*100,2)
st.markdown('Le client',str(ID_client),'à un écart de',str(diff_proba),'% de risque avec les clients de profils similaires.')