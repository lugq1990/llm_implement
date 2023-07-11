import mysql.connector
import pandas as pd


database_config = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "test",
}

def execute_mysql_query(query):
    try:
        # Connect to the MySQL server
        connection = mysql.connector.connect(**database_config)

        if connection.is_connected():
            # # Get the MySQL server version
            # cursor = connection.cursor()
            # cursor.execute("SELECT VERSION()")
            # data = cursor.fetchone()
            # print("Connected to MySQL Server Version:", data[0])

            # cursor.execute("SELECT * FROM user")
            # rows = cursor.fetchall()
            # for row in rows:
            #     print(row)
            df = pd.read_sql(query, con=connection)
            return df
    except mysql.connector.Error as err:
        print("Error:", err)

    finally:
        if 'connection' in locals() and connection.is_connected():
            # Close the connection if it's open
            connection.close()            
          
            
query = "select * from user"
df = execute_mysql_query(query=query)
df.head()