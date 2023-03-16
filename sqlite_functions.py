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

def insert_rule_db(shortcut, alias_flag, voice_alias, comment=''):
    try:
        if shortcut.strip() == '' and comment.strip() == '':
            return False
        if alias_flag:
            new_alias = conn.execute('INSERT INTO voice_aliases (alias) VALUES (?)', (voice_alias,))
            alias_id = new_alias.lastrowid
            print(alias_id)
            new_shortcut = conn.execute('INSERT INTO shortcuts (shortcut, comment, alias_id) VALUES (?, ?, ?)',
                                        (shortcut, comment, alias_id,))
        else:
            new_shortcut = conn.execute('INSERT INTO shortcuts (shortcut, comment) VALUES (?, ?)', (shortcut, comment,))
        conn.commit()
        conn.backup(in_memory)
        return True
    except Exception as e:
        print(e)
        print('Insert failed')
        return False
