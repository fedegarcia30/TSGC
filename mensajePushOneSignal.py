import onesignal
from onesignal.api import default_api
from onesignal.model.notification import Notification
from onesignal.rest import ApiException
from onesignal.model.user_identity_request_body import UserIdentityRequestBody
import subprocess
import json

def send_notification():
    # Configuración de OneSignal
    REST_API_KEY = "qz5h7cu7nejmejcqlmxt67tu7"
    APP_ID = "f74736c0-f99f-4f6e-b0fa-e5a74765b544"
    configuration = onesignal.Configuration(
        app_key="os_v2_app_65dtnqhzt5hw5mh24wtuoznvitqz5h7cu7nejmejcqlmxt67tu7iveiftnlsv43icsygmucm6wmlflvh6qkudxlnnc5u7kuxwxk2rry",  # REST API Key
    )

    # Crear una instancia del cliente de API
    with onesignal.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)

    # Crear la notificación
    notification = Notification(
        app_id=APP_ID,
        headings={"en": "¡Hola!"},
        contents={"en": "Este es un mensaje de prueba"},
        include_external_user_ids=[""],
    )

    try:
        response = api_instance.create_notification(notification)
        print(response)
    except ApiException as e:
        print(f"Error al enviar la notificación: {e}")

def get_userID(subscription_id):
    # Configuración de OneSignal
    REST_API_KEY = "qz5h7cu7nejmejcqlmxt67tu7"
    APP_ID = "f74736c0-f99f-4f6e-b0fa-e5a74765b544"
    configuration = onesignal.Configuration(
        app_key="os_v2_app_65dtnqhzt5hw5mh24wtuoznvitqz5h7cu7nejmejcqlmxt67tu7iveiftnlsv43icsygmucm6wmlflvh6qkudxlnnc5u7kuxwxk2rry",  # REST API Key
    )

    # Crear una instancia del cliente de API
    with onesignal.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)
        user_identity_request_body = UserIdentityRequestBody() 
    try:
        # Identificar al usuario por su ID de suscripción
        user = api_instance.identify_user_by_subscription_id(APP_ID, subscription_id,user_identity_request_body)
        return user
    except ApiException as e:
        print(f"Error al obtener el user ID: {e}")
        return None
    


    # Configuración de OneSignal
    REST_API_KEY = "qz5h7cu7nejmejcqlmxt67tu7"
    APP_ID = "f74736c0-f99f-4f6e-b0fa-e5a74765b544"
    configuration = onesignal.Configuration(
        app_key="os_v2_app_65dtnqhzt5hw5mh24wtuoznvitqz5h7cu7nejmejcqlmxt67tu7iveiftnlsv43icsygmucm6wmlflvh6qkudxlnnc5u7kuxwxk2rry",  # REST API Key
    )

    # Crear una instancia del cliente de API
    with onesignal.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)

    try:
        # Crear el cuerpo de la actualización
        update_body = {
            "tags": {
                "liga": liga
            }
        }
        # Actualizar el usuario
        api_instance.update_user()
        print("El tagId ha sido creado con el valor LIGA.")
    except ApiException as e:
        print(f"Error al actualizar el tag: {e}")

    # Configuración de OneSignal
    REST_API_KEY = "qz5h7cu7nejmejcqlmxt67tu7"
    APP_ID = "f74736c0-f99f-4f6e-b0fa-e5a74765b544"
    configuration = onesignal.Configuration(
        app_key="os_v2_app_65dtnqhzt5hw5mh24wtuoznvitqz5h7cu7nejmejcqlmxt67tu7iveiftnlsv43icsygmucm6wmlflvh6qkudxlnnc5u7kuxwxk2rry",  # REST API Key
    )

    # Crear una instancia del cliente de API
    with onesignal.ApiClient(configuration) as api_client:
        api_instance = default_api.DefaultApi(api_client)

    try:
        # Crear el cuerpo de la solicitud de alias
        alias_body = {
            "Nombre": alias_label,
            "id": alias_id
        }
        # Crear el alias
        response = api_instance.create_alias(APP_ID, subscription_id, alias_body)
        print("Alias creado exitosamente:", response)
    except ApiException as e:
        print(f"Error al crear el alias: {e}")

def update_tag_with_curl(onesignal_id, liga):

    APP_ID = "f74736c0-f99f-4f6e-b0fa-e5a74765b544"
    url = f"https://api.onesignal.com/apps/{APP_ID}/users/by/onesignal_id/{onesignal_id}"
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
        print("Response:", result.stdout)
    except Exception as e:
        print(f"Error al actualizar el tag con curl: {e}")

def view_user(onsignal_id):
    APP_ID = "f74736c0-f99f-4f6e-b0fa-e5a74765b544"
    REST_API_KEY = "os_v2_app_65dtnqhzt5hw5mh24wtuoznvitqz5h7cu7nejmejcqlmxt67tu7iveiftnlsv43icsygmucm6wmlflvh6qkudxlnnc5u7kuxwxk2rry"
    url = f"https://api.onesignal.com/apps/{APP_ID}/users/by/onesignal_id/{onsignal_id}"
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
            print("La clave 'liga' está presente en tags con el valor:", response_data["properties"]["tags"]["liga"])
        else:
            print("La clave 'liga' no está presente en tags.")
    except Exception as e:
        print(f"Error al ver el usuario por alias: {e}")

@app.route('/api/NuevoUsuarioHandicap')
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
                print("El tag liga está presente en tags con el valor:", response_data["properties"]["tags"]["liga"])
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
                    print("Response:", result.stdout)
                except Exception as e:
                    print(f"Error al actualizar el tag con curl: {e}")
        except Exception as e:
            print(f"Error al ver el usuario: {e}")
        
    except ApiException as e:
        print(f"Error al obtener el user ID: {e}")
        return None

actualizaTagOneSignal("9850981a-af8f-4faf-a2fc-6876467501dd","RCPH")
#userid = get_userID("9850981a-af8f-4faf-a2fc-6876467501dd")

#update_tag_with_curl(userid.identity.onesignal_id, "RCPH")
#view_user("88e3f622-2ef6-480f-ae4b-f61e742df353")