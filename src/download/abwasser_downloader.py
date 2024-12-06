'''
This script matches data to patients from the Sewage water GitHub Repository
-> is part of the project AMELAG (https://github.com/robert-koch-institut/Abwassersurveillance_AMELAG/tree/main)
 

For a location (latitude, longitude) of a patient one can get the data from the nearest station measuring air quality for a given timeframe
'''

import httpx
import pandas as pd
import warnings
from haversine import haversine
from io import BytesIO
from typing import Literal
from src.download.patients import Patient


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
        stations = pd.read_csv("data/raw/2024_11_26_abwasser_standorte.csv")
        return stations

    def get_closest_station(self, patient: Patient) -> dict:
        """
        Find the closest station to a given geographic location based on latitude and longitude 
        using the Haversine formula. 

        Args:
            patient (Patient): patient object

        Returns:
            dict: a dictionary containing the closest station and its distance from the input location. 
        """
        latitude = patient.address.latitude
        longitude = patient.address.longitude

        if latitude is None or longitude is None:
            return None

        closest_station = None
        for index, row in self.all_stations.iterrows(): 

            distance = haversine((latitude, longitude), (row["lat"], row["long"]))

            if closest_station is None or distance < closest_station["distance"]:
                closest_station = {
                    "station_name": row["Kläranlage"],
                    "distance": distance
                }
        return closest_station

        
    def get_sewage_data_patient(self, start_date: str, end_date: str, patient: Patient, virus_type: None | Literal["SARS-CoV-2", "Influenza A", "Influenza B", "Influenza A+B"] = None, is_normalsierung: None | Literal["ja", "nein"] = None)-> pd.DataFrame:
        """
        Retrieves sewage data for a given location and timeframe using weekly updated GitHub data. The repository is part of the AMELAG project by the RKI

        Args:
            start_date (str): Start date of the timeframe for which the data should be retrieved
            end_date (str): End date of the timeframe for which the data should be retrieved
            patient (Patient): patient object
            virus_type (str | None): Type of virus to retrieve data for. Options are: "SARS-CoV-2", "Influenza A", "Influenza B", "Influenza A+B". Can also be None to retrieve all data. Defaults to None.

        Returns:
            pd.DataFrame: a pandas DataFrame containing the relevant sewage data for the given location and timeframe. 
        """
        latitude = patient.address.latitude
        longitude = patient.address.longitude

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

        # get data from public GitHub repository
        request_url = "https://raw.githubusercontent.com/robert-koch-institut/Abwassersurveillance_AMELAG/main/amelag_einzelstandorte.tsv"
        response = httpx.get(request_url)

        if response.status_code == 200:
            data = pd.read_csv(BytesIO(response.content), sep='\t')
            data["datum"] = pd.to_datetime(data["datum"]) # convert to datetime
            
            # match the data to the station
            closest_station = self.get_closest_station(patient)
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

    def get_sewage_data_patient_collection(self, patients: list[Patient], start_date: str, end_date: str, virus_type: None | Literal["SARS-CoV-2", "Influenza A", "Influenza B", "Influenza A+B"] = None, is_normalsierung: None | Literal["ja", "nein"] = None)-> pd.DataFrame:
        """
        Retrieves sewage data for a given patient collection and timeframe using weekly updated GitHub data. The repository is part of the AMELAG project by the RKI

        Args:
            start_date (str): Start date of the timeframe for which the data should be retrieved
            end_date (str): End date of the timeframe for which the data should be retrieved
            virus_type (str | None): Type of virus to retrieve data for. Options are: "SARS-CoV-2", "Influenza A", "Influenza B", "Influenza A+B". Can also be None to retrieve all data. Defaults to None.
            patients (list of Patients): List of patient objects

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

        # get data from public GitHub repository
        request_url = "https://raw.githubusercontent.com/robert-koch-institut/Abwassersurveillance_AMELAG/main/amelag_einzelstandorte.tsv"
        response = httpx.get(request_url)

        if response.status_code == 200:
            data = pd.read_csv(BytesIO(response.content), sep='\t')
            data["datum"] = pd.to_datetime(data["datum"]) # convert to datetime
            
            # match the data to the station
            filtered_data = data[(data['datum'] >= start_date) & (data['datum'] <= end_date)]

            if virus_type: # filter for specific virus type
                filtered_data = filtered_data[filtered_data['typ'] == virus_type]

            if is_normalsierung: # filter for if normalization is applied
                filtered_data = filtered_data[filtered_data['normalisierung'] == is_normalsierung]

            patient_stations = []

            # match patients to stations
            for patient in patients:
                patient_station = self.get_closest_station(patient)
                patient_stations.append({"patient_id": patient.id, "standort": patient_station["station_name"]})

            patient_stations = pd.DataFrame(patient_stations)

            filtered_data = filtered_data[filtered_data['standort'].isin(patient_stations["standort"])]

            merge = pd.merge(filtered_data, patient_stations, on='standort', how='right')
            
            # checks
            assert len(patient_stations) == len(merge["patient_id"].unique()), "Error: Not all patients have a matching station"
            assert len(merge["standort"].unique()) == len(patient_stations["standort"].unique()), "Error: Not all stations are in the merged data"


            return merge 

        else: 
            warnings.warn(f"Request failed with status code {response.status_code}")

        return None
