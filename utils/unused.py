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

def set_margin_top():
    """
    Sets the margin-top property for a specific HTML element using the
    Streamlit st.html method.

    Returns:
        None: This method does not return any value.
    """
    st.html("""
      <style>
        .st-emotion-cache-z5fcl4 {
          margin-top: -65px;
        }
      </style>
    """)
    return None