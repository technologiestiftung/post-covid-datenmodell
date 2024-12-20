'''
This script matches data to patients from the Luftdaten API 
-> Umwelt Bundesamt Luftdaten (https://www.umweltbundesamt.de/daten/luft/luftdaten/luftqualitaet/eJzrWJSSuMrIwMhE19BQ18B0UUnmIkPDRXmpCxYVlyxYnOJWBJU00DWyXJwSko-sNreKbVFuctPinMSS0w6eq-a9apQ7vjgnL_20g8o5F4dPFrMBSMokdQ==)

For a location (latitude, longitude) of a patient one can get the data from the nearest station measuring air quality for a given timeframe
'''

from haversine import haversine
import httpx
import pandas as pd
import warnings
from src.download.patients import Patient


class AirdataDownloader: 
    def __init__(self):
        self.all_stations = self.get_all_stations()
       

    def get_all_stations(self, time_start: str = "2019-01-01", time_end: str = "2024-12-31") -> list:
        """
        Gets all available air quality stations in Germany that are available through
        the Umwelt Bundesamt Luftdaten API.

        Args:
            time_start (str): start date of the timeframe, default is 2019-01-01
            time_end (str): end date of the timeframe, default is 2024-12-31

        Returns:
            list: list of all available stations with their respective data
        """
        

        url = f"https://www.umweltbundesamt.de/api/air_data/v3/stations/json?use=airquality&lang=de&date_from={time_start}&date_to={time_end}&time_from=1&time_to=24"

        
        try: 
            response = httpx.get(url, timeout=20.0)
            response_data = response.json()

            # get necessary station data
            stations = []

            # if response is valid
            if response_data["data"]:
                for key, value in response_data["data"].items():
                    stations.append({
                    "id": value[0],
                    "code": value[1],
                    "name": value[2], 
                    "longitude": float(value[7]), 
                    "latitude": float(value[8])})
        except httpx.ReadTimeout:
            warnings.warn("Request timed out")
            


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

        # handle missing position
        if lat is None or long is None:
            return None

        stations = self.all_stations

        closest_station = None
        for station in stations: 

            distance = haversine((lat, long), (station["latitude"], station["longitude"]))

            if closest_station is None or distance < closest_station["distance"]:
                closest_station = {
                    "station": station,
                    "distance": distance
                }
        return closest_station


    def get_luftdaten_index_patient(self, longitude: float, latitude: float, start_date: str, end_date: str) -> pd.DataFrame: 
        '''
        Function to get the air quality data from the closest station to a given patient location
        The function uses the Umwelt Bundesamt Luftdaten API to get the data, see API here:
        https://www.umweltbundesamt.de/daten/luft/luftdaten/luftqualitaet/eJzrWJSSuMrIwMhE19BQ18B0UUnmIkPDRXmpCxYVlyxYnOJWBJU00DWyXJwSko-sNreKbVFuctPinMSS0w6eq-a9apQ7vjgnL_20g8o5F4dPFrMBSMokdQ==

        Args:
            longitude (float): longitude of the patient 
            latitude (float): latitude of the patient
            start_date (str): start date of the timeframe
            end_date (str): end date of the timeframe

        Returns: 
            pd.DataFrame: a dataframe containing the daily mean air quality index for the given timeframe (daily)
        '''

        # find nearest station 
        closest_station = self.get_closest_station(latitude, longitude)
        station_id = closest_station['station']['id']

        request_url = f"https://www.umweltbundesamt.de/api/air_data/v3/airquality/json?date_from={start_date}&time_from=1&date_to={end_date}&time_to=24&station={station_id}"
        response = httpx.get(request_url, timeout=20.0)
        response_data = response.json()

        if response_data["data"] and len(response_data["data"]) > 0: 
            
            station_data = response_data["data"].get(station_id, None)

            # INDEX - Tagesmittelwert
            daily_data = {}
            daily_data_index_mean = {}

            # sort values into their days (if multiple values per day)
            for key, value in station_data.items():
                day = key.split(" ")[0]
                if daily_data.get(day, None) is None and value[1]:
                    daily_data[day] = []
                    daily_data[day].append(value[1]) # value[1] = Index
                elif value[1]: # append only if values are valid
                    daily_data[day].append(value[1])

            for key, value in daily_data.items():
                assert len(value) > 0 # if we have a day, we should have at least one value
                assert len(value) < 25 # we can only have 24 measures as there is one per hour
                daily_data_index_mean[key] = sum(value) / len(value)

            # daily_data contains the daily values for the given timeframe, not the mean
            daily_data_index_mean = pd.DataFrame(list(daily_data_index_mean.items()), columns=['Date', 'Index'])
            daily_data_index_mean["standort"] = [(longitude, latitude)] * len(daily_data_index_mean)
            return daily_data_index_mean

        else: 
            warnings.warn("No data available for the given request")
        
        return None


    def get_luftdaten_schadstoffe_patient(self, longitude: float, latitude: float, start_date: str, end_date: str) -> pd.DataFrame:
        '''
        Function to get the schadstoffe (pollutant) data from the closest station to a given patient location
        The function uses the Umwelt Bundesamt Luftdaten API to get the data, see API here:
        https://www.umweltbundesamt.de/daten/luft/luftdaten/luftqualitaet/eJzrWJSSuMrIwMhE19BQ18B0UUnmIkPDRXmpCxYVlyxYnOJWBJU00DWyXJwSko-sNreKbVFuctPinMSS0w6eq-a9apQ7vjgnL_20g8o5F4dPFrMBSMokdQ==

        Args:
            longitude (float): longitude of the patient 
            latitude (float): latitude of the patient
            start_date (str): start date of the timeframe
            end_date (str): end date of the timeframe

        Returns: 
            pd.DataFrame: a dataframe containing the daily mean schadstoffe (pollutant) data for the given timeframe (daily)

        '''

        # find nearest station 
        closest_station = self.get_closest_station(latitude, longitude)
        station_id = closest_station['station']['id']

        schadstoff_scope_mapping = {
            1: 6,  # Feinstaub (PM10) PM10 -> stündlich gleitendes Tagesmittel 
            5: 2,  # Stickstoffdioxid NO2 -> Ein-Stunden-Mittelwert 1SMW
            9: 6,  # Feinstaub (PM2,5) PM2,5 -> stündlich gleitendes Tagesmittel
            3: 2,  # Ozon O3 -> Ein-Stunden-Mittelwert 1SMW
        }

        component_name_mapping = {
            1: "Feinstaub (PM10)",
            5: "Stickstoffdioxid",
            9: "Feinstaub (PM2,5)",
            3: "Ozon"
        }

        schadstoff_data = {}

        # iterate over all components and get the data
        for key, value in schadstoff_scope_mapping.items():
            component = key
            component_name = component_name_mapping[component]
            scope = value
        
            request_url = f"https://www.umweltbundesamt.de/api/air_data/v3/measures/json?date_from={start_date}&time_from=1&date_to={end_date}&time_to=24&station={station_id}&component={component}&scope={scope}"
            response = httpx.get(request_url, timeout=10.0)
            response_data = response.json()

            # if request is successful
            if response_data["data"] and len(response_data["data"]) > 0: 
                station_data = response_data["data"].get(station_id, None)

                daily_data = {}
                daily_data_mean = {}

                # sort values into their days (if multiple values per day)
                for key, value in station_data.items():
                    day = key.split(" ")[0]
                    if daily_data.get(day, None) is None and value[2]:
                        daily_data[day] = []
                        daily_data[day].append(value[2]) # value[2] = measurement

                    elif value[2]: # append only if values are valid
                        daily_data[day].append(value[2])

                for key, value in daily_data.items():
                    assert len(value) > 0 # if we have a day, we should have at least one value
                    assert len(value) < 25 # we can only have 24 measures as there is one per hour
                    daily_data_mean[key] = sum(value) / len(value)
                
                schadstoff_data[component_name] = daily_data_mean
            # if the measurement is not available
            else : 
                schadstoff_data[component_name] = None
            

        schadstoff_data = pd.DataFrame(schadstoff_data)
        schadstoff_data["standort"] = [(longitude, latitude)] * len(schadstoff_data)
        schadstoff_data.index.name = "Date"
        schadstoff_data.reset_index(inplace=True)
        return schadstoff_data


    def get_luftdaten_index_patient_collection(self, patients: list[Patient], start_date: str, end_date: str) -> pd.DataFrame: 
        '''
        Function to get the air quality data from a patient collection
        The function uses the Umwelt Bundesamt Luftdaten API to get the data, see API here:
        https://www.umweltbundesamt.de/daten/luft/luftdaten/luftqualitaet/eJzrWJSSuMrIwMhE19BQ18B0UUnmIkPDRXmpCxYVlyxYnOJWBJU00DWyXJwSko-sNreKbVFuctPinMSS0w6eq-a9apQ7vjgnL_20g8o5F4dPFrMBSMokdQ==

        Args:
            patients (list[Patient]): list of patient objects
            start_date (str): start date of the timeframe
            end_date (str): end date of the timeframe

        Returns: 
            pd.DataFrame: a dataframe containing the daily mean air quality index for the given timeframe (daily)
        '''
        patient_stations = []

        
        patient_positions = []
        for patient in patients:
            long_lat = (patient.address.longitude, patient.address.latitude)
            patient_positions.append({"patient_id": patient.id, "standort": long_lat})

        patient_positions = pd.DataFrame(patient_positions)

        result_df = pd.DataFrame()

        # Iterate over a range and append the DataFrames
        for position in patient_positions["standort"].unique(): 
            new_df = self.get_luftdaten_index_patient(longitude = position[0], latitude=position[1], start_date = start_date, end_date = end_date)
            result_df = pd.concat([result_df, new_df], ignore_index=True)

        merge = pd.merge(result_df, patient_positions, on='standort', how='right')

        # checks
        assert len(merge["patient_id"].unique()) == len(patients)
        assert len(patient_positions) == len(merge["patient_id"].unique()), "Error: Not all patients have a matching station"
        assert len(merge["standort"].unique()) == len(patient_positions["standort"].unique()), "Error: Not all stations are in the merged data"
        
        return merge


    def get_luftdaten_schadstoffe_patient_collection(self, patients: list[Patient], start_date: str, end_date: str) -> pd.DataFrame:
        '''
        Function to get the schadstoffe (pollutant) data from the closest station for a patient collection
        The function uses the Umwelt Bundesamt Luftdaten API to get the data, see API here:
        https://www.umweltbundesamt.de/daten/luft/luftdaten/luftqualitaet/eJzrWJSSuMrIwMhE19BQ18B0UUnmIkPDRXmpCxYVlyxYnOJWBJU00DWyXJwSko-sNreKbVFuctPinMSS0w6eq-a9apQ7vjgnL_20g8o5F4dPFrMBSMokdQ==

        Args:
            patients (list[Patient]): list of patient objects
            start_date (str): start date of the timeframe
            end_date (str): end date of the timeframe

        Returns: 
            pd.DataFrame: a dataframe containing the daily mean schadstoffe (pollutant) data for the given timeframe (daily) and for each patient (identified by patient_id)
        '''
        
        patient_stations = []

        patient_positions = []
        for patient in patients:
            long_lat = (patient.address.longitude, patient.address.latitude)
            patient_positions.append({"patient_id": patient.id, "standort": long_lat})

        patient_positions = pd.DataFrame(patient_positions)

        result_df = pd.DataFrame()

        # Iterate over a range and append the DataFrames
        for position in patient_positions["standort"].unique(): 
            new_df = self.get_luftdaten_schadstoffe_patient(longitude = position[0], latitude=position[1], start_date = start_date, end_date = end_date)
            result_df = pd.concat([result_df, new_df], ignore_index=True)

        merge = pd.merge(result_df, patient_positions, on='standort', how='right')

        # checks
        assert len(merge["patient_id"].unique()) == len(patients)
        assert len(patient_positions) == len(merge["patient_id"].unique()), "Error: Not all patients have a matching station"
        assert len(merge["standort"].unique()) == len(patient_positions["standort"].unique()), "Error: Not all stations are in the merged data"
        
        return merge