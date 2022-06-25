import asyncio
#from main.modules.cv2_utils import format_text
import requests
import time
import os
from bs4 import BeautifulSoup
from datetime import datetime

ANIME_QUERY = """
query ($id: Int, $idMal:Int, $search: String) {
  Media (id: $id, idMal: $idMal, search: $search, type: ANIME) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    format
    status
    episodes
    duration
    countryOfOrigin
    source (version: 2)
    trailer {
      id
      site
    }
    genres
    tags {
      name
    }
    averageScore
    relations {
      edges {
        node {
          title {
            romaji
            english
          }
          id
        }
        relationType
      }
    }
    nextAiringEpisode {
      timeUntilAiring
      episode
    }
    isAdult
    isFavourite
    mediaListEntry {
      status
      score
      id
    }
    siteUrl
  }
}
"""

async def return_json_senpai(query: str, vars_: dict):
    url = "https://graphql.anilist.co"
    return requests.post(url, json={"query": query, "variables": vars_}).json()

async def get_anime(vars_,less):
    if 1 == 1:
        result = await return_json_senpai(ANIME_QUERY, vars_)

        error = result.get("errors")
        if error:
            error_sts = error[0].get("message")
            print([f"[{error_sts}]"])

        data = result["data"]["Media"]   
        idm = data.get("id")
        title = data.get("title")
        tit = title.get("english")
        if tit == None:
            tit = title.get("romaji")
        title_img = f"https://img.anili.st/media/{idm}"
        
        if less == True:
          print(idm, title_img, tit)
          return idm, title_img, tit
        
        print(data)
        print(data.keys())
        return data

async def get_anime_img(query):
    vars_ = {"search": query}
    idm, title_img, title = await get_anime(vars_,less=True)

    #title = format_text(title)
    return idm, title_img, title

def get_anime_name(title):
    x = title.split(" - ")[-1]
    title = title.replace(x,"").strip().replace("S","Season ")
    title = title[:-2].strip()
    return title


async def get_anilist_data(name):
    vars_ = {"search": name}
    data = await get_anime(vars_,less=False)

    id = data.get("id")
    title = data.get("title")
    format = data.get("format")
    status = data.get("status")
    episodes = data.get("episodes")
    duration = data.get("duration")
    trailer = data.get("trailer")
    genres = data.get("genres")
    averageScore = data.get("averageScore")

    



print(asyncio.run(get_anime_img("horimiya")))