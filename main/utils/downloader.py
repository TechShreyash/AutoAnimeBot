import time
from main import lib as ses
import libtorrent as lt
from pyrogram.types import Message

def get_percent_text(percent):
    text = """
Downloading: {}%
[{}]
35.50 MB of 328.61 MB
Speed: 5.70 MB/sec
ETA: 52s
"""

async def downloader(c,m: Message):
    link = m.text.replace("/up","").strip()

    params = {
    'save_path': './',
    'storage_mode': lt.storage_mode_t(2),}

    handle = lt.add_magnet_uri(ses, link, params)
    ses.start_dht()

    r = await m.reply_text('Downloading Metadata...')
    
    while (not handle.has_metadata()):
        time.sleep(1)
    await r.edit('Got Metadata, Starting Torrent Download...')

    await r.edit("Starting"+ str(handle.name()))

    while (handle.status().state != lt.torrent_status.seeding):
        s = handle.status()
        state_str = ['queued', 'checking', 'downloading metadata', \
                'downloading', 'finished', 'seeding', 'allocating']
        await r.edit('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s ' % \
                (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                s.num_peers, state_str[s.state]))
        print(s.total_done)
        print(s.total)
        time.sleep(5)