import pandas as pd
import streamlit as st

DOC_URI = "https://doc.emdat.be/docs"
CLASSIF_KEY_DOC_URI = (
    f"{DOC_URI}/data-structure-and-content/disaster-classification-system/"
    f"#main-classification-tree"
)


def init_sidebar_filters() -> None:
    """Initialize sidebar filters."""
    ss = st.session_state

    # Not having session states mean that data has not been uploaded and that
    # filters should be disabled.
    filters_disabled = "data" not in ss

    # Set default if data
    if not filters_disabled:

        # Initialize filters once enabled
        if "filter.disabled" not in st.session_state:
            set_filters_to_default()

        col1, col2 = st.sidebar.columns(2)

        col1.number_input(
            label='**Start year**',
            min_value=ss["filter.year_min"],
            max_value=ss["filter.year_max"],
            key='filter.start'
        )

        col2.number_input(
            label='**End year**',
            min_value=ss["filter.year_min"],
            max_value=ss["filter.year_max"],
            key='filter.end'
        )

        st.sidebar.text_input(
            label="**Classification Key**",
            key="filter.classification_key",
            help="Enter the key or its initial part to filter"
        )
        st.sidebar.caption(
            f"_Check classification keys [here]({CLASSIF_KEY_DOC_URI})._"
        )

        st.sidebar.selectbox(
            label="**Region**",
            options=ss['region_list'],
            key="filter.region",
            format_func=lambda x: 'All' if x is None else x,
            on_change=process_region
        )

        st.sidebar.selectbox(
            label="**Subregion**",
            options=ss['subregion_list'],
            key="filter.subregion",
            format_func=lambda x: 'All' if x is None else x,
            on_change=process_subregion
        )

        st.sidebar.selectbox(
            label="**Country**",
            options=ss['country_list'],
            key="filter.country",
            format_func=lambda x: 'All' if x is None else x,
            on_change=process_country
        )

        st.sidebar.button(
            "Reset",
            type="primary",
            on_click=set_filters_to_default
        )

        st.sidebar.divider()


def process_region() -> None:
    """Process region and update other levels accordingly."""
    ss = st.session_state
    rd = ss['region_data']
    region = ss['filter.region']
    subregion = ss['filter.subregion']
    country = ss['filter.country']
    if region:
        valid_data = rd[rd['region'] == region]
        if subregion not in valid_data['subregion']:
            ss['filter.subregion'] = None
        if country not in valid_data['country']:
            ss['filter.country'] = None
        ss['subregion_list'] = [None] + sorted(valid_data['subregion'].unique())
        ss['country_list'] = [None] + sorted(valid_data['country'].unique())
    else:
        ss['filter.subregion'] = None
        ss['filter.country'] = None
        ss['subregion_list'] = [None] + sorted(rd['subregion'].unique())
        ss['country_list'] = [None] + sorted(rd['country'].unique())

def process_subregion() -> None:
    """Process subregion and update other levels accordingly."""
    ss = st.session_state
    rd = ss['region_data']
    region = ss['filter.region']
    subregion = ss['filter.subregion']
    country = ss['filter.country']
    if subregion:
        valid_data = rd[rd['subregion'] == subregion]
        if region not in valid_data['region']:
            ss['filter.region'] = valid_data.iloc[0]['region']
        if country not in valid_data['country']:
            ss['filter.country'] = None
        ss['country_list'] = [None] + sorted(valid_data['country'].unique())
    else:
        ss['filter.country'] = None
        if region:
            valid_data = rd[rd['region'] == region]
            ss['country_list'] = [None] + sorted(valid_data['country'].unique())
        else:
            ss['country_list'] = [None] + sorted(rd['country'].unique())


def process_country() -> None:
    """Process country and update other levels accordingly."""
    ss = st.session_state
    rd = ss['region_data']
    region = ss['filter.region']
    subregion = ss['filter.subregion']
    country = ss['filter.country']
    if country:
        valid_data = rd[rd['country'] == country]
        if region not in valid_data['region']:
            ss['filter.region'] = valid_data.iloc[0]['region']
        if subregion not in valid_data['subregion']:
            ss['filter.subregion'] = valid_data.iloc[0]['subregion']


def get_filtered_data() -> pd.DataFrame:
    """Get filtered data based on filters session states"""
    ss = st.session_state

    # Get filters states
    start = ss["filter.start"]
    end = ss["filter.end"]
    classification_key = ss["filter.classification_key"].strip()
    region = ss["filter.region"]
    subregion = ss["filter.subregion"]
    country = ss["filter.country"]

    # Initiate filtering
    data_filtered = ss['data'].copy()

    # Filter by year
    data_filtered = data_filtered[
        (data_filtered['Start Year'] >= start) &
        (data_filtered['End Year'] <= end)
        ]

    # Filter by classification key
    data_filtered = data_filtered[
        data_filtered['Classification Key'].str.match(
            classification_key.replace('*', '.*')
        )
    ]

    # Filter by region, subregion, country
    if region:
        data_filtered = data_filtered[data_filtered['Region'] == region]
    if subregion:
        data_filtered = data_filtered[data_filtered['Subregion'] == subregion]
    if country:
        data_filtered = data_filtered[data_filtered['Country'] == country]

    return data_filtered


def set_filters_to_default() -> None:
    """Set or reset filters to default values"""
    ss = st.session_state
    data = ss["data"]
    rd = ss['region_data']
    ss['filter.disabled'] = False
    year_min = data['Start Year'].min()
    year_max = data['Start Year'].max()
    ss['filter.year_min'] = year_min
    ss['filter.year_max'] = year_max
    ss['filter.start'] = year_min
    ss['filter.end'] = year_max
    ss['filter.region'] = None
    ss['filter.subregion'] = None
    ss['filter.country'] = None
    ss['region_list'] = [None] + sorted(rd['region'].unique())
    ss['subregion_list'] = [None] + sorted(rd['subregion'].unique())
    ss['country_list'] = [None] + sorted(rd['country'].unique())
