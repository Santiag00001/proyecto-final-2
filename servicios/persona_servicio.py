from accessData.entities.model import Persona, Profesion
from accessData.conexionORM import Database
from dominio.entities.modelsORM.personaDTO import PersonaBASE, ProfesionBASE
from sqlalchemy.orm import joinedload
from abc import ABC, abstractmethod
from servicios.logService import LogService

class Crud(ABC):
    def __init__(self, database):
        self.db = database
        self.log_service = LogService()

    @abstractmethod
    def crear_persona(self, per):
        pass

    @abstractmethod
    def ver_personas(self):
        pass

    @abstractmethod
    def actualizar_persona(self, persona_base, profesiones_base=None):
        pass

    @abstractmethod
    def borrar_persona(self, person_id):
        pass

    def cerrar_conexion(self):
        session = self.db.get_session()
        session.close()

class Servicio(Crud):

    

    def crear_persona(self, per: PersonaBASE):
        
        self.log_service.logger("entro al metodo crear_persona: "+str(per.nombre))
        session = self.db.get_session()
        
        # Crear el objeto Persona en la base de datos
        db_persona = Persona(nombre=per.nombre, edad=per.edad, direccion=per.direccion)
        session.add(db_persona)
        session.commit()
        
        # Recuperar el ID generado y asignarlo al DTO
        session.refresh(db_persona)
        per.id = db_persona.id  # Actualizar el ID en el DTO
        
        session.close()
        return db_persona
    
    def crear_profesion(self, pro: ProfesionBASE, persona_id: int):
        self.log_service.logger("entro al metodo crear_profesion: "+str(pro.titulo_profesional))
        session = self.db.get_session()
        
        db_profesion = Profesion(titulo_profesional=pro.titulo_profesional, persona_id=persona_id)
        session.add(db_profesion)
        session.commit()
        session.refresh(db_profesion)
        
        session.close()
        return db_profesion
    
    def ver_personas(self):
        self.log_service.logger("entro al metodo ver_personas")
        session = self.db.get_session()
        personas = session.query(Persona).options(joinedload(Persona.profesiones)).all()
        session.close()
        return personas
    
    def ver_persona(self, person_id):
        self.log_service.logger("entro al metodo ver_persona: "+str(person_id))
        session = self.db.get_session()
        person = session.query(Persona).options(joinedload(Persona.profesiones)).filter(Persona.id == person_id).first()
        session.close()
        return person

    def actualizar_persona(self, persona_base: PersonaBASE, profesiones_base: list = None):
        self.log_service.logger("entro al metodo actualizar_persona: "+str(persona_base.nombre))
        session = self.db.get_session()
        
        # Buscar la persona en la base de datos
        persona = session.query(Persona).filter(Persona.id == persona_base.id).first()
        
        if persona_base.nombre:
            persona.nombre = persona_base.nombre
        if persona_base.edad:
            persona.edad = persona_base.edad
        if persona_base.direccion:
            persona.direccion = persona_base.direccion
        
        # Actualizar o añadir profesiones si se proporcionan
        if profesiones_base:
            for profesion_base in profesiones_base:
                profesion = session.query(Profesion).filter(
                    Profesion.id == profesion_base.id, 
                    Profesion.persona_id == persona.id
                ).first()
                
                if profesion:
                    profesion.titulo_profesional = profesion_base.titulo_profesional
                else:
                    nueva_profesion = Profesion(
                        titulo_profesional=profesion_base.titulo_profesional,
                        persona_id=persona.id
                    )
                    session.add(nueva_profesion)
        
        session.commit()
        session.refresh(persona)
        session.close()
    
        return persona
    
    def borrar_persona(self, person_id):
        self.log_service.logger("entro al metodo borra_persona: "+str(person_id))
        session = self.db.get_session()
        person = session.query(Persona).filter(Persona.id == person_id).first()
        session.delete(person)
        session.commit()
        session.close()
        return {"message": "Deleted successfully"}

    def cerrarConexion(self):
        session = self.db.get_session()
        session.close()