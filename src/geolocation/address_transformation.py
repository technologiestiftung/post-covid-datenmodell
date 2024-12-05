'''
Script to transform addresses to different other geodata, like longitude and latitude

'''
import pandas as pd
import geopandas as gpd
import warnings


def get_long_lat_from_postal_code(postal_code: str) -> tuple | None:
    '''
    Function to transform (parts of) postal codes to long, lat coordinates using the postal code to long lat mapping
    provided in this Github repository: 
    https://github.com/WZBSocialScienceCenter/plz_geocoord/tree/master created by Markus Konrad in 2019
    The data was obtained by using the Google Cloud Geocoding API. the file is licensed under Apache License 2.0

    Args:
        postal_code (str): postal code of the address

    Returns: 
        tuple: longitude and latitude coordinates of the postal
    '''

    mapper_data = pd.read_csv("data/raw/2024-11-14_plz_geocoord.csv")
    mapper = {row["plz"]:(row["lng"], row["lat"] )for index, row in mapper_data.iterrows()} # make mapper

    # postal code is complete
    if len(postal_code) == 5: 
        return mapper.get(int(postal_code), None)
    
    # postal code is not complete
    else:
        mapper_data = mapper_data[mapper_data["plz"].astype(str).str.startswith(postal_code)] # find postal codes that would fit 
        gdf = gpd.GeoDataFrame(mapper_data, geometry=gpd.points_from_xy(mapper_data.lng, mapper_data.lat), crs="EPSG:4326") # make geopandas dataframe from fitting ones 
        centroid = gdf.geometry.unary_union.centroid
        return (centroid.x, centroid.y) if centroid else None

    return None


def get_landkreis_id_from_postal_code(postal_code: str) -> int | None:
    '''
    Function to transform (parts of) postal codes to landkreis id using the postal code to landkreis mapping. 
    -> source:  # source: https://public.opendatasoft.com/explore/dataset/georef-germany-postleitzahl/table/?dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6Imdlb3JlZi1nZXJtYW55LXBvc3RsZWl0emFobCIsIm9wdGlvbnMiOnt9fSwiY2hhcnRzIjpbeyJhbGlnbk1vbnRoIjp0cnVlLCJ0eXBlIjoiY29sdW1uIiwiZnVuYyI6IkNPVU5UIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiI0ZGNTE1QSJ9XSwieEF4aXMiOiJwbHpfbmFtZSIsIm1heHBvaW50cyI6NTAsInNvcnQiOiIifV0sInRpbWVzY2FsZSI6IiIsImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWV9&location=11,51.6931,8.28335&basemap=jawg.light
    Function is used when retrieving data from the RKI API, as the data is provided on a landkreisId level.
    There are special cases for Berlin postal codes, they have a separate (manual) mapping. See the document 
    
    Args:
        postal_code (str): postal code of the address

    Returns: 
        int: landkreis id of the postal code (part of AGS)
        
    '''
   
    mapper_data = pd.read_csv("data/raw/2024-12-03_postleitzahlen_kreis_id.csv")
    mapper = {row["Postleitzahl / Post code"]:row["Kreis code"]for index, row in mapper_data.iterrows()} # make mapper

    # special case: Berlin
    berlin_postal_codes = pd.read_csv("data/raw/2024-12-03_berlin_plz_mapping.csv")

    berlin_mapper = {row["plz"]: row["landkreisId"] for index, row in berlin_postal_codes.iterrows()}

    if int(postal_code) in berlin_postal_codes["plz"].values:
        print("Berlin postal code found")
        return berlin_mapper.get(int(postal_code), None)

    elif len(postal_code) == 5: 
            return mapper.get(int(postal_code), None)

    else: 
        warnings.warn(f"Postal code not found or not yet implemented for incomplete postal codes")



    




