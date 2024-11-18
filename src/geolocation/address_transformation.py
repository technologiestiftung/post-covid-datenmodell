'''
Script to transform addresses to different other geodata, like longitude and latitude

'''
import pandas as pd


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

    mapper_data = pd.read_csv("docs/2024-11-14_plz_geocoord.csv")
    mapper = {row["plz"]:(row["lng"], row["lat"] )for index, row in mapper_data.iterrows()} # make mapper

    # postal code is complete
    if len(postal_code) == 5: 
        return mapper.get(int(postal_code), None)

    # todo: handle cases where postal code is not complete

    return None

    




