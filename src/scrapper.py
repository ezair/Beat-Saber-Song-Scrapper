# Handling webscrapping from bsaber site.
import urllib2
from bs4 import BeautifulSoup

# Handling file system navigation and paths.
from os.path import join
import shutil

class SongScrapper():
    """Object used for scrapping songs from bsaber.com and downloading/
    extracting them to the proper location.
    """

    def __init__(self, path_to_custom_levels_folder):
        self.path_to_custom_levels = path_to_custom_levels
        self.bsaber_site = 'http://www.bsaber.com'


    def __download_songs_to_folder(self):
        pass


    def __extract_songs_in_folder(self):
        pass


    def scrape_songs(self):
        pass


    def scrape_new_songs(self):
        pass


    def scrape_top_songs(self):
        pass
