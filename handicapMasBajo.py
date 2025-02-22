import airtable
import json

token = 'patu8RlYjmOVmg5bf.2d0fd1baf43d70586e2ee01b489430a830dff2e97d3075b13a43baadf5b0fcfd'
base_id = 'app8fxtucu07wvetM'
table_name = 'Handicap'
email = 'fedegarcia30@gmail.com'
bbddLigas = airtable.Airtable(base_id, table_name, token)
media_nivel_jugado = 0  
records = bbddLigas.get_all(formula="FIND('"+email+"',email)")
numeroTarjetas = 10
for record in records:
    fields = record['fields']
    print(f"Tamaño de fields: {len(fields)}")
    for i in range(90, 1, -1):
        column_name = f'Tarjeta{i}'
        if fields.get(column_name) is not None:
            numeroTarjetas -= 1
            tarjeta_data = json.loads(fields.get(column_name))
            nivel_jugado = tarjeta_data.get('NivelJuego')
            if nivel_jugado is not None:
                media_nivel_jugado = media_nivel_jugado + float(nivel_jugado)
        if numeroTarjetas == 0:
            break
print(f"Media nivel jugado: {media_nivel_jugado/10}")
