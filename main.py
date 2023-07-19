from fastapi import FastAPI
import uvicorn
import os 
from controller import locationController, rotationController
from database import connect



# Create Database
connect.create_database_connection()

app = FastAPI()
locationRouter = locationController.LocationRouter()
rotationController = rotationController.RotationRouter()

@app.get("/")
async def root():
    return {"message": "KutayKoca APP"}

app.include_router(locationRouter)
app.include_router(rotationController)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(3000))