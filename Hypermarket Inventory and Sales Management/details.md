sgi
fact and dimension
pydantic ->  base model


-     conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    check_same_thread=True (the default behavior):

    SQLite enforces that the connection can only be used by the thread that created it.

    If another thread tries to use the connection, it will raise a ProgrammingError to prevent issues caused by multiple threads interacting with the same SQLite connection.

    check_same_thread=False:

    This allows the SQLite connection to be shared across multiple threads. When set to False, SQLite will not check if the connection is being accessed from a thread other than the one that created it.

    However, this should be used with caution, as SQLite is not designed for thread-safe concurrent writes. You should manually manage thread safety when using this setting.

-     conn.row_factory = sqlite3.Row

    Default Behavior:
    By default, when you execute a query using conn.execute(...), the rows are returned as tuples. For example:

    cursor = conn.execute("SELECT id, name FROM users")
    rows = cursor.fetchall()
    # rows will be a list of tuples, e.g., [(1, 'Alice'), (2, 'Bob')]


    While this works fine, it's less convenient when you need to access columns by name, especially for large datasets with many columns.

    Using sqlite3.Row:
    When you set conn.row_factory = sqlite3.Row, each row returned by the query will be an instance of sqlite3.Row, which behaves like a dictionary. This allows you to access the columns by their names instead of using column indices. Here's an example:

    conn.row_factory = sqlite3.Row
    cursor = conn.execute("SELECT id, name FROM users")
    rows = cursor.fetchall()

    for row in rows:
        print(row['id'], row['name'])  # Access columns by name


    In this case:

    row['id'] will return the value of the id column.

    row['name'] will return the value of the name column.