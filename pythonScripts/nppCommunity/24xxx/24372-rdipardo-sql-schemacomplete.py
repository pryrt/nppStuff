import sqlite3
from Npp import editor, SCINTILLANOTIFICATION

DB = None

SCHEMA_QUERY = '''
SELECT
    t.name as t_name,
    c.name as c_name
FROM
    sqlite_master AS t
JOIN
    pragma_table_info(t.name) AS c
WHERE
    /* provide a placeholder for user input */
    t.name LIKE ?
ORDER BY
    t.name,
    c.cid
;
'''

def scaffold_db():
    # pass the `check_same_thread` arg to avoid an exception:
    # 'sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread.'
    # https://stackoverflow.com/a/48234567
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE products ([product_id] INTEGER PRIMARY KEY, [product_name] TEXT)')
    cursor.execute('CREATE TABLE prices ([price_id] INTEGER PRIMARY KEY, [price] INTEGER)')
    conn.commit()
    cursor.execute('INSERT INTO products (product_id, product_name) VALUES (1,"Banana"), (2,"Aspargus")')
    cursor.execute('INSERT INTO prices (price_id, price) VALUES (1,10), (2,20)')
    conn.commit()

    return cursor


def create_tree_from_schema(schema):
    tree = {}
    for table, column in schema:
        tree.setdefault(table, []).append(column)
    return tree


def callback_CHARADDED(args):
    if args['ch'] == ord('.'):
        word_end_pos   = editor.getCurrentPos() - 1
        word_start_pos = editor.wordStartPosition(word_end_pos, True)
        current_word   = editor.getRangePointer(word_start_pos, word_end_pos - word_start_pos)

        # bind the input to the prepared statement's LIKE clause;
        # note the trailing comma -- the string will be "exploded" into chars without it
        statement = DB.execute(SCHEMA_QUERY, ('%s%%' % current_word,))
        tree = create_tree_from_schema(statement.fetchall())

        if current_word in tree:
            editor.autoCShow(0, ' '.join(tree[current_word]))

if __name__ == '__main__':
    if DB is None:
        DB = scaffold_db()

    editor.callback(callback_CHARADDED, [SCINTILLANOTIFICATION.CHARADDED])
