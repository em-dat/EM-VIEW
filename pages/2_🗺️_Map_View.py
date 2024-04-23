import streamlit as st
import plotly.graph_objects as go

from utils.sidebar import init_filters
from utils.layout import init_layout, generate_colorscale

CMAP_DOC_URI = "https://plotly.com/python/builtin-colorscales/"
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

init_layout()

if "data" not in st.session_state:
    st.error('Please, upload your dataset first on the main page', icon="🚨")
else:
    data = st.session_state['data_filtered']
    init_filters()
    if st.session_state['filter.country'] is not None:
        st.error('Mapping tool cannot be set for one single country', icon="🚨")
    else:
        st.header('EM-DAT Maps')
        cols = st.columns(8)
        variable = cols[0].selectbox("Impact Variable", VAR_DICT.keys(),
                                     format_func=lambda x: VAR_DICT.get(x))
        scope = cols[1].selectbox("Zoom Options", SCOPES,
                                  format_func=lambda x: x.title())
        custom = cols[5].toggle('Custom Color Scale', value=False)
        if not custom:
            cmap = cols[2].selectbox(
                "Color Scale", COLORMAPS, index=COLORMAPS.index('amp')
            )
            reversed = cols[3].checkbox('Reversed Scale', value=True)
            cols[3].caption(
                f"See [Plotly Documentation]({CMAP_DOC_URI})")
            if reversed:
                cmap += '_r'
            cols[6].color_picker('Top Color', '#ba0c2f', disabled=True)
            cols[7].color_picker('Bottom Color', '#ffffff', disabled=True)
        else:
            top_color = cols[6].color_picker('Top Color', '#ba0c2f')
            bottom_color = cols[7].color_picker('Bottom Color', '#ffffff')
            cmap = generate_colorscale(bottom_color, top_color)
            cols[2].selectbox("Color Scale", COLORMAPS,
                              index=COLORMAPS.index('amp'), disabled=True)
            cols[3].checkbox('Reversed Scale', value=True, disabled=True)

        data_map = data.groupby(['Country', 'Region', 'ISO']).agg(
            count=('ISO', 'count'),
            death=('Total Deaths', 'sum'),
            affected=('Total Affected', 'sum'),
            damage=("Total Damage, Adjusted ('000 US$)", 'sum')
        ).reset_index()

        data_map = data_map.merge(
            st.session_state['data'].groupby(
                ['Country', 'Region', 'ISO']).count().reset_index()[
                ['Country', 'Region', 'ISO']]
            , how='outer').fillna(0)

        # Create Choropleth map

        fig = go.Figure(data=go.Choropleth(
            locations=data_map["ISO"],
            z=data_map[variable],
            text=data_map["Country"],
            colorscale=cmap,
            autocolorscale=False,
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=.5
        ))

        fig.update_geos(
            resolution=50
        )
        fig.update_layout(
            title={
                'automargin': True,
                'text': f'{TITLE_DICT.get(variable)}',
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
