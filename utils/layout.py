import streamlit as st


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


def init_layout():
    """
    Initialize the layout of the application.

    This method sets the page configuration for the Streamlit application,
    including the page title, icon, layout style, and menu items.
    Additionally, it calls the `set_margin_top()` method to set the top margin
    of the application.

    Returns:
        None
    """
    st.set_page_config(page_title="EM-VIEW", page_icon="🌍", layout='wide',
                       menu_items={
                           'Get Help': 'https://doc.emdat.be/',
                           'Report a bug':
                               "https://github.com/dadelforge/EM-VIEW/issues",
                           'About':
                               "This app has been developped at the University "
                               "of Louvain by Damien Delforge, PhD, with the "
                               "support of USAID"})
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
