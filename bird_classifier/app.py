import cv2
import joblib 
from skimage.feature import hog
import streamlit as st 
import numpy as np 

def load_model():
    return joblib.load("bird_classifier.pkl")
def predict(image):
    model,le=load_model()
    img=cv2.resize(image,(128,128))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    feature=hog(gray,pixels_per_cell=(8,8),cells_per_block=(2,2),feature_vector=True)
    feature=feature.reshape(1,-1)
    prediction=model.predict(feature)
    return le.inverse_transform(prediction)[0]
st.title("image classification with ml")
st.write("upload an image and model will classify it")
file=st.file_uploader("choose..",type=["jpg","png","jpeg"])
if file is not None:
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Classify Image"):
        result = predict(image)
        st.success(f"Predicted Class: {result}")