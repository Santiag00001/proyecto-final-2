from accessData.conexionORM import Database  # Importar la clase Database
from accessData.entities.model import BaseDeDatos, Persona, Profesion
from dominio.entities.modelsORM.personaDTO import PersonaBASE, ProfesionBASE
from servicios.persona_servicio import Servicio
from servicios.genericService import GenericRepository

DATABASE_URL = "mysql+mysqlconnector://root:admin@localhost:3307/instituto"

def main():
    persona_service = Servicio(db)
    serviceGeneric = GenericRepository[Persona](Persona, db)

    while True:
        print("\n--- MENU ---")
        print("1. Crear persona")
        print("2. Mostrar personas")
        print("3. buscar personas")
        print("4. Actualizar personas")
        print("5. Eliminar estudiante")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre: ")
            edad = int(input("Ingrese la edad: "))
            direccion = input("Ingrese la direccion: ")
            
            tiene_profesion = input("¿Tiene una profesión? [S/n]: ").strip().lower()
            
            if tiene_profesion == "s":
                titulo_profesional = input("Ingrese el título profesional: ")
                
                # Crear persona en la base de datos
                persona_dto = PersonaBASE(None, nombre, edad, direccion)
                #persona_guardada = persona_service.crear_persona(persona_dto)
                persona_guardada = serviceGeneric.create(nombre=persona_dto.nombre, edad=persona_dto.edad, direccion=persona_dto.direccion)
                
                if persona_guardada:
                    # Crear profesión en la base de datos
                    profesion_dto = ProfesionBASE(None, titulo_profesional)
                    persona_service.crear_profesion(profesion_dto, persona_guardada.id)
                    print(f"nombre: {nombre}, edad: {edad}, direccion {direccion}, profesion: {titulo_profesional} ")

            else:
                # Crear persona en la base de datos sin profesión
                persona_dto = PersonaBASE(None, nombre, edad, direccion)
                #persona_guardada = persona_service.crear_persona(persona_dto)
                persona_dto = serviceGeneric.create(nombre=persona_dto.nombre, edad=persona_dto.edad, direccion=persona_dto.direccion)
                print(f"nombre: {nombre}, edad: {edad}, direccion {direccion} ")

        elif opcion == "2":
            #personas = persona_service.ver_personas()
            personas = serviceGeneric.getAll()
            for persona in personas:
                profesiones = ", ".join(prof.titulo_profesional for prof in persona.profesiones)
                print(f"ID: {persona.id}, Nombre: {persona.nombre}, Edad: {persona.edad}, Direccion: {persona.direccion}, Profesiones: {profesiones}")

        elif opcion == "3":
            persona_id = int(input("Ingrese el ID de la persona a consultar: "))
            #persona = persona_service.ver_persona(persona_id)
            persona = serviceGeneric.get(persona_id)
            
            if persona:
                # Mostrar información de la persona
                print(f"ID: {persona.id}, Nombre: {persona.nombre}, Edad: {persona.edad}, Dirección: {persona.direccion}")

                # Mostrar profesiones, si existen
                if persona.profesiones:
                    profesiones = ", ".join(prof.titulo_profesional for prof in persona.profesiones)
                    print(f"Profesiones: {profesiones}")
                else:
                    print("No tiene profesiones asociadas.")
            else:
                print("Persona no encontrada.")

        elif opcion == "4":

            id_persona = int(input("Ingrese el ID de la persona que desea actualizar: "))
            
            # Buscar a la persona en la base de datos
            persona = persona_service.ver_persona(id_persona)
            
            if not persona:
                print("Persona no encontrada")
            else:
                # Pedir los nuevos datos para la persona
                nombre = input(f"Ingrese el nuevo nombre (actual: {persona.nombre}): ") or persona.nombre
                edad = int(input(f"Ingrese la nueva edad (actual: {persona.edad}): ") or persona.edad)
                direccion = input(f"Ingrese la nueva dirección (actual: {persona.direccion}): ") or persona.direccion
                
                persona_base = PersonaBASE(id_persona, nombre, edad, direccion)
                
                # Revisar si la persona tiene profesiones
                profesiones_base = []
                if persona.profesiones:
                    print("La persona tiene las siguientes profesiones:")
                    for idx, profesion in enumerate(persona.profesiones, start=1):
                        print(f"{idx}. {profesion.titulo_profesional}")
                    
                    actualizar_profesiones = input("¿Desea actualizar alguna profesión? [S/n]: ").strip().lower()
                    
                    if actualizar_profesiones == "s":
                        numero_profesiones = len(persona.profesiones)
                        for idx in range(numero_profesiones):
                            cambiar = input(f"¿Desea cambiar la profesión '{persona.profesiones[idx].titulo_profesional}'? [S/n]: ").strip().lower()
                            if cambiar == "s":
                                titulo_profesional = input("Ingrese el nuevo título profesional: ")
                                profesion_base = ProfesionBASE(persona.profesiones[idx].id, titulo_profesional)
                                profesiones_base.append(profesion_base)
                
                # Actualizar la persona y las profesiones
                persona_actualizada = persona_service.actualizar_persona(persona_base, profesiones_base)
                print("Persona actualizada")

        elif opcion == "5":
            persona_id = int(input("Ingrese el ID de la persona que desea eliminar: "))
            #persona_service.borrar_persona(persona_id)
            serviceGeneric.delete(persona_id)
            print("persona eliminado")
        
        elif opcion == "6":
            persona_service.cerrarConexion()
            print("¡Hasta luego!")
            break

if __name__ == "__main__":
    db = Database(DATABASE_URL)
    engine = db.engine
    BaseDeDatos.metadata.create_all(bind=engine)
    main()