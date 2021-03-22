import io

import streamlit as st
import tabulator

import analyze_genders

uploaded_file = st.file_uploader('Input file for analysis', type='csv')

if uploaded_file is not None:
    file_like = io.BytesIO(uploaded_file.getvalue())
    genders = analyze_genders.load_data_file(file_like)
    analyze_genders.populate_genders(genders)
    df = analyze_genders.dataframe(genders)

    st.write(df)
