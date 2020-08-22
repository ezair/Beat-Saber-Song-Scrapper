"""
@author Eric Zair
@file extract_custom_songs.py
A very simple program that is used to take all beatsaber songs that were
downloaded and extract them into their own folder.
NOTE: This program assumes that you downloaded you beatsaber zipfiles
      directly in the custom_levels folder.
"""

# Extracting beatsaber zipfiles to the correct place.
from bsaber.scrapper import SongScrapper


""" Path to custom level folder. Each user has it saved somewhere different. """
CUSTOM_LEVEL_FOLDER = "D:\Games\Beat.Saber.v1.7.0.ALL.DLC\Beat Saber\Beat Saber_Data\CustomLevels"


def main():
    scrapper = SongScrapper(CUSTOM_LEVEL_FOLDER)
    scrapper.extract_all_songs_in_custom_levels_folder()
    print("All songs have been extracted.")


if __name__ == "__main__":
    main()
