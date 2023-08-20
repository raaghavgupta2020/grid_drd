
# Diabetic Retinopathy using Quantum Computing​ Web Application

Diabetic retinopathy is a significant concern in India, often referred to as the "diabetic capital," where the prevalence of diabetes is on the rise. Over the next two to three decades, the number of diabetes cases is projected to double. Diabetic retinopathy, an outcome of diabetes, can lead to vision impairment and even blindness, substantially reducing an individual's quality of life.

This condition is characterized by microvascular retinal changes and can be averted through early detection and timely intervention. However, the early detection process requires computationally intensive tasks such as image screening and classification. This is where the intersection of quantum computing and conventional image classification methods comes into play.

Quantum computing offers a promising avenue for addressing the computational challenges of image classification due to its ability to perform complex calculations much faster than classical computers. By integrating quantum computing with deep learning techniques, it becomes theoretically feasible to achieve higher accuracy in diabetic retinopathy classification. It is a great solution for rural areas (Tier 4 cities), which has small dispensaries and can afford a fundus camera, but don’t have expert medical professionals available.

### Proposed Approach : Quantum-Based Deep Convolutional Neural Network for Diabetic Retinopathy Detection.

This repository contains code for a web application that utilizes a combination of quantum computing and deep learning techniques to detect and classify diabetic retinopathy progression in retinal images. The application is built using Flask, TensorFlow, and Qiskit, and it includes features such as image classification, data storage, and visualization of analysis results.

## Dataset Used : 
<p> https://www.kaggle.com/c/aptos2019-blindness-detection/data​ </p>


## Data Description

Dataset consists of retina images taken using fundus photography under a variety of imaging conditions.

A clinician has rated each image for the severity of diabetic retinopathy on a scale of 0 to 4:

    0 - No DR       1 - DR Stage 1      2 - DR Stage 2      3 - DR Stage 3

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

### 9. Run the Flask application : ​

`python app.py​`

Access the web application by opening your web browser and navigating to `http://localhost:5000`​
Upload retinal images for classification and view the predicted results, probabilities, and recommendations for remediation.​

## Future Scope : 

#### As we look to the future, the potential for our Quantum-Enhanced CNN model to revolutionize Diabetic Retinopathy classification remains promising. Here are five pivotal avenues we plan ​to explore:​

1. Advanced Quantum Architecture : Explore deeper circuits and innovations for heightened accuracy.​
  
2. Advanced security measures | Ethical and regulatory compliance  : Strengthen data protection through encryption, authentication, and access controls, aligning with HIPAA and industry best practices and regulatory compliance, to safeguard patient data and address privacy concerns effectively.​
  
3. Quantum Robustness Enhancement : Develop strategies to counter quantum noise and enhance reliability.​
  
4. Clinical Validation Collaboration : Partner with medical institutions for rigorous accuracy validation.​
  
5. Quantum Hardware Progress : Utilize evolving quantum hardware for speed and precision gains.​

Through these strategic directions, we aim to unlock new dimensions in Diabetic Retinopathy classification and contribute to advancements in healthcare diagnostics.​

### ML Model Architecture

### Application screenshots

### Landing Page
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/f34c9bb3-6136-48ea-8c0b-8619533cc0cb)

### Database
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/e0549564-1182-4160-b876-89855f9ea62d)


### Home Page 
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/509919cd-107e-4669-9852-094da9b77687)

### Upload Image 
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/1aea876d-eb81-450d-ab3a-ab008e08786f)

### Preview Images
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/0bc3bd17-895c-4dd1-8bfc-2d17e047a4a8)

### Clicked on "View Results" at bottom
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/d3d3fcfa-0db0-47d6-aa6a-518890762590)

### Results and Probabilities Data in Tabular Form
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/6179e609-0f06-4520-8862-fd0a70a4e102)

### Database view after uploading images
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/ce4e3a7f-018c-42ec-b155-bbc3868f161e)

### Enter 'Name' and 'Age' for patient specific remediation
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/fc4ea0d3-8b78-46ca-b150-c137e9e0024d)

### User specific Remediation
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/7c48eac1-1dc2-4b49-a150-c0141a9f1b68)

### Click on 'View Graphs'
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/5e12ee3c-af9d-4e30-b4b9-217e14adea53)

### Graphical Results of all Patients
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/404a8545-9658-4111-9c19-7ab5d708a137)

### Analysis of Graph using LangeChain LLM 
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/39bc2832-e233-4f56-8c35-877d2b7a9cc8)






