from bs4 import BeautifulSoup
import requests

hosts = ['api.consumet.org']

api = [
    'https://{}/anime/gogoanime/watch/',
    'https://{}/anime/gogoanime/servers/',
    'https://{}/anime/zoro/',
    'https://{}/anime/zoro/info?id=',
    'https://{}/anime/zoro/watch?episodeId=',
    'https://{}/anime/animepahe/',
    'https://{}/anime/animepahe/info/',
    'https://{}/anime/animepahe/watch/',
    'https://animepahe.com/api?m=airing'
]

class AnimePahe():
    def __init__(self) -> None:
        pass

    def search(query):
        json = None
        for host in hosts:
            url = api[5].format(host) + query
            response = requests.get(url)

            if response.status_code == 200:
                json = response.json()
                break
        if not json:
            return
        
        results = json['results']
        return results

    def get_latest():
        url = api[8]
        response = requests.get(url).json()
        data = response['data']
        return data

    def get_episode_links(episode_id):
        json = None
        tries = 0
        while tries < 6:
            for host in hosts:
                tries += 1
                url = api[7].format(host) + episode_id
                response = requests.get(url)

                if response.status_code == 200:
                    json = response.json()
                    break
            print(f'Try {tries} failed -->',episode_id)
        if not json:
            return        
        return json
