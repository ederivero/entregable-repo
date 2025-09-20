from flask import Flask, request
from psycopg import connect
from os import environ

conexion = connect(environ.get('DATABASE_URL'))
app = Flask(__name__)

def crearTablas():
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS entregables (
                   id SERIAL PRIMARY KEY, 
                   link TEXT NOT NULL, 
                   nombre TEXT NOT NULL, 
                   fecha_entrega TIMESTAMP)''')
    conexion.commit()
    cursor.close()

@app.route('/subir-entregable', methods=['POST'])
def subirEntregable():
    cursor = conexion.cursor()
    data = request.get_json()
    cursor.execute('INSERT INTO entregables (link, nombre, fecha_entrega) VALUES (%s, %s, now())',(data.get('link'), data.get('nombre')))
    conexion.commit()
    cursor.close()

    return {
        'message':'Intento registrado exitosamente'
    }, 201


if (__name__ =='__main__'):
    app.run(debug=True)