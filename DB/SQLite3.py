import sqlite3

db_path = ''


def dict_factory(cursor, row):
    '''
    返回字典类型数据
    :param cursor:
    :param row:
    :return:
    '''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect_db():
    connect = sqlite3.connect(db_path)
    #设置返回数据类型为字典类型
    connect.row_factory = dict_factory
    cursor = connect.cursor()
    return connect, cursor


def update_by_sql(connect, cursor, sql):
    try:
        cursor.execute(sql)
        cursor.close()
        connect.commit()
        return True
    except Exception as e:
        return e


def get_data_by_sql(cursor, sql):
    cursor.execute(sql)
    cursor.close()
    data = cursor.fetchall()
    return data
