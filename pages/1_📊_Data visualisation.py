import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as pe

@st.cache_data
def load_data(file):
    return pd.read_csv(file)



    
# Home page content goes here
st.title("Data Analysis App")
# You can add more content or widgets for the Home page
    

file = st.file_uploader("Choose a file", type=['csv'])

if file is not None:
    data = load_data(file)
    rows = st.slider("Choose number of rows to display", 0, len(data), 10)
    columns = st.multiselect("Select columns", data.columns, default=data.columns.to_list())
    st.write(data[:rows][columns])

    metadata, statistics = st.tabs(["Metadata", "Statistics"])
    with metadata:
        info = st.selectbox("Choose info to display", ["Shape", "Types", "Info"])
        info_btn = st.button("Show Informations")
        if info_btn:
            if info == "Shape":
                st.write(data.shape)
            elif info == "Types":
                st.write(data.dtypes)
            elif info == "Info":
                st.write(data.info())
    with statistics:
        stat = st.selectbox("Choose static to display", ["Data Decription", "Value Counts", "Duplicate Rows"])
        stat_btn = st.button("Show statistics")
        if stat_btn:
            if stat == "Data Decription":
                st.write(data.describe())
            elif stat == "Value Counts":
                st.write(data.value_counts())
            elif stat == "Duplicate Rows":
                st.write(data.duplicated().sum())

    numerical_columns = data.select_dtypes(include=np.number).columns.to_list()
    categorical_columns = data.select_dtypes(exclude=np.number).columns.to_list()

    tab1, tab2, tab3, tab4 = st.tabs(["Scatter Plot", "Histogram", "Bar plot", "Box plot"])
        
        
    with tab1:
        x_axis, y_axis, color_col = st.columns(3)
        none = ["None"]
        with x_axis:
            selectX = st.selectbox("Select x-axis column", numerical_columns)
        with y_axis:
            selectY = st.selectbox("Select y-axis column", numerical_columns)
        with color_col:
            selectC = st.selectbox("Select color column", none + data.columns.to_list())
        scatter = pe.scatter(data, x=selectX, y=selectY, color=selectC if selectC != 'None' else None)
        st.plotly_chart(scatter)



    with tab2:
        axis = st.selectbox("Select axis column", numerical_columns)
        hist = pe.histogram(data, x=axis)
        st.plotly_chart(hist)



    with tab3:
        x_axis, y_axis, color_col = st.columns(3)
        none = ["None"]
        options = none + numerical_columns
        with x_axis:
            selectX = st.selectbox("Select x-axis column", categorical_columns, key="x")
        with y_axis:
            selectY = st.selectbox("Select y-axis column", options, key="y")
        with color_col:
            selectC = st.selectbox("Select color column", none + data.columns.to_list(), key="col")
        if selectY != 'None':
            bar = pe.bar(data, x=selectX, y=selectY, color=selectC if selectC != 'None' else None)
        else:
            bar = pe.bar(data, x=selectX, color=selectC if selectC != 'None' else None)
        st.plotly_chart(bar)



    with tab4:
        x_axis, y_axis, color_col = st.columns(3)
        none = ["None"]
        with x_axis:
            selectX = st.selectbox("Select x-axis column", categorical_columns, key="x_axis")
        with y_axis:
            selectY = st.selectbox("Select y-axis column", numerical_columns, key="y_axis")
        with color_col:
            selectC = st.selectbox("Select color column", none + data.columns.to_list(), key="color")
        box = pe.box(data, x=selectX, y=selectY, color=selectC if selectC != 'None' else None)
        st.plotly_chart(box)


