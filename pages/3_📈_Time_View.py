import streamlit as st
import plotly.express as px

from utils.sidebar import init_filters
from utils.layout import init_layout
from utils.distypes import TYPE_ORDER, TYPE_COLORS

VAR_DICT = {
    'count': 'N° Count',
    'death': 'Total Deaths',
    'affected': 'Total Affected',
    'damage': "Total Damage, Adjusted ('000 US$)"
}

init_layout()

if "data" not in st.session_state:
    st.error('Please, upload your dataset first on the main page', icon="🚨")
else:
    data = st.session_state['data_filtered']
    init_filters()
    st.header('EM-DAT Time Series')

    cols = st.columns(6)
    variable = cols[0].selectbox("Impact Variable", VAR_DICT.keys(),
                                 format_func=lambda x: VAR_DICT.get(x))
    show_type = cols[1].toggle("Show Types", value=False)

    if not show_type:
        data_time = data.groupby(
            ['Start Year']).agg(
            count=('DisNo.', 'count'),
            death=('Total Deaths', 'sum'),
            affected=('Total Affected', 'sum'),
            damage=("Total Damage, Adjusted ('000 US$)", 'sum')
        ).reset_index()
        fig = px.bar(data_time, x='Start Year', y=variable)
        fig.update_traces(marker_color='#214B8C')
    else:
        data_time = st.session_state['data_filtered'].groupby(
            ['Start Year', 'Disaster Type']).agg(
            count=('DisNo.', 'count'),
            death=('Total Deaths', 'sum'),
            affected=('Total Affected', 'sum'),
            damage=("Total Damage, Adjusted ('000 US$)", 'sum')
        ).reset_index()
        order = [i for i in TYPE_ORDER if
                 i in data_time['Disaster Type'].unique()]
        fig = px.bar(data_time, x='Start Year', y=variable,
                     color='Disaster Type',
                     category_orders={'Disaster Type': order})
        fig.for_each_trace(lambda t: t.update(marker_color=TYPE_COLORS[t.name]))

    fig['layout']['yaxis']['title'] = VAR_DICT[variable]
    st.plotly_chart(fig, use_container_width=True)
