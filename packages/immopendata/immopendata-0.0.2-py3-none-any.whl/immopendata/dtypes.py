import dataclasses
import datetime
import typing
from types import MappingProxyType

# ----------------------------------
# [ispark.py]

@dataclasses.dataclass(frozen=True)
class Station:
    Id: str
    Name: str
    Address: str
    Latitude: float
    Longitude: float

@dataclasses.dataclass(frozen=True)
class Concentration:
    ReadTime: datetime.datetime
    PM10: float
    SO2: float
    O3: float
    NO2: float
    CO: float

@dataclasses.dataclass(frozen=True)
class AQI:
    ReadTime: datetime.datetime
    PM10: float
    SO2: float
    O3: float
    NO2: float
    CO: float
    AQIIndex: float
    ContaminantParameter: str
    State: str
    Color: str
    
# [havakalitesi.py]
# ----------------------------------
# [ispark.py]

@dataclasses.dataclass(frozen=True)
class Park:
    Id: str
    Name: str
    Latitude: float
    Longitude: float
    Capacity: str
    EmptyCapacity: str
    WorkHours: str
    Type: str
    FreeTime: str
    District: str
    IsOpen: bool
    Mapper: typing.Dict[str, str] = dataclasses.field(
        init=False,
        repr=False,
        default=MappingProxyType({
            'parkID'        : 'Id',
            'parkName'      : 'Name',
            'lat'           : 'Latitude',
            'lng'           : 'Longitude',
            'capacity'      : 'Capacity',
            'emptyCapacity' : 'EmptyCapacity',
            'workHours'     : 'WorkHours',
            'parkType'      : 'Type',
            'freeTime'      : 'FreeTime',
            'district'      : 'District',
            'isOpen'        : 'IsOpen'
            }))
    
@dataclasses.dataclass(frozen=True)
class Detail:
    Id: str
    Name: str
    Latitude: float
    Longitude: float
    Capacity: str
    EmptyCapacity: str
    WorkHours: str
    Type: str
    FreeTime: str
    District: str
    LocationName: str
    UpdateTime: None | datetime.datetime
    MonthlyFee: float
    Tariff: typing.Dict[str, float]
    Address: str
    AreaPolygon: None | str
    Mapper: typing.Dict[str, str] = dataclasses.field(
        init=False,
        repr=False,
        default=MappingProxyType({
            'parkID'        : 'Id',
            'parkName'      : 'Name',
            'lat'           : 'Latitude',
            'lng'           : 'Longitude',
            'capacity'      : 'Capacity',
            'emptyCapacity' : 'EmptyCapacity',
            'workHours'     : 'WorkHours',
            'parkType'      : 'Type',
            'freeTime'      : 'FreeTime',
            'district'      : 'District',
            'locationName' : 'LocationName',
            'updateDate'   : 'UpdateTime',
            'monthlyFee'   : 'MonthlyFee',
            'tariff'       : 'Tariff',
            'address'      : 'Address',
            'areaPolygon'  : 'AreaPolygon'
            }))
