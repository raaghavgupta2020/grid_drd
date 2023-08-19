import os
import sys

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Preprocessing utilities
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Model building
from keras import layers
from tensorflow.keras.optimizers import Adam
from keras.models import Sequential
from tensorflow.keras.applications import DenseNet121
from keras.callbacks import Callback, ModelCheckpoint


from PIL import Image
from models.model import build_model, preprocess_image

# Some utilites
import numpy as np
from utils import base64_to_pil
from flask_sqlalchemy import SQLAlchemy
import openai
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.schema import HumanMessage
from langchain.prompts.example_selector import LengthBasedExampleSelector
from os import environ
from dotenv import load_dotenv

load_dotenv()


# Creating a new Flask Web application.
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = './models/pretrained/model.h5'
# MODEL_PATH = './models/pretrained/DenseNet-BC-121-32-no-top.h5'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:raghavguptapostgresql@localhost:5432/diabeticRetinopathy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# db.init_app(app)

with app.app_context():
    db.create_all()

# Loading trained model
model = build_model()
model.load_weights(MODEL_PATH)
print('Model loaded. Start serving...')

# OPENAI_API_KEY = environ.get('OPENAI_API_KEY')
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY");

# modelllm = GPT2LMHeadModel.from_pretrained('gpt2')
# tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
# tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")  # Replace with the actual model name
# modell = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
# generator = pipeline('text-generation', model=modell, tokenizer=tokenizer)

class PredictedData(db.Model):
    __tablename__ = 'predicted_data'
    id = db.Column(db.Integer, primary_key=True)
    image_data = db.Column(db.String, nullable=False)
    result = db.Column(db.String, nullable=False)
    probability = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<PredictedData(id={self.id}, result='{self.result}', probability={self.probability})>"


def model_predict(img, model):
    """
    Classify the severity of DR of image using pre-trained CNN model.

    Keyword arguments:
    img -- the retinal image to be classified
    model -- the pretrained CNN model used for prediction

    Predicted rating of severity of diabetic retinopathy on a scale of 0 to 4:

    0 - No DR
    1 - Mild
    2 - Moderate
    3 - Severe
    4 - Proliferative DR

    """
    
    ## Preprocessing the image
    x_val = np.empty((1, 224, 224, 3), dtype=np.uint8)
    img = img.resize((224,) * 2, resample=Image.LANCZOS)
    x_val[0, :, :, :] = img

    preds = model.predict(x_val)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/home', methods=['GET'])
def home():
    # home page
    return render_template('home.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the image from post request
        img = base64_to_pil(request.json)

        # Save the image to ./uploads
        # img.save("./uploads/image.png")

        # Make prediction on the image
        preds = model_predict(img, model)

        # Process result to find probability and class of prediction
        pred_proba = "{:.3f}".format(np.amax(preds))    # Max probability
        pred_class = np.argmax(np.squeeze(preds))

        diagnosis = ["No DR", "Mild", "Moderate", "Severe", "Proliferative DR"]

        result = diagnosis[pred_class]               # Convert to string
        
        # Serialize the result
        print(result)
        return jsonify(result=result, probability=pred_proba)

    return None

@app.route('/save_to_database', methods=['POST'])
def save_to_database():
    data = request.json.get('data')
    print(data)
    filename = request.json.get('filename')
    print(filename)

    # Save data to the database
    new_data = PredictedData(image_data=filename, result=data['result'], probability=data['probability'])
    db.session.add(new_data)
    db.session.commit()

    return jsonify(message='Data saved to the database')

@app.route('/data_table', methods=['GET'])
def data_table():
    data = PredictedData.query.all()
    return render_template('data_table.html', data=data)

# @app.route('/generate_response', methods=['POST'])
# def generate_response():
#     data = request.get_json()
#     input_text = data.get('input_text')
#     # Tokenize input
#     input_ids = tokenizer.encode(input_text, return_tensors='pt')
#     # Generate response
#     with torch.no_grad():
#         output = modelllm.generate(input_ids, max_length=200)[0]
#         response = tokenizer.decode(output, skip_special_tokens=True)
#     return jsonify({'response': response})

# @app.route('/generate_response', methods=['POST'])
# def generate_response():
#     data = request.get_json()
#     input_text = data.get('input_text')
#     # Generate response
#     response = generator(input_text, max_length=150)[0]['generated_text']
#     return jsonify({'response': response})


@app.route("/generate_response",  methods = ['POST'])
def generate_response():
    content_type = request.headers.get('Content-Type')
    prompt = None
    if (content_type == 'application/json'):
        json_payload = request.json
        prompt = json_payload['input_text']
    else:
        return 'Content-Type not supported!'

    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY,temperature=0, model_name='gpt-3.5-turbo')
    resp = llm([HumanMessage(content=prompt)])
    
    return {
        'statusCode': 200,
        'body': resp.content
    }

@app.route('/get_chart_data', methods=['GET'])
def get_chart_data():
    severity_counts = db.session.query(
        PredictedData.result,
        db.func.count(PredictedData.result)
    ).group_by(PredictedData.result).all()

    # Create a dictionary to store severity counts
    data = {severity: count for severity, count in severity_counts}

    return jsonify(data)


@app.route('/view_graphs')
def view_graphs():
    return render_template('graphs.html')


@app.route('/delete_entry/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    try:
        
        entry_to_delete = PredictedData.query.get(entry_id)
        if entry_to_delete:
            db.session.delete(entry_to_delete)
            db.session.commit()
            return jsonify(message='Entry deleted successfully'), 200
        else:
            return jsonify(message='Entry not found'), 404

    except Exception as e:
        return jsonify(message='An error occurred', error=str(e)), 500




if __name__ == '__main__':
    # app.run(port=5002, threaded=False)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()

