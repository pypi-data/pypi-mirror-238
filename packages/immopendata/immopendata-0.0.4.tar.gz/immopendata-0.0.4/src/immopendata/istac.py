import xml.etree.ElementTree as ET
import datetime, requests, enum

Month = enum.Enum('Month',('OCAK','ŞUBAT','MART','NİSAN','MAYIS','HAZIRAN','TEMMUZ','AĞUSTOS','EYLÜL','EKİM','KASIM','ARALIK'))

Landfills = {
	'Hekimbaşı Aktarma': '00000000000100000010',
	'Şile Aktarma' :'00000000000100000020',
	'Aydınlı Aktarma': '00000000000100000019',
	'Küçükbakkalköy Aktarma': '00000000000100000018',
	'Yenibosna Aktarma': '00000000000100000014',
	'Silivri Aktarma': '00000000000100000016',
	'Baruthane Aktarma': '00000000000100000021',
	'Halkalı Aktarma': '00000000000100000023',
	'Odayeri Düzenli Depolama': '00000000000100000012',
	'Geri Kazanım ve Kompost': '00000000000100000001',
	'Kömürcüoda Atık Bertaraf': '00000000000100000013',
	'Seymen Düzenli Depolama': '00000000000100000017',
	'Kemerburgaz IBB Atık Yakma ve Enerji Üretme': '00000000000100000162',
	'Odayeri Çöp Sızıntı Suyu Arıtma': '00000000000100000040',
	'Kömürcüoda Çöp Sızıntı Suyu Arıtma': '00000000000100000082'
	}

def GetTotalWeightByYear(stationId:str, year:int) -> list[dict]:
    """This method provides the amount of waste collected since 2016 in Transfer Stations.
    The input value must take one of the following:

    Station Id - Station Name
    
    [Asia Transfer Stations]
    00000000000100000010 – Hekimbaşı Aktarma
    00000000000100000020 – Şile Aktarma
    00000000000100000019 – Aydınlı Aktarma
    00000000000100000018 – Küçükbakkalköy Aktarma

    [Europa Transfer Stations]
    00000000000100000014 – Yenibosna Aktarma
    00000000000100000016 – Silivri Aktarma
    00000000000100000021 – Baruthane Aktarma
    00000000000100000023 – Halkalı Aktarma

    [Other Facilities]
    00000000000100000012 – Odayeri Düzenli Depolama
    00000000000100000001 – Geri Kazanım ve Kompost
    00000000000100000013 – Kömürcüoda Atık Bertaraf
    00000000000100000017 – Seymen Düzenli Depolama
    00000000000100000162 – Kemerburgaz IBB Atık Yakma ve Enerji Üretme
    00000000000100000040 – Odayeri Çöp Sızıntı Suyu Arıtma
    00000000000100000082 – Kömürcüoda Çöp Sızıntı Suyu Arıtma

    Parameters:
        stationId (str): The desired transfer stations id.
        year (int): The year for which the data is requested.
 
    Returns:
        list[dict]: District Municipality and montly total waste amounts of the entered year.
    """
    with requests.Session() as s:
        url = 'https://api.ibb.gov.tr/istac-zwr-toplam-yil-ws'
        headers={
            'Accept-Encoding':'gzip,deflate',
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction':'urn:sap-com:document:sap:rfc:functions:ZWR_TOPLAM_YIL_WS:ZWR_TOPLAM_TARTIM_FNRequest'
            }
        data = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
                    <Body>
                     <ZWR_TOPLAM_TARTIM_FN xmlns="urn:sap-com:document:sap:rfc:functions">
                      <MJAHR xmlns="">{year}</MJAHR>
                      <ZWDPLANT xmlns="">{stationId}</ZWDPLANT>
                     </ZWR_TOPLAM_TARTIM_FN>
                    </Body>
                   </Envelope>"""

        r = requests.post(url, data=data, headers=headers)
        r.raise_for_status()

        root = ET.fromstring(r.content)
        records = []
        for it in root.findall('*//item'):
            year = it.find('MJAHR').text
            month = Month[it.find('AY').text].value  
            recordDate = f'{year}-{month:02d}-01'
            
            records.append({
                'RecordDate': recordDate,
                'City': it.find('CITY1').text,
                'Weight': float(it.find('EWEIGHT_NET').text)
                })
                
        return records