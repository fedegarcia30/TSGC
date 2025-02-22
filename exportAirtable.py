import requests
import json
import airtable


# Configuración de Airtable
token = 'patQR2tDbsEaW67qU.97bb8899b82b80d25ea25efa89cea2acf24d8a8b4ae96e9489133000f6f95ae1'
base_id = 'appDwQa5OnmkIO0Ee'
table_name = 'ConfigTable'

# conexion a la API de Airtable
bbddLigas = airtable.Airtable(base_id, table_name, token)


url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4))
    with open('TSGCMetadata.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
else:
    print(f"Error: {json.dumps(response.json(), indent=4)}")