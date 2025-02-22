import csv
import requests
import time
import random

input_file = 'handicaps.csv'
output_file = 'outputHCP.csv'

with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
    open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile, delimiter=';')
    
    for row in reader:
        if len(row) == 2:
            name,license_number = row
            try:
                response = requests.get(f'http://127.0.0.1:5000/api/handicap?licencia={license_number}')
                time.sleep(3)
                handicap = response.json().get('handicap', 'N/A')
                if response.status_code == 200:
                    writer.writerow([name, license_number, handicap])
                    print(f"Handicap de {name}: {handicap}")
                else:
                    writer.writerow(row)
            except Exception as e:
                print(f"Error al obtener handicap de {name}: {e}")
    time.sleep(random.uniform(1, 6))
    
print("Proceso terminado")  