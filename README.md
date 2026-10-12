# TruthCheck – Fake News Detection System

## 📌 Overview
TruthCheck is a web-based fake news detection system built using Python, Machine Learning, and Natural Language Processing (NLP). It helps users analyze news articles and predict whether they are **REAL or FAKE**.

The project aims to address the spread of misinformation by providing a simple platform for news analysis.

## ⚙️ How I Built It
- **Machine Learning:** Trained a classification model using the `Fake.csv` and `True.csv` datasets to identify patterns in real and fake news.
- **Text Processing:** Used text preprocessing and a vectorizer to convert news articles into numerical features that the model can understand.
- **Flask:** Built the web application to accept news input, run predictions, and display results.
- **Multilingual Support:** Integrated `langdetect` to identify the input language and `deep-translator` to translate supported languages into English before prediction.
- **Web Scraping:** Used `Requests` and `BeautifulSoup` to fetch news content from online sources.
- **MongoDB Atlas:** Integrated a cloud database to store user information, news articles, and prediction history.

## 🔄 How It Works
1. The user enters a news article or fetches available news content.
2. The system detects the language and translates the text into English when required.
3. The text is processed and converted into numerical features.
4. The trained machine learning model predicts whether the news is REAL or FAKE.
5. The result is displayed on the web interface, and the relevant data can be stored in MongoDB Atlas.

## 🛠️ Technologies Used
- Python
- Flask
- Scikit-learn
- NLP and text vectorization
- HTML and CSS
- MongoDB Atlas
- PyMongo
- langdetect and deep-translator
- Requests and BeautifulSoup

## 🎯 Objective
To demonstrate how machine learning and web technologies can be combined to analyze news content and help users identify potentially misleading information.

## ⚠️ Disclaimer
TruthCheck provides machine learning-based predictions, not guaranteed fact verification. Results should be checked against reliable news sources.

