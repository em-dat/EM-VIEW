API_ENDPOINT = 'https://api.emdat.be/v1'

API_METADATA = {
    "Source:": "EM-DAT API",
    "URL": API_ENDPOINT,
    "Version:": "1.0.0"
}

BASE_QUERY = """
query FullQuery {{
  api_version
  public_emdat(
    cursor: {{ limit: -1 }}
    filters: {{
      include_hist: true
    }}
  ) {{
    data {{
      {include_fields}
    }}
  }}
}}
"""

# Mapper of API field name to EM-DAT xlsx file column names
COLUMN_MAP = {
    "disno": "DisNo.",
    "historic": "Historic",
    "classif_key": "Classification Key",
    "group": "Disaster Group",
    "subgroup": "Disaster Subgroup",
    "type": "Disaster Type",
    "subtype": "Disaster Subtype",
    "external_ids": "External IDs",
    "name": "Event Name",
    "iso": "ISO",
    "country": "Country",
    "subregion": "Subregion",
    "region": "Region",
    "location": "Location",
    "origin": "Origin",
    "associated_types": "Associated Types",
    "ofda_response": "OFDA/BHA Response",
    "appeal": "Appeal",
    "declaration": "Declaration",
    "aid_contribution": "AID Contribution ('000 US$)",
    "magnitude": "Magnitude",
    "magnitude_scale": "Magnitude Scale",
    "latitude": "Latitude",
    "longitude": "Longitude",
    "river_basin": "River Basin",
    "start_year": "Start Year",
    "start_month": "Start Month",
    "start_day": "Start Day",
    "end_year": "End Year",
    "end_month": "End Month",
    "end_day": "End Day",
    "total_deaths": "Total Deaths",
    "no_injured": "No. Injured",
    "no_affected": "No. Affected",
    "no_homeless": "No. Homeless",
    "total_affected": "Total Affected",
    "reconstr_dam": "Reconstruction Costs ('000 US$)",
    "reconstr_dam_adj": "Reconstruction Costs, Adjusted ('000 US$)",
    "insur_dam": "Insured Damage ('000 US$)",
    "insur_dam_adj": "Insured Damage, Adjusted ('000 US$)",
    "total_dam": "Total Damage ('000 US$)",
    "total_dam_adj": "Total Damage, Adjusted ('000 US$)",
    "cpi": "CPI",
    "admin_units": "Admin Units",
    "gadm_admin_units": "GADM Admin Units",
    "entry_date": "Entry Date",
    "last_update": "Last Update"
}

DATA_FIELDS = list(COLUMN_MAP.keys())
