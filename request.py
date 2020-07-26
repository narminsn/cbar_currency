import requests
import  datetime
import requests
import json, xmljson
from lxml.html import fromstring, tostring


second = datetime.datetime.now().second



def parse_data(url):
    response = requests.get(url)

    bank_mezenne = []
    xml = fromstring(response.content)
    json_data = json.dumps(xmljson.badgerfish.data(xml))

    data = json.loads(json_data)
    # list_data1 = data["valcurs"]["valtype"][0]
    list_data2 = data["valcurs"]["valtype"][1]
    for index, item in enumerate(list_data2["valute"]):

        obj = {
            "code" : item["@code"],
            "name" : item["name"]["$"],
            "value" : item["value"]["$"],
            'time' : second,
            'id': index,
            'difference' : 'glyphicon glyphicon-minus'

        }

        bank_mezenne.append(obj)

    return bank_mezenne


#
# print(parse_data("https://www.cbar.az/currencies/02.10.2019.xml"))
# print(parse_data("https://www.cbar.az/currencies/01.10.2019.xml"))