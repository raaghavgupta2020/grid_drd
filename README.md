
# Diabetic Retinopathy using Quantum Computing​ Web Application

### Proposed Approach : Quantum-Based Deep Convolutional Neural Network for Diabetic Retinopathy Detection. ​

This repository contains code for a web application that utilizes a combination of quantum computing and deep learning techniques to detect and classify diabetic retinopathy progression in retinal images. The application is built using Flask, TensorFlow, and Qiskit, and it includes features such as image classification, data storage, and visualization of analysis results.

## Data Description

Dataset consists of retina images taken using fundus photography under a variety of imaging conditions.

A clinician has rated each image for the severity of diabetic retinopathy on a scale of 0 to 4:

    0 - No DR

    1 - DR Stage 1

    2 - DR Stage 2

    3 - DR Stage 3

## Requirements Installation

### 1. Clone the repository to your local machine:​
```
git clone https://github.com/raaghavgupta2020/grid_drd​
```
### 2. Create a virtual environment and activate it:​
```
python -m venv venv​
venv\Scripts\activate​
```
### 3. Install the required packages from the requirements.txt file:​
`pip install -r requirements.txt​`

### 4. Create a database in postgreSQL with name -> "diabeticRetinopathy"
### 5. Update the below line -> ​

`app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:<password>@localhost:5432/diabeticRetinopathy'​`

### 6. Run this query in you pgadmin4 to create the required tables ->​
```
CREATE TABLE IF NOT EXISTS public.predicted_data ​
( ​
  id serial PRIMARY KEY, ​
  image_data text, ​
  result text, ​
  probability double precision ​
);​
```
### 7. "OR"​
```
CREATE TABLE IF NOT EXISTS public.predicted_data​
(​
    id integer NOT NULL DEFAULT nextval('predicted_data_id_seq'::regclass),​
    image_data text COLLATE pg_catalog."default",​
    result text COLLATE pg_catalog."default",​
    probability double precision,​
    CONSTRAINT predicted_data_pkey PRIMARY KEY (id)​
)​
```
### 8. Create a .env file and create a variable called "OPENAI_API_KEY" and enter your openai api key ​
Refer to this link for the same :​

`
https://www.maisieai.com/help/how-to-get-an-openai-api-key-for-chatgpt​
`

​### 9. Run the Flask application : ​

`python app.py​`

Access the web application by opening your web browser and navigating to `http://localhost:5000`​
Upload retinal images for classification and view the predicted results, probabilities, and recommendations for remediation.​

