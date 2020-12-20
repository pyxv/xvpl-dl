## user vars ##

# provide a custom download path, defaults to current dir 
# (playlists always download into their own folder)
custom_dl_dir = ''

# prevents duplicates across playlist download folders
# set to false if you want a full set of videos for each 
# individual playlist, even if it means duplicates
dedupe_all = True

## end user vars ##

print('\n🔞 🍆 💦 XVIDEOS PLAYLIST DOWNLOADER (xvpl-dl)\n')

print('\n🛠️  settings:\n')
print('  custom_dl_dir: ' + str(custom_dl_dir))
print('  dedupe_all: ' + str(dedupe_all))

import sys
import os
from urllib.parse import urlparse
import requests
import youtube_dl
from bs4 import BeautifulSoup

class Playlist:
    # html classes and attributes
    pagination_class = 'pagination'
    header_attrib = 'profile-title'
    dl_dir = os.curdir

    def __init__(self, url):
        self.url = url
        self.pages = []
        self.videos = []
        
        print ('\n⏳ initialising playlist...\n   ➡️ ' + self.url)
        content = requests.get(self.url)
        self.soup = BeautifulSoup(content.text, 'html.parser')

        self.name = self.make_pl_name()
        self.make_page_urls()
        for page_url in self.pages:
            page = Page(page_url)
            self.videos = self.videos + page.videos

        print ('     ➡️ total pages: ' + str(len(self.pages)))
        print ('     ➡️ total videos: ' + str(len(self.videos)))
        print ('')

    def download(self):
        pl_dl_dir = os.path.join(self.dl_dir, self.name, '')
        # see: https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L141
        self.ydl_opts = {
            'outtmpl': pl_dl_dir + '%(title)s-%(id)s.%(ext)s',
            'download_archive': 'dl_hist' if dedupe_all else pl_dl_dir + 'dl_hist',
        }
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download(self.videos)

    def total_pages(self):
        pagination_block = self.soup.find(class_=self.pagination_class)
        try:
            return int(pagination_block.find(attrs={"class": "last-page"}).string)
        except:
            return len(pagination_block.find_all('li')) - 1

    def make_pl_name(self):
        header = self.soup.find(id=self.header_attrib)
        profile = header.find(attrs={"class": "name"}).string
        last_path_fragment = urlparse(self.url).path.split('/')[-1]
        return (profile + '--' + last_path_fragment)

    def make_page_urls(self):
        last_page = self.total_pages()
        for p in range(0,last_page):
            page_url = self.url + '/' + str(p)
            self.pages.append(page_url)

class Page:
    url_root = 'https://xvideos.com/'

    # html classes and attributes
    content_class = 'mozaique'
    id_attrib = 'data-id'

    def __init__(self, url):
        self.url = url
        self.content = requests.get(url)
        self.soup = BeautifulSoup(self.content.text, 'html.parser')
        self.videos = []

        # get all video links from current page
        self.extract_video_urls()

    def extract_video_urls(self):
        videos_block = self.soup.find(class_=self.content_class)
        video_elements = videos_block.find_all(attrs={self.id_attrib: True})
        for video in video_elements:
            self.videos.append(self.url_root + 'video' + video.get(self.id_attrib) + '/')

args = sys.argv

print('\n📚 playlists queued:\n')

for pl in args[1:]:
    print ('   ➡️ ' + pl)

print('\n📥 commencing download...')

for pl in args[1:]:
    playlist = Playlist(pl)
    if custom_dl_dir:
        playlist.dl_dir = custom_dl_dir
    playlist.download()
