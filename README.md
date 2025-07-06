# **Sentiment Analysis Model - Deploy using AWS Services or Hugging Face**

## **Project Overview**
The goal of this project is to deploy a fine tuned sentiment analysis model, utilizing AWS services to make it available as a web application. The application will enable users to input text and receive sentiment predictions on whether the sentiment is **Positive**, **Negative**, or **Neutral**. This project incorporates fine-tuned sentiment analysis models, AWS EC2, S3, RDS, and web deployment using Streamlit.

---

## **Table of Contents**
- [Project Description](#project-description)
- [Link for the Model](#link-for-the-model)
- [Dataset](#dataset)
- [Approach](#approach)
- [Technologies Used](#technologies-used)
- [Deployment Guide](#deployment-guide)
- [Model Evaluation](#model-evaluation)
- [Expected Results](#expected-results)
- [Project Deliverables](#project-deliverables)
- [License](#license)

---

## **Project Description**

This project involves deploying a sentiment analysis model using AWS services (EC2, S3, RDS) and a web application built with **Streamlit**. The model classifies tweets as **Positive**, **Negative**, or **Neutral**, based on the sentiment expressed towards the specified entity.

---

## **Link for the Model**

Here is the link for the fine-tuned model:
- [Fine Tuned Sentiment Analysis BERT Model](https://huggingface.co/Praveen-R/Tweet_sentiment_analysis_with_BERT)

---

## **Dataset**

The dataset used in this project is a **Twitter Sentiment Analysis** dataset. The dataset includes tweets with an associated entity and sentiment classification.

- **Link to the dataset**: [Twitter Sentiment Dataset](https://raw.githubusercontent.com/GuviMentor88/Training-Datasets/refs/heads/main/twitter_training.csv)
  
**Dataset Columns:**
1. **Tweet ID** (optional): A unique identifier for each tweet.
2. **Entity** (optional): The topic or entity related to the tweet.
3. **Sentiment**: The sentiment of the tweet (Positive, Negative, or Neutral).
4. **Tweet Content**: The text content of the tweet.

---

## **Approach**

### 1. **Data Preparation**
- Fine-tune a pre-trained sentiment analysis model using the dataset or create your own machine learning model.
- Store the trained model and application code (`app.py`) on an **Amazon S3 bucket**.

### 2. **Infrastructure Setup**
- Launch an **Amazon EC2 instance** with necessary IAM roles and security settings.
- Ensure **Internet Gateway** access for the EC2 instance to download model files.

### 3. **Environment Configuration**
- Install the required libraries (Streamlit, Boto3, Transformers, etc.) on the EC2 instance.
- Download the model and application files from **S3**.

### 4. **Application Deployment**
- Run the **Streamlit** application on the EC2 instance.

### 5. **Database Setup**
- Set up an **Amazon RDS** instance for storing user data (username, login time).

### 6. **Security Configuration**
- Configure security groups and IAM roles to ensure safe access to S3, EC2, and RDS.

### 7. **Model Evaluation**
- Evaluate models based on **Accuracy**, **Precision**, **Recall**, **F1-Score**, and **ROC-AUC**.

---

## **Technologies Used**
- **Machine Learning / Deep Learning**: Hugging Face, Transformers, PyTorch/TensorFlow
- **AWS Services**: EC2, S3, RDS
- **Web Application**: Streamlit
- **Database**: Amazon RDS (MySQL)
- **Other Libraries**: Boto3, Transformers, torch

---

## **Deployment Guide**

1. **Setup EC2 Instance**:
   - Launch an EC2 instance with appropriate IAM roles and security groups.
   - Ensure the instance has internet access via an Internet Gateway.

2. **Install Required Libraries**:
   - SSH into the EC2 instance and install libraries such as `Streamlit`, `Boto3`, `transformers`, `torch`, etc.

3. **Deploy the Web Application**:
   - Download the fine-tuned model and `app.py` from the S3 bucket.
   - Run the **Streamlit** application.

4. **Set Up the Database**:
   - Create an RDS instance and configure PostgreSQL to store user information (username, login time).

5. **Security Configuration**:
   - Modify security groups to allow inbound traffic to the application (default: 8501 for Streamlit).
   - Set up IAM roles for secure access to AWS services.

---

## **Model Evaluation**

The sentiment analysis model will be evaluated using the following metrics:
- **Accuracy**: The percentage of correct predictions.
- **Precision**: The proportion of true positive predictions among all positive predictions.
- **Recall**: The proportion of true positive predictions among all actual positive cases.
- **F1-Score**: The harmonic mean of precision and recall.
- **ROC-AUC**: Area under the Receiver Operating Characteristic curve.

---

## **Expected Results**

- **Functional Web Application**: A fully functional web app for sentiment analysis accessible via the internet.
- **Scalable Deployment**: An AWS infrastructure that scales according to user demand.
- **Documentation**: Comprehensive project documentation for setup, deployment, and usage.

---

## **Project Deliverables**
1. **Data Files**: 
   - `twitter_training.csv` dataset used for training the model.
2. **Source Code**: 
   - Python scripts and notebooks used for the model, app, and deployment.
3. **Documentation**: 
   - A README file for setup, deployment, and usage instructions.

---

