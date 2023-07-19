from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    lat = Column(String)
    lon = Column(String)

class Routes(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    seo = Column(String)