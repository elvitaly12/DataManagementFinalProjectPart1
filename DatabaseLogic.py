import DBConnector as Connector
from DBConnector import DatabaseException
from DBConnector import ReturnValue
from psycopg2 import sql


def createDB() -> None:
    conn = None
    try:
        conn = Connector.DBConnector()
        script = open('CREATE_script.sql', 'r')
        conn.execute(script)
        conn.commit()
    except DatabaseException.ConnectionInvalid as e:
        print(e)
    except DatabaseException.NOT_NULL_VIOLATION as e:
        print(e)
    except DatabaseException.CHECK_VIOLATION as e:
        print(e)
    except DatabaseException.UNIQUE_VIOLATION as e:
        print(e)
    except DatabaseException.FOREIGN_KEY_VIOLATION as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        # will happen any way after try termination or exception handling
        conn.close()

def registerUser(username, chat_id):
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO Users(username, chat_id, active) VALUES({username_input}, {chat_id_input}, {active_input})").format(
            username_input=sql.Literal(username),
            chat_id_input=sql.Literal(chat_id),
            active_input=sql.Literal(True))
        rows_effected, _ = conn.execute(query)
        conn.commit()
    except DatabaseException.NOT_NULL_VIOLATION:
        conn.close()
        return ReturnValue.BAD_PARAMS
    except DatabaseException.CHECK_VIOLATION:
        conn.close()
        return ReturnValue.BAD_PARAMS
    except DatabaseException.UNIQUE_VIOLATION:
        conn.close()
        return ReturnValue.ALREADY_EXISTS
    except DatabaseException.database_ini_ERROR:
        conn.close()
        return ReturnValue.ERROR
    except DatabaseException.ConnectionInvalid:
        conn.close()
        return ReturnValue.ERROR
    except Exception:
        conn.close()
        return ReturnValue.ERROR
    finally:
        conn.close()
        return ReturnValue.OK

def unregisterUser(username):
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("UPDATE Users "
                        "SET active = False "
                        "WHERE username={username_input}").format(username_input=sql.Literal(username))
        rows_effected, _ = conn.execute(query)
        # conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        return ReturnValue.ERROR

    conn.close()
    return ReturnValue.OK

def getChat_idByUsername(username):
    conn = None
    rows_effected = None
    res = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT chat_id FROM Users "
                        "WHERE username={username_input}").format(username_input=sql.Literal(username))
        rows_effected, res = conn.execute(query)
        conn.commit()
    except Exception:
        conn.close()
        return ReturnValue.ERROR
    finally:
        conn.close()
        if rows_effected is None or rows_effected <= 0:
            return -1
        else:
            return res[0]['chat_id']

def getUsernameByChatID(chat_id):
    conn = None
    rows_effected = None
    res = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("SELECT username FROM Users "
                        "WHERE chat_id={chat_id_input}").format(chat_id_input=sql.Literal(chat_id))
        rows_effected, res = conn.execute(query)
        conn.commit()
    except Exception:
        conn.close()
        return ReturnValue.ERROR
    finally:
        conn.close()
        if rows_effected is None or rows_effected <= 0:
            return -1
        else:
            return res[0]['username']

