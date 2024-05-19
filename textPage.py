import streamlit as st
from textblob import TextBlob
from PIL import Image

    
def getPolarity(userText):
    tb = TextBlob(userText)
    polarity = round(tb.polarity, 2)
    subjectivity = round(tb.subjectivity, 2)
    if polarity>0:
        return polarity, subjectivity, "Positive"
    elif polarity==0:
        return polarity, subjectivity, "Neutral"
    else:
        return polarity, subjectivity, "Negative"

def getSentiments(userText, type):
    polarity, subjectivity, status = getPolarity(userText)
    if(status=="Positive"):
        image = Image.open('./images/positive.PNG')
    elif(status == "Negative"):
        image = Image.open('./images/negative.PNG')
    else:
        image = Image.open('./images/neutral.PNG')
    col1, col2, col3 = st.columns(3)
    col1.metric("Polarity", polarity, None)
    col2.metric("Subjectivity", subjectivity, None)
    col3.metric("Result", status, None)
    st.image(image, caption=status)
        

def renderPage():
    st.title("Sentiment Analysis")
    
    st.subheader("User Input Text Analysis")
    st.text("Analyzing text data given by the user to find sentiments within it.")
    st.text("")
    userText = st.text_input('User Input', placeholder='Input text HERE')
    st.text("")
   
    if st.button('Predict'):
        if(userText!="" and type!=None):
            st.text("")
            getSentiments(userText, type)
            