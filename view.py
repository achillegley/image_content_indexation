import streamlit as st
import os
from PIL import Image
import numpy as np
import pandas as pd
import pickle
import tensorflow
from sklearn.neighbors import NearestNeighbors
import searcher
from numpy.linalg import norm
import cv2

st.title('POSTE DE CADASTRE')

def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join('uploads',uploaded_file.name),'wb') as f:
            f.write(uploaded_file.getbuffer())
        return 1
    except:
        return 0


def make_clickable(i):
    theLink="images/" + (str(i)).split('/')[1]
    return '<a href="http://127.0.0.1:8003/'+str(theLink)+'"  target="_blank">'+str((str(i)).split('/')[1])+'</a>'

# steps
# file upload -> save
uploaded_file = st.file_uploader("Veuiller choisir une image")
if uploaded_file is not None:
    if save_uploaded_file(uploaded_file):
        # display the file
        display_image = Image.open(uploaded_file)
        st.image(display_image)
        result={}
        result=searcher.true_final_search(uploaded_file.name)
        first_result=list(result.keys())[0]
        st.subheader("Le premier document trouvé")
        display_first_result = Image.open("images/"+(str(first_result)).split('/')[1])
        st.image(display_first_result)
        st.subheader("Liste des documents proches")
        print(result)
        df = pd.DataFrame(
            {
                "Documents": list(result.keys()),
                'Action': [make_clickable(i) for i in list(result.keys()) ]
            })
        df = df.to_html(escape=False)
        st.write(df, unsafe_allow_html=True)
        #st.table(df)
    else:
        st.header("Some error occured in file upload")
