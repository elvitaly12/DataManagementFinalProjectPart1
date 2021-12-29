import Utility.DBConnector as Connector
from Utility.Exceptions import DatabaseException
from Utility.DBConnector import ResultSet
from psycopg2 import sql


from enum import Enum
# return values for your functions
class ReturnValue(Enum):
    OK = 0
    NOT_EXISTS = 1
    ALREADY_EXISTS = 2
    ERROR = 3
    BAD_PARAMS = 4

class _Exceptions(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class _Exceptions(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


# exceptions classes, you can print the exception using print(exception)
class DatabaseException(_Exceptions):
    class ConnectionInvalid(_Exceptions):
        pass

    class NOT_NULL_VIOLATION(_Exceptions):
        pass

    class FOREIGN_KEY_VIOLATION(_Exceptions):
        pass

    class UNIQUE_VIOLATION(_Exceptions):
        pass

    class CHECK_VIOLATION(_Exceptions):
        pass

    class database_ini_ERROR(_Exceptions):
        pass


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

def registerUser(username):
    conn = None
    try:
        conn = Connector.DBConnector()
        query = sql.SQL("INSERT INTO Users(id, name) VALUES({id}, {username})").format(id=sql.Literal(ID),
                                                                                       username=sql.Literal(name))
        rows_effected, _ = conn.execute(query)
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
        conn.close()
        return ReturnValue.OK
