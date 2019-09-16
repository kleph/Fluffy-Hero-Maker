import json
import os
import sqlite3

from dnd5_character.DnD5Class import DnD5Class
from utils.utilities import list_to_str

CLASS_DATA_DIR = 'databases/data/classes/'

CREATE_CLASS_TABLE_REQUEST = '''CREATE TABLE IF NOT EXISTS dnd5_classes 
                                (id integer primary key, name text not null, hit_dice, weapon_proficiencies_to_add 
                                skill_proficiency_choices_number, skill_proficiency_choices_list, class_features, 
                                class_feature_choices_names, class_feature_choices_lists, class_feature_choices_number,
                                armor_proficiencies)'''

INSERT_CLASS_INTO_REQUEST = '''INSERT INTO dnd5_classes(name, hit_dice, weapon_proficiencies_to_add, 
                                class_features, armor_proficiencies) 
                                values (?,?,?,?,?)'''

DROP_CLASS_TABLE_REQUEST = '''DROP TABLE IF EXISTS dnd5_classes'''


def insert_dnd5_classes():
    classes = get_all_classes_from_json()
    if len(classes) > 0:
        connection = sqlite3.connect('dnd5_db.db')
        connection.executemany(INSERT_CLASS_INTO_REQUEST, classes)
        connection.commit()
        connection.close()


def get_all_classes_from_json():
    classes = []
    for file in os.listdir(CLASS_DATA_DIR):
        file_path = CLASS_DATA_DIR + file
        if file_path.endswith(".json"):
            with open(file_path) as fd:
                json_data = json.load(fd)
                for dnd_class in json_data:
                    element = (dnd_class["name"],
                               dnd_class["hit_dice"],
                               list_to_str(dnd_class["weapon_proficiencies_to_add"]),
                               list_to_str(dnd_class["class_features"]),
                               list_to_str(dnd_class["armor_proficiencies_to_add"])
                               )
                    classes.append(element)
    return classes


def look_for_class_by_name(name):
    if name != "":
        connection = sqlite3.connect('dnd5_db.db')
        cursor = connection.cursor()
        select_request = '''SELECT * from dnd5_classes WHERE name = (?) '''
        cursor.execute(select_request, (name,))
        record = cursor.fetchone()
        dnd_class = change_record_into_class(record)
        connection.close()
        return dnd_class
    return None



def get_all_classes_names():
    names = []
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT name from dnd5_classes'''
    cursor.execute(select_request)
    records = cursor.fetchall()
    for i in records:
        names.append(i[0])
    return names


def change_record_into_class(record):
    if record is not None:
        dnd_class = DnD5Class("temp")
        dnd_class.name = record[1]
        dnd_class.hit_dice = record[2]
        dnd_class.weapon_proficiencies_to_add = record[3].split(', ')
        dnd_class.class_features = record[5].split(', ')
        dnd_class.armor_proficiencies_to_add = record[9].split(', ')
        return dnd_class
    return None

