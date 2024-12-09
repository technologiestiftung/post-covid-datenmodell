'''
This script retrieves weather data from the Brightsky API
-> Brightsky API (https://brightsky.dev/docs/#/)

For a location (latitude, longitude) of a patient one can get the weather data for a given timeframe
'''

import httpx
import pandas as pd
import warnings
from src.download.patients import Patient


class WeatherdataDownloader: 
    def __init__(self):
        self.weather_unit_mapping = {
            "precipitation": "Niederschlag (mm)",
            "pressure_msl": "Luftdruck (hPa)",
            "sunshine": "Sonnenscheindauer (min)",
            "temperature": "Temperatur (°C)",
            "wind_speed": "Windgeschwindigkeit (km / h)",
            "relative_humidity": "Relative Luftfeuchtigkeit (%)",
        }

    def get_weatherdata_patient(self, latitude: float, longitude: float, start_date: str, end_date: str ) -> pd.DataFrame:
        """
        Function to get the weatherdata from the longitude, latitude position of one patient.
        The function uses the Brightsky API to get the data, see API documentation here: https://brightsky.dev/docs/#/

        Args: 
            latitude (float): the latitude postion of the patient
            longitude (float): the longitude postion of the patient
            start_date : start date of the timeframe, in format: "YYYY-MM-DD"
            end_date : end date of the timeframe, in format: "YYYY-MM-DD"

        Returns:
            pd.DataFrame containing the 'Tagesmittelwerte', daily means of the weather data, including the following columns:
            'Tag', 'precipitation', 'pressure_msl', 'sunshine', 'temperature', 'wind_speed', 'relative_humidity'
        """

         # adjust times to match API format
        start_date_timed = start_date + "T00:00:00"
        end_date_timed = end_date + "T23:00:00"

        request_url = f"https://api.brightsky.dev/weather?lat={latitude}&lon={longitude}&date={start_date_timed}&last_date={end_date_timed}&units=dwd&tz=Europe/Berlin"
        response = httpx.get(request_url)
        response_data = response.json()
        

       
        if "weather" in response_data.keys():  # valid response
            numeric_cols = ['precipitation', 'pressure_msl', 'sunshine', 'temperature', 'wind_speed', 'relative_humidity']

            timeseries_data = pd.DataFrame(response_data["weather"]) # hourly data
            timeseries_data = timeseries_data[["timestamp", 'precipitation', 'pressure_msl', 'sunshine', 'temperature', 'wind_speed', 'relative_humidity']]
            timeseries_data["Tag"] = timeseries_data["timestamp"].apply(lambda x: x.split("T")[0]) # get daily data
            daily_means = timeseries_data.groupby('Tag')[numeric_cols].mean() # mean skips NaN values by default
            daily_means.reset_index(inplace=True)
            daily_means.rename(columns=self.weather_unit_mapping, inplace=True)
            daily_means["standort"] = [(longitude, latitude)] * len(daily_means)

            return daily_means # timeseries_data
        else: 
            warnings.warn("No data available for the given request")
        return None


    def get_weatherdata_patient_collection(self, patients: list[Patient], start_date: str, end_date: str ) -> pd.DataFrame:
        """
        Function to get the weatherdata from a collection of patients.
        The function uses the Brightsky API to get the data, see API documentation here: https://brightsky.dev/docs/#/

        Args: 
            patients: patient collection
            start_date : start date of the timeframe, in format: "YYYY-MM-DD"
            end_date : end date of the timeframe, in format: "YYYY-MM-DD"

        Returns:
            pd.DataFrame containing the 'Tagesmittelwerte', daily means of the weather data, including the following columns:
            'Tag', 'precipitation', 'pressure_msl', 'sunshine', 'temperature', 'wind_speed', 'relative_humidity'
        """

        patient_positions = []
        for patient in patients:
            long_lat = (patient.address.longitude, patient.address.latitude)
            patient_positions.append({"patient_id": patient.id, "standort": long_lat})


        patient_positions = pd.DataFrame(patient_positions)

        result_df = pd.DataFrame()

        # Iterate over a range and append the DataFrames
        for position in patient_positions["standort"].unique(): 
            new_df = self.get_weatherdata_patient(longitude = position[0], latitude=position[1], start_date = start_date, end_date = end_date)
            result_df = pd.concat([result_df, new_df], ignore_index=True)

        merge = pd.merge(result_df, patient_positions, on='standort', how='right')

        # checks
        assert len(merge["patient_id"].unique()) == len(patients)
        assert len(patient_positions) == len(merge["patient_id"].unique()), "Error: Not all patients have a matching station"
        assert len(merge["standort"].unique()) == len(patient_positions["standort"].unique()), "Error: Not all stations are in the merged data"
        
        return merge
        