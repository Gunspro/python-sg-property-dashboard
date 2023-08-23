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
        res = requests.get(url = "http://0.0.0.0:8000/dataviewer/properties")
        property_data = res.json()
        df_all = pd.DataFrame(property_data)

        if df['number_of_rooms'].nunique() == 1:
            df_all = df_all[df_all['number_of_rooms'] == df['number_of_rooms'].iloc[0]]

        fig = px.bar(df, x='block_and_address', y='price', title='Bar Chart Price by Block', color='price',
                 color_continuous_scale='RdYlBu')
        st.plotly_chart(fig)

        left_col, right_col = st.columns(2)
        combined_df = df_all.merge(df, on=cols, how='left', suffixes=('', '_filtered'))
        
        fig = px.scatter(
        df_all,
        x="price",
        y="floor_size",
        title="Overview of prices of HDB flats compared to your desired input",
        color="price",
        color_continuous_scale='Viridis', 
        hover_data=['block_and_address', 'number_of_rooms'],
        )

      
        fig.update_traces(
        marker=dict(size=8, opacity=0.2),  
        selector=dict(mode='markers') 
        )

        if not df.empty:

            filtered_trace = px.scatter(
                df,
                x="price",
                y="floor_size",
                color="price",
                hover_data=['block_and_address', 'number_of_rooms'],
                color_continuous_scale='Viridis',  
            ).data[0]

            filtered_trace.update(marker=dict(size=12)) 
            

            fig.add_trace(filtered_trace)

        fig2 = px.scatter(df, x="block_and_address", y="price", title="Price by Block", color='floor_size', color_continuous_scale='RdYlBu')
        
        left_col.plotly_chart(fig, use_container_width=True)
        right_col.plotly_chart(fig2, use_container_width=True)