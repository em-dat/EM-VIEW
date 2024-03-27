import streamlit as st

from utils.sidebar import init_filters, filter_data
from utils.layout import init_layout

init_layout()

if st.session_state['data'] is None:
    st.error('Please, upload your dataset first on the main page', icon="🚨")
else:
    data = st.session_state['data_filtered']
    init_filters()
    st.header('EM-DAT Table')
    columns = st.multiselect("Columns:", data.columns,
                             default=["DisNo.", "Country", "Disaster Type",
                                      "Total Deaths", "Total Affected",
                                      "Total Damage, Adjusted ('000 US$)"])

    display_rows = 15
    st.dataframe(data[columns], height=(display_rows + 1) * 35 + 3,
                 use_container_width=True)
