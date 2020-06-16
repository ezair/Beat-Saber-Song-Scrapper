# Handling webscrapping from bsaber site.
from bs4 import BeautifulSoup
import requests
import re

# Handling file system navigation and paths.
from os.path import join
import shutil


class SongScrapper():
    """Object used for scrapping songs from bsaber.com and downloading/
    extracting them to the proper location.
    """

    def __init__(self, path_to_custom_levels):

        """ Location that custom songs are going to be saved at. """
        self.__path_to_custom_levels = path_to_custom_levels

        """ These are the options that we can query songs by. """
        self.__sorted_by_options = ['new', 'top', 'most-difficult']

        """ The time periods that we can query songs to grab by. """
        self.__time_period_options = \
            ['24-hours', '7-days', '30-days', '3-months', 'all']

        """ Website that we are parsing from. """
        self.__bsaber_site = 'http://www.bsaber.com/songs'

    
    def __check_valid_sorted_by_option(self, sorted_by):
        if sorted_by not in self.__sorted_by_options:
            raise ValueError("Error: Option must be of the following: "
                             f"{self.__sorted_by_options}")


    def __check_valid_time_period(self, time_period):
        if time_period not in self.__time_period_options:
            raise ValueError("Error: Option must be of the following: "
                             f"{self.__time_period_options}")


    def scrape_songs(self, sorted_by='new', time_period='all',
                     number_of_songs=21):
        # Let's make sure that we are querying by valid options.
        self.__check_valid_sorted_by_option(sorted_by)
        self.__check_valid_time_period(time_period)

        # Alright, now that we know that the queries are valid,
        # we need to construct the proper URL to the webpage that
        # the songs we want to query are on.
        url_to_songs = join(self.__bsaber_site, sorted_by)

        # If we are querying for a new song, then no time period
        # is assigned in the url. Only add a time period to the URL
        # if the song is not queried for new.
        if sorted_by != 'new':
            url_to_songs = join(url_to_songs, '?time=' + time_period)

        # We create a dict of song_names mapped to the download link of the
        # song so that displaying the song and downloading them is an easier
        # task.
        dict_of_songs = {}
        page = requests.get(url_to_songs).text
        soup = BeautifulSoup(page, features='html.parser')
        #x = soup.find_all(re.compile('^h[1-6]$'))
        x = soup.find_all(re.compile('^h[6]$'))
        for y in x:
            print(y)
        # for y in x:
        #     print(x)
        # print(page)

    def __download_songs_to_folder(self):
        pass


    def __extract_songs_in_folder(self):
        pass


def main():
    scrapper = SongScrapper('')
    scrapper.scrape_songs(sorted_by='top', time_period='24-hours')


if __name__ == "__main__":
    main()
