'''
This script retrieves weather data from the Brightsky API
-> Brightsky API (https://brightsky.dev/docs/#/)

For a location (latitude, longitude) of a patient one can get the weather data for a given timeframe
'''

import httpx
import pandas as pd
import warnings


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

    def get_weatherdata(self, latitude: float, longitude: float, start_date: str, end_date: str ) -> pd.DataFrame:
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

            return daily_means # timeseries_data
        else: 
            warnings.warn("No data available for the given request")
        return None