import plotly.express as px
import streamlit as st

from utils.distypes import TYPE_ORDER, TYPE_COLORS
from utils.filters import get_filtered_data
from utils.layout import PAGE_HELP_TEXT

VAR_DICT = {
    'count': 'N° Count',
    'death': 'Total Deaths',
    'affected': 'Total Affected',
    'damage': "Total Damage, Adjusted ('000 US$)"
}

st.session_state["page"] = "time"

if "data" not in st.session_state:
    st.error('Please, upload your dataset first on the main page', icon="🚨")
else:
    data = get_filtered_data()

    cols = st.columns(2)
    variable = cols[0].selectbox(
        "Impact Variable",
        VAR_DICT.keys(),
        format_func=lambda x: VAR_DICT.get(x)
    )
    stacker = cols[1].selectbox(
        "Stack by",
        [None, 'Types', 'Regions', 'Subregions'])

    if stacker is None:
        data_time = data.groupby(
            ['Start Year']).agg(
            count=('DisNo.', 'count'),
            death=('Total Deaths', 'sum'),
            affected=('Total Affected', 'sum'),
            damage=("Total Damage, Adjusted ('000 US$)", 'sum')
        ).reset_index()
        fig = px.bar(data_time, x='Start Year', y=variable)
        fig.update_traces(marker_color='#214B8C')

    elif stacker == 'Types':
        data_time = data.groupby(
            ['Start Year', 'Disaster Type']).agg(
            count=('DisNo.', 'count'),
            death=('Total Deaths', 'sum'),
            affected=('Total Affected', 'sum'),
            damage=("Total Damage, Adjusted ('000 US$)", 'sum')
        ).reset_index()

        order = [i for i in TYPE_ORDER if
                 i in data_time['Disaster Type'].unique()]
        fig = px.bar(
            data_time,
            x='Start Year',
            y=variable,
            color='Disaster Type',
            category_orders={'Disaster Type': order}
        )
        fig.for_each_trace(lambda t: t.update(marker_color=TYPE_COLORS[t.name]))

    elif stacker == 'Regions':
        data_time = data.groupby(
            ['Start Year', 'Region']).agg(
            count=('DisNo.', 'count'),
            death=('Total Deaths', 'sum'),
            affected=('Total Affected', 'sum'),
            damage=("Total Damage, Adjusted ('000 US$)", 'sum')
        ).reset_index()

        fig = px.bar(
            data_time,
            x='Start Year',
            y=variable,
            color='Region'
        )
    elif stacker == 'Subregions':
        data_time = data.groupby(
            ['Start Year', 'Subregion']).agg(
            count=('DisNo.', 'count'),
            death=('Total Deaths', 'sum'),
            affected=('Total Affected', 'sum'),
            damage=("Total Damage, Adjusted ('000 US$)", 'sum')
        ).reset_index()

        fig = px.bar(
            data_time,
            x='Start Year',
            y=variable,
            color='Subregion'
        )

    fig['layout']['yaxis']['title'] = VAR_DICT[variable]
    st.plotly_chart(fig, use_container_width=True)

    # Page Help
    # ---------
    with st.expander("See page details", expanded=False,
                     icon=':material/info:'):
        st.markdown(PAGE_HELP_TEXT[st.session_state.page])
