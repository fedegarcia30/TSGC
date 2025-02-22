from flask import Flask, request, jsonify
import requests
import json

import mysql.connector

app = Flask(__name__)
app.config['port'] = 5001

# Configuración de la conexión a la base de datos
db_config = {
    'user': 'tsgc',
    'password': 'LuisFede!234',
    'host': '92.205.150.118',
    'database': 'TheSecretGolfClub'
}

@app.route('/')
def home():
    return "Welcome to TSGC MySQL Connect!"

# Ruta para actualizar registros en la tabla CCVM
@app.route('/update_record', methods=['GET'])
def update_record():
    tabla = request.args.get('liga')
    email = request.args.get('email')
    data = request.args.get('data')
    new_data = json.loads(data)
    print(new_data.get('Nombre'))
    if not email or not new_data:
        return jsonify({'error': 'Faltan parámetros'}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        update_query = """
            UPDATE {tabla}
            SET Nombre = %s, Partidos = %s, Torneos = %s, Puntos = %s, HCPGolfos = %s, HCPOficial = %s
            WHERE Email = %s
            """.format(tabla=tabla)

        cursor.execute(update_query, (new_data['Nombre'], new_data['Partidos'], new_data['Torneos'], new_data['Puntos'], new_data['HCPGolfos'], new_data['HCPOficial'], email))
        conn.commit()
        print(email)
        if cursor.rowcount == 0:
            return jsonify({'error': 'No se encontró el registro con el email proporcionado'}), 404

        return jsonify({'message': 'Registro actualizado exitosamente'}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

    finally:
        cursor.close()
        conn.close()
        
@app.route('/check_connection', methods=['GET'])
def check_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        conn.close()
        return jsonify({'message': 'Conexión exitosa'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    