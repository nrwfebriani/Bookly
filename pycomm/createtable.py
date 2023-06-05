import mysql.connector
from mysql.connector import errorcode

# Obtain connection string information from the portal

config = {
    "host": "senpro-bookly.mysql.database.azure.com",
    "user": "powerpuffgirls",
    "password": "bookly123_",
    "database": "db-bookly",
    "client_flags": [mysql.connector.ClientFlag.SSL],
    "ssl_ca": "DigiCertGlobalRootCA.crt.pem",
}

# Construct connection string

try:
    conn = mysql.connector.connect(**config)
    print("Connection established")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with the user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = conn.cursor()

    # Drop previous table of same name if one exists
    cursor.execute("DROP TABLE IF EXISTS inventory;")
    print("Finished dropping table (if existed).")

    # Create table
    cursor.execute(
        "CREATE TABLE user (id serial PRIMARY KEY, username VARCHAR(50), name VARCHAR(50), email VARCHAR(50), password VARCHAR(50));"
    )
    print("Finished creating table.")

    # Insert some data into table
    cursor.execute(
        "INSERT INTO user (username, name, email, password) VALUES (%s, %s, %s, %s);",
        ("admin", "Admin", "admin@gmail.com", "12345"),
    )
    print("Inserted", cursor.rowcount, "row(s) of data.")
    cursor.execute(
        "INSERT INTO user (username, name, email, password) VALUES (%s, %s, %s, %s);",
        ("febri", "Febri", "febri@gmail.com", "12345"),
    )
    print("Inserted", cursor.rowcount, "row(s) of data.")

    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")
