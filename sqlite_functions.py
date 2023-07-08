import sqlite3

conn = sqlite3.connect('helper.db', check_same_thread=False)
in_memory = sqlite3.connect(':memory:', check_same_thread=False)
conn.backup(in_memory)

def get_help_from_db(transcribed_word, fuzzy, flags):
    search_results = {'shortcuts_values': [], 'shortcuts_comments': [], 'shortcuts_tags': []}
    if fuzzy == True:
        transcribed_word = '%'+transcribed_word+'%'
    print(flags)
    if flags[0] == 1:
        search_results['shortcuts_values'] = in_memory.execute(
            'SELECT shortcuts.id, shortcuts.shortcut, shortcuts.comment, voice_aliases.alias FROM shortcuts LEFT JOIN voice_aliases ON shortcuts.alias_id = voice_aliases.id WHERE shortcuts.shortcut LIKE (?)',
            (transcribed_word,)).fetchall()
    if flags[1] == 1:
        search_results['shortcuts_comments'] = in_memory.execute(
            'SELECT shortcuts.id, shortcuts.shortcut, shortcuts.comment, voice_aliases.alias FROM shortcuts LEFT JOIN voice_aliases ON shortcuts.alias_id = voice_aliases.id WHERE shortcuts.comment LIKE (?)',
            (transcribed_word,)).fetchall()
    if flags[2] == 1:
        search_results['shortcuts_tags'] = in_memory.execute(
        'SELECT shortcuts.id, shortcuts.shortcut, shortcuts.comment, voice_aliases.alias FROM shortcuts INNER JOIN voice_aliases ON shortcuts.alias_id = voice_aliases.id WHERE voice_aliases.alias LIKE (?)',
        (transcribed_word,)).fetchall()
    return search_results

def insert_entry(shortcut, alias_flag, voice_alias, comment=''):
    try:
        if shortcut.strip() == '':
            return False, 'Empty shortcut. Please input shortcut'
        if alias_flag:
            new_alias = conn.execute('INSERT INTO voice_aliases (alias) VALUES (?)', (voice_alias,))
            #alias_id = new_alias.lastrowid
            new_shortcut = conn.execute('INSERT INTO shortcuts (shortcut, comment, alias_id) VALUES (?, ?, ?)',
                                        (shortcut, comment, new_alias.lastrowid,))
        else:
            new_shortcut = conn.execute('INSERT INTO shortcuts (shortcut, comment) VALUES (?, ?)', (shortcut, comment,))
        conn.commit()
        conn.backup(in_memory)
        return True, 'Insert successful'
    except Exception as e:
        print(e)
        return False, e

def get_aliases():
    try:
        in_memory.row_factory = lambda cursor, row: row[0]
        aliases = in_memory.execute('SELECT alias FROM voice_aliases').fetchall()
        in_memory.row_factory = None
        return aliases, 'Aliases showed'
    except Exception as e:
        print(e)
        return False, e

def change_alias():
    try:
        return [], 'Alias changed'
    except Exception as e:
        print(e)
        return False, e

def bulk_insert_entry(import_list):
    try:
        length_one   = []
        length_two   = []
        length_three = []
        for row in import_list:
            if len(row) == 2:
                length_two.append(row)
            elif len(row) == 3:
                length_three.append(row)
            elif len(row) == 1:
                length_one.append(row)
        if length_one != []:
            new_shortcut = conn.executemany('INSERT INTO shortcuts (shortcut) VALUES (?)', length_one)
        if length_two != []:
            new_shortcut = conn.executemany('INSERT INTO shortcuts (shortcut, comment) VALUES (?, ?)', length_two)
        if length_three != []:
            for row in length_three:
                new_tag = conn.execute('INSERT INTO voice_aliases (alias) VALUES (?)', (length_three[2],))
                new_shortcut = conn.execute('INSERT INTO shortcuts (shortcut, comment, alias_id) VALUES (?, ?, ?)', (length_three[0], length_three[1], new_tag))
        conn.commit()
        conn.backup(in_memory)
        return True, 'Import successful'
    except Exception as e:
        print(e)
        return False, e

def delete_row(id):
    try:
        deleting_row_result = conn.execute('DELETE FROM shortcuts.shortcut WHERE shortcuts.id = (?)', (id,)).fetchall()
        print(deleting_row_result)
        conn.commit()
        conn.backup(in_memory)
        return True, 'Shortcut removal successful'
    except Exception as e:
        print(e)
        return False, e

def update_row(id, index, value, *e):
    try:
        print(e)
        print('id,index,value')
        print(id)
        print(index)
        print(value)
        if index == 0:
            updating_row_result = conn.execute('UPDATE shortcuts SET shortcut=(?) WHERE id = (?)', (value, id,)).fetchall()
        elif index == 1:
            updating_row_result = conn.execute('UPDATE shortcuts SET comment=(?) WHERE id = (?)', (value, id,)).fetchall()
        elif index == 2:
            updating_row_result = conn.execute('UPDATE shortcuts SET alias_id = (SELECT id FROM voice_aliases WHERE alias = (?)) WHERE id = (?);',
                                               (value, id,)).fetchall()
        else:
            return False, 'wrong column'
        print(updating_row_result)
        conn.commit()
        conn.backup(in_memory)
        return True, 'Update successful'
    except Exception as e:
        print(e)
        return False, e

def delete_alias(alias_value):
    try:
        deleting_alias_result = conn.execute('DELETE FROM voice_aliases WHERE voice_aliases.alias = (?)', (alias_value,)).fetchall()
        print(deleting_alias_result)
        conn.commit()
        conn.backup(in_memory)
        return True, 'Tag removal successful'
    except Exception as e:
        print(e)
        return False, e