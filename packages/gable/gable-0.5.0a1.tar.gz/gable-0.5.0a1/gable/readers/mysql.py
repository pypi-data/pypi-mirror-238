import mysql.connector  # type: ignore


def create_mysql_connection(
    user: str, password: str, db: str, host: str = "localhost", port: int = 3306
):
    """
    Create a connection to a MySQL database.

    :param user:     The database user name.
    :param password: The database password.
    :param db:       The database name.
    :param host:     The database host.
    :param port:     The database port.
    :return:         A MySQLdb Connection instance.
    """
    conn = mysql.connector.connect(
        database=db,
        user=user,
        passwd=password,
        host=host,
        port=port,
    )
    return conn
