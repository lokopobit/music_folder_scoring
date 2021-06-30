# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 19:09:52 2020

@author: lokopobit
"""

import os
import json
import time
from shutil import copyfile

def match_songs_folder_and_old_json_format(songs, music_folder_dict_name):
    '''
    

    Parameters
    ----------
    songs : TYPE
        DESCRIPTION.
    music_folder_dict_name : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    f = open(music_folder_dict_name, 'r')
    music_folder_dict = json.load(f)
    f.close()

    for score in range(1,6):
        songs_folder_score = []
        for song in songs:
            if song[:2] == str(score)+'_':
                songs_folder_score.append(song)       
        songs_folder_score = set(songs_folder_score)
        
        songs_dict_score = []
        for song, song_score in music_folder_dict.items():
            if song_score == score:
                songs_dict_score.append(str(score)+'_'+song)
        songs_dict_score = set(songs_dict_score)
        
        songs_diff = songs_folder_score-songs_dict_score
        for song in songs_diff:
            music_folder_dict[song[2:]] = score
            
    f = open(music_folder_dict_name, 'w')
    json.dump(music_folder_dict, f)
    f.close()
        
    

def transform_json_to_new_format(music_folder_dict_name):
    '''

    Parameters
    ----------
    music_folder_dict_name : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    f = open(music_folder_dict_name, 'r')
    music_folder_dict = json.load(f)
    f.close()
    
    new_music_folder_dict = {}
    new_music_folder_dict['NonScored'] = []
    for score in range(1,6):
        score_key = 'Score_'+str(score)
        new_music_folder_dict[score_key] = []
        
    for song_name, score in music_folder_dict.items():
        if score in range(1,6):
            score_key = 'Score_'+str(score)
            new_music_folder_dict[score_key].append(str(score)+'_'+song_name)
        else:
            score_key = 'NonScored'
            new_music_folder_dict[score_key].append(song_name)
            
    f = open(music_folder_dict_name, 'w')
    json.dump(new_music_folder_dict, f)
    f.close()

def create_json_if_does_not_exist_else_loaded_it(music_folder_dict_name, songs, save=False):
    '''
    

    Parameters
    ----------
    music_folder_dict_name : TYPE
        DESCRIPTION.
    songs : TYPE
        DESCRIPTION.
    save : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    None.

    '''
    
    if not os.path.exists(music_folder_dict_name):
        music_folder_dict = {}
        music_folder_dict['NonScored'] = []
        for score in range(1,6):
            score_key = 'Score_'+str(score)
            music_folder_dict[score_key] = []
        for song in songs: music_folder_dict['NonScored'].append(song)
        if save:
            f = open(music_folder_dict_name, 'w')
            json.dump(music_folder_dict, f)
            f.close()
            
    else:
        f = open(music_folder_dict_name, 'r')
        music_folder_dict = json.load(f)
        f.close()
        
    return music_folder_dict
 
def score_songs(music_folder, music_folder_dict, music_folder_dict_name):
    '''
    

    Returns
    -------
    None.

    '''
    
    def get_score_input():
        score = 0.0
        while type(score) != type(5):
            try:                    
                score = int(input('Provide score for this song: '))
            except:
                print('Score must be integer')
        return score
        
        
    NonScoredSongs = music_folder_dict['NonScored']
    exit_main = False
    for song_name in NonScoredSongs:
        if song_name[-3:] == 'jpg':
            print('INFO', 'Images are skipped')
            continue
        
        song_path = os.path.join(music_folder, song_name)    
        try:
            os.startfile(song_path)
            
            score = get_score_input()
            
            if score == 0:
                print('Break execution')
                exit_main = True 
            while score not in list(range(1,6))+[0]:
                print('INFO', 'Score must be between 1 and 5. Enter 0 to exit')
                score = get_score_input()
                if score == 0:
                    print('Break execution')
                    exit_main = True                
                    
            if exit_main: break
            
            print('Updating', song_name, 'score')
            score_key = 'Score_'+str(score)
            music_folder_dict[score_key].append(str(score)+'_'+song_name)
            music_folder_dict['NonScored'].remove(song_name)
            new_song_path = os.path.join(music_folder, str(score)+'_'+song_name)
            os.rename(song_path, new_song_path)
                
                
        except:
            print('ERROR', song_name)
            
            
    f = open(music_folder_dict_name, 'w')
    json.dump(music_folder_dict, f)
    f.close()
            

def check_if_songs_folder_matching_new_json_format(songs, music_folder_dict_name):
    '''
    

    Parameters
    ----------
    songs : TYPE
        DESCRIPTION.
    music_folder_dict_name : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    f = open(music_folder_dict_name, 'r')
    music_folder_dict = json.load(f)
    f.close()

    diff_list = []
    for score in range(1,6):
        songs_folder_score = []
        for song in songs:
            if song[:2] == str(score)+'_':
                songs_folder_score.append(song)       
        songs_folder_score = set(songs_folder_score)
        
        songs_dict_score = music_folder_dict['Score_'+str(score)]
        songs_dict_score = set(songs_dict_score)
        
        songs_diff = songs_folder_score-songs_dict_score
        diff_list.append(songs_diff == set())
        
    return all(diff_list)


def copy_best_songs(music_folder, score=5):
    '''
    

    Parameters
    ----------
    music_folder : TYPE
        DESCRIPTION.
    best_songs_folder : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    best_songs_folder = music_folder+'_score_'+str(score)
    if not os.path.exists(best_songs_folder):
        os.mkdir(best_songs_folder)
    all_best_song = os.listdir(best_songs_folder)
    music_folder_dict_name = music_folder.split("\\")[-1] +'_'+ "music_folder_dict.json"
    f = open(music_folder_dict_name, 'r')
    music_folder_dict = json.load(f)
    f.close()
    
    for song_name in music_folder_dict['Score_'+str(score)]:
        if song_name not in all_best_song:
            source_song_path = os.path.join(music_folder, song_name)
            destination_song_path = os.path.join(best_songs_folder, song_name)
            copyfile(source_song_path, destination_song_path)
    

def main(music_folder):
    songs = os.listdir(music_folder)    
    music_folder_dict_name = music_folder.split("\\")[-1] +'_'+ "music_folder_dict.json"
    
    # match_songs_folder_and_old_json_format(songs, music_folder_dict_name)
    # transform_json_to_new_format(music_folder_dict_name)
    music_folder_dict=create_json_if_does_not_exist_else_loaded_it(music_folder_dict_name, songs, save=False)    
    score_songs(music_folder, music_folder_dict, music_folder_dict_name)
    is_check_correct = check_if_songs_folder_matching_new_json_format(songs, music_folder_dict_name)
    if is_check_correct:
        copy_best_songs(music_folder)
        print('INFO: Bests songs copied')
    else:
        print('ERROR: songs folder NOT matching new json format')
    time.sleep(10)
    

# music_folder = r'C:\Users\juan\Downloads\all_remember'
music_folder = r'C:\Users\juan\Downloads\all_regaeton'
main(music_folder)
