import streamlit as st


def load_css():

    st.markdown("""
    <style>

    /* --------------------------------------------------
       Hide Streamlit Default Navigation
    -------------------------------------------------- */

    [data-testid="stSidebarNav"]{
        display:none !important;
    }

    [data-testid="stSidebarNavItems"]{
        display:none !important;
    }

    /* --------------------------------------------------
       Main App
    -------------------------------------------------- */

    .stApp{
        background:#0F172A;
        color:#F8FAFC;
    }

    /* --------------------------------------------------
       Sidebar
    -------------------------------------------------- */

    section[data-testid="stSidebar"]{
        background:#1E293B;
    }

    /* --------------------------------------------------
       Buttons
    -------------------------------------------------- */

    .stButton > button{

        width:100%;
        border-radius:12px;
        border:none;
        padding:12px;
        font-weight:600;
        transition:0.3s;
    }

    .stButton > button:hover{
        transform:scale(1.02);
    }

    /* --------------------------------------------------
       Cards
    -------------------------------------------------- */

    div[data-testid="metric-container"]{

        background:#1E293B;

        border:1px solid #334155;

        border-radius:14px;

        padding:18px;
    }

    /* --------------------------------------------------
       Inputs
    -------------------------------------------------- */

    textarea,
    input{

        border-radius:10px !important;

    }

    </style>
    """, unsafe_allow_html=True)