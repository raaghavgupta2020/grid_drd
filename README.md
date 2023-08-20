
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

### Application screenshots

### Landing Page
[image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/d455e50a-b477-4b8e-9b63-4df387c5ce60)

### Database
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/27849f88-7b1c-48a2-baca-2e18823773bb)

### Home Page 
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/28fe3333-baa5-419d-a26c-005c045b34da)

### Upload Image 
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/8610a15d-fef0-4017-9e80-f24507eb3ed8)

### Preview Images
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/33352291-88aa-42ad-89e0-7350cdbbf083)

### Clicked on "View Results" at bottom
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/a252d855-4f99-4219-bce1-3ca6c3f575af)

### Results and Probabilities Data in Tabular Form
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/92b71d27-ee22-498d-bdfc-97007198d6ea)

### Database view after uploading images
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/fd1b3b2d-336e-4fb4-9fa5-db3b8cecca74)

### Enter 'Name' and 'Age' for patient specific remediation
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/6037480a-73b2-4e54-bc52-fc6e84050c50)

### User specific Remediation
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/6414027a-7d56-42d0-9e99-3a399f090e3b)

### Click on 'View Graphs'
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/252b0140-2976-4309-959c-3d06572b3448)

### Graphical Results of all Patients
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/b732545d-2a9a-4c3c-b881-806ad9b6e53e)

### Analysis of Graph using LangeChain LLM 
![image](https://github.com/raaghavgupta2020/grid_drd/assets/59497482/9ddc842c-cace-406d-8651-261cc4fcf15c)











