import requests
from bs4 import BeautifulSoup

# URL de la página web
url = 'https://www.eaebarcelona.com/es/landing/elige-tu-master?utm_content=IBBB00N158X&c=IBBB00N158X&msclkid=d81a5b0aa00f1f3463983cae28907407&utm_source=bing&utm_medium=cpc&utm_campaign=EAEBCN-DS-Espa%C3%B1a_Bing_WCPBCN--WTPMaster-BING-NAC-BT_sea-prf_bt_WAAGen_always-on_und_bt_es_es_elo_ongoing_IBBB00N158X&utm_term=eae%20business%20school'

# Realizar la solicitud HTTP
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Encontrar todos los elementos con la clase especificada
elements = soup.find_all('div', class_='col-12 col-md-6')

# Extraer la información de cada elemento
for element in elements:
    title = element.find('h4').text
    description = element.find('p').text
    link = element.find('a', class_='gp-button link--generic-advanced')['href']
    image = element.find('img')['src']
    
    print(f'Título: {title}')
    print(f'Descripción: {description}')
    print(f'Enlace: {link}')
    print(f'Imagen: {image}')
    print('---')