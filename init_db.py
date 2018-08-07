import json
import sys

import sqlalchemy
from postgresql.python import os
from sqlalchemy import Column, Integer, Text

POSTGRES = {
    'user': 'lexor',
    'pw': '',
    'db': 'it_place_db',
    'host': 'localhost',
    'port': '5432',
}
connection_string = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db = sqlalchemy.create_engine(connection_string)
engine = db.connect()
j_table = sqlalchemy.table(
        "table_menu", Column('id', Integer),
        Column('name', Text),
        Column('alt', Text),
        Column('image', Text),
        Column('ingredients', Text),
        Column('price', Integer))


def get_json(file_name):
    try:
        data = json.load((open(os.path.abspath(os.curdir) + file_name)))
    except FileExistsError as err:
        print(err.__str__())
        exit(0)
    for x in data:
        statement = j_table.insert().values(
            id=x['id'],
            name=x['name'],
            alt=x['alt'],
            image=x['image'],
            ingredients=x['ingredients'],
            price=x['price']
        )
        engine.execute(statement)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        get_json(sys.argv[1])
    else:
        get_json('static/menu.json')