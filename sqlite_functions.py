import sqlite3

conn = sqlite3.connect('helper.db', check_same_thread=False)
in_memory = sqlite3.connect(':memory:', check_same_thread=False)
conn.backup(in_memory)

def get_help_from_db(transcribed_word, fuzzy, flags):
    search_results = {'shortcuts_values':[],'shortcuts_comments':[],'shortcuts_aliases':[]}
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
        search_results['shortcuts_aliases'] = in_memory.execute(
        'SELECT shortcuts.id, shortcuts.shortcut, shortcuts.comment, voice_aliases.alias FROM shortcuts INNER JOIN voice_aliases ON shortcuts.alias_id = voice_aliases.id WHERE voice_aliases.alias LIKE (?)',
        (transcribed_word,)).fetchall()
    return search_results

def insert_entry(shortcut, alias_flag, voice_alias, comment=''):
    try:
        #print(shortcut)
        #print(alias_flag)
        #print(voice_alias)
        #print(comment)
        if shortcut.strip() == '':
            #print("what")
            return False
        if alias_flag:
            new_alias = conn.execute('INSERT INTO voice_aliases (alias) VALUES (?)', (voice_alias,))
            #print("new_alias")
            #print(new_alias)
            alias_id = new_alias.lastrowid
            #print("alias_id")
            #print(alias_id)
            new_shortcut = conn.execute('INSERT INTO shortcuts (shortcut, comment, alias_id) VALUES (?, ?, ?)',
                                        (shortcut, comment, alias_id,))
        else:
            new_shortcut = conn.execute('INSERT INTO shortcuts (shortcut, comment) VALUES (?, ?)', (shortcut, comment,))
        #print("new_shortcut")
        #print(new_shortcut)
        conn.commit()
        conn.backup(in_memory)
        return True
    except Exception as e:
        print(e)
        print('Insert failed')
        return False

def delete_row(id):
    try:
        deleting = conn.execute("DELETE FROM shortcuts WHERE shortcuts.id = (?)", (id,)).fetchall()
        conn.commit()
        conn.backup(in_memory)
        return True
    except Exception as e:
        print(e)
        print('Deleting row failed')
        return False

def delete_alias(alias_value):
    try:
        deleting = conn.execute("DELETE FROM voice_aliases WHERE voice_aliases.alias = (?)", (alias_value,)).fetchall()
        conn.commit()
        conn.backup(in_memory)
        return True
    except Exception as e:
        print(e)
        print('Deleting alias failed')
        return False