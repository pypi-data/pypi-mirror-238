from datetime import datetime
import requests, re

def GetAQIStations() -> list[dict]:
    """Information of Air Quality stations is shared with this web service.

    Id (int): Contains StationId information. It is a unique field.
    
    Name (str): Contains the station name information.
    
    Address (str): Contains station address information.
    
    Latitude (float): Contains the Latitude of the station.
    
    Longitude (float): Contains the Longitude of the station.
    
    Returns:
        dict: Returns the list of stationId, Name, Address and Location.
    """
    with requests.Session() as s:
        url = 'https://api.ibb.gov.tr/havakalitesi/OpenDataPortalHandler/GetAQIStations'
        r = s.get(url, headers={'Accept-Encoding': 'gzip, deflate'})
        r.raise_for_status()

        pattern  = r'POINT\s\((?P<Lng>.*)\s(?P<Lat>.*)\)'
        stations = []

        for station in r.json():
            address  = station.pop('Adress')
            location = station.pop('Location')
            matches  = re.match(pattern, location)
            station.update({
                'Address': address,
                'Latitude': float(matches.group('Lat')),
                'Longitude': float(matches.group('Lng'))
                })
            stations.append(station)
            
        return stations
    
def GetAQIByStationId(stationId: str, startDate: datetime, endDate: datetime) -> tuple[list[dict], list[dict]]:
    """With this web service, Concentration and Air Quality Index (AQI)
    information is shared according to the start and end dates of the station
    whose ID is entered.
    
    Parameters:
        stationId (int): It is the Unique Id of the station whose measurement information will be retrieved.
        
        startDate (datetime): The specified date is determined as the startdate of the measurements.
        
        endDate (datetime): The specified date is determined as the end date of the measurements.
 
    Returns:
        list[dict]: PM10, SO2, O3, NO2 and CO measured from the Station's Analyzer contains the value of the data.
        
        list[dict]: The values of PM10, SO2, O3, NO2 and CO raw data measured from the Analyzer of the station after
        calculating the AirQuality Index and the HKI value for that hour, the Pollutant parameter,the status
        and the status includes color.
    """
    with requests.Session() as s:
        url = 'https://api.ibb.gov.tr/havakalitesi/OpenDataPortalHandler/GetAQIByStationId'
        params = {
            'StationId': stationId,
            'StartDate': startDate.strftime('%d.%m.%Y %H:%M:%S'),
            'EndDate': endDate.strftime('%d.%m.%Y %H:%M:%S')
            }
        r = s.get(url, params=params, headers={'Accept-Encoding': 'gzip, deflate'})
        r.raise_for_status()

        C, A = [], []
        for record in r.json():
            ReadTime = record.pop('ReadTime')
            ReadTime = datetime.fromisoformat(ReadTime).isoformat()
            if c := record.get('Concentration'):
                c |= {'ReadTime': ReadTime}
                C.append(c)
            if a := record.get('AQI'):
                a |= {'ReadTime': ReadTime}
                A.append(a)

        return C, A