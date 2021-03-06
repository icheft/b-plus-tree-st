import re
import io
import pandas as pd
from datetime import datetime
import pydotplus
import bplus
import os
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import streamlit as st
import pandas as pd


@st.cache(allow_output_mutation=True)
def get_data():
    return []


# @st.cache(allow_output_mutation=True)
# def tree(max_degree=3):
#     return bplus.vis.GraphableBPlusTree(order=max_degree)


def app(max_degree):
    # If no, then initialize count to 0
    # If count is already initialized, don't do anything
    if 'data' not in st.session_state:
        st.session_state.data = []

    st.title("B+ Tree Interactive Visualizer")
    # bplustree = tree(max_degree)
    row_input_1, row_input_2, row_input_3 = st.columns(
        (4, 1, 1))
    with row_input_1:
        key = st.number_input(
            "Key for Insertion/Deletion", min_value=0, step=1)

    exist_key = False
    with row_input_2:
        if st.button("Insert"):
            if key in st.session_state.data:
                exist_key = True
            else:
                exist_key = False
                st.session_state.data.append(key)
            # get_data().append(key)
            # bplustree.insert(key)

    with row_input_3:
        if st.button("Clear"):
            # for k in get_data():
            #     bplustree.delete(k)
            # get_data().clear()
            st.session_state.data.clear()
            # bplustree.clean(max_degree)

    # with row_input_4:
    #     # st.write(get_data())
    #     delete_key = None
    #     if st.button("Delete"):
    #         delete_key = key
    #         bplustree.delete(delete_key)
    #         get_data().remove(delete_key)

    # if (len(get_data()) > 0):
    #     g = bplustree.view_graph()
    #     st.graphviz_chart(g, use_container_width=True)
    #     graphs = pydot.graph_from_dot_data(g.source)
    #     graph = graphs[0]
    #     output_graphviz_png = graph.create_png()
    #     btn = st.download_button(
    #         label="Download Graph",
    #         data=output_graphviz_png,
    #         file_name=f"{datetime.now()}.png",
    #         mime="image/png"
    #     )

    if exist_key:
        st.warning("Key already exists")

    bplustree = bplus.vis.GraphableBPlusTree(order=max_degree)
    if (len(st.session_state.data) > 0):
        for key in st.session_state.data:
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
