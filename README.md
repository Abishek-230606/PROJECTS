#  Major Projects by Abishek JS

Welcome to my repository of major academic and personal machine learning projects.
This space showcases my journey in AI and deep learning, starting with a CNN-based medical image classifier for chest X-rays.

---

## 📌 Project 1: Chest X-Ray Classification (Normal vs Tuberculosis vs Pneumonia)

### 🔍 Overview
This project uses a Convolutional Neural Network (CNN) to classify chest X-ray images into three categories:
- **Normal**
- **Tuberculosis**
- **Pneumonia**

It demonstrates my understanding of image preprocessing, data augmentation, model architecture, training, and evaluation using TensorFlow and Keras.

---

### 📁 Dataset Structure

The dataset is organized into three splits:
dataset/
├── train/ 
       ├── Normal/ 
       ├── Tuberculosis/ 
       │── Pneumonia/ 
├── val/    
       ├── Normal/    
       ├── Tuberculosis/ 
       │─ Pneumonia/
├── test/    
        ├── Normal/   
        ├── Tuberculosis/ 
        ├── Pneumonia/



---

### 🧪 Model Architecture

- 3 Convolutional layers with ReLU activation
- MaxPooling layers to reduce spatial dimensions
- Flatten + Dense layers for classification
- Dropout to prevent overfitting
- Softmax output layer for multi-class prediction

---

### ⚙️ Technologies Used

- Python
- TensorFlow / Keras
- NumPy
- Matplotlib
- scikit-learn

---

### 📊 Evaluation Metrics

- Accuracy
- Confusion Matrix
- Classification Report

---

### 🚀 How to Run

1. Clone the repository  
2. Install dependencies:
3. pip install tensorflow numpy matplotlib scikit-learn,tensorflow.
3. Place your dataset in the `dataset/` folder as shown above  
4. Run the notebook `Chest_Xray_CNN_Classifier.ipynb`


### 🙋‍♂️ About Me

I’m Abishek JS,
currently pursuing B.Tech in Computer Science and Engineering with a specialization in Artificial Intelligence and Machine Learning.
I’m passionate about building real-world AI solutions and documenting my learning journey through projects like this.

---

### 📬 Contact

Feel free to connect with me on Linkdin - https://www.linkedin.com/in/abishek-js
