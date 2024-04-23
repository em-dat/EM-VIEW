from datetime import date
import streamlit as st

DOC_URI = "https://doc.emdat.be/docs"
CLASSIF_KEY_DOC_URI = f"{DOC_URI}/data-structure-and-content/disaster-classification-system/#main-classification-tree"


def init_filters():
    # Get session state variables
    region_list = [None] + sorted(
        st.session_state["region_data"]['Region'].unique())
    subregion_list = [None] + sorted(
        st.session_state["region_data"]['Subregion'].unique())
    country_list = [None] + sorted(st.session_state["region_data"]['Country'])

    # Set up filters
    col1, col2 = st.sidebar.columns(2)

    col1.number_input(label='**Start year**',
                      min_value=st.session_state['data']['Start Year'].min(),
                      value=st.session_state['filter.start'],
                      max_value=date.today().year,
                      key='filter.start',
                      on_change=filter_data),

    col2.number_input(label='**End year**',
                      min_value=st.session_state['data']['Start Year'].min(),
                      value=st.session_state['filter.end'],
                      max_value=date.today().year,
                      key='filter.end',
                      on_change=filter_data)

    st.sidebar.text_input(label="**Classification Key**",
                          value=st.session_state['filter.clkey'],
                          key="filter.clkey",
                          on_change=filter_data,
                          help="Enter the key or its initial part to filter")
    st.sidebar.caption(
        f"_Check classification keys [here]({CLASSIF_KEY_DOC_URI})._")

    st.sidebar.selectbox(label="**Region**", options=region_list,
                         index=region_list.index(
                             st.session_state['filter.region']),
                         key="filter.region",
                         format_func=lambda x: 'All' if x is None else x,
                         on_change=update_region)

    st.sidebar.selectbox(label="**Subregion**", options=subregion_list,
                         index=subregion_list.index(
                             st.session_state['filter.subregion']),
                         key="filter.subregion",
                         format_func=lambda x: 'All' if x is None else x,
                         on_change=update_subregion)

    st.sidebar.selectbox(label="**Country**", options=country_list,
                         index=country_list.index(
                             st.session_state['filter.country']),
                         key="filter.country",
                         format_func=lambda x: 'All' if x is None else x,
                         on_change=update_country)

    st.sidebar.button("Reset", type="primary", on_click=reset_filters)


def filter_data():
    data_filtered = st.session_state['data'].copy()
    pstart, pend = st.session_state['filter.start'], st.session_state[
        'filter.end']
    clkey = st.session_state['filter.clkey']
    region = st.session_state["filter.region"]
    subregion = st.session_state["filter.subregion"]
    country = st.session_state["filter.country"]

    data_filtered = data_filtered[(data_filtered['Start Year'] >= pstart) & (
            data_filtered['End Year'] <= pend)]
    data_filtered = data_filtered[
        data_filtered['Classification Key'].str.match(clkey.replace('*', '.*'))]
    if region:
        data_filtered = data_filtered[data_filtered['Region'] == region]
    if subregion:
        data_filtered = data_filtered[data_filtered['Subregion'] == subregion]
    if country:
        data_filtered = data_filtered[data_filtered['Country'] == country]

    st.session_state['data_filtered'] = data_filtered


def update_region():
    region_data = st.session_state['region_data']
    region = st.session_state['filter.region']
    subregion = st.session_state['filter.subregion']
    country = st.session_state['filter.country']
    if region:
        valid_data = region_data[region_data['Region'] == region]
        if subregion not in valid_data['Subregion']:
            st.session_state['filter.subregion'] = None
        if country not in valid_data['Country']:
            st.session_state['filter.country'] = None
    else:
        st.session_state['filter.subregion'] = None
        st.session_state['filter.country'] = None
    filter_data()


def update_subregion():
    region_data = st.session_state['region_data']
    region = st.session_state['filter.region']
    subregion = st.session_state['filter.subregion']
    country = st.session_state['filter.country']
    if subregion:
        valid_data = region_data[region_data['Subregion'] == subregion]
        if region not in valid_data['Region']:
            st.session_state['filter.region'] = valid_data.iloc[0]['Region']
        if country not in valid_data['Country']:
            st.session_state['filter.country'] = None
    else:
        st.session_state['filter.country'] = None
    filter_data()


def update_country():
    region_data = st.session_state['region_data']
    region = st.session_state['filter.region']
    subregion = st.session_state['filter.subregion']
    country = st.session_state['filter.country']
    if country:
        valid_data = region_data[region_data['Country'] == country]
        if region not in valid_data['Region']:
            st.session_state['filter.region'] = valid_data.iloc[0]['Region']
        if subregion not in valid_data['Subregion']:
            st.session_state['filter.subregion'] = valid_data.iloc[0][
                'Subregion']
    filter_data()


def reset_filters():
    data = st.session_state['data']
    st.session_state['filter.start'] = data['Start Year'].min()
    st.session_state['filter.end'] = data['Start Year'].max()
    st.session_state["filter.clkey"] = ''
    st.session_state["filter.region"] = None
    st.session_state["filter.subregion"] = None
    st.session_state["filter.country"] = None
    filter_data()
