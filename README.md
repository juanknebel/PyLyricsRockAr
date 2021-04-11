## PyLyricsJK: A Pythonic Implementation of https://rock.com.ar/

Originally based on the implementation of PyLyrics

## Dependencies to be installed
* beautifulsoup4
* requests
* tqdm (optional only if you use the example scrap.py)
* pandas (optional only if you use the example scrap.py)
* setuptools (if you are going to install in your virtualenv)

## Install (using pip)
1. First build the package
    ```bash
    python setup.py sdist
    ```
2. Install with pip
    ```bash
    pip install dist/PyLyricsRockAr-0.0.1.tar.gz
    ```

## How to use
1. Import in you python project
    ```python
    from py_lyrics_rock_ar import PyLyricsRockAr
    ```
2. Use it to retrieve all the artitst in the site. 
It will be generate a json file (available_artists.json) in your project file 
with all the artists and theirs id to be used to get the almbums, tracks and
lyrics.
    ```python
    PyLyricsRockAr.get_all_the_artists_links()
    ```
3. How to get a lyric.
    ```python
        artist_id = id_from_the_json_file()
        artist = PyLyricsRockAr.get_artist(artist_id)

        albums = PyLyricsRockAr.get_albums(artist)
        one_album = search_from_specific_album_criteria(albums)
        
        tracks = PyLyricsRockAr.get_tracks(one_album)
        one_track = search_from_specific_track_criteria(tracks)
        lyrics = PyLyricsRockAr.get_lyrics(one_track)
    ```

## Contact
For any request and comment please contact me: juanknebel (at) gmail.com.

## Disclaimer
This script is used for educational purposes only to obtain as large a database as possible of national rock lyrics. The use of these lyrics will be to build and NLP final work to get my Specialist Data Science Degree.
