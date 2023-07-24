from modules import calculate
from fastapi import APIRouter
from fastapi import Path
from database.connect import create_database_connection
from database.models import Routes, Location
from pydantic import BaseModel

class CalculateItem(BaseModel):
    lat: str | None = None
    lon: str | None = None

class RotationRouter(APIRouter):
    def __init__(self, prefix: str= '/rotations'):
        super().__init__()
        self.prefix = prefix
        self.dbSession = create_database_connection()

        @self.get('/')
        def getHome():
            return {
                "message": "welcome"
            }

        @self.post('/calculate')
        def getCalcute(bodyData: CalculateItem):
            try:

                # Get All Location
                locations = self.dbSession.query(Location).all()
                # result = calculate.getClosestStops(locations=locations, user=bodyData)
                result = calculate.find_closest_coordiate(bodyData, locations)
                
                start_coordinate = f"{bodyData.lat},{bodyData.lon}"
                end_coordinate = f"{result['lat']},{result['lon']}"

                route = calculate.createRotation(start_coordinate=start_coordinate, end_coordinate=end_coordinate)
            
                return {
                    "message": "success",
                    "data": result,
                    "route": route
                }

                
            except:
                return {
                    "message": "not success",
                    "data": 'null'
                }