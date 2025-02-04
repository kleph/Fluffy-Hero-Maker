import json
import os
import sqlite3

from dnd5_character.DnD5Spell import DnD5Spell
from utils.dice_roller import roll_die

SPELL_DATA_DIR = 'databases/data/spells/'


CREATE_SPELL_TABLE_REQUEST = '''CREATE TABLE IF NOT EXISTS dnd5_spells 
                        (id integer primary key, name text not null, school text, saving_throw text,
                         casting_time text, ritual text, range text, components text, duration text,
                         level integer, description text, need_concentration text, upgrade text, classes text
                         )'''

# 1: name
# 2: school
# 3: saving_throw,
# 4: casting_time
# 5: ritual
# 6: range
# 7: components
# 8: duration
# 9: level
# 10: description
# 11: need_concentration
# 12: upgrade
# 13: classes
INSERT_SPELLS_INTO_REQUEST = '''INSERT INTO dnd5_spells
                            (name, school, saving_throw, casting_time, ritual, range, components, duration, level, 
                            description, need_concentration, upgrade, classes) values (?,?,?,?,?,?,?,?,?,?,?,?,?)'''


DROP_SPELL_TABLE_REQUEST = '''DROP TABLE IF EXISTS dnd5_spells'''


def get_number_of_spells_in_db():
    """Returns an integer of the number of spells in the database"""
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()

    select_request = '''SELECT count() from dnd5_spells'''
    cursor.execute(select_request)
    number_of_rows = cursor.fetchone()[0]
    connection.close()
    return number_of_rows


def insert_dnd5_spell_data():
    if get_number_of_spells_in_db() == 0:
        spells = get_all_spells_from_json()
        if len(spells) > 0:
            connection = sqlite3.connect('dnd5_db.db')
            connection.executemany(INSERT_SPELLS_INTO_REQUEST, spells)
            connection.commit()
            connection.close()
    else:
        print("Spells already in database")


def get_all_spells_from_json():
    spells = []
    for file in os.listdir(SPELL_DATA_DIR):
        file_path = SPELL_DATA_DIR + file
        if file_path.endswith(".json"):
            with open(file_path) as fd:
                json_data = json.load(fd)
                for spell in json_data:
                    element = (spell["name"],
                               spell["school"],
                               spell["saving throw"],
                               spell["casting time"],
                               spell["ritual"],
                               spell["range"],
                               spell["components"],
                               spell["duration"],
                               spell["level"],
                               spell["description"],
                               spell["concentration"],
                               spell["upgrade"],
                               ",".join(spell["classes"])
                               )
                    spells.append(element)
    return spells


def get_all_spell_names_from_db():
    names = []
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT name from dnd5_spells'''
    cursor.execute(select_request)
    records = cursor.fetchall()
    for i in records:
        names.append(i[0])
    connection.close()
    return names


def get_all_spell_names_of_level(level):
    names = []
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT name from dnd5_spells where level = (?)'''
    cursor.execute(select_request, (level,))
    records = cursor.fetchall()
    for i in records:
        names.append(i[0])
    connection.close()
    return names


def get_all_spells_of_class(spell_class):
    names = []
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT name FROM dnd5_spells WHERE instr(classes, (?))'''
    cursor.execute(select_request, (spell_class,))
    records = cursor.fetchall()
    for i in records:
        names.append(i[0])
    connection.close()
    return names


def get_all_spells_of_class_and_level(spell_class, level):
    names = []
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT name FROM dnd5_spells WHERE instr(classes, (?)) AND level = (?)'''
    cursor.execute(select_request, (spell_class, level))
    records = cursor.fetchall()
    for i in records:
        names.append(i[0])
    connection.close()
    return names


def get_random_spell():
    number = get_number_of_spells_in_db()
    roll = roll_die(number - 1)
    spell = get_spell_by_id(roll)
    return spell


def get_spell_by_id(spell_id):
    if spell_id > 0:
        connection = sqlite3.connect('dnd5_db.db')
        cursor = connection.cursor()
        select_request = '''SELECT * from dnd5_spells WHERE id = (?) '''
        cursor.execute(select_request, (spell_id,))
        record = cursor.fetchone()
        spell = change_record_into_spell(record)
        connection.close()
        return spell
    return None


def get_spells_of_school(school_choice):
    names = []
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT name from dnd5_spells where school = (?)'''
    cursor.execute(select_request, (school_choice,))
    records = cursor.fetchall()
    for i in records:
        names.append(i[0])
    connection.close()
    return names


def get_all_schools():
    """Returns a list of the schools of magic as strings from the database"""
    schools = []
    connection = sqlite3.connect('dnd5_db.db')
    cursor = connection.cursor()
    select_request = '''SELECT DISTINCT school from dnd5_spells'''
    cursor.execute(select_request)
    records = cursor.fetchall()
    for i in records:
        schools.append(i[0])
    connection.close()
    return schools


def look_for_spell_by_name(name):
    """
    Returns a spell from his name
    :parameter name: a string representing the name of the spell
    :return DnD5Spell object with the data of the spell
    """
    spell = DnD5Spell("test")
    if name != "":
        connection = sqlite3.connect('dnd5_db.db')
        cursor = connection.cursor()
        select_request = '''SELECT * from dnd5_spells WHERE name = (?) '''
        cursor.execute(select_request, (name,))
        record = cursor.fetchone()
        spell = change_record_into_spell(record)
        connection.close()
        return spell
    return None


def change_record_into_spell(record):
    """"
    Turns a record into a spell object
    :parameter record: the database record as a tuple representing a spell
    :return DnD5Spell object with the proper data
    """
    spell = DnD5Spell("temp")
    if record is not None:
        spell.name = record[1]
        spell.school = record[2]
        spell.saving_throw = record[3]
        spell.casting_time = record[4]
        spell.ritual = record[5]
        spell.range = record[6]
        spell.components = record[7]
        spell.duration = record[8]
        spell.level = record[9]
        spell.description = record[10]
        spell.concentration = record[11]
        spell.upgrade = record[12]
        spell.classes = record[13].split(',')
        return spell
    return None
