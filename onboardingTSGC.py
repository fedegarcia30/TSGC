import json
from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import pdfplumber
import airtable
import requests
from io import BytesIO
import os
import time
import mysql.connector
import onesignal
from onesignal.api import default_api
from onesignal.model.user_identity_request_body import UserIdentityRequestBody
import subprocess
import json

app = Flask(__name__)

# Configuración de la conexión a la base de datos
db_config = {
    'user': 'tsgc',
    'password': 'LuisFede!234',
    'host': '92.205.150.118',
    'database': 'TheSecretGolfClub'
}

@app.route('/')
def home():
    return "Welcome to TSGC!"

@app.route('/api/test')
def get_data():
    try:
        liga = devuelveTablaLiga("GOLFOS")
        creaJugadorConfiguracion("pruebaAPI@gmail.com","Prueba API",liga)
        return creaJugadorEnLiga("pruebaAPI@gmail.com","Prueba API",liga,"CM01911152")
    except requests.exceptions.HTTPError as http_err:
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
    except Exception as err:
        return jsonify({'error': f'Other error occurred: {err}'}), 500
    return respuesta

@app.route('/api/handicap')
def get_handicap():
    try:
        licencia = request.args.get('licencia')
        response = requests.get('https://rfegolf.es/PaginasServicios/ServicioHandicap.aspx?HLic='+licencia)
        # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        handicap_value = soup.find('td', class_='SeccionClubs_RowCentrado').text
        name_value = soup.find('td', class_='SeccionClubs_RowIzquierda').text
        respuesta = jsonify({'handicap': handicap_value, 'name': name_value})
        print(respuesta)
    except requests.exceptions.HTTPError as http_err:
        respuesta = jsonify({'error': f'Error al crear el usuario: {err}'})
        respuesta.headers.add("Access-Control-Allow-Origin", '*')
        return respuesta, 500
    except Exception as err:
        respuesta = jsonify({'error': f'Error al crear el usuario: {err}'})
        respuesta.headers.add("Access-Control-Allow-Origin", '*')
        return respuesta, 50
    respuesta.headers.add("Access-Control-Allow-Origin", '*')
    return respuesta


@app.route('/api/NuevoUsuarioHandicap')
def get_NuevoUsuarioHandicap():
    licencia = request.args.get('licencia')
    nombre = request.args.get('nombre')
    email = request.args.get('email')
    url = "https://api.rfeg.es/files/summaryhandicap/" + licencia[-6:] + ".pdf"
    response = requests.get(url)
    pdf_file = BytesIO(response.content)
    pdf = pdfplumber.open(pdf_file)
    p0 = pdf.pages[0]
    table_settings = {
    "vertical_strategy": "text",
    "horizontal_strategy": "text",
    }
    table = p0.extract_table(table_settings)
    p3 = pdf.pages[4]
    table_p3 = p3.extract_table(table_settings)
    # Airtable API configuration
    token = 'patK75uFoPtI0qMNm.a71979b53e4ff353159574ef4b245e4ec46d73c329cee4ca3ed2e495ca5a273c'
    base_id = 'appB6QQMNnJ4pgMLt'
    table_name = 'Handicap'

    # Connect to Airtable
    bbdd = airtable.Airtable(base_id, table_name, token)
    # Create a record with name and email
    record = {
        "Name": nombre,
        "email":email
    }
    # Add new rows to Airtable
    for row in table:
        try:
            for cell in row:
                try:
                    if (1 <= int(row[0]) <= 20):
                        if cell.count('/') == 2 and len(cell.split('/')[1]) == 3:
                            json_data = {
                                "Fecha": row[1],
                                "Campo": "VACIO",
                                "HCP": row[row.index(cell) + 1],
                                "HCPJuego": row[row.index(cell) + 2],
                                "Resultado": row[row.index(cell) + 3],
                                "RBA": "0",
                                "NivelJuego": ""
                            }
                            p3 = pdf.pages[4]
                            table_p3 = p3.extract_table(table_settings)
                            for row_p3 in table_p3:
                                if row_p3[0] == row[0]:
                                    json_data["NivelJuego"] = row_p3[-1]
                                    break
                            # Add the processed card to the list
                            posicionTarjeta = 21-int(row[0])
                            record["Tarjeta" + str(posicionTarjeta)] = json.dumps(json_data)
                except:
                    try:
                            celdaSplit = cell.split()
                            if celdaSplit[0].isdigit() & (1 <= int(celdaSplit[0]) <= 20) & (len(celdaSplit[1]) == 10):
                                for celda in row:
                                    try:
                                        if celda.count('/') == 2 and len(celda.split('/')[1]) == 3:
                                            json_data = {
                                            "Fecha": celdaSplit[1],
                                            "Campo": "VACIO",
                                            "HCP": row[row.index(celda) + 1],
                                            "HCPJuego": row[row.index(celda) + 2],
                                            "Resultado": row[row.index(celda) + 3],
                                            "RBA": "0",
                                            "NivelJuego": ""
                                            }
                                            for row_p3 in table_p3:
                                                try:
                                                    if row_p3[0] == celdaSplit[0]:
                                                        json_data["NivelJuego"] = row_p3[-1]
                                                        break
                                                except:
                                                    continue

                                            posicionTarjeta = 21-int(celdaSplit[0])
                                            record["Tarjeta" + str(posicionTarjeta)] = json.dumps(json_data)
                                    except:
                                        continue
                    except:
                        continue
                continue
        except:
            continue
    # Print the processed cards
    if len(record) < 20:
        print("Hay menos de 20 registros procesados.")
    try:
        bbdd.insert(record)
        respuesta = jsonify({'message': 'Usuario handicap creado correctamente'})
    except Exception as err:
        respuesta = jsonify({'error': f'Error al crear el usuario: {err}'})
        respuesta.headers.add("Access-Control-Allow-Origin", '*')
        return respuesta, 500

    pdf.close()
    return respuesta

@app.route('/api/creaJugadorConfiguracion')
def creaJugadorConfiguracion():
    email = request.args.get('email')
    nombre = request.args.get('nombre')
    liga = request.args.get('liga')
    licencia = request.args.get('licencia')
    token = 'patK75uFoPtI0qMNm.a71979b53e4ff353159574ef4b245e4ec46d73c329cee4ca3ed2e495ca5a273c'
    base_id = 'appB6QQMNnJ4pgMLt'
    table_name = 'Jugadores'
    liga_id = devuelveTablaLiga(liga)
    bbddJugadores = airtable.Airtable(base_id, table_name, token)
    try:
        hcp = float(request.args.get('hcp').replace(',', '.'))
    except ValueError:
        respuesta = jsonify({'error': 'Invalid hcp value. It must be a decimal number.'})
        respuesta.headers.add("Access-Control-Allow-Origin", '*')
        return respuesta, 400
    record = {
    "email":email,
    "Nombre": nombre,
    "Liga" : [liga_id],
    "licencia": licencia,
    "handicapOficial" : hcp,
    }
    try:
        print(record)
        bbddJugadores.insert(record)
        print("Usuario creado correctamente")
        respuesta = jsonify({'message': 'Usuario creado correctamente'})
    except Exception as err:
        respuesta = jsonify({'error': f'Error al crear el usuario: {err}'})
        respuesta.headers.add("Access-Control-Allow-Origin", '*')
        return respuesta, 500
    respuesta.headers.add("Access-Control-Allow-Origin", '*')
    return respuesta, 200

def devuelveIdJugador(email):
    token = 'patK75uFoPtI0qMNm.a71979b53e4ff353159574ef4b245e4ec46d73c329cee4ca3ed2e495ca5a273c'
    base_id = 'appB6QQMNnJ4pgMLt'
    table_name = 'Jugadores'
    bbddLigas = airtable.Airtable(base_id, table_name, token)
    try:
        records = bbddLigas.get_all(formula="FIND('"+email+"',email)")
        idJugador = records[0].get('id')
        print("id Jugador:"+idJugador)
    except Exception as err:
        return jsonify({'error': f'Error al obtener el ID del jugador: {err}'}), 500
    return idJugador


def devuelveTablaLiga(liga):
    token = 'patK75uFoPtI0qMNm.a71979b53e4ff353159574ef4b245e4ec46d73c329cee4ca3ed2e495ca5a273c'
    base_id = 'appB6QQMNnJ4pgMLt'
    table_name = 'ConfigTable'
    bbddLigas = airtable.Airtable(base_id, table_name, token)
    try:
        records = bbddLigas.get_all(formula="FIND('"+liga+"',Liga)")
        leaderboard = records[0].get('id')
        print(leaderboard)
    except Exception as err:
        return jsonify({'error': f'Error al obtener la tabla de la liga: {err}'}), 500
    return leaderboard

def devuelveNombreTablaLiga(liga):
    token = 'patK75uFoPtI0qMNm.a71979b53e4ff353159574ef4b245e4ec46d73c329cee4ca3ed2e495ca5a273c'
    base_id = 'appB6QQMNnJ4pgMLt'
    table_name = 'ConfigTable'
    bbddLigas = airtable.Airtable(base_id, table_name, token)
    try:
        records = bbddLigas.get_all(formula="FIND('"+liga+"',Liga)")
        leaderboard = records[0].get('fields').get('Leaderboard')
        print(leaderboard)
    except Exception as err:
        return jsonify({'error': f'Error al obtener la tabla de la liga: {err}'}), 500
    return leaderboard

@app.route('/api/creaJugadorEnLiga')
def creaJugadorEnLiga():
    email = request.args.get('email')
    nombre = request.args.get('nombre')
    liga = request.args.get('liga')
    token = 'patK75uFoPtI0qMNm.a71979b53e4ff353159574ef4b245e4ec46d73c329cee4ca3ed2e495ca5a273c'
    base_id = 'appB6QQMNnJ4pgMLt'
    table_name= devuelveNombreTablaLiga(liga)
    time.sleep(1)
    try:
        hcp = float(request.args.get('hcp').replace(',', '.'))
        if ((hcp > 15) and (table_name != "RSHECCSILVER")):
            hcp = 15
    except ValueError:
        respuesta = jsonify({'error': 'Invalid hcp value. It must be a decimal number.'})
        respuesta.headers.add("Access-Control-Allow-Origin", '*')
        return respuesta, 400
    idJugador = devuelveIdJugador(email)
    time.sleep(1)
    bbdd = airtable.Airtable(base_id, table_name, token)
    field = {
                "Nombre": nombre,
                "HCPGolfos": hcp,
                "SlopeRACE": 0,
                "Tarjeta1": 0,
                "Tarjeta2": 0,
                "Tarjeta3": 0,
                "Tarjeta4": 0,
                "Tarjeta5": 0,
                "Tarjeta6": 0,
                "Tarjeta7": 0,
                "Tarjeta8": 0,
                "Tarjeta9": 0,
                "Tarjeta10": 0,
                "email": email,
                "Theopen": "0",
                "Themasters": "0",
                "Ryder": "0",
                "ChristmasMaster": "0",
                "Recompra": 0,
                "Pachangas": 0,
                "Torneos": 0,
                "Partidos": 0,
                "NumTarjetas": 0,
                "Pagado2024": "0",
                "Jugadores" : [idJugador],
                "FotosGolfos": [{"url": "https://res.cloudinary.com/golfosapp/image/upload/v1739127171/TSGC/b1pvzqy2c6rxbs4qdx2y.png"}]
            }
    try:
        bbdd.insert(field)
        respuesta = jsonify({'message': 'Usuario creado correctamente en la liga'})
    except Exception as err:
        respuesta = jsonify({'error': f'Error al crear el usuario: {err}'})
        respuesta.headers.add("Access-Control-Allow-Origin", '*')
        return respuesta, 500
    return respuesta ,200

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

@app.route('/api/actualizaTagOneSignal')
def actualizaTagOneSignal():
    subscription_id = request.args.get('subscription_id')
    liga = request.args.get('liga')
    REST_API_KEY = "os_v2_app_65dtnqhzt5hw5mh24wtuoznvitqz5h7cu7nejmejcqlmxt67tu7iveiftnlsv43icsygmucm6wmlflvh6qkudxlnnc5u7kuxwxk2rry"
    APP_ID = "f74736c0-f99f-4f6e-b0fa-e5a74765b544"
    configuration = onesignal.Configuration(
        app_key=REST_API_KEY
    )

    # Crear una instancia del cliente de API
    with onesignal.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        user_identity_request_body = UserIdentityRequestBody() 
    try:
        # Identificar al usuario por su ID de suscripción
        userid = api_instance.identify_user_by_subscription_id(APP_ID, subscription_id,user_identity_request_body)
        url = f"https://api.onesignal.com/apps/{APP_ID}/users/by/onesignal_id/{userid.identity.onesignal_id}"
        headers = {
            'Authorization: Key ' + REST_API_KEY,
            'accept:' 'application/json'
        }

        try:
            result = subprocess.run(
                ["curl", "--request", "GET", url, "-H", f"Authorization: Key {REST_API_KEY}", "-H", "accept: application/json"],
                capture_output=True,
                text=True
            )
            response_data = json.loads(result.stdout)
            if "properties" in response_data and "tags" in response_data["properties"] and "liga" in response_data["properties"]["tags"]:
                return jsonify({'La clave '+liga+' está presente en tags con el valor': str(response_data["properties"]["tags"]["liga"])}), 200
            else:
                url = f"https://api.onesignal.com/apps/{APP_ID}/users/by/onesignal_id/{userid.identity.onesignal_id}"
                headers = {
                    'Content-Type': 'application/json; charset=utf-8',
                }
                data = {
                    "properties": {
                        "tags": {
                            "liga": liga
                        }
                    }
                }

                try:
                    result = subprocess.run(
                        ["curl", "-X", "PATCH", url, "-H", json.dumps(headers), "-d", json.dumps(data)],
                        capture_output=True,
                        text=True
                    )
                    return jsonify({'message': 'Tag actualizado correctamente'}), 200
                except Exception as e:
                    return jsonify({'Error al actualizar el tag con curl': str(e)}), 500
        except Exception as e:
            return jsonify({'Error al ver el usuario': str(e)}), 500
        
    except Exception as e:
        return jsonify({'Error al obtener el user ID': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
    host = 'http://127.0.0.1:5000/api'

