# create the test database
import sqlite3
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('CREATE TABLE products ([product_id] INTEGER PRIMARY KEY, [product_name] TEXT)')
cursor.execute('CREATE TABLE prices ([price_id] INTEGER PRIMARY KEY, [price] INTEGER)')
conn.commit()
cursor.execute('INSERT INTO products (product_id, product_name) VALUES (1,"Banana"), (2,"Aspargus")')
cursor.execute('INSERT INTO prices (price_id, price) VALUES (1,10), (2,20)')
conn.commit()


# code for autocomplete, NOTE, there is a reuse of the cursor object
from Npp import editor, SCINTILLANOTIFICATION

schema_query = '''
SELECT
    t.name as t_name,
    c.name as c_name
FROM
    sqlite_master AS t
JOIN
    pragma_table_info(t.name) AS c
ORDER BY
    t.name,
    c.cid
'''

def create_tree_from_schema(schema):
    tree = {}
    for table, column in schema:
        tree.setdefault(table, []).append(column)
    return tree

tree = create_tree_from_schema(cursor.execute(schema_query).fetchall())

def callback_CHARADDED(args):

    if args['ch'] == ord('.'):
        word_end_pos   = editor.getCurrentPos() - 1
        word_start_pos = editor.wordStartPosition(word_end_pos, True)
        current_word   = editor.getRangePointer(word_start_pos, word_end_pos - word_start_pos)

        if current_word in tree:
            editor.autoCShow(0, ' '.join(tree[current_word]))
