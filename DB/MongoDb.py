import pymongo

db_path = 'mongodb://u_dev:u_dev@localhost:37017/pm?authSource=dev'


def connect_mongo(dbname):
    connect = pymongo.MongoClient(db_path)
    db = connect[dbname]
    return db, connect


def find_mongo(dbname, collection, ):
    db, connect = connect_mongo(dbname)
    result = db[collection].find({})
    connect.close()
    return result


def insert_mongo(dbname, collection, filed):
    '''
    :param dbname:
    :param collection:
    :param filed:insert data,like [{},{},...]
    :return:
    '''
    db, connect = connect_mongo(dbname)
    result = db[collection].insert_many(filed)
    connect.close()
    return result


def delete_mongo(dbname, collection, filed):
    '''

    :param dbname:
    :param collection:
    :param filed: delete data,like [{},{},...]
    :return:
    '''
    db, connect = connect_mongo(dbname)
    result = db[collection].delete_many(filed)
    connect.close()
    return result


if __name__ == "__main__":
    data = {
        "id": "4000202005GWP097",
        "num": "GWP097",
    }
    filed = []
    for i in range(150000, 150010):
        data["id"] = "400{}5GWP097".format(i)
        data["num"] = "GWP{}".format(i)
        filed.append(data.copy())
    result = insert_mongo("dev", "test", filed)
    print(result)
