import streamlit as st
import pickle
import pandas as pd
import shap
import request

import json, urllib.request

#shap_values_test = pickle.load( open( "../credit_score_app/static/data/shap_values_test.p", "rb" ) )
#df_shap_test = pickle.load( open( "../credit_score_app/static/data/df_shap_test.p", "rb" ) )
#best_model = pickle.load( open( "../credit_score_app/static/data/best_model.pickle", "rb" ) )
#df = pickle.load( open( "../credit_score_app/static/data/test_prediction.pickle", "rb" ) )
#test = pickle.load( open( "../credit_score_app/static/data/test_preprocess.p","rb") )
#test = pd.read_csv('../credit_score_app/static/data/test_preprocess_sample.csv')
#test = test.set_index('SK_ID_CURR')

# https://api-scoring-pret-a-depenser.herokuapp.com/predict
#predict = json.loads('pred.json')
#print(predict)
import urllib
url = "http://127.0.0.1:5000/prediction_complete"
df = urllib.request.urlopen(url).read()
out = json.load(urllib.urlopen(url))
st.write(out.sample(3))