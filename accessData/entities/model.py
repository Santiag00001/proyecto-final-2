from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

BaseDeDatos = declarative_base()

class Persona(BaseDeDatos):
    __tablename__ = "persona"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(20), unique=True, index=True)
    edad = Column((Integer))
    direccion = Column(String(50))
    
    profesiones = relationship("Profesion", back_populates="persona", cascade="all, delete-orphan")

class Profesion(BaseDeDatos):
    __tablename__ = "profesion"

    id = Column(Integer, primary_key=True, index=True)
    titulo_profesional = Column(String(50))

    persona_id = Column(Integer, ForeignKey('persona.id'))
    persona = relationship("Persona", back_populates="profesiones")

DATABASE_URL = "mysql+mysqlconnector://root:admin@localhost:3307/instituto"

engine = create_engine(DATABASE_URL)

BaseDeDatos.metadata.create_all(engine)

print("Tablas de persona y profesion creadas exitosamente.")