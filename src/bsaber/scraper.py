"""
@author Eric Zair
@file scraper.py

Contains the SongScraper object.

SongScraper is used for extracting zipfiles of custom songs to the custom_levels
folder for the vr game, beatsaber.

In addition to this, SongScraper can also scrape songs from the bsaber.com website.
"""

# Handling webscrapping from bsaber site.
from bs4 import BeautifulSoup
import requests

# Parsing html data for finding the correct beatsaber songs.
import re

# Handling file system navigation and paths.
from os.path import join, exists
from os import mkdir, listdir
import zipfile
import shutil


class SongScraper():
    """Object used for scrapping songs from bsaber.com and
    downloading/extracting them to the proper location.
    """

    def __init__(self, path_to_custom_levels_folder):
        """ Constructs a SongScrpper object.

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
        self.__bsaber_site = 'https://www.bsaber.com/'


    def sorted_by_options(self):
        """Return all possible sorting options that the user can query songs with.

        Returns:
            list(str): The sorting options that the user can query songs with.
        """
        return self.__sorted_by_options


    def time_period_options(self):
        """Return all possible time periods that the user can scrape songs with.

        Returns:
            list(str): The time periods that a user can scrape songs with.
        """
        return self.__time_period_options


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
        song_folder = path_to_song_zipfile.split('.zip')[0] + path_to_song_zipfile.split('.zip')[1]

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
            display_error_message (bool, optional): If the user wants to see the potential.
            errors that are thrown. Defaults to True.
        """
        all_files_in_custom_level_folder = listdir(self.__path_to_custom_levels)

        list_of_zipfiles = [file for file in all_files_in_custom_level_folder
                            if file.endswith('.zip')]

        for zip_file in list_of_zipfiles:
            self.__extract_song_in_custom_levels_folder(join(self.__path_to_custom_levels, zip_file))


    def __find_songs_given_url(self, url_to_songs, number_of_songs=21):
        """Given the url to songs we want to scrape, we return a dict containing each song's name
           and download link.

        Args:
            url_to_songs (str): The url that the songs we wish to scrape are located at.

            number_of_songs (int, optional): The number of songs we want to grab. Defaults to 21.

        Returns:
            dict(str, str): dict with each entry representing a song.
            <song_name> -> <song_download_link>.
        """
        request = requests.get(url_to_songs)

        if request.status_code != 200:
            raise requests.exceptions.HttpError('Error in scrape_songs(), unable to access file.')

        soup = BeautifulSoup(request.text, features='html.parser')

        # The song title and song name for each song is contained in a h4 tag.
        # Also, we only want the amount of songs that the user requests :)
        print(url_to_songs)
        song_tags = soup.find_all(re.compile('h4$'))[: number_of_songs]

        # This will be a dict of <song_title, song_download_link>.
        # It will be the object that we return at the end of this method.
        dict_of_songs = {}

        for bs4_song_tag in song_tags:

            # Find song title.
            song_tag_as_str = str(bs4_song_tag)
            html_tags = song_tag_as_str.split('\n')
            print(f"htlm_tags: {html_tags}")
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


    def get_song_results(self, sorted_by='new', time_period='all'):
        """Return a dict of songs based on the given sorted_by and time_period fields given.

        Args:
            sorted_by (str, optional): The type of song you are querying for.
                                       Options: ['new', 'top', 'most-difficult'].
                                       Defaults to 'new'.

            time_period (str, optional): The time period that you want to download a song from.
                                         Options: ['24-hours', '7-days', '30-days', '3-months', 'all']
                                        Defaults to 'all'.

        Returns:
            dict(str, str): dict with each entry representing a song.
            <song_name> -> <song_download_link>.
        """
        # Let's make sure that we are querying by valid options.
        self.__check_valid_sorted_by_option(sorted_by)
        self.__check_valid_time_period(time_period)

        # Alright, now that we know that the queries are valid,
        # we need to construct the proper URL to the webpage that
        # the songs we want to query are on.
        url_to_songs = self.__bsaber_site + "songs/" + sorted_by

        # If we are querying for a new song, then no time period
        # is assigned in the url. Only add a time period to the URL
        # if the song is not queried for new.
        if sorted_by != 'new':
            url_to_songs += '/?time=' + time_period

        # We create a dict of song_names mapped to the download link of the
        # song so that displaying the song and downloading them is an easier
        # task.
        return self.__find_songs_given_url(url_to_songs)


    def get_searched_for_song_results(self, song):
        """Return a dict containing the songs queried by a specific song that the user wants to find.

        Args:
            song_user_searched_for (str): The song that the user wants to search for.

        Returns:
            dict(str, str): dict with each entry representing a song.
            <song_name> -> <song_download_link>.
        """
        # A search for the song "this is an example " would construct the link:
        # https://bsaber.com/?s=this+is+an+example&orderby=relevance&order=DESC&
        url_to_song = self.__bsaber_site + "/?s=" + song.replace(' ', '+') + '&'

        return self.__find_songs_given_url(url_to_song)


    def download_songs(self, dict_of_songs, display_error_message=True):
        """Given a dict_of_songs <song_name> -> <song_download_link>, we download each song to
        the custom_levels/ beatsaber folder. Each song is a .zip file when downloaded.

        Args:
            dict_of_songs dict(str): A dict containing a collection of songs.
            <song_name> -> <link to song>.

            display_error_message (bool, optional): True if user wants to output an error if it occurs
                                                    , False otherwise. Defaults to True.
        """
        for song in dict_of_songs:
            try:
                # This user agent header is required so the page does not through a 403
                # permission denied error.
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                                         'Chrome/39.0.2171.95 Safari/537.36'}

                # Alright, lets access the location of where the .zip file we want to download is.
                # In order to "download" it we need to copy it's file contents to a local file on
                # our machine.
                r = requests.get(dict_of_songs[song], stream=True, headers=headers)

                # Here is the local file on our machine that we will copy the .zip file content to.
                song_save_location = join(self.__path_to_custom_levels, song) + '.zip'

                with open(song_save_location, 'wb') as download_file:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, download_file)

            # If we get a 404 or or 403 error, we come here.
            except Exception as e:
                if display_error_message:
                    print(e)


    def download_extract_songs(self, dict_of_songs, display_error_message=True):
        """Download all songs in the given dict and then extract them in the custom_levels
        beatsaber folder.

        Args:
            dict_of_songs dict(str, str): Dict <song_title> -> <song_download_link>

            display_error_message (bool, optional): True if user wants to display possible errors,
                                                    False otherwise. Defaults to True.
        """
        self.download_songs(dict_of_songs, display_error_message=display_error_message)
        self.extract_all_songs_in_custom_levels_folder(display_error_message=display_error_message)
