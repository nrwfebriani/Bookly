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

    # Update name in the table
    # cursor.execute("UPDATE user SET name = %s WHERE username = %s;", (300, "apple"))
    print("Updated", cursor.rowcount, "row(s) of data.")

    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
    print("Done.")
