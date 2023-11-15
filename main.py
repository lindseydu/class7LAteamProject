import streamlit as st
import importlib

# Dictionary of pages
pages = {
    "Q1 How many students have received the Pell grant?": "page1",
    "Q2 What are the most popular things?": "page2",
    "Q3 What does this program look like?": "page3"
    # Add more pages as needed
}

# Sidebar selection
page = st.sidebar.selectbox("Select the question you want answers for:", options=list(pages.keys()))

# Import the selected page module and call its show function
if page:
    page_module = importlib.import_module(pages[page])
    page_module.show()
