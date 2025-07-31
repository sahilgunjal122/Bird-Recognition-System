import requests
import os


def get_bird_image_url(bird_name):
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("GOOGLE_CX")
    query = bird_name + " bird"
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&searchType=image&key={api_key}&cx={search_engine_id}&num=1"

    try:
        response = requests.get(url)
        data = response.json()
        return data['items'][0]['link'] if 'items' in data else None
    except Exception as e:
        print("Error fetching image:", e)
        return None
