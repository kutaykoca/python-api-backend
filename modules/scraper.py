import requests
import re
import json
from bs4 import BeautifulSoup
import environment


# Core Session 
session = requests.Session()


def getLocationName():
    try:
        url = f"{environment.BASE_URL}/ajax/busline/list/bandirma"
        req = session.get(url, verify=False)

        return req.text
    except:
        return False


def getLocationDetail(locationName):
    try:
        url = f"{environment.BASE_URL}/hat/{locationName}"
        req = session.get(url, verify=False)
        regex = r'let stationsData =(.*])'
        stationsData = json.loads(re.search(regex, str(req.text)).group(1))

        return stationsData
    except:
        return False

def getRouteCode(routeName):
    try:
        url = f"{environment.BASE_URL}/hat/{routeName}"
        req = session.get(url, verify=False)
        regex = r'data: {"routeCode":(.*")'
        routeCode = re.search(regex, str(req.text)).group(1).strip().replace('"', '').replace("\"", "")

        return routeCode
    except:
        return False

def getLiveBus(routeCode):
    try:
        url = f"{environment.BASE_URL}/ajax/busline/live"
        params = {
            "routeCode": routeCode
        }

        req = session.post(url, data=params, verify=False)
        
        return json.loads(req.text)
    except:
        pass
    

    # Detail Scraping Operation