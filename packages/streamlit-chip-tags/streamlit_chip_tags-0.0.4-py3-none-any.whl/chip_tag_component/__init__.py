import os
import streamlit as st
import streamlit.components.v1 as components

_RELEASE = True 

if not _RELEASE:
    _chips_tags = components.declare_component(

        "chips_tags",
        url="http://localhost:3001",

    )
else:
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _chips_tags = components.declare_component("chips_tags", path=build_dir)

def chips_tags(data=None, styles=None, title=None, default=None, key="foo"):
    """
    Args:
    - data: array of dicts
        args:
        - index
        - label
        - value
    - styles: css styles to add to html elements
    - title: title of the tags
    """

    value = _chips_tags(data=data, styles=styles, title=title, default=default, key=key)

    return value