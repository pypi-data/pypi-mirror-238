from datetime import datetime
import requests

ParkColumns = {
    'parkID'       : 'Id',
    'parkName'     : 'Name',
    'lat'          : 'Latitude',
    'lng'          : 'Longitude',
    'capacity'     : 'Capacity',
    'emptyCapacity': 'EmptyCapacity',
    'workHours'    : 'WorkHours',
    'parkType'     : 'Type',
    'freeTime'     : 'FreeTime',
    'district'     : 'District',
    'isOpen'       : 'IsOpen'
    }

DetailColumns = {
    'parkID'       : 'Id',
    'parkName'     : 'Name',
    'lat'          : 'Latitude',
    'lng'          : 'Longitude',
    'capacity'     : 'Capacity',
    'emptyCapacity': 'EmptyCapacity',
    'workHours'    : 'WorkHours',
    'parkType'     : 'Type',
    'freeTime'     : 'FreeTime',
    'district'     : 'District',
    'locationName' : 'LocationName',
    'updateDate'   : 'UpdateTime',
    'monthlyFee'   : 'MonthlyFee',
    'tariff'       : 'Tariff',
    'address'      : 'Address',
    'areaPolygon'  : 'AreaPolygon'
    }

def GetAllParks() -> list[dict]:
    """This method will return the information of all Ispark car parks.
    The returning list will have dictionary with the following parameters

    Capacity (int): The total capacity of the park.
    
    District (str): District where the park is located.
    
    EmptyCapacity (int): Empty capacity of the park.
    
    FreeTime (int): Free parking time (minute).
    
    Id (int): Contains Park Id information. It is a unique field.
    
    IsOpen (bool): Is the park open.
    
    Latitude (float): Latitude information of the park.
    
    Longitude (float): Longitude information of the park.
    
    Name (str): Contains park name information.
    
    Type (str): Type of park (on road, open, closed).
    
    WorkHours (str): Working hours of the park.
    
    Returns:
        list[dict]: The information of all Ispark car parks
    """
    with requests.Session() as s:        
        url = 'https://api.ibb.gov.tr/ispark/Park'
        r = s.get(url, headers={'Accept-Encoding': 'gzip,deflate'})
        r.raise_for_status()

        parks = []
        for park in r.json():
            park = {newName: park[oldName] for oldName, newName in ParkColumns.items()}
            park.update({
                'Latitude': float(park['Latitude']),
                'Longitude': float(park['Longitude']),
                'IsOpen': park['IsOpen'] != 0
                })
            parks.append(park)
            
        return parks
    
def GetParkDetail(parkId: int) -> dict:
    """With this web service, detailed information of any Ispark car park
    can be accessed with given parkId

    Id (int): Contains Park Id information. It is a unique field.
    
    Name (str): Contains park name information.
    
    Latitude (float): Contains park latitude information.
    
    Longitude (float): Contains park longitude information.
    
    Capacity (int): The total capacity of the park.
    
    EmptyCapacity (int): The empty capacity of the park.
    
    WorkHours (str): Park opening hours.
    
    Type (str): Type of park (on road, open, closed).
    
    FreeTime (int): Free parking time (minute).
    
    District (str): District where the park is located.
    
    LocationName (str): Contains location name information.
    
    UpdateTime (str): Update date and time of information
    
    MonthlyFee (float): Monthly Subscription Fee.
    
    Tariff (dict[str, float]): List of Tariff Information object with Tariff(string) and Price(float) key-value pairs
    
    Address (str): Parking lot address.
    
    AreaPolygon (str): Parking polygon information.
    
    Parameters:
        parkId (int): The desired park id.
 
    Returns:
        dict: Detailed information about desired car park.
    """
    with requests.Session() as s:        
        url = 'https://api.ibb.gov.tr/ispark/ParkDetay'
        details = []

        r = s.get(url, params={'id': parkId}, headers={'Accept-Encoding': 'gzip,deflate'})
        r.raise_for_status()

        detail, = r.json()
        detail = {newName: detail[oldName] for oldName, newName in DetailColumns.items()}

        tariff = {}
        for t in detail['Tariff'].split(';'):
            interval, price = t.replace(',', '.').split(':')
            tariff[interval.rstrip()] = float(price)

        if updateTime := detail['UpdateTime']:
            updateTime = datetime.strptime(updateTime, '%d.%m.%Y %H:%M:%S').isoformat()

        detail.update({
            'Tariff': tariff,
            'Latitude': float(detail['Latitude']),
            'Longitude': float(detail['Longitude']),
            'UpdateTime': updateTime
            })
        
        return detail