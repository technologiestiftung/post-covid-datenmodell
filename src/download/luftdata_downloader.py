'''
This script matches data to patients from the Luftdaten API 
-> Umwelt Bundesamt Luftdaten (https://www.umweltbundesamt.de/daten/luft/luftdaten/luftqualitaet/eJzrWJSSuMrIwMhE19BQ18B0UUnmIkPDRXmpCxYVlyxYnOJWBJU00DWyXJwSko-sNreKbVFuctPinMSS0w6eq-a9apQ7vjgnL_20g8o5F4dPFrMBSMokdQ==)

For a location (latitude, longitude) of a patient one can get the data from the nearest station measuring air quality for a given timeframe
'''

from haversine import haversine
import httpx


class AirdataDownloader: 
    def __init__(self):
        self.all_stations = self.get_all_stations()


    def get_all_stations(self) -> list:
        """
        Gets all available air quality stations in Germany that are available through
        the Umwelt Bundesamt Luftdaten API.

        Returns:
            list: list of all available stations with their respective data
        """
        
        # todo: adjust timeframe?
        url = "https://www.umweltbundesamt.de/api/air_data/v3/stations/json?use=airquality&lang=de&date_from=2019-01-01&date_to=2019-01-01&time_from=9&time_to=9"

        response = httpx.get(url)
        response_data = response.json()

        # get necessary station data
        stations = []

        for key, value in response_data["data"].items():
            stations.append({
            "id": value[0],
            "code": value[1],
            "name": value[2], 
            "longitude": float(value[7]), 
            "latitude": float(value[8])})

        # todo: handle API errors or no data

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


    def get_luftdaten_index(self, station_id: str, start_date: str, end_date: str) -> dict: 
        '''
        Function to get the air quality data from the closest station to a given patient location
        The function uses the Umwelt Bundesamt Luftdaten API to get the data, see API here:
        https://www.umweltbundesamt.de/daten/luft/luftdaten/luftqualitaet/eJzrWJSSuMrIwMhE19BQ18B0UUnmIkPDRXmpCxYVlyxYnOJWBJU00DWyXJwSko-sNreKbVFuctPinMSS0w6eq-a9apQ7vjgnL_20g8o5F4dPFrMBSMokdQ==

        Args:
            station_id (str): ID of the needed station
            start_date (str): start date of the timeframe
            end_date (str): end date of the timeframe

        Returns: 
            dict: a dictionary containing the daily mean air quality index for the given timeframe (daily)
        '''
        request_url = f"https://www.umweltbundesamt.de/api/air_data/v3/airquality/json?date_from={start_date}&time_from=1&date_to={end_date}&time_to=24&station={station_id}"
        response = httpx.get(request_url)
        response_data = response.json()
        if response_data["data"]: 
            station_data = response_data["data"].get(station_id, None)


            # INDEX - Tagesmittelwert
            daily_data = {}
            daily_data_index_mean = {}

            # sort values into their days (if multiple values per day)
            for key, value in station_data.items():
                day = key.split(" ")[0]
                if daily_data.get(day, None) is None and value[2]:
                    daily_data[day] = []
                    daily_data[day].append(value[1]) # value[1] = Index
                elif value[1]: # append only if values are valid
                    daily_data[day].append(value[1])

            for key, value in daily_data.items():
                assert len(value) > 0 # if we have a day, we should have at least one value
                assert len(value) < 25 # we can only have 24 measures as there is one per hour
                daily_data_index_mean[key] = sum(value) / len(value)

        # daily_data contains the daily values for the given timeframe, not the mean
        return daily_data_index_mean


    def get_luftdaten_schadstoffe(self, station_id: str, start_date: str, end_date: str) -> dict:

        schadstoff_scope_mapping = {
            1: 6,  # Feinstaub (PM10) PM10 -> stündlich gleitendes Tagesmittel 
            5: 2,  # Stickstoffdioxid NO2 -> Ein-Stunden-Mittelwert 1SMW
            9: 6,  # Feinstaub (PM2,5) PM2,5 -> stündlich gleitendes Tagesmittel
            3: 2,  # Ozon O3 -> Ein-Stunden-Mittelwert 1SMW
        }

        schadstoff_data = {}

        # iterate over all components and get the data
        for key, value in schadstoff_scope_mapping.items():
            component = key
            scope = value
        
            request_url = f"https://www.umweltbundesamt.de/api/air_data/v3/measures/json?date_from={start_date}&time_from=1&date_to={end_date}&time_to=24&station={station_id}&component={component}&scope={scope}"
            response = httpx.get(request_url)
            response_data = response.json()

            if response_data["data"]: 
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
                    # print(value)
                    assert len(value) > 0 # if we have a day, we should have at least one value
                    assert len(value) < 25 # we can only have 24 measures as there is one per hour
                    daily_data_mean[key] = sum(value) / len(value)
                
                schadstoff_data[str(component)] = daily_data_mean
            

        
        return schadstoff_data