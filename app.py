import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="AI Data Analyst Assistant",
    initial_sidebar_state="collapsed"
)


st.title("AI Data Analyst Assisstant")
st.subheader("Put your data| Get insights | Improve Decision")

st.subheader("Upload your dataset")

file = st.file_uploader('Upload csv files')

if file:
    df = pd.read_csv(file)


    st.session_state["df"] = df


    st.write("File uploaded successfully")

    st.dataframe(df)


    rows , columns = df.shape

    col1 , col2 = st.columns(2)
    
    with col1:
        if st.button("Check for rows"):
             st.metric("Rows" , rows)
    
    
    with col2:
         if st.button("Check for number of columns"):
             st.metric("Columns", columns)

    if st.button("Let's move to data cleaning ->"):
        st.switch_page("pages/01_data_cleaning.py")
