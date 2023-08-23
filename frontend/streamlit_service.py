import streamlit as st
import json
import requests
import re

import pandas as pd
from pandas.api.types import is_categorical_dtype, is_numeric_dtype

import plotly.express as px
import osmnx as ox

def infer_data_types(df):
    for col in df.columns:
        if all(re.match(r'^-?\d+$', str(val)) for val in df[col]):
            df[col] = df[col].astype(int)
    return df

def lowercase_if_string(value):
    if isinstance(value, str):
        return value.lower()
    return value


def streamlit_service():
    option = st.selectbox('What do you want to do today?', 
    #TODO: Need to create more options that allows users to view different types of functions like graph format
    ("View all properties", 'Something else'))
    st.write("")
    modify = st.checkbox("Filter")

    if modify:
        modification_container = st.container()
        res = requests.get(url = "http://0.0.0.0:8000/dataviewer/properties")
        property_data = res.json()
        df = pd.DataFrame(property_data).convert_dtypes()
        infer_data_types(df)
    
        with modification_container:
            to_filter_columns = st.multiselect("Filter Dataframe on", df.columns)
            for cols in to_filter_columns:
                left, right = st.columns((1,20))
                if is_categorical_dtype(df[cols]):
                    user_cat_input = right.multiselect("Select the option(s)", df[cols].unique(),
                    default=list(df[cols].unique()),)
                    df = df[df[column].isin(user_cat_input)]
                elif is_numeric_dtype(df[cols]):
                    if st.checkbox(f"Choose between two values for {cols}", key=f"{cols}_numeric_checkbox"):
                        _min = int(df[cols].min())
                        _max = int(df[cols].max())
                        min_year = st.number_input(f"Min {cols}", min_value=_min, max_value=_max, value=_min)
                        max_year = st.number_input(f"Max {cols}", min_value=_min, max_value=_max, value=_max)
                        df = df[df[cols].between(min_year, max_year)]
                    else:
                        selection = st.selectbox("Choose an option", ("More Than", "Less Than", "Equals"), key=f"{cols}_numeric_selectbox")
                        _val = int(df[cols].min())
                        value = st.number_input(f"Building age more than {cols}", value=_val)
                        if selection == "More Than":
                            df = df[df[cols] >= value]
                        elif selection == "Less Than":
                            df = df[df[cols] >= value]
                        else:
                            df = df[df[cols] == value]
                else:
                    user_text_input = right.text_input(
                    f"Substring or regex in {cols}",
                    )
                    if user_text_input:
                        df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)
                        df = df[df[cols].astype(str).str.contains(user_text_input.lower())]
                        
    else:               
        res = requests.get(url = "http://0.0.0.0:8000/dataviewer/properties")
        property_data = res.json()
        df = pd.DataFrame(property_data)
        
    if st.button("Generate"):
        # st.dataframe(df)
        left_col, right_col = st.columns(2)
        
        # bar_chart = st.bar_chart(data=df.set_index('block_and_address')['price'])
        fig = px.bar(df, x='block_and_address', y='price', title='Price by Block', color='price',
                 color_continuous_scale='RdYlBu')
        
        left_col.plotly_chart(fig, use_container_width=True)
