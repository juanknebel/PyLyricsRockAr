from py_lyrics_rock_ar import PyLyricsRockAr
import pandas as pd
import tqdm
import time


def scrap_as_dataframes():
    datasets = []
    index = 1
    file_artists_scrapped = "./artists_scrapped.txt"
    artists_scrapped = []

    try:
        with open(file_artists_scrapped, "r") as file_in:
            artists_scrapped = file_in.read().splitlines()
    except FileNotFoundError:
        pass

    # Add a few waits in the loop in order to not take down the page.
    for an_artist in tqdm.tqdm(PyLyricsRockAr.available_artist()):
        # Skip the artist that allready scrapped
        if an_artist in artists_scrapped:
            continue

        artist = PyLyricsRockAr.get_artist(an_artist)
        time.sleep(1)
        albums = PyLyricsRockAr.get_albums(artist)
        time.sleep(1)
        for an_album in albums:
            tracks = PyLyricsRockAr.get_tracks(an_album)

            lyrics = []
            for a_track in tracks:
                lyrics += [PyLyricsRockAr.get_lyrics(a_track)]

            lyrics_df = pd.DataFrame(
                zip(tracks, lyrics), columns=["track_name", "lyric"]
            )
            lyrics_df["release_year"] = an_album.year()
            lyrics_df["album"] = an_album.name()
            lyrics_df["artist"] = artist.name()

            datasets += [lyrics_df]
            time.sleep(1)

        # Save a temporary scrap in case the connection resets
        if index % 10 == 0 and len(datasets) > 0:
            df_temp = pd.concat(datasets)
            df_temp.to_csv(f"./data/lyrics_{index}.csv", index=False, sep=";")
            with open(file_artists_scrapped, "w") as file_out:
                file_out.writelines("\n".join(list(df_temp.artist.unique())))
        time.sleep(10)
        index += 1

    if datasets == []:
        raise ImportWarning("No lyric to add.")

    df = pd.concat(datasets)
    df.to_csv("lyrics.csv", index=False, sep=";")


if __name__ == "__main__":
    # PyLyricsRockAr.get_all_the_artists_links()
    # print(PyLyricsRockAr.available_artist())
    scrap_as_dataframes()