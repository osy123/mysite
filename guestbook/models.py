import MySQLdb
from django.db import models
from mysite.settings import DATABASES

# Create your models here.
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

def insert(guestbook):
    try:
        conn = connect()
        cursor = conn.cursor()

        sql = """ insert
                    into guestbook
                 values (null, '%s', '%s', '%s', now())
            """ % guestbook

        count = cursor.execute(sql)

        cursor.close()
        conn.commit()
        conn.close()

        return count == 1

    except MySQLdb.Error as e:
        print("Error {0}: {1}".format(e.args[0], e.args[1]))
        return None


def fetchall():
    try:
        conn = connect()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        sql = """ select no, name, message,
                    date_format(reg_date, '%Y-%m-%d %H:%i:%s') as reg_date
                    from guestbook
                    order by reg_date desc """

        cursor.execute(sql)

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    except MySQLdb.Error as e:
        print("Error {0}: {1}".format(e.args[0], e.args[1]))
        return None


def delete(guestbook):
    try:
        conn = connect()
        cursor = conn.cursor()

        sql = """ delete from guestbook
                        where no = "%s"
                        and   password = "%s"
                    """ % guestbook

        count = cursor.execute(sql)

        cursor.close()
        conn.commit()
        conn.close()

        return count == 1

    except MySQLdb.Error as e:
        print("Error {0}: {1}".format(e.args[0], e.args[1]))
        return None


