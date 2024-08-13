import plotly.graph_objects as go
import streamlit as st

from utils.filters import get_filtered_data
from utils.layout import generate_colorscale, PAGE_HELP_TEXT

SCOPES = ['world', 'africa', 'asia', 'europe', 'north america', 'south america']
COLORMAPS = [
    'aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance', 'blackbody',
    'bluered', 'blues', 'blugrn', 'bluyl', 'brbg', 'brwnyl', 'bugn', 'bupu',
    'burg', 'burgyl', 'cividis', 'curl', 'darkmint', 'deep', 'delta', 'dense',
    'earth', 'edge', 'electric', 'emrld', 'fall', 'geyser', 'gnbu', 'gray',
    'greens', 'greys', 'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno',
    'jet', 'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
    'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl', 'piyg',
    'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn', 'puor', 'purd',
    'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdgy', 'rdpu', 'rdylbu',
    'rdylgn', 'redor', 'reds', 'solar', 'spectral', 'speed', 'sunset',
    'sunsetdark', 'teal', 'tealgrn', 'tealrose', 'tempo', 'temps', 'thermal',
    'tropic', 'turbid', 'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu',
    'ylorbr', 'ylorrd']

VAR_DICT = {
    'count': 'N° Count',
    'death': 'Total Deaths',
    'affected': 'Total Affected',
    'damage': "Total Damage, Adjusted ('000 US$)"
}
TITLE_DICT = {
    'count': 'Number of Disasters per Country',
    'death': 'Total Deaths per Country',
    'affected': 'Total Affected per Country',
    'damage': "Total Damage per Country (in '000 of US$)"
}
st.session_state["page"] = "map"

if "data" not in st.session_state:
    st.error('Please, upload your dataset first on the main page', icon="🚨")
else:
    # Data & period
    data = get_filtered_data()
    year_min = data['Start Year'].min()
    year_max = data['End Year'].max()
    if year_min < year_max:
        period = f"{year_min}-{year_max}"
    else:
        period = f"{year_min}"

    if st.session_state['filter.country'] is not None:
        st.error('Mapping tool cannot be set for one single country', icon="🚨")
    else:

        # Controls
        row0_cols = st.columns(3, vertical_alignment="center")
        row1_cols = st.columns([1,1,1,3], vertical_alignment="center")
        variable = row0_cols[0].selectbox(
            "Impact Variable",
            VAR_DICT.keys(),
            format_func=lambda x: VAR_DICT.get(x)
        )
        scope = row0_cols[1].selectbox(
            "Zoom Options",
            SCOPES,
            format_func=lambda x: x.title()
        )
        aggregator = row0_cols[2].selectbox(
            'Aggregate by',
            ['Total', 'Yearly Average', 'Yearly Median']
        )
        custom = row1_cols[3].toggle('Custom Color Scale', value=False)
        land_color = row1_cols[0].color_picker(
            label='No Data',
            value='#dddddd'
        )
        if not custom:
            cmap = row1_cols[1].selectbox(
                "Color Scale", COLORMAPS, index=COLORMAPS.index('amp')
            )
            reversed = row1_cols[2].toggle('Reversed Scale', value=True)

            if reversed:
                cmap += '_r'
        else:
            top_color = row1_cols[1].color_picker('Top Color', '#ba0c2f')
            bottom_color = row1_cols[2].color_picker('Bottom Color', '#ffffff')
            cmap = generate_colorscale(bottom_color, top_color)

        # Map

        annual_data = data.groupby(
            ['Country', 'Region', 'ISO', 'Start Year']).agg(
            count=('ISO', 'count'),  # Counting occurrences per year
            death=('Total Deaths', 'sum'),  # Summing deaths per year
            affected=('Total Affected', 'sum'),  # Summing affected per year
            damage=("Total Damage, Adjusted ('000 US$)", 'sum')
            # Summing damage per year
        ).reset_index()

        if aggregator == 'Total':
            data_map = annual_data.groupby(['Country', 'Region', 'ISO']).agg(
                count=('count', 'sum'),
                death=('death', 'sum'),
                affected=('affected', 'sum'),
                damage=('damage', 'sum')
            ).reset_index()
        elif aggregator == 'Yearly Average':
            data_map = annual_data.groupby(['Country', 'Region', 'ISO']).agg(
                count=('count', 'mean'),
                death=('death', 'mean'),
                affected=('affected', 'mean'),
                damage=('damage', 'mean')
            ).reset_index()
        elif aggregator == 'Yearly Median':
            data_map = annual_data.groupby(['Country', 'Region', 'ISO']).agg(
                count=('count', 'median'),
                death=('death', 'median'),
                affected=('affected', 'median'),
                damage=('damage', 'median')
            ).reset_index()

        data_map = data_map.merge(
            st.session_state['data'].groupby(
                ['Country', 'Region', 'ISO']).count().reset_index()[
                ['Country', 'Region', 'ISO']]
            , how='outer').fillna(0)

        # Create Choropleth map

        fig = go.Figure(
            data=go.Choropleth(
                locations=data_map["ISO"],
                z=data_map[variable],
                text=data_map["Country"],
                colorscale=cmap,
                autocolorscale=False,
                reversescale=True,
                marker_line_color='darkgray',
                marker_line_width=.5,
            )
        )

        fig.update_geos(
            resolution=50,
            showland=True,
            landcolor=land_color,
        )
        fig.update_layout(
            title={
                'automargin': True,
                'text': f'{TITLE_DICT.get(variable)} ({period} {aggregator})',
                'font': {
                    'family': 'Arial',
                    'size': 24
                }
            },
            height=600,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular',
                scope=scope
            ),
            annotations=[dict(
                x=1,
                y=0.,
                xref='paper',
                yref='paper',
                text=f"Source: {st.session_state['metadata']['Source:']}",
                showarrow=False
            )]
        )

        st.plotly_chart(fig, use_container_width=True)

        # Page Help
        # ---------
        with st.expander("See page details", expanded=False,
                         icon=':material/info:'):
            st.markdown(PAGE_HELP_TEXT[st.session_state.page])
