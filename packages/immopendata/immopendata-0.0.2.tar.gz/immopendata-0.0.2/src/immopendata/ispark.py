from dtypes import Detail, Park

from datetime import datetime
import requests

def GetAllParks() -> list[Park]:
    with requests.Session() as s:        
        url = 'https://api.ibb.gov.tr/ispark/Park'
        r = s.get(url, headers={'Accept-Encoding':'gzip,deflate'})
        r.raise_for_status()

        parks = []
        for park in r.json():
            _ = {newName:park[oldName] for oldName, newName in Park.Mapper.items()}
            _.update({'Latitude':float(_['Latitude']), 'Longitude':float(_['Longitude']), 'IsOpen': _['IsOpen'] != 0})
            parks.append(Park(**_))
            
        return parks
    
def GetParkDetail(parkId:int) -> Detail:
    with requests.Session() as s:        
        url = 'https://api.ibb.gov.tr/ispark/ParkDetay'
        details = []

        r = s.get(url, params={'id':parkId}, headers={'Accept-Encoding':'gzip,deflate'})
        r.raise_for_status()

        detail, = r.json()
        _ = {newName:detail[oldName] for oldName, newName in Detail.Mapper.items()}

        tariff = {}
        for t in _['Tariff'].split(';'):
            interval, price = t.replace(',','.').split(':')
            tariff[interval.rstrip()] = float(price)

        if updateTime := _['UpdateTime']:
            updateTime = datetime.strptime(updateTime, '%d.%m.%Y %H:%M:%S')

        _.update({'Tariff':tariff, 'Latitude':float(_['Latitude']), 'Longitude':float(_['Longitude']), 'UpdateTime':updateTime})
        detail = Detail(**_)
        return detail


p = GetAllParks()
