import xml.etree.ElementTree as ET
import datetime, requests, enum

StationColumns = {
    'guid'       : 'Id',
    'istasyon_no': 'No',
    'adi'        : 'Name',
    'aktif'      : 'IsOpen',
    'bos'        : 'EmptyCapacity',
    'dolu'       : 'FullCapacity',
    'lat'        : 'Latitude',
    'lon'        : 'Longitude',
    'sonBaglanti': 'UpdateTime'
    }

def GetStationStatus(stationId: int) -> dict:
    """With this method (post), the status information of the stations
    serving on the İsbike application can be displayed.

    Parameters:
        stationId (int): Station guid (singular) information. (Available from the GetAllStationStatus method)
 
    Returns:
        Id (int): Unique ID of the station
        No (int): station number
        Name (str): station name
        IsOpen (bool): Station status information
        EmptyCapacity (int): Empty parking at the station information.
        FullCapacity (int): Park full at the station information.
        Latitude (float): The station's latitude information
        Longitude (float): Longitude of the station
        UpdateTime (str): Last access time to station
    """
    with requests.Session() as s:
        url = 'https://api.ibb.gov.tr/ispark-bike/GetStationStatus'
        headers = {'Accept-Encoding': 'gzip,deflate'}
        params = {'guid': stationId}

        r = requests.post(url, params=params, headers=headers)
        r.raise_for_status()

        station, = r.json().get('dataList')
        station = {newName: station[oldName] for oldName, newName in StationColumns.items()}
        station.update({
                    'No': int(station['No']),
                    'EmptyCapacity': int(station['EmptyCapacity']),
                    'FullCapacity': int(station['FullCapacity']),
                    'Latitude': float(station['Latitude']),
                    'Longitude': float(station['Longitude']),
                    'UpdateTime': station['UpdateTime'].rsplit('.', 1)[0]
                    })                
        return station
    
def GetAllStationStatus() -> list[dict]:
    """With this method (post), the status information of all stations
    serving on the İsbike application can be displayed.
 
    Returns:
        list[dict]: Returns list of all station information
    """
    with requests.Session() as s:
        url = 'https://api.ibb.gov.tr/ispark-bike/GetAllStationStatus'
        headers={'Accept-Encoding': 'gzip,deflate'}

        r = requests.post(url, headers=headers)
        r.raise_for_status()
        
        if stations := r.json().get('dataList'):
            _ = []
            for station in stations:
                station = {newName: station[oldName] for oldName, newName in StationColumns.items()}
                station.update({
                    'No': int(station['No']),
                    'EmptyCapacity': int(station['EmptyCapacity']),
                    'FullCapacity': int(station['FullCapacity']),
                    'Latitude': float(station['Latitude']),
                    'Longitude': float(station['Longitude']),
                    'UpdateTime': station['UpdateTime'].rsplit('.', 1)[0]
                    })
                _.append(station)
            stations = _
        return stations
