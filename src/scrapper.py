"""
@author Eric Zair
@file scrapper.py

Contains the SongScrapper object.

SongScrapper is used for extracting zipfiles of custom songs to the custom_levls
folder for the vr game, beatsaber.

In addition to this, SongScrapper can also scrape songs from the bsaber.com website.
"""

# Handling webscrapping from bsaber site.
from bs4 import BeautifulSoup
import requests
from urllib import request

import urllib

# Parsing html data for finding the correct beatsaber songs.
import re

# Handling file system navigation and paths.
from os.path import join, exists
from os import mkdir, listdir
import zipfile


class SongScrapper():
    """Object used for scrapping songs from bsaber.com and
    downloading/extracting them to the proper location.
    """


    def __init__(self, path_to_custom_levels_folder):
        """ Constructs a SongScrapper object.

        Args:
            path_to_custom_levels_folder (str): The location of the custom_levels/
                                                folder in your beatsaber game.
        """

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


    def __extract_song_in_custom_levels_folder(self, path_to_song_zipfile,
                                               display_error_message=True):
        """Helper method for self.extract_all_songs_in_custom_levels_folder().

        Builds a new folder for a custom song and extracts the zipfile's content
        into that new folder.
        """
        # Make a new temp folder to store the zip file into.
        song_folder = path_to_song_zipfile.split('.zip')[0] + \
            path_to_song_zipfile.split('.zip')[1]

        # Don't want to create a folder that already exists.
        if not exists(song_folder):
            mkdir(join(self.__path_to_custom_levels, song_folder))

            try:
                with zipfile.ZipFile(path_to_song_zipfile, 'r') as zipfile_to_extract:
                    zipfile_to_extract.extractall(song_folder)
            except Exception as e:
                if display_error_message:
                    print(e)

                # Program gets stalled for input if I don't pass here.
                pass


    def extract_all_songs_in_custom_levels_folder(self, display_error_message=True):
        """Extract each custom song's zipfile into a new folder located
        in the custom_levels/ folder in the beatsaber game.

        Args:
            display_error_message (bool, optional): If the user wants to see the potenital 
            errors that are thrown. Defaults to True.
        """
        all_files_in_custom_level_folder = listdir(self.__path_to_custom_levels)

        list_of_zipfiles = [file for file in all_files_in_custom_level_folder
                            if file.endswith('.zip')]

        for zip_file in list_of_zipfiles:
            self.__extract_song_in_custom_levels_folder(join(self.__path_to_custom_levels, zip_file))


    # TODO
    def scrape_songs(self, sorted_by='new', time_period='all',
                     number_of_songs=21):
        # Let's make sure that we are querying by valid options.
        self.__check_valid_sorted_by_option(sorted_by)
        self.__check_valid_time_period(time_period)

        # Alright, now that we know that the queries are valid,
        # we need to construct the proper URL to the webpage that
        # the songs we want to query are on.
        url_to_songs = self.__bsaber_site + "/" + sorted_by

        # If we are querying for a new song, then no time period
        # is assigned in the url. Only add a time period to the URL
        # if the song is not queried for new.
        if sorted_by != 'new':
            url_to_songs = url_to_songs + '/?time=' + time_period

        # We create a dict of song_names mapped to the download link of the
        # song so that displaying the song and downloading them is an easier
        # task.
        page_data = requests.get(url_to_songs).text
        soup = BeautifulSoup(page_data, features='html.parser')

        # The song title and song name for each song is contained in a h4 tag.
        # Also, we only want the amount of songs that the user requests :)
        song_tags = soup.find_all(re.compile('h4$'))[: number_of_songs]

        # This will be a dict of <song_title, song_download_link>.
        # It will be the object that we return at the end of this method.
        dict_of_songs = {}

        for bs4_song_tag in song_tags:
            # NOTE
            # This line is disgusting, but basically the bs4 tags look like this:
            #   <h4 class="entry-title" itemprop="name headline">
            #   <a href="https://bsaber.com/songs/b6d6/" title="Escape From Midwich Valley">
            #   Escape From Midwich Valley </a>
            #   </h4>

            # Find song title.
            song_tag_as_str = str(bs4_song_tag)
            html_tags = song_tag_as_str.split('\n')
            song_title = html_tags[2].strip(' </a>')

            # Build the link that goes to the song's downloadable zip file.
            ahref_tag = html_tags[1]
            # The song's link is always <a href="https://bsaber.com/songs/' + the primary
            # key of the song. The primary key can be found at the end of the link that goes to
            # the song's webpage.
            song_primary_key = ahref_tag.replace('<a href="https://bsaber.com/songs/', "")[: 4]
            song_link = 'https://beatsaver.com/api/download/key/' + song_primary_key

            dict_of_songs[song_title] = song_link

        return dict_of_songs


    # TODO
    def download_songs(self, dict_of_songs, display_error_message=True):
        for song in dict_of_songs:
            # Access the file that is located at the songs url path.
            # Recall that the dict passed in is a dict of <song_title, link_to_song>.
            try:
                response = request.urlopen(dict_of_songs[song])
                download_file = str(response.read())

                # Need to copy the info from the downloaded zip file to the new file
                # which is located in the beatsaber custom levels folder/name_of_song.zip
                song_save_location = join(self.__path_to_custom_levels, song) + '.zip'
                new_file_to_store_download = open(song_save_location)

                for line in download_file.split('\\n'):
                    new_file_to_store_download.write(line + '\n')
                new_file_to_store_download.close()
            except Exception as e:
                if display_error_message:
                    print(e + '\n')


    def download_extract_songs(self, dict_of_songs, display_error_message=True):
        self.download_songs(dict_of_songs, display_error_message=display_error_message)
        self.extract_all_songs_in_custom_levels_folder(display_error_message=display_error_message)


def main():
    custom_levels_path = "D:\Games\Beat.Saber.v1.7.0.ALL.DLC\Beat Saber\Beat Saber_Data\CustomLevels"
    scrapper = SongScrapper(custom_levels_path)

    # Test out webscrapping.
    scrapped_songs = scrapper.scrape_songs()

    # print("Song titles: ")
    # for song in scrapped_songs:
    #     print("Song Title:", song)
    #     print("Song Download Link:", scrapped_songs[song])
    #     print()

    scrapper.download_extract_songs(scrapped_songs)


if __name__ == "__main__":
    main()
