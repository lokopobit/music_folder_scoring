# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 19:09:52 2020

@author: lokopobit
"""

import os
import json

music_folder = r'C:\Users\juan\Downloads\Remember'
songs = os.listdir(music_folder)
save = False

if not os.path.exists('music_folder_dict.json'):
    music_folder_dict = {}
    for song in songs: music_folder_dict[song] = -1
    if save:
        f = open('music_folder_dict.json', 'w')
        json.dump(music_folder_dict, f)
        f.close()
        
else:
    f = open('music_folder_dict.json', 'r')
    music_folder_dict = json.load(f)
    f.close()
    
exit_main = False
for song in songs:
    if song[-3:] == 'jpg':
        print('INFO', 'Images are skipped')
        continue
    
    if (song in music_folder_dict.keys()):
        song_key = song
        if (music_folder_dict[song] != -1):
            print('INFO', song, 'already scored')
            continue
        
    elif (song[2:] in music_folder_dict.keys()):
        song_key = song[2:]
        if (music_folder_dict[song[2:]]!= -1):
            print('INFO', song, 'already scored')
            continue
    
    song_path = os.path.join(music_folder, song)    
    try:
        os.startfile(song_path)
        score = int(input('Provide score for this song: '))
        if score == 0:
            print('Break execution')
            exit_main = True 
        while score not in list(range(1,6))+[0]:
            print('INFO', 'Score must be between 1 and 5. Enter 0 to exit')
            score = int(input('Provide score for this song: '))
            if score == 0:
                print('Break execution')
                exit_main = True                
                
        if exit_main: break
        
        print('Updating', song, 'score')
        music_folder_dict[song_key] = score
        new_song_path = os.path.join(music_folder, str(score)+'_'+song)
        os.rename(song_path, new_song_path)
            
            
    except:
        print('ERROR', song)
        
        
f = open('music_folder_dict.json', 'w')
json.dump(music_folder_dict, f)
f.close()