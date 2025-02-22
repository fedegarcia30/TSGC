import onesignal
from onesignal.api import players_api
from onesignal.rest import ApiException

# Configuración de OneSignal
configuration = onesignal.Configuration(
    app_key="TUS_APP_KEY"  # Tu REST API Key de OneSignal
)

# Crear cliente para interactuar con la API de OneSignal
with onesignal.ApiClient(configuration) as api_client:
    api_instance = players_api.PlayersApi(api_client)
    
    subscription_id = "1e1dd134-047a-47fb-ab11-eac220b57fa5"  # Reemplaza con el Subscription ID del usuario
    new_external_id = "SCHIERBEEK"    # Reemplaza con el nuevo external ID que deseas asignar

    try:
        # Actualizar external ID
        player = api_instance.update_player(
            player_id=subscription_id,  # Usamos el Subscription ID como el player ID
            external_id=new_external_id  # Nuevo external ID
        )
        print("External ID actualizado correctamente:", player)
    except ApiException as e:
        print("Error al actualizar el External ID:", e)
