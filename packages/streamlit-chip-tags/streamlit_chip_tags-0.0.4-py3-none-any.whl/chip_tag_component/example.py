import streamlit as st
from __init__ import chips_tags

st.set_page_config(layout="centered")

title="Probability Equipment will be in category"
data = [
            {"index":0, "label":"Attack", "value":""},
            {"index":1, "label":"Magic", "value":""},
            {"index":2, "label":"Defense", "value":""},
            {"index":3, "label":"Movement", "value":""},
            {"index":4, "label":"Roaming", "value":""},
            {"index":5, "label":"Jungling", "value":""},
        ]

styles_ = {
    "chips-container": {
        "white-space":"wrap",
        "display":"flex",
        "flex-direction":"row",
        "justify-content":"flex-start",
        "align-items":"flex-start",
        "flex-wrap":"wrap",
        "row-gap":"5px"
    },
    # "the-chip": {
    #     "flex":"1"
    # }
}

cols = st.columns([3,4])
with cols[0]:
    val_ = chips_tags(data, styles=styles_, title=None)

with cols[1]:
    st.subheader("James is here")


