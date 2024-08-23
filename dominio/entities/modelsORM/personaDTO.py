class PersonaBASE:
    def __init__(self, id, nombre, edad, direccion):
        self._id = id
        self._nombre = nombre
        self._edad = edad
        self._direccion = direccion

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def edad(self):
        return self._edad

    @edad.setter
    def edad(self, edad):
        self._edad = edad

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, direccion):
        self._direccion = direccion


class ProfesionBASE:
    def __init__(self, id, titulo_profesional):
        self._id = id
        self._titulo_profesional = titulo_profesional

    @property
    def id(self):
        return self._id

    @property
    def titulo_profesional(self):
        return self._titulo_profesional

    @titulo_profesional.setter
    def titulo_profesional(self, titulo_profesional):
        self._titulo_profesional = titulo_profesional
