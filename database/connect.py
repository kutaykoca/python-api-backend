from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Location

def create_database_connection():
    engine = create_engine('sqlite:///kutaykoca.db', echo=True)  # Örnek olarak SQLite veritabanı kullanıyoruz
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
