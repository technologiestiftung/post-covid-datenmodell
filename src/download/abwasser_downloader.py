'''
This script matches data to patients from the Sewage water API 
-> the API is part of the project AMELAG (https://github.com/robert-koch-institut/Abwassersurveillance_AMELAG/tree/main) and the API is accessed via zenodo
 
For the API an access token to Zenodo is needed

For a location (latitude, longitude) of a patient one can get the data from the nearest station measuring air quality for a given timeframe
'''

import httpx
import pandas as pd
import warnings
from src.utils.settings import settings
from haversine import haversine
from io import BytesIO
from typing import Literal


class SewagedataDownloader:
    def __init__(self):
        self.all_stations = self.get_all_stations()


    def get_all_stations(self) -> pd.DataFrame:
        """
        Gets all available sations for sewage data in Germany. 
        Data is provided by the RKI via csv file and contains lonitude and latitude

        Returns: 
            pd.DataFrame: DataFrame with all available stations

        """
        stations = pd.read_csv("docs/2024_11_26_abwasser_standorte.csv")
        return stations

    def get_closest_station(self, lat: float, long: float) -> dict:
        """
        Find the closest station to a given geographic location based on latitude and longitude 
        using the Haversine formula. 

        Args:
            lat (float): Latitude of the reference point
            long (float): Longitude of the reference point

        Returns:
            dict: a dictionary containing the closest station and its distance from the input location. 
        """

        if lat is None or long is None:
            return None

        closest_station = None
        for index, row in self.all_stations.iterrows(): 

            distance = haversine((lat, long), (row["lat"], row["long"]))

            if closest_station is None or distance < closest_station["distance"]:
                closest_station = {
                    "station_name": row["Kläranlage"],
                    "distance": distance
                }
        return closest_station

        


    def get_sewage_data(self, start_date: str, end_date: str, longitude: float, latitude: float, virus_type: None | Literal["SARS-CoV-2", "Influenza A", "Influenza B", "Influenza A+B"] = None, is_normalsierung: None | Literal["ja", "nein"] = None)-> pd.DataFrame:
        """
        Retrieves sewage data for a given location and timeframe using an API provided by the RKI / Zenodo. 
        The API is part of the AMELAG project by the RKI

        Args:
            start_date (str): Start date of the timeframe for which the data should be retrieved
            end_date (str): End date of the timeframe for which the data should be retrieved
            lat (float): Latitude of the reference point
            long (float): Longitude of the reference point
            virus_type (str | None): Type of virus to retrieve data for. Options are: "SARS-CoV-2", "Influenza A", "Influenza B", "Influenza A+B". Can also be None to retrieve all data. Defaults to None.

        Returns:
            pd.DataFrame: a pandas DataFrame containing the relevant sewage data for the given location and timeframe. 
        """

        # handle invalid timeframes
        if start_date is None or end_date is None:
            warnings.warn("No dates provided")
            start_date = "2022-06-01" # set default timeframe
            end_date = "2024-12-31"
        if start_date <= '2022-06-01' or end_date >= '2024-12-31':
            start_date = "2022-06-01" # set default timeframe
            end_date = "2024-12-31"
            warnings.warn("The API is only available for the timeframe between 2022-06-01 and 2024-12-31")

        # adjust dates to datetimes for comparison
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date) 

        # make API request - the request url points to the RKI publication on Zenodo which is updated weekly
        request_url = "https://zenodo.org/api/records/14192192/files/amelag_einzelstandorte.tsv/content" # the link to the RKI publication
        response = httpx.get(request_url, params={'access_token': settings.SEWAGE_ACESS_TOKEN})

        if response.status_code == 200:
            data = pd.read_csv(BytesIO(response.content), sep='\t')
            data["datum"] = pd.to_datetime(data["datum"]) # convert to datetime
            
            # match the data to the station
            closest_station = self.get_closest_station(latitude, longitude)
            print(f"Es werden die Daten der Station {closest_station['station_name']} verwendet")
            filtered_data = data[data['standort'] == closest_station['station_name']]
            filtered_data = filtered_data[(filtered_data['datum'] >= start_date) & (filtered_data['datum'] <= end_date)]

            if virus_type: # filter for specific virus type
                filtered_data = filtered_data[filtered_data['typ'] == virus_type]

            if is_normalsierung: # filter for if normalization is applied
                filtered_data = filtered_data[filtered_data['normalisierung'] == is_normalsierung]

            return filtered_data

        else: 
            warnings.warn(f"Request failed with status code {response.status_code}")

        return None
