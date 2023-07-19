import json
from fastapi import APIRouter
from fastapi import Path
from modules import scraper, tools
from database.models import Routes, Location
from database.connect import create_database_connection
import environment
import itertools

class LocationRouter(APIRouter):
    def __init__(self, prefix: str = '/locations'):
        super().__init__()
        self.prefix = prefix
        self.dbSession = create_database_connection()

        @self.get('/')
        async def getHome():
            return {
                "message": "welcome",
            }
        

        @self.get('/getRoutes')
        async def getRoute():
            try:
                getAllRoutes = json.loads(scraper.getLocationName())
                if self.dbSession.query(Routes).count() > 0:
                    self.dbSession.query(Routes).delete()
                    self.dbSession.commit()
                
                # Save Data
                for route in getAllRoutes:
                    dbRoute = Routes(
                        name=route['seo'],
                        seo=route['name']
                    )

                    self.dbSession.add(dbRoute)
                self.dbSession.commit()
                
                return {
                    "message": "success",
                    "data": getAllRoutes
                }
            except:
                return {
                    "message": "not success",
                    "data": "null"
                }
        
        @self.get('/detail/{routeName}')
        async def getRouteDetail(routeName:str =Path(..., description='Route Name') ):
            try:
                getRouteDetail = scraper.getLocationDetail(locationName=routeName)

                return {
                    "message": "success",
                    "data": getRouteDetail
                }
            except:
                return {
                    "message": "not success",
                    "data": "null"
                }
        

        @self.get('/routes')
        async def getRoutes():
            try:

                getAllRoutesData = json.loads(scraper.getLocationName())
                routes = []

                for route in getAllRoutesData:
                    routes.append(
                        scraper.getLocationDetail(locationName=route['seo'])
                    )
                

                # Save Database
                if self.dbSession.query(Location).count() > 0:
                    self.dbSession.query(Location).delete()
                    self.dbSession.commit()
                
                for r in itertools.chain(*routes):
                    dbSave = Location(
                        name=r['name'],
                        lat=r['mapLat'],
                        lon=r['mapLong']
                    )
                    self.dbSession.add(dbSave)
                
                self.dbSession.commit()

                return {
                    "message": "success",
                    "data": routes
                }
            except:
                return {
                    "message": "not success"
                }
        
        @self.get('/buses/{routeName}')
        async def getAllBus(routeName:str = Path(..., description="Route Name")):
            try:
                # Get route code 
                routeCode = scraper.getRouteCode(routeName=routeName)

                # Live Bus
                liveBus = scraper.getLiveBus(routeCode=routeCode)

                return {
                    "message": "success",
                    "routeCode": str(routeCode),
                    "data": liveBus
                }
            except:
                return {
                    "message": "not success",
                    "data": "null"
                }
