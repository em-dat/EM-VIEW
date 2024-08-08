PAGE_HELP_TEXT = {
    'home': """
    **EM-VIEW** provides summarization and vizualisation features for your 
    [**EM-DAT**](https://www.emdat.be) **International Disaster 
    Database** dataset. 
    
    EM-DAT contains data about **:earth_africa: global :collision: disaster 
    occurrence and impact**. 
    1. EM-DAT data is freely accessible for non-commercial use after 
    registration at [public.emdat.be](https://public.emdat.be). 
    2. Uploading your EM-DAT data file (:point_down: below).
    3. Use the **EM-VIEW** pages (:point_left: sidebar) to access summary 
    statistics, tabular data, maps, and time series.  
    4. Change the scope of your analysis using the :point_left: sidebar filters.
    
    ## Upload your EM-DAT file
    """,
    "metric": """
        The Metric View page displays _aggregated statistics_ for the main
        EM-DAT _impact variables_ in the dataset or its filtered selection. 
        The numbers are calculated using the provided EM-DAT file. Users may 
        use the :point_left: sidebar filters to explore subsets of the data. 

        **Impact Variables**

        - **N° Count**: disaster occurrences at the country level, 
        - **Total Deaths**: associated mortality, including long-term missing 
        people,
        - **Total Affected**: total number of affected people necessitating 
        assistance, including injured, homeless, and otherwise affected,
        - **Total Dam. ('000 US\$')**: total economic damage reported in 
        thousands of \$US, adjusted for inflation.

        See the EM-DAT documentation portal for more information on 
        [Impact Variables](https://doc.emdat.be/docs/data-structure-and-content/impact-variables/).

        **Aggregated Statistics**

        - **Total**: total for the corresponding impact variables,
        - **Yearly Average**: the expected impact, on average, per year, 
        - **Yearly Median**: the expected impact, using the median, per year, 
        such that 50% of years are expected to have more or less than the 
        median.
        - **Reporting %**: the reporting percentage for the corresponding impact
        variables, indicating the rate at which EM-DAT reports the impact 
        figure in the selected disaster entries. Non-reported impacts could 
        either be null or unknown. 

        Reporting percentage varies across disaster types.
        See the EM-DAT documentation portal for [key insights on interpreting
        the EM-DAT data](https://doc.emdat.be/docs/known-issues-and-limitations/).

        **Distribution per Disaster Types (%)**

        The bar chart show the distribution of the total impact, for each 
        considered impact variable, expressed as the percentage of total in the
        dataset or its filtered selection. 

        """,
    "table": """
    The Table View page displays a multi-selection of columns and their data 
    content based on the EM-DAT uploaded dataset or its filtered selection. 
    Users may use the :point_left: sidebar filters to explore subsets of the 
    data. 

    **Columns Selection**

    User may use the :point_up_2: multiselect tool to filter the columns to 
    display. For a complete description of the column variables, we refer to
    the [EM-DAT Public Table](https://doc.emdat.be/docs/data-structure-and-content/emdat-public-table/) 
    documentation.
    """,
    "map": """
    The Map View page makes it possible to build maps at the country level 
    based on the uploaded dataset or its filtered selection. Users may use the 
    :point_left: sidebar filters to explore subsets of the data.
    
    **Impact Variables**

    - **N° Count**: disaster occurrences at the country level, 
    - **Total Deaths**: associated mortality, including long-term missing 
    people,
    - **Total Affected**: total number of affected people necessitating 
    assistance, including injured, homeless, and otherwise affected,
    - **Total Damage, Adjusted ('000 US\$')**: total economic damage reported in 
    thousands of \$US, adjusted for inflation.

    See the EM-DAT documentation portal for more information on 
    [Impact Variables](https://doc.emdat.be/docs/data-structure-and-content/impact-variables/).

    **Aggregated Statistics**

    - **Total**: total for the corresponding impact variables,
    - **Yearly Average**: the expected impact, on average, per year, 
    - **Yearly Median**: the expected impact, using the median, per year, 
    such that 50% of years are expected to have more or less than the 
    median.
    
    **Color Scales**
    
    Color scales can be selected based on those available from the `plotly`
    graphing libraries. More info: https://plotly.com/python/colorscales/.
    
    Alternatively, the user can use a custom color scale, enabled by the 
    :point_up_2: "Custom Color Scale" toggle button. 
    
    **Troubleshooting**
    
    World maps are built using an attribute joint on ISO-3166 alpha-3 codes.
    EM-DAT contains some code for historical data or conflictual areas that 
    may not be mapped using the reference used by the `plotly` graphing library.
    For a list of these exceptions and additional information, see
    [Spatial Information and Geocoding](https://doc.emdat.be/docs/data-structure-and-content/spatial-information).
    
    **Disclaimer**
    
    This tool relies on the world delineation provided the `plotly` graphing 
    library. The way the EM-DAT data is presented and documented on this app
    does not reflect any geopolitical views held by the EM-DAT team, or the 
    views of our partners, including the United States Agency for International
    Development or the United States Government.
     
    """,
    "time": """
    The Time View page displays time series of yearly aggregated data based on 
    the uploaded dataset or its filtered selection. Users may use the 
    :point_left: sidebar filters to explore subsets of the data.
    
    **Impact Variables**

    - **N° Count**: disaster occurrences at the country level, 
    - **Total Deaths**: associated mortality, including long-term missing 
    people,
    - **Total Affected**: total number of affected people necessitating 
    assistance, including injured, homeless, and otherwise affected,
    - **Total Damage, Adjusted ('000 US\$')**: total economic damage reported in 
    thousands of \$US, adjusted for inflation.
    
    **Stacked Bars**
    
    Optionally, users may use the :point_up_2: "Stack by" select box to displayed stacked 
    bars illustrating the impact distribution between:
    - Disaster Types,
    - Regions,
    - Subregions
    
    For information on disaster types, we refer to the [EM-DAT Disaster 
    Classification System](https://doc.emdat.be/docs/data-structure-and-content/disaster-classification-system/).  
    For information on regions and subregions, we refer to the EM-DAT page on
    [Spatial Information and Geocoding](https://doc.emdat.be/docs/data-structure-and-content/spatial-information/).
    
    """
}


def format_num(num):
    """
    Parameters
    ----------
    num : int or str
        The number to be formatted.

    Returns
    -------
    str or None
        The formatted number as a string if the input is a valid number,
        otherwise None.

    """
    try:
        return f"{int(num):,}"
    except ValueError:
        return None


def hex_to_rgb(hex_color: str):
    """
    Parameters
    ----------
    hex_color : str
        The hexadecimal color code to convert to RGB. The hex_color should be
        in the format '#RRGGBB', where RR, GG, BB are the hexadecimal values
        representing the red, green, and blue color channels respectively.

    Returns
    -------
    rgb : tuple
        A tuple containing the RGB values of the color. The values are integers
        ranging from 0 to 255, representing the intensity of the red, green, and
        blue color channels respectively.

    Examples
    --------
    >>> hex_to_rgb('#FF0000')
    (255, 0, 0)

    >>> hex_to_rgb('#00FF00')
    (0, 255, 0)

    >>> hex_to_rgb('#0000FF')
    (0, 0, 255)
    """
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    rgb = tuple(
        int(hex_color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return rgb


def generate_colorscale(bottom_color, top_color):
    """
    Parameters
    ----------
    bottom_color : str
        The color at the bottom of the gradient. Should be in hexadecimal format.

    top_color : str
        The color at the top of the gradient. Should be in hexadecimal format.

    Returns
    -------
    list
        A list representing the colorscale gradient. Each element of the list is a sub-list
        containing two values: a float representing the position in the gradient (ranging from 0.0 to 1.0)
        and a string representing the RGB color value at that position.
    """
    # Convert both colors to RGB
    bottom_rgb = hex_to_rgb(bottom_color)
    top_rgb = hex_to_rgb(top_color)

    # Create a gradient
    colorscale = [
        [0.0, f'rgb({top_rgb[0]}, {top_rgb[1]}, {top_rgb[2]})'],
        [1.0, f'rgb({bottom_rgb[0]}, {bottom_rgb[1]}, {bottom_rgb[2]})']
    ]
    return colorscale
