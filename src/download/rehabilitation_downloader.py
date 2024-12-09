'''
this script matches data to patients from the rehabilitation center data
-> source https://www.reha-einrichtungsverzeichnis.de/suche.html

For a location (latitude, longitude) of a patient one can get the data from the nearest rehabilitation center

'''

import pandas as pd
import json
from haversine import haversine
from src.download.patients import Patient

class RehabilitationDownloader:
    def __init__(self):
        self.all_stations = self.get_all_stations()


    def get_all_stations(self) -> pd.DataFrame: 
        '''
        Gets all available stations for rehabilitation centers in Germany.
        Data comes from https://www.reha-einrichtungsverzeichnis.de/suche.html

        Returns: 
            pd.DataFrame: DataFrame with all available stations with rehabilitation offers
        '''
        with open("data/raw/2024-12-02_post_covid_reha.json", 'r') as file:
            stations_data = json.load(file)
        stations = pd.DataFrame(stations_data["data"])

        return stations


    def get_closest_station(self, patient: Patient) -> dict:
        """
        Find the closest station to a given geographic location based on latitude and longitude 
        using the Haversine formula. 

        Args:
            patient (Patient): Patient object

        Returns:
            dict: a dictionary containing the closest station and its distance (km) from the input location. 
        """
        latitude = patient.address.latitude
        longitude = patient.address.longitude

        if latitude is None or longitude is None:
            return None

        closest_station = None

        for index, row in self.all_stations.iterrows():

            distance = haversine((latitude, longitude), (float(row["latitude"]), float(row["longitude"])))

            if closest_station is None or distance < closest_station["distance"]:
                closest_station = {
                    "patient_id": patient.id,
                    "reha_station_short": row["nameKurz"],
                    "reha_station_long": row["nameLang"],
                    "distance": distance
                }
        return closest_station


    def get_rehabilitation_data_patient(self, patient: Patient) -> pd.DataFrame: 
        """
        Get the rehabilitation data for a patient based on the location. 
        The data is based on the closest station to the patient's location. 

        Args:
            patient (Patient): Patient object

        Returns:
            pd.DataFrame: DataFrame containing the rehabilitation data for the patient
        """
        closest_station = pd.DataFrame(self.get_closest_station(patient), index = [0])

        return closest_station


    def get_rehabilitation_data_patient_collection(self, patients)-> pd.DataFrame:
        """
        Get the rehabilitation data for a patient based on the location. 
        The data is based on the closest station to the patient's location. 

        Args:
            patients (list): List of patient objects

        Returns:
            pd.DataFrame: DataFrame containing the rehabilitation data for the patient
        """
        
        result_df = pd.DataFrame()

        # Iterate over a range and append the DataFrames
        for patient in patients: 
            new_df = self.get_rehabilitation_data_patient(patient = patient)
            result_df = pd.concat([result_df, new_df], ignore_index=True)


        # checks
        assert len(result_df["patient_id"].unique()) == len(patients)
    
        return result_df

        
