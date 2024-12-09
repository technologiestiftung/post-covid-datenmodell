'''
This script is used to access data relatived to SARS-CoV-2 infections in Germany.
It uses a csv file from the Robert Koch Institute (RKI) that contains information about the infections in Germany.
-> The csv comes from their repository: https://github.com/robert-koch-institut/SARS-CoV-2-Infektionen_in_Deutschland

The data is filtered by the postal code of the patient to get the closest "station" (landkreis) to the patient.
The data can additionally be filtered by age group (groups are provided by the RKI) and gender

'''

import httpx
import pandas as pd
import warnings
from io import BytesIO

from src.download.patients import Patient
from src.geolocation.address_transformation import get_landkreis_id_from_postal_code
from src.utils.time_age_calculation import calculate_age, find_age_group




class CovidDataDownloader:
    def __init__(self):
        self.age_groups =[
        {"group": "A00-A04", "min_age": 0, "max_age": 4},
        {"group": "A05-A14", "min_age": 5, "max_age": 14},
        {"group": "A15-A34", "min_age": 15, "max_age": 34},
        {"group": "A35-A59", "min_age": 35, "max_age": 59},
        {"group": "A60-A79", "min_age": 60, "max_age": 79},
        {"group": "A80+", "min_age": 90, "max_age": 150},]


    def get_closest_station(self, postal_code: str)-> str or None:
        '''
        Function gets the closest station by using the postal code of the patient(s)

        Args:
            postal_code (str): postal code of the patient(s)
        Returns: 
            str | None: closest "station" to the patient(s), the landkreis id that can be used to get the covid data
        '''
        landkreis_id = get_landkreis_id_from_postal_code(postal_code) 

        return landkreis_id


    def get_coviddata_patient(self, patient: Patient, start_date: str, end_date: str, filter_gender: bool = False, filter_age: bool = False)-> pd.DataFrame:
        '''
        Function to get the covid data for a single patient.

        Args: 
            patient (Patient): patient object
            start_date (str): start date of the timeframe, in format: "YYYY-MM-DD"
            end_date (str): end date of the timeframe, in format: "YYYY-MM-DD"
            patient: patient object
            filter_gender (bool): if True, the data will be filtered
            filter_age (bool): if True, the data will be filtered

        Returns: 
            pd.DataFrame containing the covid data for the selected timeframe, (if applied) gender and age group
        '''

        # get relevant landkreis_id
        landkreis_id = self.get_closest_station(patient.address.postal_code)

        if landkreis_id is None: # abort if no landkreis_id is found
            return None

        request_url = "https://media.githubusercontent.com/media/robert-koch-institut/SARS-CoV-2-Infektionen_in_Deutschland/refs/heads/main/Aktuell_Deutschland_SarsCov2_Infektionen.csv"

        with httpx.stream("GET", request_url, timeout = httpx.Timeout(80.0)) as response:
            if response.status_code == 200:
                # Stream the data directly into a BytesIO buffer
                buffer = BytesIO()
                for chunk in response.iter_bytes():
                    buffer.write(chunk)
                buffer.seek(0)  # Reset the buffer pointer to the beginning
                    
                df = pd.read_csv(buffer) 
                
                # filter df
                df = df[df["IdLandkreis"] == landkreis_id] # filter for landkreis_id
                # info: Refdatum as it is either the date of the first symptoms or the date the person reported the symptoms
                df["Refdatum"] = pd.to_datetime(df["Refdatum"])
                df = df[(df["Refdatum"] >= start_date) & (df["Refdatum"] <= end_date)] # filter for date range
                if filter_gender: 
                    gender = patient.gender
                    if gender:
                        gender_mapping = {"male": "M", "female": "W", "other": "unbekannt", "unknown": "unbekannt"}
                        gender_mapped = gender_mapping.get(gender, None)
                        df = df[df["Geschlecht"] == gender_mapped] # filter for gender
                    else: 
                        warnings.warn("We could not find a gender for the patient")

                if filter_age:  # filter for age group
                    age = calculate_age(patient.birth_date)
                    age_group = find_age_group(age, self.age_groups)
                    if age and age_group:
                        df = df[df["Altersgruppe"] == age_group]
                    else: 
                        warnings.warn("No age or age group could be found")

                # add patient info
                df["patient_id"] = patient.id
                return df

            else:
                warnings.warn("No data could be retrieved")

        return None

    def get_coviddata_patient_collection(self, patients: list(Patient), start_date: str, end_date: str, filter_gender: bool = False, filter_age: bool = False)-> pd.DataFrame:
        '''
        Function to get the covid data for a patient collection.

        Args: 
            patients (list(Patient)): patient collection
            start_date (str): start date of the timeframe, in format: "YYYY-MM-DD"
            end_date (str): end date of the timeframe, in format: "YYYY-MM-DD"
            patient: patient object
            filter_gender (bool): if True, the data will be filtered
            filter_age (bool): if True, the data will be filtered

        Returns: 
            pd.DataFrame containing the covid data for the selected timeframe, (if applied) gender and age group
        '''

        # get all relevant patient info
        gender_mapping = {"male": "M", "female": "W", "other": "unbekannt", "unknown": "unbekannt"}


        patient_info = []

        for patient in patients:
            patient_landkreis = self.get_closest_station(postal_code = patient.address.postal_code)
            patient_age = calculate_age(patient.birth_date)
            patient_age_group = find_age_group(patient_age, self.age_groups)
            patient_gender_mapped = gender_mapping.get(patient.gender, None)

            patient_info.append({"patient_id": patient.id, 
                                "IdLandkreis": patient_landkreis, 
                                "patient_geschlecht": patient_gender_mapped, 
                                "patient_altersgruppe": patient_age_group})


        patient_info = pd.DataFrame(patient_info)
        landkreis_ids = patient_info["IdLandkreis"].unique()

        # make request
        request_url = "https://media.githubusercontent.com/media/robert-koch-institut/SARS-CoV-2-Infektionen_in_Deutschland/refs/heads/main/Aktuell_Deutschland_SarsCov2_Infektionen.csv"
        with httpx.stream("GET", request_url, timeout = httpx.Timeout(80.0)) as response:
            if response.status_code == 200:
                # Stream the data directly into a BytesIO buffer
                buffer = BytesIO()
                for chunk in response.iter_bytes():
                    buffer.write(chunk)
                buffer.seek(0)  # Reset the buffer pointer to the beginning
                    
                df = pd.read_csv(buffer) 
                # filter df
                df = df[df["IdLandkreis"].isin(landkreis_ids)] # filter for landkreis_id
                
                # info: Refdatum as it is either the date of the first symptoms or the date the person reported the symptoms
                df["Refdatum"] = pd.to_datetime(df["Refdatum"])
                df = df[(df["Refdatum"] >= start_date) & (df["Refdatum"] <= end_date)] # filter for date range

                merge = pd.merge(df, patient_info, on='IdLandkreis', how='right')
                
                # further filtering - if wanted
                if filter_age: 
                    merge = merge[merge["Altersgruppe"] == merge["patient_altersgruppe"]]
                if filter_gender: 
                    merge = merge[merge["Geschlecht"] == merge["patient_geschlecht"]]

                return merge

            else:
                warnings.warn("No data could be retrieved")

            return None