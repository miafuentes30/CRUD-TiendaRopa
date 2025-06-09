from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse

usuario = "postgres" #Configurar
contraseña = urllib.parse.quote_plus("mia")  #Configurar

DATABASE_URL = f"postgresql://{usuario}:{contraseña}@localhost:5432/tienda_ropa"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()