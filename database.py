import psycopg2
from dbconfig import config


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def execute(command):
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # execution of a request
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"\n!!! - {error}\n")
    finally:
        if conn is not None:
            conn.close()


def create_user(user_id, name, eoo):
    execute(
        """ INSERT INTO personal (id, name, eoo) VALUES ('%s', '%s', '%s'); """ % (user_id, name, eoo)
    )


def delete_user(user_id):
    execute(
        """DELETE FROM personal WHERE id = '%s';""" % user_id
    )


def update_users_last_login_date(user_id):
    execute(
        """UPDATE personal SET date = CURRENT_DATE WHERE id = '%s';""" % user_id
    )


if __name__ == '__main__':
    connect()
    delete_user(1)
    create_user(1, 'nn', True)
    update_users_last_login_date(1)
