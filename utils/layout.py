import streamlit as st
def format_num(num):
    try:
        return f"{int(num):,}"
    except ValueError:
        return None

def init_layout():
    st.set_page_config(page_title="EM-VIEW", page_icon="🌍", layout='wide',
                       menu_items={
                           'Get Help': 'https://doc.emdat.be/',
                           'Report a bug': "https://github.com/dadelforge/EM-VIEW/issues",
                           'About': "This app has been developped at the University"
                                    " of Louvain by Damien Delforge, PhD, with the "
                                    "support of USAID"})
    #add_logo()
    set_margin_top()
    return None
def set_margin_top():
    st.markdown("""
      <style>
        .st-emotion-cache-z5fcl4 {
          margin-top: -65px;
        }
      </style>
    """, unsafe_allow_html=True)
    return None

def add_logo():
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://www.emdat.be/images/emdat.svg);
                background-repeat: no-repeat;
                background-size: 320px;
                padding-top: 20px;
                background-position: 20px 20px;
            }
        </style>
        """, unsafe_allow_html=True, )
    return None