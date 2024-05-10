import requests
import json

def get_hotels(api_key, location, radius=5000, keyword='hotel'):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'key': api_key,
        'location': location,
        'radius': radius,
        'keyword': keyword
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['results']
    else:
        print("Error:", response.status_code)
        return None

def main():
    api_key = 'your_api_key'
    location = '25.276987,55.296249'  # Dubai coordinates
    radius = 5000  # 5 km radius around Dubai
    keyword = 'hotel'
    hotels = get_hotels(api_key, location, radius, keyword)
    if hotels:
        for hotel in hotels:
            print(hotel['name'], hotel['vicinity'])
    else:
        print("No hotels found.")

if __name__ == "__main__":
    main()
