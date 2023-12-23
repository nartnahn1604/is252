import os
import re
import streamlit as st
import pandas as pd
from PIL import Image

def chosen_province(province, model):
    filename = f"denguefever_{model}_in_{province}.png"
    metric_filename = f"_denguefever_prediction_results_by_{model}_in_{province}.xlsx"
    if model == "CNN":
        model += "_lan4"
        filename = "1nstep_" + filename
        metric_filename = "0_6_nstep" + metric_filename

    visual_path = os.path.abspath(f"./predict_visualization/{model}/{filename}")
    st.session_state["visual"] = visual_path

    metric_path = os.path.abspath(f"./predict_metrics/{model}/{metric_filename}")
    metric_data = pd.read_excel(metric_path)
    metric_data = metric_data.drop(columns=["Unnamed: 0"])
    st.session_state["metrics"] = metric_data

if 'provinces' not in st.session_state:
    provinces = []
    for i in os.walk("./RNN/").__next__()[2]:
        result = re.search(r'_([^_]+)\.', i)
        if result:
            provinces.append(result.group(1))
    st.session_state["provinces"] = provinces

st.header("GROUP 8")

models = ["RNN", "CNN", "LSTM"]

if 'visual' not in st.session_state:
    chosen_province(st.session_state["provinces"][0], models[0])

with st.sidebar:
    province = st.selectbox("Province", st.session_state["provinces"])
    model = st.selectbox("Model", models)
    st.button("Load", on_click=chosen_province, args=[province, model])

with st.container():
    st.subheader("Predict result")
    st.image(Image.open(st.session_state['visual']))

    st.subheader("Metrics")
    st.dataframe(st.session_state["metrics"], use_container_width=True, hide_index=True)
# if st.session_state['reload'] and not st.session_state['reload']:
