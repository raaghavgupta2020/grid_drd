
# Diabetic Retinopathy using Quantum Computing​ Web Application

### Proposed Approach : Quantum-Based Deep Convolutional Neural Network for Diabetic Retinopathy Detection. ​

The steps are mentioned below :

Step 1 : Our proposed approach stands at the intersection of cutting-edge quantum computing and the power of convolutional neural networks (CNNs) to address the pressing challenge of Diabetic Retinopathy progression detection.​

Step 2 : With an emphasis on efficiency and accuracy, we've crafted a hybrid model that integrates quantum circuits into a classical CNN framework. The quantum circuits bring forth the capabilities to capture intricate data interactions, while the CNN leverages its image-processing features. ​

Step 3 : Our approach capitalizes on transfer learning, incorporating a pre-trained CNN backbone, and integrates a quantum layer, resulting in a uniquely dynamic architecture. This synergy empowers our model to swiftly and accurately classify Diabetic Retinopathy severity levels. 

Step 4 : By unifying quantum and classical strengths, our solution offers an exciting avenue for early detection, personalized treatment, and furthering medical insights in the realm of Diabetic Retinopathy. Basically, in our model we're using Classification using optimized multiple-qubit gate quantum NN.​

#### This novel solution aims to enhance the accuracy, efficiency, and scalability of disease classification, ultimately leading to early diagnosis and improved patient outcomes.​
​
For classification of Diabetic Retinopathy from retinal images : 
<p align="center">
  <img src="https://github.com/snsten/Diabetic-Retinopathy-WebApp/blob/master/data/prediction.jpg">
</p>

## Diabetic Retinopathy
Diabetic retinopathy is an eye condition that can cause vision loss and blindness in people who have diabetes. It affects blood vessels in the retina.

No Diabetic Retinopathy    |  Severe Diabetic Retinopathy
:-------------------------:|:-------------------------:
![](https://github.com/snsten/Diabetic-Retinopathy-WebApp/blob/master/data/no_dr.jpg)  |  ![](https://github.com/snsten/Diabetic-Retinopathy-WebApp/blob/master/data/severe_dr.jpg)

## Data Description

Dataset consists of retina images taken using fundus photography under a variety of imaging conditions.

A clinician has rated each image for the severity of diabetic retinopathy on a scale of 0 to 4:

    0 - No DR

    1 - DR Stage 1

    2 - DR Stage 2

    3 - DR Stage 3

## About the Model used for prediction
### Densely Connected Convolutional Networks or DenseNet 

Dense Convolutional Network (DenseNet), which connects each layer to every other layer in a feed-forward fashion. Whereas traditional convolutional networks with L layers have L connections - one between each layer and its subsequent layer.

A more efficient model variant DenseNet-BC (DenseNet-Bottleneck-Compressed) networks are trained. Using the DenseNet-BC-121-32 model as the base model.

Advantages of DenseNet-BC are:
 - Reduced number of parameters
 - Similar or Better performance
 - Better accuracy
 
 
 Dense Net architecture as shown in the original paper which shows the connections from each layer to every other layer:
 
 <p align="center">
  <img src="https://github.com/snsten/Diabetic-Retinopathy-WebApp/blob/master/data/densenet.jpg">
</p>
 


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
​
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

### 7. In the "app.py" file with your postgresql username, password and localhost 

## Run the Webapp by executing 
`python app.py`
