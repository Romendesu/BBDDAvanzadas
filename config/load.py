from config.config import Config

config = Config()
server_values = config.get_server_values()
postgresql_values = config.get_postgresql_values()

# Importar la configuración del servidor
SERVER_IP = server_values["SERVER_IP"]
SERVER_PORT = server_values["SERVER_PORT"]
TEMPLATE_DIR = server_values["TEMPLATE_DIR"]

# Importar la configuración de la base de datos
DATABASE_HOST = postgresql_values["DATABASE_HOST"]
DATABASE_NAME = postgresql_values["DATABASE_NAME"]
DATABASE_USER = postgresql_values["DATABASE_USER"]
DATABASE_PASSWORD = postgresql_values["DATABASE_PASSWORD"]
DATABASE_PORT = postgresql_values["DATABASE_PORT"]
