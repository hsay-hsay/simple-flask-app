import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import base64
import streamlit_authenticator as stauth
import pickle
from pathlib import Path

names = ["admin"]
usernames = ["admin"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)
    
credentials = {
    "usernames":{
        usernames[0]:{
            "name":names[0],
            "password":hashed_passwords[0]
            }         
        }
}

authenticator = stauth.Authenticate(credentials, "sample_app", "abcd", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:

    @st.cache
    def get_data(file_path):
        return pd.read_csv(file_path)
        
    st.title('Streamlit Tasks')
    authenticator.logout("Logout", "main")

    # use image from url for background
    def add_bg_from_url():
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("https://cdn.britannica.com/79/4679-050-BC127236/Titanic.jpg");
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    add_bg_from_url() 

    # use local image for background
    # def add_bg(image_file):
    #     with open(image_file, "rb") as image_file:
    #         encoded_string = base64.b64encode(image_file.read())
    #     st.markdown(
    #     f"""
    #     <style>
    #     .stApp {{
    #         background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
    #         background-size: cover;
    #         opacity:0.8;
    #     }}
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    #     )
    # add_bg('./data/nice_boat.jpg')

    st.markdown(
        """
        <style>
        .block-container {
            background-color: #F5F5F5;
            opacity: 0.95;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    df = get_data('Titanic-Dataset.csv')

    dataset = st.container()
    pie_chart = st.container()
    bar_plot = st.container()
    image = st.container()

    with dataset:
        st.subheader('The Dataset')
        st.write('The dataset contains information about passengers aboard the RMS Titanic dataset.')
        
        button = st.button("Display Dataset")
        
        if button:
            st.write(df.head(10))
        
    with pie_chart:
        st.subheader('Port of Embarkation')
        st.write('Distribution of passengers based on the port of embarkation.')
        embarked = df.Embarked
        # st.write(embarked.head(10))
        vc = embarked.value_counts()
        temp = {'C':'Cherbourg', 'Q':'Queenstown', 'S':'Southampton'}
        labels = [temp[i] for i in vc.keys()]
        values = vc.values
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        st.plotly_chart(fig)
        
    with bar_plot:
        st.subheader('Sex')
        st.write('Distribution of passengers based on their genders.')
        sex = df.Sex
        vc = sex.value_counts()
        labels, values = vc.keys(), vc.values
        fig = go.Figure(data=[go.Bar(x=labels, y=values,marker=dict(color=['lightblue','lightgreen']))])
        fig.update_layout(xaxis_title='Sex',
                        yaxis_title='Count',
                        legend_title='Legend')
        st.plotly_chart(fig)
