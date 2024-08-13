# EM-VIEW: A Community Dashboard for your EM-DAT Data

![Optional Alt Text](images/emview_preview.png)


This is a [Streamlit](https://streamlit.io/) Web App designed for visualize 
the [EM-DAT International Disaster Database](https://www.emdat.be/) data 
contained in your official EM-DAT xlsx file. EM-VIEW has multiple tabs with 
specific features responding to filters:
- Metric view: impact statistics indicators with their disaggregation by 
disaster types;
- Table view: the EM-DAT dataframe that can be filtered by column names;
- Map view: global or regional impact maps at the country level;
- Time view: yearly-aggregated timeseries of impact, with multiple stacking 
options.

You can download the EM-DAT data by registering at https://public.emdat.be/.

## Use the app on Streamlit Community Cloud

Visit https://emview.streamlit.app/

## Install, Use, and Custom the App Locally 

The app relies on streamlit version 1.37.

Streamlit can be installed with command:
   ```bash
   pip install streamlit
   ```

See `requirements.txt`.

Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

With streamlit installed, use the following command to run the app:
   ```bash
    streamlit run app.py
   ```