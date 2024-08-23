from typing import Generic, TypeVar
from accessData.conexionORM import Database
from sqlalchemy.orm import joinedload

T = TypeVar('T')

class GenericRepository(Generic[T]):
    
    def __init__(self, model: T,  database: Database):
        self.model = model
        self.db = database

    def create(self, **kwargs):
        instance = self.model(**kwargs)
        session = self.db.get_session()
        session.add(instance)
        session.commit()
        session.refresh(instance)
        session.close()
        return instance
    

    def getAll(self):
        session = self.db.get_session()
        try:
            # Usa joinedload para cargar la relación 'profesiones' junto con 'Persona'
            instance = session.query(self.model).options(joinedload(self.model.profesiones)).all()
        finally:
            session.close()
        return instance
    

    def get(self, id):
        session = self.db.get_session()
        instance = session.query(self.model).get(id)
        session.close()
        return instance


    def update(self, id, obj_data) -> T:
        session = self.db.get_session()
        obj = session.query(self.model).get(id)
        for var, value in vars(obj_data).items():
            setattr(obj, var, value)
        print('obj listo para update')
        print(vars(obj))
        session.commit()
        session.refresh(obj)
        session.close()
        return obj
    

    def delete(self, id):
        instance = self.get(id)
        session = self.db.get_session()
        session.delete(instance)
        session.commit()