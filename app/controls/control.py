import pyodbc
import json
import pymongo


def connectToSqlServer(server, database, username, password):
    """
    connection local database
    """
    try:
        # Establishing the connection
        conn = pyodbc.connect(driver = "SQL Server", 
                              server=server, 
                              user=username,
                              password=password, 
                              database=database,
                              port= 1433)
        return conn
    except Exception as e:
        print("Error connecting to SQL Server:", e)
        return None
    
def cursorDatabase(database):
    """
    connection app server
    """
    try:
        uri = "mongodb+srv://unilever-digital:U2024-digital@cluster0.ixcliyp.mongodb.net/"
        # Establishing the connection
        conn = pymongo.MongoClient(uri)
        return conn[database]
    except Exception as e:
        print("Error connecting to MongoDB:", e)
        return None

def noSqlTransform(rows):
    """tranform Sql table to tree Node json

    Args:
        table (dataframe)): sql table
    """
    try:
    
        # Convert rows to a list of dictionaries
        results = []
        for row in rows:
            results.append(dict(row))

        # Convert the list of dictionaries to JSON
        return json.dumps(results)
    except Exception as e:
        print(e)