import asyncio
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

async def get_anime(vars_):
    try:
        result = await return_json_senpai(ANIME_QUERY, vars_)

        error = result.get("errors")
        if error:
            error_sts = error[0].get("message")
            print([f"[{error_sts}]"])

        data = result["data"]["Media"]   
        idm = data.get("id")
        title = data.get("title")
        title = title.get("english")
        title_img = f"https://img.anili.st/media/{idm}"
        return idm, title_img, title
    except:
        print(f"error {vars_["search"}")
        return await get_anime(vars_)

async def get_anime_img(query):
    vars_ = {"search": query}
    idm, title_img, title = await get_anime(vars_)
    return idm, title_img, title

def get_anime_name(title):
    x = title.split("-")[-1]
    title = title.replace(x,"").strip()
    return title
