from models import PostgreSQL, OperacionesAlumno, OperacionesProfesor
from models import Alumnos, Profesores

def clear_screen() -> None:
    import subprocess
    import platform
    
    if platform.system() == "Windows":
        subprocess.call('cls', shell=True)
    else:
        subprocess.call('clear', shell=True)

def database_menu(
        pg: PostgreSQL, 
        gestor_alumno: OperacionesAlumno,
        gestor_profesor: OperacionesProfesor,
    ):
    while True:
        clear_screen()
        print("Bienvenido al menú de la base de datos")
        print("Seleccione una opción (1-3)")
        print("1. Obtener información de la base de datos")
        print("2. Añadir contenido a la base de datos")
        print("3. Consultar información")
        print("4. Salir")
        
        try:
            user_input = int(input("> "))
        except ValueError:
            print("Opción no válida. Por favor, ingrese un número.")
            input("Presione Enter para continuar...")
            continue
        
        match user_input:
            case 1:
                get_version = pg.obtain_database_version()
                if get_version:
                    print("Información de la base de datos:")
                    print("Postgres:", get_version)
                input("Presione Enter para continuar...")
            case 2:
                while True:
                    clear_screen()
                    print("Ventana para la creación de contenido, seleccione una opción:")
                    print("1. Crear tablas")
                    print("2. Crear contenido")
                    print("3. Volver al menú principal")
                    
                    try:
                        content_option = int(input("> "))
                    except ValueError:
                        print("Opción no válida. Por favor, ingrese un número.")
                        input("Presione Enter para continuar...")
                        continue
                    
                    match content_option:
                        case 1:
                            pg.create_tables()
                            print("Tablas creadas exitosamente.")
                            input("Presione Enter para continuar...")
                        case 2:
                            print("Seleccione una operación a realizar:")
                            print("1. Ingresar alumno")
                            print("2. Ingresar profesor")
                            
                            try:
                                user_insert_input = int(input("> "))
                            except ValueError:
                                print("Opción no válida. Por favor, ingrese un número.")
                                input("Presione Enter para continuar...")
                                continue
                            
                            match(user_insert_input):
                                case 1:
                                    import uuid
                                    id = str(uuid.uuid4())
                                    nombre = input("Ingrese el nombre del alumno.\n> ")
                                    email = input("Ingrese el correo del alumno.\n> ")
                                    alumno = Alumnos(id=id, nombre=nombre,email=email)

                                    gestor_alumno.insert_one_student(alumno=alumno)
                                    input("Presione Enter para continuar...")
                                case 2:
                                    import uuid
                                    id = str(uuid.uuid4())
                                    nombre = input("Ingrese el nombre del profesor.\n> ")
                                    profesor = Profesores(id=id, nombre=nombre)

                                    gestor_profesor.insert_one_teacher(profesor=profesor)
                                    input("Presione Enter para continuar...")
                        case 3:
                            break
                        case _:
                            print("Opción no disponible.")
                            input("Presione Enter para continuar...")
            case 3:
                print("Seleccione que categoría le gustaria consultar:")
                print("1. Alumnos")
                print("2. Profesores")

                try:
                    user_select_input = int(input("> "))
                except ValueError:
                    print("Opción no válida. Por favor, ingrese un número.")
                    input("Presione Enter para continuar...")
                    continue
                            
                match(user_select_input):
                    case 1:
                        alumnos = gestor_alumno.get_all_students()
                        for alumno in alumnos:
                            print(alumno)
                        input("Presione Enter para continuar")

                    case 2:
                        profesores = gestor_profesor.get_all_teachers()
                        for profesor in profesores:
                            print(profesor)
                        input("Presione Enter para continuar")

                    case _:
                        print("Opcion no implementada")
                        input("Presione Enter para continuar")
            case 4:
                break
            case _:
                print("Opción no válida.")
                input("Presione Enter para continuar...")
