#to run :
# aller à http://127.0.0.1:5000/

# Import all packages and libraries
import pandas as pd
import numpy as np
from flask import Flask, render_template,jsonify, request
import pickle


model = pickle.load( open( "./credit_score_app/static/data/best_model.pickle", "rb" ) )

df = pd.read_csv('./credit_score_app/static/data/test_preprocess_sample.csv')
app= Flask(__name__, template_folder='templates')

app.config.from_object('config')
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods = ['POST'])

def predict():
    '''
    For rendering results on HTML GUI
    '''

    all_id_client = list(df['SK_ID_CURR'].unique())

    
    seuil = 0.625

    ID = request.form['id_client']
    ID = int(ID)
    if ID not in all_id_client:
        prediction="Ce client n'est pas répertorié"
    else :
        X = df[df['SK_ID_CURR'] == ID]
        X = X.drop(['SK_ID_CURR'], axis=1)

        #data = df[df.index == comment]
        probability_default_payment = model.predict_proba(X)[:, 1]
        if probability_default_payment >= seuil:
            prediction = "Prêt NON Accordé, risque de défaut"
        else:
            prediction = "Prêt Accordé"
        


    return render_template('index.html', prediction_text=prediction)


# Define endpoint for flask
app.add_url_rule('/predict', 'predict', predict)

@app.route('/prediction_complete')

def pred_model():


    Xtot = df.drop(['SK_ID_CURR'], axis=1)
    seuil = 0.625
    y_pred = model.predict_proba(Xtot)[:,1]
    y_seuil = y_pred >= seuil
    y_seuil = np.array(y_seuil> 0)*1
    df_pred = df.copy()
    df_pred['Proba']=y_pred
    df_pred['PREDICTION']=y_seuil

    test_prediction = df_pred.to_json()
    with open("./credit_score_app/static/data/pred.json", "w") as outfile:
        outfile.write(test_prediction)
    return jsonify({'status': 'ok',
                    'df': test_prediction,
                    })
# Run app.
# Note : comment this line if you want to deploy on heroku
if __name__ == '__main__':
    app.run()
#app.run()
#app.run(debug=True)