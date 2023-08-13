import streamlit as st
import json
import requests

def streamlit_service():
    option = st.selectbox('What do you want to do today?', 
    #TODO: Need to create more options that allows users to view different types of functions like graph format
    ("View all properties", 'Something else'))
    st.write("")

    if st.button("Generate") and option == "View all properties":
        res = requests.get(url = "http://0.0.0.0:8000/dataviewer/properties")
        property_data = res.json()

        st.write("Raw Data:")
        st.dataframe(property_data)