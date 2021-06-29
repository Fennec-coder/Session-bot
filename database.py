import psycopg2
from dbconfig import config

from Specimen import User


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
        answer = None
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # execution of a request
        cur.execute(command)
        # trying to get a response
        try:
            answer = cur.fetchall()
        except:
            pass
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        return answer
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"\n!!! - {error}\n")
    finally:
        if conn is not None:
            conn.close()


def create_user(user_obj: User.User):
    execute(
        """ INSERT INTO personal 
        (id,
        name,
        date,
        language,
        utc
                  VALUES ('%s','%s','%s','%s','%s'); """
        % (user_obj.id, user_obj.name, user_obj.date, user_obj.language, user_obj.utc)
    )


def delete_user(user_id):
    execute(
        """DELETE FROM personal WHERE id = '%s';""" % user_id
    )


def update_users_last_login_date(user_id):
    execute(
        """UPDATE personal SET date = CURRENT_DATE WHERE id = '%s';""" % user_id
    )


def user_existence(user_id):
    return execute(
        """SELECT EXISTS (select 1 from personal where id = '%s');""" % user_id
    )[0][0]


def _get_info(source, user_id):
    answer = execute(
        """SELECT * from '%s' where id = '%s';""" % (source, user_id)
    )
    if len(answer) == 0:
        return None
    return answer[0]


def _update_user(user_id, variable, value):
    execute(
        """UPDATE personal SET %s = '%s' WHERE id = '%s';""" % (variable, value, user_id)
    )


def update_user_name(user_id, user_name):
    execute(
        """UPDATE personal SET name = '%s' WHERE id = '%s';""" % (user_id, user_name)
    )


def get_user_array(user_id):
    answer = execute(
        """SELECT * from personal where id = '%s';""" % user_id
    )
    if len(answer) == 0:
        return None
    return answer[0]


def get_user_obj(user_id):
    example = User.User(0)
    example.fill_information_with_an_array(get_user_array(user_id))
    return example


def get_user_settings_obj(user_id):
    example = User.Position()
    example.fill_information_with_an_array(_get_info('settings', user_id))
    return example


def get_user_position_obj(user_id):
    example = User.Position()
    example.fill_information_with_an_array(_get_info('position', user_id))
    return example


if __name__ == '__main__':
    pass
