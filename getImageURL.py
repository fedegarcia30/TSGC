import airtable

token = 'patK75uFoPtI0qMNm.a71979b53e4ff353159574ef4b245e4ec46d73c329cee4ca3ed2e495ca5a273c'
base_id = 'appB6QQMNnJ4pgMLt'
table_name = 'RSHECCSILVER'

airtable = airtable.Airtable(base_id, table_name, token)

records = airtable.get_all(view='Grid view')
with open('outputURL.csv', 'w') as file:
    for record in records:
        email = record['fields'].get('email', '')
        image_url = record['fields'].get('FotosGolfos', [{}])[0].get('url', '')
        file.write(f"{email};{image_url}\n")

    

