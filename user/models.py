import MySQLdb

# Create your models here.
from mysite.settings import DATABASES


def connect():
    try:
        conn = MySQLdb.connect(host=DATABASES['default']['HOST'],
                               port=int(DATABASES['default']['PORT']),
                               user=DATABASES['default']['USER'],
                               password=DATABASES['default']['PASSWORD'],
                               db=DATABASES['default']['NAME'],
                               charset='utf8')
        return conn

    except MySQLdb.Error as e:
        print("Error {0}: {1}".format(e.args[0], e.args[1]))
        return None


def get(email, password):
    try:
        conn = connect()

        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        sql = """
                select no, name from user
                    where email = "%s" and password = "%s"
            """ % (email, password)

        cursor.execute(sql)

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row

    except MySQLdb.Error as e:
        print("Error {0}: {1}".format(e.args[0], e.args[1]))
        return None


def insert(user):
    try:
        conn = connect()
        cursor = conn.cursor()

        sql = """ insert into user
                    values (null, '%s', '%s',
                '%s', '%s', now())
            """ % user

        count = cursor.execute(sql)

        cursor.close()
        conn.commit()
        conn.close()

        return count == 1

    except MySQLdb.Error as e:
        print("Error {0}: {1}".format(e.args[0], e.args[1]))
        return None
