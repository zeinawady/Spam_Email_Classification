import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

# Define the function to transform text
ps = PorterStemmer()

def transform_text(text): 
    text = text.lower() 
    text = nltk.word_tokenize(text) 
 
    y = [] 
    for i in text: 
        if i.isalpha(): 
            y.append(i) 
 
    text = y[:] 
    y.clear() 
 
    for i in text: 
        if i not in stopwords.words('english') and i not in string.punctuation: 
            y.append(i) 
 
    text = y[:] 
    y.clear() 
 
    for i in text: 
        y.append(ps.stem(i)) 

    return " ".join(y)

# Load TF-IDF vectorizer
tfidf = pickle.load(open('vectorizer.pkl','rb'))

# Load the models dictionary
models = pickle.load(open('Spam_classification_final_project.pkl', 'rb'))

#st.title("Email Spam or Ham Classifier")
st.title("Email Spam or Ham Classifier")
st.subheader("Welcome to our Spam or Ham Email Classifier app! Simply enter the text of the email you'd like to classify and choose a model to make a prediction.")

input_sms = st.text_area("Enter the Text", height=240)

selected_model = st.selectbox("Choose Model", list(models.keys()))

if st.button('Predict'):
    
    # 1. preprocess
    transformed_sms = transform_text(input_sms)
    # 2. vectorize
    vector_input = tfidf.transform([transformed_sms])
    # 3. predict using selected model
    result = models[selected_model].predict(vector_input)[0]
    # 4. Display
    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")
       
       
