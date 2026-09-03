import streamlit as st

st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] {
        background-color: #F0F4FA;
        padding-top: 1rem;
    }
    [data-testid="stSidebarNav"] a {
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        margin: 0.15rem 0.5rem;
        font-weight: 500;
    }
    [data-testid="stSidebarNav"] a:hover {
        background-color: #DCE6F5;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: #1F3B73;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] span {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)