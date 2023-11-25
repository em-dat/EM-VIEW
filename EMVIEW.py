import io
from datetime import date

import pandas as pd
import streamlit as st

from utils.sidebar import init_filters, filter_data

st.set_page_config(page_title="EM-VIEW", page_icon="🌍", layout='wide',
                   menu_items={
                       'Get Help': 'https://www.extremelycoolapp.com/help',
                       'Report a bug': "https://www.extremelycoolapp.com/bug",
                       'About': "# This is a header. This is an *extremely* cool app!"})

@st.cache_data
def load_data(file):
    data = pd.read_excel(uploaded_file, sheet_name=0)
    metadata = dict(
        pd.read_excel(uploaded_file, sheet_name=1, header=None).values)
    return data, metadata


# App
# ----

if "data" not in st.session_state:
    st.session_state["data"] = None
    st.session_state["region_data"] = None
    st.session_state["columns"] = None
    st.session_state["start"] = 2000
    st.session_state["end"] = date.today().year
    st.session_state["clkey"] = ""
    st.session_state["region"] = None
    st.session_state["subregion"] = None
    st.session_state["country"] = None

st.write("# EM-VIEW Disaster Dashboard")

st.write("""
**EM-VIEW** provides summarization and vizualisation features for your 
[EM-DAT](https://www.emdat.be) dataset. The **EM-DAT International Disaster 
Database** contains data about **:earth_africa: global :collision: disaster 
occurrence and impact**. 
1. EM-DAT data is freely accessible for non-commercial use after registration at 
[public.emdat.be](https://public.emdat.be). 
2. Uploading your EM-DAT data file (:point_down: below).
3. Use the **EM-VIEW** pages (:point_left: sidebar) to access summary statistics, 
tabular data, maps, and time series.  
4. Change the scope of your analysis using the :point_left: sidebar filters.
         """)
st.write("## Upload your EM-DAT file")

uploaded_file = st.file_uploader("Upload your EM-DAT xlsx file...")

if uploaded_file is not None:
    data, metadata = load_data(uploaded_file)
    st.session_state['data'] = data
    st.session_state['start'] = int(data['Start Year'].min())
    st.session_state['end'] = int(data['Start Year'].max())
    st.session_state['region_data'] = data[
        ['Region', 'Subregion', 'Country']].drop_duplicates()
    st.session_state['metadata'] = metadata
    st.session_state['filename'] = uploaded_file.name
    filter_data()

st.sidebar.subheader('Filters')

if st.session_state['data'] is not None:
    data = st.session_state['data']
    st.success("File upload successful")
    exp1 = st.expander('**Medatata**')
    exp1.write(st.session_state['filename'])
    exp1.write(st.session_state['metadata'])
    buffer = io.StringIO()
    data.info(buf=buffer)
    s = buffer.getvalue()
    exp1.text(s)
    init_filters()
    #st.write(st.session_state)
