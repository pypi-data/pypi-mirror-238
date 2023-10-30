from dtypes import Station, Concentration, AQI

from datetime import datetime
import requests, re

def GetAQIStations() -> list[Station]:
    '''Bu web servis ile Hava Kalitesi istasyonlarının bilgileri paylaşılmıştır

    Returns
    -------
    stations
        Portal üzerinde kayıtlı Hava Kalitesi istasyonlarını içeren bir liste
    '''
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
            stations.append(Station(**station))
            
        return stations
    
def GetAQIByStationId(stationId: str, startDate: datetime, endDate: datetime) -> tuple[list[Concentration], list[AQI]]:
    '''Bu web servis ile Id’si girilen istasyonun başlangıç ve bitiş tarihine göre Konsantrasyon (Concentration) ve 
    Hava Kalitesi Index (AQI) bilgileri paylaşılmaktadır.

    Parameters
    ----------
    stationId : str
        Ölçüm bilgileri getirilecek istasyonun Id’sidir. ('GetAQIStations' metodu ile ulaşılabilir.)
        
    startDate : datetime
        Belirtilen tarih ölçümlerin başlangıç tarihi olarak belirlenir.
        
    endDate : datetime
        Belirtilen tarih ölçümlerin  bitiş tarihi (dahil) olarak belirlenir.

    Returns
    -------
    C: list[Concentration]
        Ölçüm tarihi bilgisi ve istasyonun analizörden ölçülen PM10, SO2, O3, NO2 ve CO ham verilerinin değerini içerir.
        
    A: list[AQI]
        Ölçüm tarihi bilgisi ve istasyonun analizörden ölçülen PM10, SO2, O3, NO2 ve CO ham verilerinin Hava Kalitesi 
        Index'i hesaplandıktan sonraki değerlerini ve o saat için HKI değerini, Kirletici parametreyi, durumu ve durumun 
        rengini içerir.

    '''
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
            ReadTime = datetime.fromisoformat(ReadTime)
            if c := record.get('Concentration'):
                c |= {'ReadTime': ReadTime}
                C.append(Concentration(**c))
            if a := record.get('AQI'):
                a |= {'ReadTime': ReadTime}
                A.append(AQI(**a))

        return C, A
