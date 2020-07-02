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
            print("\nSorry, that is not a number.")
            continue

        if sorting_option == 1:
            return "new"
        elif sorting_option == 2:
            return "top"
        elif sorting_option == 3:
            return "most difficult"
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
    for i in range(1, len(scrapped_songs_dict) + 1):
        print(f"{i}. {list(scrapped_songs_dict.keys())[i - 1]}")


def get_song_number(scrapped_songs_dict):
    while True:
        display_songs_in_scrapped_dict(scrapped_songs_dict)

        try:
            song_number = int(input("\nSelect the song you want to download: "))
        except ValueError:
            print("\nSorry, that is not a number! Please enter a number.")
            continue

        if song_number < 1 or song_number > len(scrapped_songs_dict):
            print("\nError, please choose a valid number.")
        else:
            return song_number


# TODO
def add_new_record_to_dict_of_songs_to_download(scrapped_songs_dict, dict_of_songs_to_download,
                                                selected_song_number):
    # Convert the dict of songs that we have to a list of tuples where each entry is
    # (name of the song, the link to download the song).
    #
    # This is really useful because now we can map our selected_song_number that the user choose
    # to the entry in the scrapped_songs_dict.
    dict_of_songs_as_tuple = [(song_name, download_link)
                              for song_name, download_link in scrapped_songs_dict.items()]

    dict_of_songs_to_download[dict_of_songs_as_tuple[selected_song_number] = \
        dict_of_songs_as_tuple[selected_song_number[1]]


def main():
    dict_of_songs_to_download = {}
    while True:
        # Locals might need to move up a row. TBA.
        sorting_option = get_sorting_option_from_user()

        # If new is given to scrape_songs(), then we do not ask for a time period because
        # scrape_songs() is called with 'all' by default when sorted_by is given.
        time_period = 'all' if sorting_option == 'new' else get_time_period_option_from_user()

        scrapper = SongScrapper(CUSTOM_LEVEL_FOLDER)
        scrapped_songs_dict = scrapper.scrape_songs(sorted_by=sorting_option, time_period=time_period)

        # User choose which single song to download.
        selected_song_number = get_song_number(scrapped_songs_dict)

        # Add the song that the user wants to the dict of songs that we will download.
        # These songs will later be downloaded.
        add_new_record_to_dict_of_songs_to_download(scrapped_songs_dict, selected_song_number,
                                                    selected_song_number)

        print(dict_of_songs_to_download)


if __name__ == "__main__":
    main()
