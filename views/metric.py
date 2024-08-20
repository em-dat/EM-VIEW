import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from utils.distypes import TYPE_ORDER, TYPE_COLORS
from utils.filters import get_filtered_data
from utils.layout import format_num, PAGE_HELP_TEXT

st.session_state["page"] = "metric"

if "data" not in st.session_state:
    st.error('Please, upload your dataset first on the main page', icon="🚨")
else:
    data: pd.DataFrame = get_filtered_data()

    st.html("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 20px;
    }
    </style>
    """)

    # Table Header Row - 0
    # --------------------
    scol00, scol01, scol02, scol03, scol04 = st.columns(
        5,
        vertical_alignment="center"
    )
    scol01.markdown(
        '**N° Count**',
        help="Number of disasters at the country level"
    )
    scol02.markdown(
        '**Total Deaths**',
        help="Total of dead and missing people"
    )
    scol03.markdown(
        '**Total Affected**',
        help="Total of injured, affected, and homeless people"
    )
    scol04.markdown(
        "**Total Dam. ('000 US$)**",
        help="Total Damage in thousand of US$, adjusted for inflation."
    )

    # Table Total Row - 1
    # -------------------

    scol10, scol11, scol12, scol13, scol14 = st.columns(
        5,
        vertical_alignment="center"
    )
    scol10.markdown('**Total**')
    scol11.metric(
        'N° Count',
        format_num(data['DisNo.'].nunique()),
        label_visibility='collapsed'
    )
    scol12.metric(
        'Total Deaths',
        format_num(data['Total Deaths'].sum()),
        label_visibility='collapsed'
    )
    scol13.metric(
        'Total Affected',
        format_num(data['Total Affected'].sum()),
        label_visibility='collapsed'
    )
    scol14.metric(
        "Total Dam. ('000 US$)",
        format_num(data["Total Damage, Adjusted ('000 US$)"].sum()),
        label_visibility='collapsed'
    )

    # Table Average Row - 2
    # ---------------------
    scol20, scol21, scol22, scol23, scol24 = st.columns(
        5,
        vertical_alignment="center"
    )
    scol20.markdown('**Yearly Average**')
    scol21.metric(
        'N° Count',
        format_num(data.groupby('Start Year')['DisNo.'].nunique().mean()),
        label_visibility='collapsed'
    )
    scol22.metric(
        'Average Total Deaths :skull:',
        format_num(data.groupby('Start Year')['Total Deaths'].sum().mean()),
        label_visibility='collapsed'
    )
    scol23.metric(
        'Total Affected :hospital:',
        format_num(data.groupby('Start Year')['Total Affected'].sum().mean()),
        label_visibility='collapsed'
    )
    scol24.metric(
        "Total Dam. ('000 :heavy_dollar_sign:)",
        format_num(
            data.groupby('Start Year')[
                "Total Damage, Adjusted ('000 US$)"
            ].sum().mean()
        ),
        label_visibility='collapsed'
    )

    # Table Median Row - 3
    # --------------------
    scol30, scol31, scol32, scol33, scol34 = st.columns(
        5,
        vertical_alignment="center"
    )
    scol30.markdown('**Yearly Median**')
    scol31.metric(
        'N° Count',
        format_num(data.groupby('Start Year')['DisNo.'].nunique().median()),
        label_visibility='collapsed'
    )
    scol32.metric(
        'Average Total Deaths :skull:',
        format_num(data.groupby('Start Year')['Total Deaths'].sum().median()),
        label_visibility='collapsed'
    )
    scol33.metric(
        'Total Affected :hospital:',
        format_num(data.groupby('Start Year')['Total Affected'].sum().median()),
        label_visibility='collapsed'
    )
    scol34.metric(
        "Total Dam. ('000 :heavy_dollar_sign:)",
        format_num(
            data.groupby('Start Year')[
                "Total Damage, Adjusted ('000 US$)"].sum().median()
        ),
        label_visibility='collapsed'
    )

    # Table Reporting Row - 4
    # -----------------------
    scol40, scol41, scol42, scol43, scol44 = st.columns(
        5,
        vertical_alignment="center"
    )
    scol40.markdown('**Reporting %**')
    scol41.metric(
        'N° Count',
        None,
        label_visibility='collapsed'
    )
    scol42.metric(
        'Average Total Deaths :skull:',
        format_num(data['Total Deaths'].count() / len(data) * 100),
        label_visibility='collapsed'
    )
    scol43.metric(
        'Total Affected :hospital:',
        format_num(data['Total Affected'].count() / len(data) * 100),
        label_visibility='collapsed'
    )
    scol44.metric(
        "Total Dam. ('000 :heavy_dollar_sign:)",
        format_num(
            data["Total Damage, Adjusted ('000 US$)"].count() / len(data) * 100
        ),
        label_visibility='collapsed'
    )

    # Type Disaggregation
    # -------------------

    df = data.groupby('Disaster Type').agg(
        count=('Disaster Type', 'count'),
        death=('Total Deaths', 'sum'),
        affected=('Total Affected', 'sum'),
        damage=("Total Damage, Adjusted ('000 US$)", 'sum')
    ).reset_index()

    df['count'] = (df['count'] / df['count'].sum()) * 100
    df['death'] = (df['death'] / df['death'].sum()) * 100
    df['affected'] = (df['affected'] / df['affected'].sum()) * 100
    df['damage'] = (df['damage'] / df['damage'].sum()) * 100
    df = df.round(1)

    order = [i for i in TYPE_ORDER if i in df['Disaster Type'].unique()][::-1]
    colors = [c for k, c in TYPE_COLORS.items() if
              k in df['Disaster Type'].unique()][::-1]
    df = df.set_index('Disaster Type').loc[order].reset_index()

    # Create subplots
    fig = make_subplots(
        rows=1, cols=4,
        shared_yaxes=True,
        subplot_titles=(
            "N° Count", "Total Deaths", "Total Affected", "Total Damage")
    )

    # First col - N° Count
    fig.add_trace(
        go.Bar(
            y=df['Disaster Type'],
            x=df['count'],
            orientation='h',
            marker_color=colors,
            name='N° Count'
        ),
        1,
        1
    )

    # Second col - Death
    fig.add_trace(
        go.Bar(
            y=df['Disaster Type'],
            x=df['death'],
            orientation='h',
            marker_color=colors,
            name='Death'
        ),
        1,
        2
    )

    # Third col - Affected
    fig.add_trace(
        go.Bar(
            y=df['Disaster Type'],
            x=df['affected'],
            orientation='h',
            marker_color=colors,
            name='Affected'
        ),
        1,
        3
    )

    # Fourth col - Damage
    fig.add_trace(
        go.Bar(
            y=df['Disaster Type'],
            x=df['damage'],
            orientation='h',
            marker_color=colors,
            name='Damage'
        ),
        1,
        4
    )

    # Update x-axis label
    for i in range(1, 5):
        fig['layout']['xaxis{}'.format(i)]['title'] = 'Percent %'

    # Update layout
    fig.update_layout(
        title="Distribution per Disaster Types (%)",
        height=500 + 10 * len(df) ** .75,
        showlegend=False
    )
    fig.update_xaxes(range=[0, 100])

    st.plotly_chart(fig, use_container_width=True)

    # Page Help
    # ---------
    with st.expander("See page details", expanded=False,
                     icon=':material/info:'):
        st.markdown(PAGE_HELP_TEXT[st.session_state.page])
