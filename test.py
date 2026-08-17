import requests

lat = '40.7128'
lon = '-74.0060'
api_url = 'https://api.api-ninjas.com/v1/reversegeocoding?lat={}&lon={}'.format(lat, lon)
response = requests.get(api_url, headers={'X-Api-Key': 'rPh9HugPg4yUw1I0xSNFPp1GQdZo7fhTgAyq9VSr'})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)