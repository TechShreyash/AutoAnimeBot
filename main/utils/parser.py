import feedparser

def parse():
    a = feedparser.parse("https://subsplease.org/rss/")
    b = a["entries"]

    data = []

    def trim_title(title: str):
        title, ext = title.replace("[SubsPlease]","").strip().split("[",maxsplit=2)
        _, ext = ext.split("]",maxsplit=2)
        title = title.strip() + ext
        return title

    for i in b:
        item = {}
        item['title'] = trim_title(i['title'])
        item['size'] = i['subsplease_size']
        item['link'] = i['link']
        data.append(item)

    data.reverse()
    return data