from datetime import datetime
import requests
from os import environ

APP_ID = environ.get('APP_ID')
APP_KEY = environ.get('APP_KEY')
TOKEN = environ.get('TOKEN')
GENDER = 'male'
WEIGHT_KG = 100
HEIGHT_CM = 170
AGE = 18
today,time = (datetime.now().strftime('%Y-%m-%d T%H:%M')).split('T')

nutritionix_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'
sheety_endpoint_post = environ.get('SHEETY_ENDPOINT_POST')

exercise = input("Tell me what exercise you did: ")

headers = {
    'x-app-id': APP_ID,
    'x-app-key': APP_KEY,
}
exercise_config = {
    'query': exercise,
    'gender': GENDER,
    'weight_kg': WEIGHT_KG,
    'height_cm': HEIGHT_CM,
    'age': AGE
}
sheety_config = {

}
response = requests.post(url=nutritionix_endpoint, json=exercise_config, headers=headers)
response.raise_for_status()
result = response.json()

for exercise in result['exercises']:
    sheety_config = {
        'workout': {
            'date': today,
            'time': time,
            'exercise': exercise['name'],
            'duration': round(exercise['duration_min']),
            'calories': round(exercise['nf_calories']),
        }
    }
sheety_headers = {
    'Authorization': f'Bearer {TOKEN}'
}

sheety_response = requests.post(url=sheety_endpoint_post, json=sheety_config, headers=sheety_headers)
sheety_response.raise_for_status()

