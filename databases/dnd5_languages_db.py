import json
import os
import sqlite3

CREATE_LANGUAGE_TABLE_REQUEST = '''CREATE TABLE IF NOT EXISTS languages
                              (id integer primary key, name text not null, restricted)'''

DROP_LANGUAGE_TABLE_REQUEST = '''DROP TABLE IF EXISTS languages'''


def insert_dnd5_language():
    languages = get_all_languages_from_json('languages')
    if len(languages) > 0:
        connection = sqlite3.connect('dnd5_db.db')
        connection.executemany("INSERT INTO languages(name, restricted) values (?,?)", languages)
        connection.commit()
        connection.close()
    else:
        print("Languages already in database")


def get_all_languages_from_json(file_name):
    languages = []
    # Considering "json_list.json" is a json file
    directory = os.getcwd() + '/databases/'
    with open(directory + '/data/' + file_name + '.json') as fd:
        json_data = json.load(fd)
        for language in json_data:
            element = (language["name"],
                       language["restricted"]
                       )
            languages.append(element)
    return languages


def get_all_languages():
    languages = []
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT name from languages'''
    cursor.execute(select_request)
    records = cursor.fetchall()
    for i in records:
        languages.append(i[0])
    return languages


def get_all_unrestricted_languages():
    languages = []
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT name from languages WHERE restricted = "" '''
    cursor.execute(select_request)
    records = cursor.fetchall()
    for i in records:
        languages.append(i[0])
    return languages

