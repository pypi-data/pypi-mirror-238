import psycopg2  # type: ignore


def create_postgres_connection(
    user: str, password: str, db: str, host: str = "localhost", port: int = 5432
) -> psycopg2.extensions.connection:  # type: ignore
    """
    Create a connection to a PostgreSQL database.

    :param user:     The database user name.
    :param password: The database password.
    :param db:       The database name.
    :param host:     The database host.
    :param port:     The database port.
    :return:         A psycopg2 connection instance.
    """
    conn = psycopg2.connect(
        dbname=db, user=user, password=password, host=host, port=port, sslmode="prefer"
    )
    return conn
