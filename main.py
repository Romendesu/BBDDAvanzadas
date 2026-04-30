import argparse
from app import create_app
from config import SERVER_IP, SERVER_PORT
from models import PostgreSQL

def database_menu(pg: PostgreSQL):
    print("Bienvenido al menu de la base de datos")
    while True:
        try:
            print("Seleccione una opción (1-2)")
            print("1. Obtener información de la base de datos")
            print("2. Crear contenido")
            print("3. Salir")
            user_input = int(input("> "))

            # Análisis de la entrada del usuario
            match(user_input):
                case 1:
                    get_version = pg.obtain_database_version()
                    if get_version:
                        print("Información de la base de datos:")
                        print("Postgres:",get_version)
                    continue
                case 2:
                    print("Ventana para la creacion de contenido, seleccione una opcion:")
                    while True:
                        print("1. Crear tablas")
                        print("2. Crear contenido")
                        print("3. Salir")
                        content_option = int(input(">"))
                        match content_option:
                            case 1:
                                pg.create_tables()
                                continue_opt = input("Desea continuar: S/N\n>")
                                if continue_opt.lower() == "n": 
                                    break
                                continue
                            case 2:
                                continue
                            case 3:
                                break
                            case _:
                                print("Opcion no disponible")
                                continue
                    continue
                case 3:
                    print("Saliendo de la interfaz")
                    break
                case _:
                    print("Opción no valida.")
                    continue
        except Exception as e:
            print("Error:", e)

def main():
    parser = argparse.ArgumentParser()

    # Añadir argumentos a la ejecucción del servidor
    parser.add_argument(
        "--db", "--database",
        action="store_true",
        help="Muestra el menu de configuración de la base de datos"
    )
    parser.add_argument(
        "--rs", "--runserver",
        action="store_true",
        help="Ejecuta el servidor de la base de datos"
    )

    postgres = PostgreSQL()
    args = parser.parse_args()

    # Segun el argumento pasado, la función main ejecutara un parámetro u otro
    if args.db:
        database_menu(pg = postgres)
    elif args.rs:
        app = create_app()
        app.run(
            host = SERVER_IP,               
            port = SERVER_PORT,           
            debug= True
        )
    else: 
        parser.print_help()

if __name__ == "__main__":
    main()
    