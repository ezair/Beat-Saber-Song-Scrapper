"""
@author Eric Zair
@file bsaber_scraper.py

Main program for scraping songs that the user requests off of bsaber.com, downloading them,
adding them to the customlevels folder, and extracing them withthe name of the song as
the foldername.
"""

# For scraping, download, and extracting beatsaber custom songs.
from bsaber.scraper import SongScraper


"""Path to the location where custom levels are stored in your beatsaber game."""
CUSTOM_LEVEL_FOLDER = "D:\Games\Beat.Saber.v1.7.0.ALL.DLC\Beat Saber\Beat Saber_Data\CustomLevels"


def user_wants_to_search_for_specific_song():
    """Return whether the user wants to search for a specific song or not.

    Returns:
        bool: True if user wants to search for a specific song, false otherwise.
    """
    while True:
        try:
            option = int(input("How would you like search for a song?\n"
                                "1. Enter the name of the song I want to find.\n"
                                "2. Search by Hot, New, or Most Difficult.\n\n"
                                "Enter: "))
        except ValueError:
            print("\nSorry, that is not number.\n")
            continue

        options = [True, False]
        if option in range(1, 3):
            return options[option - 1]


def get_sorting_option_from_user():
    """Return the sorting option that the user wants to sort songs by.
    Options: [New, top, Most Difficult]

    Returns:
        str: The sorting option the user will sort songs by.
    """
    while True:
        try:
            sorting_option = int(input("Select the type of song you want to download:\n"
                                       "1. New\n"
                                       "2. Top\n"
                                       "3. Most Difficult\n\n"
                                       "Enter: "))
        except ValueError:
            print("\nSorry, that is not a number.\n")
            continue

        valid_sorting_options = ['new', 'top', 'most-difficult']
        if sorting_option in range(1, 4):
            return valid_sorting_options[sorting_option - 1]
        else:
            print(f"\nSorry, {sorting_option} is not a valid option.")


def get_time_period_option_from_user():
    """Return the time period the user wants to query songs from.
    Options: [24-hours, 7-days, 30-days, all]

    Returns:
        str: Time period that the user wants to query songs from.
    """
    while True:
        try:
            time_period = int(input("What time period would you like these songs to be from?\n"
                                    "1. 24-hours\n"
                                    "2. 7-days\n"
                                    "3. 30-days\n"
                                    "4. all\n\n"
                                    "Enter: "))
        except ValueError:
            print("\nSorry, that is not a number.")
            continue

        valid_time_periods = ['24-hours', '7-days', '30-days', 'all']

        if time_period in range(1, 5):
            return valid_time_periods[time_period - 1]
        else:
            print(f"\nSorry, {time_period} is not a valid option.")


def display_songs_in_scrapped_dict(scrapped_songs_dict):
    """Display the songs that the user can pick from to download.

    Args:
        scrapped_songs_dict dict(str, str): dict containing the songs that a user can download.
    """
    for i in range(1, len(scrapped_songs_dict) + 1):
        print(f"{i}. {list(scrapped_songs_dict.keys())[i - 1]}")


def display_other_options():
    """Print out the options that a user can do that are not just downloading a song.
    """
    print("> - Next Song page.")
    print("< - Previous song page.")
    print("q - to quit")


def get_user_option(scrapped_songs_dict):
    """Return the selected option for the action that the user wants to take in the program.

    Args:
        scrapped_songs_dict (dict[str, str]): Dict <song name> -> <song download link>.

    Returns:
        (str, int): The option that the user wants to take in the program.
    """
    while True:
        display_songs_in_scrapped_dict(scrapped_songs_dict)
        display_other_options()

        user_option = input("\nSelect the song you want to download or "
                            "select another option: ").lower()

        # If the user enters in a digit, that means they are trying to find a song.
        # Need to make sure that the song is valid.
        if user_option.isdigit():
            song_number = int(user_option)

            if song_number < 1 or song_number > len(scrapped_songs_dict):
                print("\nError, please choose a valid number.\n")
            else:
                return user_option

        # User did not enter a digit, so they must be trying to enter a symbol.
        # We want to make sure that they enter a valid symbol.
        elif user_option not in ['q', '<', '>', '?']:
            print("\nError, that is not a valid option. Please choice a valid option.\n")

        else:
            return user_option


def add_new_record_to_dict_of_songs_to_download(scrapped_songs_dict, dict_of_songs,
                                                selected_song_number):
    # Convert the dict of songs that we have to a list of tuples where each entry is
    # (name of the song, the link to download the song).
    #
    # This is really useful because now we can map our selected_song_number that the user choose
    # to the entry in the scrapped_songs_dict.
    list_of_song_names = list(scrapped_songs_dict)
    song_user_wants_to_download = list_of_song_names[selected_song_number - 1]
    dict_of_songs[song_user_wants_to_download] = scrapped_songs_dict[song_user_wants_to_download]


def download_songs_exit_program(scraper, dict_of_songs_to_download):
    """Download songs contained in passed in dict and exit the program.

    Args:
        scraper (Scraper): The Scraper object used to download in the passed in dict.

        dict_of_songs_to_download (dict[str, str]): Dict of song names mapped to the
                                                    download link of the song.
    """
    scraper.download_extract_songs(dict_of_songs_to_download)

    if dict_of_songs_to_download:
        print("The following songs have been downloaded and extracted: ")

        for downloaded_song in dict_of_songs_to_download:
            print(f"\t{downloaded_song}")

        print("\nHave a good day!\n")

    exit(0)


def main():
    # All songs that the user is going to download will go here.
    # At the end of the method these will be downloaded and extracted.
    dict_of_songs_to_download = {}
    scraper = SongScraper(CUSTOM_LEVEL_FOLDER)

    while True:
        if user_wants_to_search_for_specific_song():
            # The user is going to search for a song via the search bar on bsaber.com.
            song_user_wants_to_search_for = input("Enter the song you want to search for: ")
            scraper.get_searched_for_song_results(song=song_user_wants_to_search_for)
        else:
            # The user is going to query for a song by providing a sorting type and a time period.
            sorting_option = get_sorting_option_from_user()

            # If new is given to scrape_songs(), then we do not ask for a time period because
            # scrape_songs() is called with 'all' by default when sorted_by is given.
            time_period = 'all' if sorting_option == 'new' else get_time_period_option_from_user()

            scrapped_songs_dict = scraper.get_song_results(sorted_by=sorting_option,
                                                           time_period=time_period)

        # User decides if they wanna download a song, go to next/previous page of songs, or quit.
        user_option = get_user_option(scrapped_songs_dict)

        if user_option in ['q', 'quit']:
            download_songs_exit_program(scraper, dict_of_songs_to_download)

        # Since the input is a digit, we know that the user wants to download a song,
        # so we can go ahead and add that song to our dict of songs that we will download.
        elif user_option.isdigit():

            add_new_record_to_dict_of_songs_to_download(scrapped_songs_dict=scrapped_songs_dict,
                                                        dict_of_songs=dict_of_songs_to_download,
                                                        selected_song_number=int(user_option))

        print(f"\nCurrent list of downloaded songs: {[song for song in dict_of_songs_to_download]}")


if __name__ == "__main__":
    main()
