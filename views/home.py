import io
from typing import Any

import pandas as pd
import requests
import streamlit as st

from utils.layout import PAGE_HELP_TEXT
from utils.filters import set_filters_to_default
from utils.archload import ARCHIVE_ENDPOINT, ARCHIVE_PARAMS, ARCHIVE_METADATA
from utils.apiload import API_ENDPOINT, BASE_QUERY, DATA_FIELDS, COLUMN_MAP, \
    API_METADATA


# Page functions
# --------------

@st.cache_data
def load_data(
        file: str,
        metadata: dict | None = None
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Load data from EM-DAT xlsx file.

    Parameters
    ----------
    file: str
        The xlsx file to load the data from.
    metadata: dict, optional
        The metadata dictionary. If None (default), metadata is loaded from the
        xlsx file.

    Returns
    -------
    tuple: (pd.DataFrame, Dict[str, Any])
        Contains data and metadata extracted from the xlsx file.
        The first item is a DataFrame containing the data.
        The second item is a dictionary containing the metadata.

    """
    data = pd.read_excel(file, sheet_name=0)
    if metadata is None:
        metadata = dict(
            pd.read_excel(file, sheet_name=1, header=None).values)

    return data, metadata

@st.cache_data
def load_from_archive() -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Load data from the EM-DAT archive using the Dataverse API.

    Returns
    -------
    tuple: (pd.DataFrame, Dict[str, Any])
        Contains data and metadata extracted from the archive.
    """
    try:
        response = requests.get(ARCHIVE_ENDPOINT, params=ARCHIVE_PARAMS)
        response.raise_for_status()
        content = io.BytesIO(response.content)
        return load_data(content, ARCHIVE_METADATA)
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to load data from archive: {e}")
        return pd.DataFrame(), {}
    except Exception as e:
        st.error(f"An error occurred while processing archive data: {e}")
        return pd.DataFrame(), {}


@st.cache_data
def load_from_api(api_key: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Load data from the EM-DAT API using the provided API key.

    Parameters
    ----------
    api_key: str
        The EM-DAT API key.

    Returns
    -------
    tuple: (pd.DataFrame, Dict[str, Any])
        Contains data and metadata fetched from the API.
    """
    try:
        fields = '\n    '.join(DATA_FIELDS)
        query = BASE_QUERY.format(
            api_key=api_key,
            include_fields=fields
        )
        headers = {'Authorization': f'{api_key}'}
        response = requests.get(API_ENDPOINT, json={"query": query},
                                headers=headers)
        response.raise_for_status()
        data = response.json()['data']['public_emdat']['data']
        data = pd.DataFrame(data)
        data = data[COLUMN_MAP.keys()]
        data.rename(columns=COLUMN_MAP, inplace=True)
        return data, API_METADATA
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to load data from API: {e}")
        return pd.DataFrame(), {}
    except Exception as e:
        st.error(f"An error occurred while processing API data: {e}")
        return pd.DataFrame(), {}


def process_data(data: pd.DataFrame, metadata: dict[str, Any], filename: str) -> None:
    """
    Process the loaded data and update session state.

    Parameters
    ----------
    data: pd.DataFrame
        The loaded disaster data.
    metadata: dict[str, Any]
        Metadata associated with the dataset.
    filename: str
        Name of the source file or data source.
    """
    if data.empty:
        return

    st.success(f"Data loaded successfully from {filename}")
    ss = st.session_state
    ss['data'] = data
    ss['metadata'] = metadata
    ss['filename'] = filename
    region_data = data[['Region', 'Subregion', 'Country']].drop_duplicates()
    ss['region_list'] = [None] + sorted(region_data['Region'].unique())
    ss['subregion_list'] = [None] + sorted(region_data['Subregion'].unique())
    ss['country_list'] = [None] + sorted(region_data['Country'].unique())
    region_data.columns = [i.lower() for i in region_data.columns]
    ss['region_data'] = region_data
    buffer = io.StringIO()
    data.info(buf=buffer)
    ss['info'] = buffer.getvalue()
    set_filters_to_default()


# Page content
# ------------

st.session_state['page'] = 'home'

st.header('EM-VIEW Disaster Dashboard')
st.write(PAGE_HELP_TEXT[st.session_state['page']])

# Data Loading Options
# --------------------
st.subheader("Data Loading Options")
load_option = st.radio(
    "Select how you want to load the EM-DAT data:",
    [
        "Upload your EM-DAT file",
        "Load the EM-DAT archive",
        "Use API key"
    ],
    index=0
)

if load_option == "Upload your EM-DAT file":
    uploaded_file = st.file_uploader(
        "Upload your EM-DAT xlsx file...",
        type=['xlsx'],
    )
    if uploaded_file:
        data, metadata = load_data(uploaded_file)
        process_data(data, metadata, uploaded_file.name)

elif load_option == "Load the EM-DAT archive":
    if st.button("Load Archive"):
        with st.spinner("Downloading and processing archive data..."):
            data, metadata = load_from_archive()
            process_data(data, metadata, "EM-DAT Archive")

elif load_option == "Use API key":
    api_key = st.text_input("Enter your EM-DAT API key", type="password")
    if st.button("Load from API"):
        if api_key:
            with st.spinner("Fetching data from API..."):
                data, metadata = load_from_api(api_key)
                process_data(data, metadata, "EM-DAT API")
        else:
            st.error("Please enter an API key.")

if "data" in st.session_state:
    # Display File Metadata
    exp1 = st.expander('**Metadata**')
    exp1.write(f"**Filename**: {st.session_state['filename']}")
    exp1.write(st.session_state['metadata'])
    exp1.text(st.session_state['info'])
