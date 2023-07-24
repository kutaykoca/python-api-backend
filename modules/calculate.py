import math
import requests
import environment
from geopy.distance import geodesic

def calculateDistance(lat1, lon1, lat2, lon2):
    R = 6371  # Dünya yarıçapı (kilometre cinsinden)
    dLat = math.radians(lat2 - lat1)  # Enlem farkı
    dLon = math.radians(lon2 - lon1)  # Boylam farkı
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c  # İki nokta arasındaki mesafe

    return distance

def getClosestStops(locations, user):
    
    closesStation = None
    minDistance = float('inf')



    for station in locations:
        distance  = calculateDistance(
            lat1=float(user.lat),
            lon1=float(user.lon),
            lat2=float(station.lat),
            lon2=float(station.lon)
        )
        
        if distance < minDistance:
            closesStation = station
            minDistance = distance
    
    result = {
        "name": closesStation.name,
        "lat": closesStation.lat,
        "lon": closesStation.lon,
        "distance": minDistance
    }
    
    return result

def createRotation(start_coordinate, end_coordinate):
    try:
        api_key = environment.GOOGLE_API
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_coordinate}&destination={end_coordinate}&key={api_key}"
        response = requests.get(url)

        data = response.json()

        if data['status'] != 'OK':
            raise Exception(data['error_message'])

        route = data['routes'][0]

        return route
    except:
        return False
    

def find_closest_coordiate(target, coordinates):
    try:
        min_distance = float('inf')
        closest_coordiate = None

        my_coordiate = (target.lat, target.lon)
        
        for coordinate in coordinates:
            
            target_coordinate = (coordinate.lat, coordinate.lon)
            
            distance = geodesic(my_coordiate, target_coordinate).meters
            
            if distance < min_distance:
                min_distance = distance
                closest_coordiate = coordinate
            
        return {
            "name": closest_coordiate.name,
            "lat": closest_coordiate.lat,
            "lon": closest_coordiate.lon,
            "distance": min_distance
        }
    except:
        return None