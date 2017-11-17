# Python import
import pymysql.cursors

g_host = 'localhost'
g_user = 'samueldrouin'
g_password = 'XqB4ao9yj2c9NPsKaWz2qTR1C9hLtU4e'
g_db = 'CF-Richelieu'
g_charset = 'utf8'


def execute_query_return_all(sql):
    """
    Execute any query and pass all fetched items in the return
    :param sql: Query string
    :return: Category or subcategory dictionary
    """
    results = ""
    connection = pymysql.connect(host=g_host,
                                 user=g_user,
                                 password=g_password,
                                 db=g_db,
                                 charset=g_charset,
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
    finally:
        connection.close()
        return results

def create_place(name, road, city):
    """
    Create a new place in database
    :param name: Place name
    :param road: Road in address
    :param city: City in address
    :return: True is successful
    """
    connection = pymysql.connect(host=g_host,
                                 user=g_user,
                                 password=g_password,
                                 db=g_db,
                                 charset=g_charset,
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO places (name, road, city) VALUES ('%s','%s','%s')" %(name, road, city)
            cursor.execute(sql)
            connection.commit()

    except pymysql.Error as e:
        connection.rollback()
        print(e)
        return e
    finally:
        connection.close()
