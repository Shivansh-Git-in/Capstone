from pickle import FALSE
import streamlit as st
from streamlit_option_menu import option_menu

def show():
    with st.sidebar:
        st.markdown("""
                    # Features
                    """, unsafe_allow_html = False)
        selected = option_menu(
            menu_title = None, 
            
            options = ["Text", "Image"],
            icons = ["card-text", "image"],
            
            default_index = 0, 
        )
        return selected
    
