import streamlit as st

from utils.filters import get_filtered_data
from utils.layout import PAGE_HELP_TEXT

DEFAULT_COLUMNS = [
    "DisNo.",
    "Country",
    "Disaster Type",
    "Total Deaths",
    "Total Affected",
    "Total Damage, Adjusted ('000 US$)"
]

st.session_state["page"] = "table"

if "data" not in st.session_state:
    st.error('Please, upload your dataset first on the main page', icon="🚨")
else:
    data = get_filtered_data()
    st.header('Table View')

    columns = st.multiselect(
        "Select columns:",
        data.columns,
        default=DEFAULT_COLUMNS
    )

    display_rows = 15
    st.dataframe(
        data[columns],
        height=(display_rows + 1) * 35 + 3,
        use_container_width=True
    )
    # Page Help
    # ---------
    with st.expander("See page details", expanded=False,
                     icon=':material/info:'):
        st.markdown(PAGE_HELP_TEXT[st.session_state.page])