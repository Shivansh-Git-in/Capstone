import streamlit as st
import sidebar
import textPage
import imagePage

page = sidebar.show()

if page=="Text":
    textPage.renderPage()

elif page=="Image":
    imagePage.renderPage()