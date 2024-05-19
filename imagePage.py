import streamlit as st
from PIL import Image
import modals
import numpy as np


getEmoji = {
    "happy" : "😊",
    "neutral" : "😐",
    "sad" : "😔",
    "disgust" : "🤢",
    "surprise" : "😲",
    "fear" : "😨",
    "angry" : "😡",
}
    
    
def showEmotionData(emotion, topEmotion, image, idx):
    x, y, w, h = tuple(emotion["box"])
    cropImage = image[y:y+h, x:x+w]
    
    cols = st.columns(7)
    keys = list(emotion["emotions"].keys())
    values = list(emotion["emotions"].values())
    emotions = sorted(emotion["emotions"].items(), key =
             lambda kv:(kv[1], kv[0]))
                
    st.components.v1.html("""
                                <h3 style="color: #ef4444; font-family: Source Sans Pro, sans-serif; font-size: 20px; margin-bottom: 0px; margin-top: 0px;">Person detected {}</h3>
                                """.format(idx), height=30)
    col1, col2, col3 = st.columns([3,1,2])
    
    with col1:
        st.image(cropImage, width=200)
    with col2:
        st.metric(keys[0].capitalize()+" "+getEmoji[keys[0]], round(values[0], 2), None)
        st.metric(keys[1].capitalize()+" "+getEmoji[keys[1]], round(values[1], 2), None)
        st.metric(keys[2].capitalize()+" "+getEmoji[keys[2]], round(values[2], 2), None)
        st.metric(keys[3].capitalize()+" "+getEmoji[keys[3]], round(values[3], 2), None)
        
    with col3:
        st.metric(keys[4].capitalize()+" "+getEmoji[keys[4]], round(values[4], 2), None)
        st.metric(keys[5].capitalize()+" "+getEmoji[keys[5]], round(values[5], 2), None)
        st.metric(keys[6].capitalize()+" "+getEmoji[keys[6]], round(values[6], 2), None)
        st.metric("Top Emotion", emotions[len(emotions)-1][0].capitalize()+" "+getEmoji[topEmotion[0]], None)
        
        
    st.components.v1.html("""
                                <hr>
                                """, height=5)


        
        
# @st.cache
def load_image(image_file):
    image = Image.open(image_file, 'r')
    return image
    
    
def clickImage():
    img_file_buffer = st.camera_input("Take a picture")
    
    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        image_np = np.array(Image.open(img_file_buffer))
        emotions, topEmotion, _ = modals.imageEmotion(image_np)
        
        
        if emotions is not None:
            with st.expander("Expand to see individual result"):
                with st.container():
                    contentcopy = Image.fromarray(image_np)
                    contentcopy = np.array(contentcopy)
                    for i in range(len(emotions)):
                        showEmotionData(emotions[i], topEmotion, contentcopy, i + 1)

            st.write("")
            st.write("")
            col1, col2 = st.columns([4, 2])

            with col1:
                st.image(image_np, width=300)

            with col2:
                st.metric("Top Emotion", topEmotion[0].capitalize() + " " + getEmoji[topEmotion[0]], None)
                st.metric("Emotion Percentage", str(round(topEmotion[1] * 100, 2)), None)
    else:
        emotions = None


def uploadFile():
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    print("Uploaded File :", uploaded_file)
    if uploaded_file is not None:
        content = Image.open(uploaded_file)
        content = np.array(content)
        shape = np.shape(content)
        if len(shape)<3:
            st.error('Your image has a bit-depth less than 24. Please upload an image with a bit-depth of 24.')
            return
        
        emotions, topEmotion, image = modals.imageEmotion(content)

    else:
        emotions = None

    if emotions is not None and len(emotions)==0:
        st.text("No faces found!!") 
    if emotions is not None:
        # Showcasing result
        with st.expander("Expand to see individual result"):
            with st.container():
                st.write("")
                st.write("")
                contentcopy = Image.open(uploaded_file)
                contentcopy = np.array(contentcopy)
                for i in range (len(emotions)):
                    showEmotionData(emotions[i], topEmotion, contentcopy, i+1)
        
        
        st.write("")
        st.write("")
        col1, col2 = st.columns([4,2])
        
        with col1:
            st.image(image, width=300)
        with col2:
            st.metric("Top Emotion", topEmotion[0].capitalize() + " " + getEmoji[topEmotion[0]], None)
            st.metric("Emotion Percentage", str(round(topEmotion[1]*100, 2)), None)
        

def renderPage():
    st.title("Sentiment Analysis")
    
    st.subheader("Facial Emotion Analysis")
    st.text("Input an image and to find emotions in it.")
    st.text("")
    option = st.selectbox(
     'How would you like to provide an image ?',
     ('Upload','Click image'))
    
    if option=="Upload":
        uploadFile()
    elif option=="Click image":
        clickImage()