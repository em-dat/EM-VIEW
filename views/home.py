import io
from typing import Any

import pandas as pd
import streamlit as st

from utils.layout import PAGE_HELP_TEXT


# Page functions
# --------------

@st.cache_data
def load_data(file: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Load data from EM-DAT xlsx file.

    Parameters
    ----------
    file: str
        The xlsx file to load the data from.

    Returns
    -------
    tuple: (pd.DataFrame, Dict[str, Any])
        Contains data and metadata extracted from the xlsx file.
        The first item is a DataFrame containing the data.
        The second item is a dictionary containing the metadata.

    """
    data = pd.read_excel(file, sheet_name=0)
    metadata = dict(
        pd.read_excel(file, sheet_name=1, header=None).values)
    return data, metadata


# Page content
# ------------

st.session_state['page'] = 'home'

st.header('EM-VIEW Disaster Dashboard')
st.write(PAGE_HELP_TEXT[st.session_state['page']])

uploaded_file = st.file_uploader(
    "Upload your EM-DAT xlsx file...",
    type=['xlsx'],
)

if uploaded_file:
    data, metadata = load_data(uploaded_file)
    st.success("File upload successful")
    ss = st.session_state
    ss['data'] = data
    ss['metadata'] = metadata
    ss['filename'] = uploaded_file.name
    region_data = data[['Region', 'Subregion', 'Country']].drop_duplicates()
    ss['region_list'] = [None] + sorted(region_data['Region'].unique())
    ss['subregion_list'] = [None] + sorted(region_data['Subregion'].unique())
    ss['country_list'] = [None] + sorted(region_data['Country'].unique())
    region_data.columns = [i.lower() for i in region_data.columns]
    ss['region_data'] = region_data
    buffer = io.StringIO()
    data.info(buf=buffer)
    ss['info'] = buffer.getvalue()

if "data" in st.session_state:
    # Display File Metadata
    exp1 = st.expander('**Metadata**')
    exp1.write(f"**Filename**: {st.session_state['filename']}")
    exp1.write(st.session_state['metadata'])
    exp1.text(st.session_state['info'])