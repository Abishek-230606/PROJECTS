#  Major Projects by Abishek JS

Welcome to my repository of major academic and personal machine learning projects.
This space showcases my journey in AI and deep learning, starting with a CNN-based medical image classifier for chest X-rays.

---

## 📌 Project : Chest X-Ray Classification (Normal vs Tuberculosis vs Pneumonia)


## 📌 Overview
This project focuses on building a **deep learning–based medical image classification system** to classify chest X-ray images into three categories:

- **Normal**
- **Pneumonia**
- **Tuberculosis**

The objective is to assist in faster and more reliable preliminary diagnosis by leveraging **transfer learning** while ensuring **clinically meaningful evaluation**, not just high accuracy.

---

## 🎯 Problem Statement
Chest X-ray interpretation is a time-critical task that requires expert radiologists. In many real-world scenarios, especially in resource-constrained environments, automated decision-support systems can help doctors by providing an initial classification.

However, medical datasets often suffer from **class imbalance**, making naïve accuracy-based models unreliable.  
This project addresses that challenge by focusing on **balanced evaluation using recall, F1-score, and confusion matrices**.

---


---

### 📁 Dataset Structure

The dataset is organized into **training, validation, and test sets** using a 70-15-15 split:


The dataset is organized into three splits:
dataset/ ├── train/ │   ├── Normal/ │   ├── Tuberculosis/ │   └── Pneumonia/ ├── val/ │   ├── Normal/ │   ├── Tuberculosis/ │   └── Pneumonia/ ├── test/ │   ├── Normal/ │   ├── Tuberculosis/ │   └── Pneumonia/



---


Each folder contains chest X-ray images corresponding to its class.

---

## ⚙️ Data Preprocessing
- All images resized to **224 × 224**
- Pixel values normalized to **[0, 1]**
- Images loaded as **RGB** (required for pretrained CNNs)
- **Data augmentation applied only to training data**:
  - Rotation
  - Width & height shifts
  - Zooming
- **No augmentation applied to validation or test sets**

This ensures **true and unbiased evaluation**.

---

## 🧠 Model Architecture

### 🔹 Why Transfer Learning?
Training a CNN from scratch requires very large datasets, which are rarely available in medical imaging.  
To overcome this, **transfer learning** was used.

### 🔹 Backbone: EfficientNetB0
EfficientNetB0 was selected because:
- Efficient and lightweight
- Pretrained on ImageNet
- Uses compound scaling (depth, width, resolution)
- Strong generalization with fewer parameters

### 🔹 Classification Head
The custom head added on top of EfficientNet consists of:
- Global Average Pooling
- Batch Normalization
- Dense layer (ReLU activation)
- Dropout (0.5) for regularization
- Final Dense layer with **Softmax** (3 classes)

---

## 🏋️ Training Strategy

### Phase 1: Feature Extraction
- EfficientNet backbone **frozen**
- Only classification head trained
- Optimizer: **Adam**
- Loss: **Categorical Cross-Entropy**

### Handling Class Imbalance
Initial results revealed **majority-class bias**, where the model predicted Tuberculosis excessively.

To fix this:
- **Class weights** were computed from the training set
- Misclassification of minority classes penalized more heavily
- Model retrained from scratch with class weights

---

## 📊 Evaluation Metrics
Accuracy alone was found to be misleading due to class imbalance.  
Final evaluation includes:

- **Confusion Matrix**
- **Precision**
- **Recall**
- **F1-Score**
- Class-wise performance analysis

This ensures the model is **clinically meaningful**, not just numerically impressive.

---

## 📈 Results Summary
- High recall achieved for **Normal** and **Pneumonia** after class-weight correction
- Tuberculosis no longer dominates predictions
- Balanced performance across classes
- Demonstrates the importance of **proper evaluation in medical ML**

> ⚠️ Note: Lower overall accuracy after class balancing is expected and acceptable, as it reflects improved fairness and reliability.

---

## 🚧 Limitations
- Dataset remains imbalanced despite class weighting
- Model trained only in Phase-1 (backbone frozen)
- No explainability techniques (e.g., Grad-CAM) included yet

---

## 🔮 Future Improvements
- Phase-2 fine-tuning of EfficientNet backbone
- Collecting more balanced datasets
- Adding explainability (Grad-CAM)
- Exploring focal loss for harder examples

---

## 🧑‍💻 Author
**Abishek JS**  
Second-Year CSE Student (AI & ML)  

---

## 📜 Disclaimer
This project is intended for **academic and research purposes only** and should not be used as a standalone diagnostic tool in clinical practice.
