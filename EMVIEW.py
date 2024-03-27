import io
from datetime import date
from utils.layout import init_layout
import pandas as pd
import streamlit as st

from utils.sidebar import init_filters, filter_data


@st.cache_data
def load_data(file):
    data = pd.read_excel(uploaded_file, sheet_name=0)
    metadata = dict(
        pd.read_excel(uploaded_file, sheet_name=1, header=None).values)
    return data, metadata


# App
# ----

init_layout()

if "data" not in st.session_state:
    st.session_state["data"] = None
    st.session_state['is_filter'] = False

st.write("# EM-VIEW Disaster Dashboard")

st.write("""
**EM-VIEW** provides summarization and vizualisation features for your 
[**EM-DAT**](https://www.emdat.be) **International Disaster 
Database** dataset. 

EM-DAT contains data about **:earth_africa: global :collision: disaster 
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
    st.session_state['metadata'] = metadata
    st.session_state['filename'] = uploaded_file.name

# st.sidebar.subheader('Filters')

if st.session_state['data'] is not None:
    st.success("File upload successful")

    if not st.session_state['is_filter']:
        st.session_state['filter.start'] = data['Start Year'].min()
        st.session_state['filter.end'] = data['Start Year'].max()
        st.session_state["filter.clkey"] = ''
        st.session_state["filter.region"] = None
        st.session_state["filter.subregion"] = None
        st.session_state["filter.country"] = None
        st.session_state['region_data'] = data[
            ['Region', 'Subregion', 'Country']].drop_duplicates()
        st.session_state['is_filter'] = True

    init_filters()
    filter_data()

    exp1 = st.expander('**Medatata**')
    exp1.write(st.session_state['filename'])
    exp1.write(st.session_state['metadata'])
    data = st.session_state['data']
    buffer = io.StringIO()
    data.info(buf=buffer)
    s = buffer.getvalue()
    exp1.text(s)
