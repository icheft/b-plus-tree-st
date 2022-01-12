import re
import io
import pandas as pd
import bplus
import os
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import streamlit as st
from apps import user_input, bulk

LOGO_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/google/313/fire_1f525.png"
SORT_BY_POPULAR = 0
SORT_BY_RECENT = 1


# Set page title and favicon.
st.set_page_config(
    page_title="B+ Tree",
    page_icon=LOGO_URL, layout="centered",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': '''B+ Tree implementation by Friends. Do. Sports. Team'''
    }
)

apps = {"User Input": "cursor-text", "Bulk Input from Textfile": "upload"}

titles = [title.lower() for title in list(apps.keys())]
params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles.index(params["page"][0].lower()))
else:
    default_index = 0


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def sidebar():

    with st.sidebar:
        selected = option_menu("Menu", options=list(apps.keys()),
                               icons=list(apps.values()), menu_icon="house", default_index=default_index)
        max_degree = st.number_input(
            "Max Degree", min_value=3, max_value=10, step=1, value=3)
        if selected == "Bulk Input from Textfile":
            input_method = st.radio(
                "Build Method",
                ('One-by-one', 'Bottom-up'))
        else:
            input_method = None
    return selected, max_degree, input_method


def app():
    selected, max_degree, input_method = sidebar()
    if selected == "User Input":
        user_input.app(max_degree)
    elif selected == "Bulk Input from Textfile":
        bulk.app(max_degree, input_method)


if __name__ == '__main__':
    load_css("apps/style.css")
    lottie_yt = load_lottieurl(
        'https://assets4.lottiefiles.com/private_files/lf30_din9k7cf.json')
    st_lottie(lottie_yt, speed=.5, height=200, key="initial")

    app()
