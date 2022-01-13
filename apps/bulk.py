import re
import io
import pydotplus
import pandas as pd
from datetime import datetime
import bplus
from io import StringIO
from PIL import Image
import os
import sys
import shutil
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import streamlit as st


@st.cache(allow_output_mutation=True)
def get_data():
    return []


def read_file():
    uploaded_file = st.file_uploader("Choose an input file")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

        # To read file as string:
        string_data = stringio.read()
        return string_data
    else:
        return None


def app(max_degree, input_method):

    st.title("B+ Tree Visualizer")
    raw_string = read_file()

    if 'data' not in st.session_state:
        st.session_state.data = []

    if raw_string is not None:
        tmp_keys = list(map(int, raw_string.strip().split()))
        # get_data().clear()
        st.session_state.data.clear()
        st.session_state.data.extend(tmp_keys)
        # get_data().extend(tmp_keys)

    row_input_1, row_input_2, row_input_3 = st.columns((4, 1, 1))
    with row_input_1:
        key = st.number_input("Key for Insertion", min_value=0, step=1)

    exist_key = False
    with row_input_2:
        if st.button("Insert", key=1):
            if key in st.session_state.data:
                exist_key = True
            else:
                exist_key = False
                # get_data().append(key)
                st.session_state.data.append(key)

    with row_input_3:
        if st.button("Reset"):
            # get_data().clear()
            st.session_state.data.clear()
            if raw_string is not None:
                tmp_keys = list(map(int, raw_string.strip().split()))
                st.session_state.data.extend(tmp_keys)

    if exist_key:
        st.warning("Key already exists")

    bplustree = bplus.vis.GraphableBPlusTree(order=max_degree)
    if (len(st.session_state.data) > 0):
        if input_method == "Bottom-up":
            # sort asceding
            keys = sorted(st.session_state.data, reverse=False)
            print(keys)
        else:
            keys = st.session_state.data
        for key in keys:
            bplustree.insert(key)

        g = bplustree.view_graph()
        st.graphviz_chart(g, use_container_width=True)

        graph = pydotplus.graph_from_dot_data(g.source)
        # graph = graphs[0]
        output_graphviz_png = graph.create_png()
        btn = st.download_button(
            label="Download Graph",
            data=output_graphviz_png,
            file_name=f"{datetime.now()}.png",
            mime="image/png"
        )
