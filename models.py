import sqlalchemy
from sqlalchemy import Column

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
engine = db.connect()


class Table:
    """
    Класс-wrapper для описания сущности таблицы в БД.
    Создан исключительно ради экономии кода
    """
    def __init__(self, table_name, db_engine):
        """
        Функция инициализации
        :param table_name: название таблицы
        :param db_engine: объект управления БД
        """
        self.__name = table_name
        self.__engine = db_engine
        self.__table = sqlalchemy.table(name=table_name)

    def add_columns(self, *columns):
        """
        Функция добавления колонок в таблицу БД
        :param columns: список кортежей имя колонки - тип
        """
        for column in columns:
            col = Column(column[0], column[1])
            self.__table.append_column(col)

    def do_select(self):
        """
        Функция осуществляет выборку из БД
        :return:
        """
        query = self.__table.select()
        return self.__engine.execute(query)

    def do_insert(self, **kwargs):
        """
        Функция осуществляет вставку новой строки в таблиу БД
        :param kwargs: словарь имя колонки - значение
        """
        i = self.__table.insert().values(kwargs)
        self.__engine.execute(i)

    def do_delete(self, row_id):
        """
        Функция удаления строки из БД
        :param row_id: номер строки
        """
        obj = self.__table.delete().where(self.__table.c.id == row_id)
        self.__engine.execute(obj)
