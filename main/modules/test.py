# Temporary        


import os
import shutil


class GogoAPI():
    def __init__(self) -> None:
        pass

    def get_episode_links(self, anime, ep_num):
        url = api1 + self.anime
        data = get(url, json=True)
        sources = data.get('sources')
        m3u8 = []

        if sources and len(sources) != 0:
            for source in sources:
                url = source.get('url').strip()
                if url and url not in m3u8:
                    m3u8.append(url)

        url = api2 + self.anime
        servers = get(url, json=True)

        output = {'m3u8': m3u8, 'servers': servers}
        return output


class ZoroAPI():
    def __init__(self, anime, ep_num=None) -> None:
        self.name, self.ep_num = anime, int(ep_num)

    def search(self):
        url = api3 + self.name
        data = get(url, json=True)
        results = data.get('results')
        return results

    def get_episode_links(self):
        results = self.search()
        if results and len(results) != 0:
            anime_id = results[0].get('id')

        url = api4 + anime_id
        data = get(url, json=True)
        episodes = data.get('episodes')

        if not (episodes and len(episodes) >= self.ep_num):
            return None

        episode_id = episodes[self.ep_num - 1].get('id')
        url = api5 + episode_id
        data = get(url, json=True)
        sources = data.get('sources')
        subtitles = data.get('subtitles')
        m3u8 = []

        for source in sources:
            quality = source.get('quality')
            if quality == 'auto':
                link = source.get('url')
                m3u8.append(link)

        sub = None
        for subtitle in subtitles:
            lang = subtitle.get('lang')
            if lang == 'English':
                sub = subtitle.get('url')

        output = {'m3u8': m3u8, 'subtitle': sub}
        return output

