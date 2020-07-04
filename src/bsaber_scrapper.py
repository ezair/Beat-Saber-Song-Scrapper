from bsaber.scrapper import SongScrapper


CUSTOM_LEVEL_FOLDER = "D:\Games\Beat.Saber.v1.7.0.ALL.DLC\Beat Saber\Beat Saber_Data\CustomLevels"


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

        if sorting_option == 1:
            return "new"
        elif sorting_option == 2:
            return "top"
        elif sorting_option == 3:
            return "most-difficult"
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

        if time_period == 1:
            return "24-hours"
        elif time_period == 2:
            return "7-days"
        elif time_period == 3:
            return "30-days"
        elif time_period == 4:
            return "all"
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
    dict_of_songs[song_user_wants_to_download] = \
        scrapped_songs_dict[song_user_wants_to_download]


def main():
    # All songs that the user is going to download will go here.
    # At the end of the method these will be downloaded and extracted.
    dict_of_songs_to_download = {}

    while True:
        # Locals might need to move up a row. TBA.
        sorting_option = get_sorting_option_from_user()

        # If new is given to scrape_songs(), then we do not ask for a time period because
        # scrape_songs() is called with 'all' by default when sorted_by is given.
        time_period = 'all' if sorting_option == 'new' else get_time_period_option_from_user()

        scrapper = SongScrapper(CUSTOM_LEVEL_FOLDER)
        scrapped_songs_dict = scrapper.scrape_songs(sorted_by=sorting_option, time_period=time_period)

        # User decides if they wanna download a song, go to next/previous page of songs, or quit.
        user_option = get_user_option(scrapped_songs_dict)

        # Download the songs, exit the program.
        if user_option == 'q' or user_option == 'quit':
            scrapper.download_extract_songs(dict_of_songs_to_download)

            if dict_of_songs_to_download:
                print("The following songs have been downloaded and extracted: ")

                for downloaded_song in dict_of_songs_to_download:
                    print(f"\t{downloaded_song}")
                print("\nHave a good day!\n")

            exit(0)

        # Since the input is a digit, we know that the user wants to download a song,
        # so we can go ahead and add that song to our dict of songs that we will download.
        elif user_option.isdigit():
            add_new_record_to_dict_of_songs_to_download(scrapped_songs_dict=scrapped_songs_dict,
                                                        dict_of_songs=dict_of_songs_to_download,
                                                        selected_song_number=int(user_option))

        print(f"\nCurrent list of downloaded songs: {[song for song in dict_of_songs_to_download]}")


if __name__ == "__main__":
    main()
