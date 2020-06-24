# Handling webscrapping from bsaber site.
from bs4 import BeautifulSoup
import requests
import re

# Handling file system navigation and paths.
from os.path import join, exists
from os import mkdir, listdir, replace
import zipfile


class SongScrapper():
    """Object used for scrapping songs from bsaber.com and
    downloading/extracting them to the proper location.
    """

    def __init__(self, path_to_custom_levels_folder):
        """ Constructs a SongScrapper object. """

        """ Location that custom songs are going to be saved at. """
        self.__path_to_custom_levels = path_to_custom_levels_folder

        """ These are the options that we can query songs by. """
        self.__sorted_by_options = ['new', 'top', 'most-difficult']

        """ The time periods that we can query songs to grab by. """
        self.__time_period_options = \
            ['24-hours', '7-days', '30-days', '3-months', 'all']

        """ Website that we are parsing from. """
        self.__bsaber_site = 'http://www.bsaber.com/songs'


    def __check_valid_sorted_by_option(self, sorted_by):
        """Helper method for scrape_songs().
        Make sure that sorted_by is a valid param that can be passed to the
        scrape_songs() method.

        Args:
            sorted_by (str): Checked to make sure that it is in
            __sorted_by_options.

        Raises:
            ValueError: If sorted_by is not a member of __sorted_by_options.
        """
        if sorted_by not in self.__sorted_by_options:
            raise ValueError("Error: Option must be of the following: "
                             f"{self.__sorted_by_options}")


    def __check_valid_time_period(self, time_period):
        """Make sure that the time_period is a valid param that can be passed
        to the scrape_songs() method.

        Args:
            time_period (str): Checked to make sure that it is in
                                __time_period_options.

        Raises:
            ValueError: If time_period is not a member of
                        __time_period_options.
        """
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
        page_data = requests.get(url_to_songs).text
        soup = BeautifulSoup(page_data, features='html.parser')
        # x = soup.find_all(re.compile('^h[1-6]$'))
        x = soup.find_all(re.compile('a'))
        for y in x:
            print(y)
        print(x)
        # for y in x:
        #     print(x)
        # print(page)

    # last.
    def download_songs_to_folder(self):
        pass


    def __extract_song_in_custom_levels_folder(self, path_to_song_zipfile):
        # Make a new temp folder to store the zip file into.
        song_folder = path_to_song_zipfile.split('.zip')[0] + \
            path_to_song_zipfile.split('.zip')[1]

        # Don't want to create a folder that already exists.
        if not exists(song_folder):
            mkdir(join(self.__path_to_custom_levels, song_folder))

            with zipfile.ZipFile(path_to_song_zipfile, 'r') as zipfile_to_extract:
                zipfile_to_extract.extractall(song_folder)

    def extract_all_songs_in_custom_levels_folder(self):
        all_files_in_custom_level_folder = listdir(self.__path_to_custom_levels)

        list_of_zipfiles = [file for file in all_files_in_custom_level_folder
                            if file.endswith('.zip')]

        for zip_file in list_of_zipfiles:
            self.__extract_song_in_custom_levels_folder(join(self.__path_to_custom_levels, zip_file))


def main():
    custom_levels_path = "D:\Games\Beat.Saber.v1.7.0.ALL.DLC\Beat Saber\Beat Saber_Data\CustomLevels"
    scrapper = SongScrapper(custom_levels_path)

    # Test out webscrapping.
    # scrapper.scrape_songs(sorted_by='top', time_period='24-hours')

    # Test out extracting.
    scrapper.extract_all_songs_in_custom_levels_folder()

if __name__ == "__main__":
    main()
