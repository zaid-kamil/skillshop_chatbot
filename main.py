from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import random

app = Flask(__name__)

model_data = {}

with open('model.pkl','rb') as f:
    model_data = pickle.loads(f.read())

rdf = pd.read_csv('bot_response_dataset.csv')

def predict_tag(txt='Hello world', vectorizer=None,
                model=None,binarizer=None,*args,**kwargs):
    input_vector = vectorizer.transform([txt])
    result = model.predict(input_vector)
    output_tag = binarizer.inverse_transform(result)
    return output_tag[0]

def get_bot_reply(predicted_tag):
    resultdf = rdf[rdf['tag']==predicted_tag] 
    responses = resultdf.response.to_list()
    return random.choice(responses)

@app.route('/')
def index():
    return render_template('index.html',title='skillshop chatbot')

@app.route('/predict')
def predict():
    if request.args.get('query'):
        query = request.args.get('query')
        tag = predict_tag(query, **model_data)
        if tag:
            response = get_bot_reply(tag)
        else:
            response = 'sorry, i am still learning. Call us to get more info'
    else:
        response = 'please ask me a question'

    return jsonify({'botreply':response, 'query' : query})

if __name__ == '__main__':
    app.run(debug=True)