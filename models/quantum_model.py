import os
import cv2
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from qiskit import QuantumCircuit
from qiskit.circuit.library import TwoLocal
from qiskit import Aer , execute
from qiskit.visualization import CircuitPlotter
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Add
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc


#Defining paths to the dataset directories
images_dir = 'kaggle/diabetic_retinopathy_detection/images'
labels_dir = 'kaggle/diabetic_retinopathy_detection/labels'

#Loading images and labels
def load_data(images_dir, labels_dir):
    image_files = os.listdir(images_dir)
    images = [cv2.imread(os.path.join(images_dir, img)) for img in image_files]
    
    label_files = os.listdir(labels_dir)
    labels = [open(os.path.join(labels_dir, label_file)).readline().strip() for label_file in label_files]
    
    return images, labels
    
#Callng the data loading function
images, labels = load_data(images_dir, labels_dir)

#Spliting the dataset into training and testing sets
train_images, test_images, train_labels, test_labels = train_test_split(images, labels, test_size=0.2, random_state=42)

#Resizing images to (75, 75, 3) and normalize pixel values
input_shape = (75, 75)
train_images_resized = [cv2.resize(img, input_shape) for img in train_images]
test_images_resized = [cv2.resize(img, input_shape) for img in test_images]
train_images_normalized = np.array(train_images_resized) / 255.0
test_images_normalized = np.array(test_images_resized) / 255.0

#Label Encoding
label_encoder = LabelEncoder()
train_labels_encoded = label_encoder.fit_transform(train_labels)
test_labels_encoded = label_encoder.transform(test_labels)

#Converting labels to one-hot encoded vectors (optional)
num_classes = len(label_encoder.classes_)
train_labels_onehot = tf.keras.utils.to_categorical(train_labels_encoded, num_classes)
test_labels_onehot = tf.keras.utils.to_categorical(test_labels_encoded, num_classes)

#Quantum Circuit Generation
def create_quantum_circuit(input_shape, qubits):
    # Create a quantum circuit
    quantum_circuit = QuantumCircuit(qubits)
    
    # Add quantum gates to the circuit
    for qubit in qubits:
        quantum_circuit.h(qubit)  # Apply Hadamard gate to each qubit
        for target_qubit in qubits:
            if qubit != target_qubit:
                quantum_circuit.cx(qubit, target_qubit)  # Apply CNOT gate between qubits
    
    # Add more quantum gates or layers as needed based on your model
    
    return quantum_circuit
    
#Create the CNN model with quantum layers
def create_cnn_model(input_shape, num_classes, quantum_circuit):
    # Classical CNN model
    cnn_input = Input(shape=input_shape)
    cnn_layer1 = Conv2D(32, (3, 3), activation='relu')(cnn_input)
    cnn_pool1 = MaxPooling2D((2, 2))(cnn_layer1)
    cnn_layer2 = Conv2D(64, (3, 3), activation='relu')(cnn_pool1)
    cnn_pool2 = MaxPooling2D((2, 2))(cnn_layer2)
    cnn_flatten = Flatten()(cnn_pool2)
    
    # Quantum layer
    # backend = Aer.get_backend('statevector_simulator')  # Change to suitable backend
    # quantum_layer = tfq.layers.PQC(quantum_circuit, backend)
    # quantum_output = quantum_layer(cnn_flatten)
    backend = Aer.get_backend('statevector_simulator')  # Change to suitable backend
    quantum_layer = quantum_circuit  # Use the quantum circuit directly
    quantum_output = execute(quantum_layer, backend).result().get_statevector()
    
    # Merge classical and quantum outputs
    combined_output = Add()([cnn_flatten, quantum_output])
    
    # Fully connected layers
    dense_layer1 = Dense(128, activation='relu')(combined_output)
    output_layer = Dense(num_classes, activation='softmax')(dense_layer1)
    
    # Create and compile the model
    model = tf.keras.Model(inputs=cnn_input, outputs=output_layer)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model
    
#Set hyperparameters
batch_size = 32
epochs = 10
learning_rate = 0.001

#Training loop
def train_quantum_model(model, train_data, train_labels):
    # Compile the model
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    # Start training
    model.fit(train_data, train_labels, batch_size=batch_size, epochs=epochs, validation_split=0.1)

    
#Model evaluation
def evaluate_model(model, test_data, test_labels):
    # Evaluate the model on the test data
    loss, accuracy = model.evaluate(test_data, test_labels)
    
    # Print the evaluation results
    print("Test Loss:", loss)
    print("Test Accuracy:", accuracy)

# Main function
def main():
    # Load and preprocess data
    images, labels = load_data(images_dir, labels_dir)
    # train_images, test_images, train_labels, test_labels = preprocess_data(images, labels)

    qubits = [0, 1, 2]
    # Create quantum CNN model
    quantum_circuit = create_quantum_circuit(input_shape, qubits)  # Define qubits
    model = create_cnn_model(input_shape, num_classes, quantum_circuit)

    # Train quantum CNN model
    train_quantum_model(model, train_images_normalized, train_labels_onehot)

    # Evaluate model
    evaluate_model(model, test_images_normalized, test_labels_onehot)

    # After evaluating your model using the evaluate_model function
    predictions = model.predict(test_images_normalized)
    predicted_labels = np.argmax(predictions, axis=1)
    true_labels = np.argmax(test_labels_onehot, axis=1)

    # Compute confusion matrix
    cm = confusion_matrix(true_labels, predicted_labels)

    # Calculate precision, recall, F1-score, and support
    report = classification_report(true_labels, predicted_labels, target_names=label_encoder.classes_, output_dict=True)
    precision = report['weighted avg']['precision']
    recall = report['weighted avg']['recall']
    f1 = report['weighted avg']['f1-score']

    # Compute ROC curve and AUC
    fpr, tpr, thresholds = roc_curve(true_labels, predictions[:, 1])
    roc_auc = auc(fpr, tpr)
    
    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(len(label_encoder.classes_))
    plt.xticks(tick_marks, label_encoder.classes_, rotation=45)
    plt.yticks(tick_marks, label_encoder.classes_)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.show()

    # Plot ROC curve
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = {:.2f})'.format(roc_auc))
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc='lower right')
    plt.show()

    # Print precision, recall, F1-score, and AUC
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1-score:", f1)
    print("AUC:", roc_auc)


if __name__ == "__main__":
    main()