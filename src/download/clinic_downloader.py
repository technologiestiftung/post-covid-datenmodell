'''
This script matches data to patients from the clinic (for long covid) data
-> source: https://www.bmg-longcovid.de/service/buergertelefon-und-regionale-kliniksuche
'''

import pandas as pd
import json
from haversine import haversine

from src.download.patients import Patient
from src.geolocation.address_transformation import get_long_lat_from_postal_code


class ClinicDownloader:
    def __init__(self): 
        self.all_stations = self.get_all_stations()



    def get_all_stations(self) -> pd.DataFrame:
        '''
        Gets all available stations for clinics in Germany.
        Data comes from https://www.bmg-longcovid.de/service/buergertelefon-und-regionale-kliniksuche

        Returns: 
            pd.DataFrame: DataFrame with all available stations with clinic offers
        '''
        with open("data/raw/2024-12-02_post_covid_ambulanzen_kliniken.json", "r") as file:
            stations_data = json.load(file)
        
        stations = pd.DataFrame(stations_data["data"])

        # Add longitude and latitude columns
        stations["longitude"] = None
        stations["latitude"] = None

        # Update longitude and latitude if available
        for index, row in stations.iterrows():
            long_lat = get_long_lat_from_postal_code(row["zip"])
            if long_lat is not None:
                stations.loc[index, ["longitude", "latitude"]] = long_lat
            else:
                stations.loc[index, ["longitude", "latitude"]] = None, None

        return stations


    def get_closest_station(self, patient)-> dict:
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
            if row["latitude"] is None or row["longitude"] is None:
                continue

            else:

                distance = haversine((latitude, longitude), (float(row["latitude"]), float(row["longitude"])))

                if closest_station is None or distance < closest_station["distance"]:
                    closest_station = {
                        "patient_id": patient.id,
                        "name": row["name"],
                        "state": row["state"],
                        "place": row["place"],
                        "zip": row["zip"],
                        "link": row["link"],
                        "type": row["type"],
                        "focusarea1": row["focusarea1"],
                        "focusarea2": row["focusarea2"],
                        "distance": distance
                    }
        return closest_station


    def get_clinic_data_patient(self, patient) -> pd.DataFrame: 
        """
        Get the clinic data for a patient based on the location. 
        The data is based on the closest station to the patient's location. 

        Args:
            patient (Patient): Patient object

        Returns:
            pd.DataFrame: DataFrame containing the clinic data for the patient
        """

        closest_station = pd.DataFrame(self.get_closest_station(patient), index = [0])

        return closest_station


    def get_clinic_data_patient_collection(self, patients: list[Patient])-> pd.DataFrame:
        """
        Get the clinic data for a patient based on the location. 
        The data is based on the closest station to the patient's location. 

        Args:
            patients (list of Patients): List of patient objects

        Returns:
            pd.DataFrame: DataFrame containing the clinic data for the patient
        """
        
        result_df = pd.DataFrame()

        # Iterate over a range and append the DataFrames
        for patient in patients: 
            new_df = self.get_clinic_data_patient(patient = patient)
            result_df = pd.concat([result_df, new_df], ignore_index=True)


        # checks
        assert len(result_df["patient_id"].unique()) == len(patients)
    
        return result_df
