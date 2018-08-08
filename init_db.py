import json
import sys

import sqlalchemy
import os
from sqlalchemy import Column, Integer, Text, MetaData, Table
from sqlalchemy_utils import database_exists, create_database

POSTGRES = {
    'user': 'lexxor',
    'pw': 'lexorsdatabase',
    'db': 'lexxor$it_place_db',
    'host': 'lexxor.mysql.pythonanywhere-services.com',
    'port': '3306',
}
connection_string = 'mysql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s?charset=utf8' % POSTGRES
db = sqlalchemy.create_engine(connection_string)
if not database_exists(db.url):
    create_database(db.url)
    engine = db.connect()
    metadata = MetaData()
    table_menu = Table('table_menu', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', Text),
                    Column('alt', Text),
                    Column('image', Text),
                    Column('ingredients', Text),
                    Column('price', Integer))
    table_orders = Table('table_order', metadata,
                       Column('id', Integer, primary_key=True, autoincrement=True),
                       Column('items', Text),
                       Column('name', Text),
                       Column('address', Text),
                       Column('state', Text),
                       Column('time', Text))
    metadata.create_all(engine)
else:
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
        get_json('/static/menu.json')
