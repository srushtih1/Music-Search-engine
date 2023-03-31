#api token for genius.com website
GENIUS_API_TOKEN='ZQEoc3jPsYWwnW-Aqa1_5GsaVKyre20WzVIVTFACQzp08gDUcSVSzzA78do7h7f5'

import collections.abc
from collections.abc import Mapping
collections.Callable = collections.abc.Callable

# Make HTTP requests
import requests
# Scrape data from an HTML document
from bs4 import BeautifulSoup
# I/O
import os
# Search and manipulate strings
import re
#to store the scraped data in json format
import json

#an array for storing the scraped object
a = []

# Get artist object from Genius API
def request_artist_info(artist_name, page):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
    search_url = base_url + '/search?per_page=10&page=' + str(page)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    #print("response: " + response.text)
    #json_data = response.json()
    # if len(json_data['response']['hits']) == 0:
    #     print(f"Error: Could not get artist info for {artist_name}")
    #     return None
    return response

# Get Genius.com song url's from artist object
def request_song_url(artist_name, song_cap):
    page = 1
    songs = []
    
    while True:
        response = request_artist_info(artist_name, page)
        json = response.json()
        # Collect up to song_cap song objects from artist
        song_info = []
        for hit in json['response']['hits']:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                song_info.append(hit)
    
        # Collect song URL's from song objects
        for song in song_info:
            if (len(songs) < song_cap):
                url = song['result']['url']
                songs.append(url)
                print(url)
            
        if (len(songs) == song_cap):
            break
        else:
            page += 1
        
    print('Found {} songs by {}'.format(len(songs), artist_name))   
    return songs
    
# Scrape lyrics from a Genius.com song URL
def scrape_song_lyrics(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='Lyrics__Container-sc-1ynbvzw-6 YYrds').get_text()
    title = html.find('title').text.strip().replace(' Lyrics | Genius Lyrics', '')
    artist = artist_name
    
    #remove identifiers like chorus, verse, etc
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    #remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
    
    if (not(lyrics is None)):

        obj = {
            'artist' : artist,
            'title' : title,
            'lyrics' : lyrics,
            'url' : url
        }
        a.append(obj)
        closed(a)
   
    print(a)
    return [[lyrics]]   
    

#to store the scraped data into a json file    
def closed(new_data,filename = 'scraped_songs_2.json'):
    with open (filename,'w',encoding="utf8") as outfile:
        json.dump(new_data,outfile, indent=4 ,ensure_ascii=False) 
    

def write_lyrics_to_file(artist_name, song_count):
    response = request_artist_info(artist_name, 1)
    if response is None:
        print(f"Skipping lyrics for {artist_name}")
        return
    urls = request_song_url(artist_name, song_count)
    #print("okay")
    for url in urls:       
        lyrics = scrape_song_lyrics(url)
    
    #print('Wrote {} lines to file from {} songs'.format(num_lines, song_count)) 

# Read in artist names from file
with open('artists.txt') as f:
    artist_names = [line.strip() for line in f.readlines()]

# Loop through artist names and scrape lyrics
for artist_name in artist_names:
    print(f"Scraping lyrics for {artist_name}")
    write_lyrics_to_file(artist_name, 100)
