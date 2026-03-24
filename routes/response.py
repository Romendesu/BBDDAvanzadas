# Empleo de Factory Method para las siguientes consultas:
# 1. Obtener TODOS los profesores, alumnos, grados o matrículas
# 2. Manejo de rutas POST
# 3. Obtener UN profesor, alumno, grado o matrícula

from flask import jsonify

HTTP_OK = 200
HTTP_ERROR = 400
HTTP_NO_CONTENT = 204
class ResponseJSON():

    @staticmethod
    def ok(data):
        return jsonify({
                'HTTP-STATUS': 'OK',
                'HTTP-CODE': HTTP_OK,
                'DATA': data
            }), HTTP_OK

    @staticmethod
    def error(error_msg:str):
        return jsonify({
                'HTTP-STATUS': "ERROR",
                'HTTP-CODE': HTTP_ERROR,
                'ERROR-MSG': error_msg
        }), HTTP_ERROR
    
    @staticmethod
    def no_content(msg = None):
        return jsonify({
            "HTTP-CODE": HTTP_NO_CONTENT,
            "HTTP-STATUS": "NO CONTENT",
            'MSG': msg
        }), HTTP_NO_CONTENT 