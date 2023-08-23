import streamlit as st
from streamlit_service import streamlit_service

def streamlit_app():
    st.title("Property Data")
    streamlit_service()

if __name__ == "__main__":
    streamlit_app()