from pymongo import MongoClient
import pyodbc
import json
import pymongo
import schedule
import time
import requests


def connectToSqlServer(server, database, username, password):
    try:
        # Establishing the connection
        conn = pyodbc.connect(driver="SQL Server",
                              server=server,
                              user=username,
                              password=password,
                              database=database,
                              port=1433)
        return conn
    except Exception as e:
        print("Error connecting to SQL Server:", e)
        return None


def connectToMongoDB(database):
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


def tableSqlServerFetch(conn, table_name, columns):
    """
    Fetch data from a SQL Server table and convert it to JSON format.

    Args:
        conn (connection): Connection object to the SQL Server database.
        table_name (str): Name of the table from which to fetch data.
        columns (list): List of column names in the table.

    Returns:
        str: JSON representation of the fetched data.

    Raises:
        Exception: If an error occurs during the execution.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        results = []
        for row in rows:
            result_dict = {col: value for col, value in zip(columns, row)}
            results.append(result_dict)

        # Convert the list of dictionaries to JSON
        return results
    except Exception as e:
        print(e)
        raise


def tableMongoDBFetch(collection, query=None, projection=None):
    """
    Fetch data from a MongoDB collection and convert it to JSON format.

    Args:
        collection (pymongo.collection.Collection): Collection object from which to fetch data.
        query (dict): Query to filter documents (optional).
        projection (dict): Projection to include/exclude fields in the result (optional).

    Returns:
        str: JSON representation of the fetched data.

    Raises:
        Exception: If an error occurs during the execution.
    """
    try:
        # Fetch documents from the collection
        if query is None:
            query = {}
        if projection is None:
            projection = {}

        cursor = collection.find(query, projection)
        rows = list(cursor)

        # Remove _id field from each document
        for doc in rows:
            doc.pop('_id', None)

        # Convert the list of dictionaries to JSON
        return rows
    except Exception as e:
        print(e)
        raise


def tableMongoDBFetch_100data(collection, query=None, projection=None):
    """
    Fetch 100 rows of data from a MongoDB collection and convert it to JSON format.

    Args:
        collection (pymongo.collection.Collection): Collection object from which to fetch data.
        query (dict): Query to filter documents (optional).
        projection (dict): Projection to include/exclude fields in the result (optional).

    Returns:
        str: JSON representation of the fetched data.

    Raises:
        Exception: If an error occurs during the execution.
    """
    try:
        # Fetch documents from the collection
        if query is None:
            query = {}
        if projection is None:
            projection = {}

        cursor = collection.find(query, projection).limit(
            100)  # Limit to 100 rows
        rows = list(cursor)

        # Remove _id field from each document
        for doc in rows:
            doc.pop('_id', None)

        # Convert the list of dictionaries to JSON
        return rows
    except Exception as e:
        print(e)
        raise


def central_processing():
    try:
       cartonToAppEnginePCL()

    except Exception as e:
        print("An error occurred while calling the API:", str(e))


def schedule_api_calls():
    schedule.every(10).seconds.do(central_processing)
    while True:
        schedule.run_pending()
        time.sleep(1)


def cartonToAppEnginePCL():
    try:
        connection = pyodbc.connect(driver="ODBC Driver 17 for SQL Server",
                                    server='localhost',
                                    database='Vision_Mas140',
                                    uid='sa',
                                    pwd='Password.1',
                                    port=1433)
        cursor = connection.cursor()
    except:
        connection = pyodbc.connect(driver="SQL Server",
                                    server='192.168.2.4',
                                    database='Vision_Mas140',
                                    uid='Control',
                                    pwd='123456',
                                    port=1433)
        cursor = connection.cursor()

    uri = "mongodb+srv://unilever-digital:U2024-digital@cluster0.ixcliyp.mongodb.net/"
    client = MongoClient(uri)
    db = client['Vision_Mas140']
    collection = db['Table_ResultCarton']

    cursor.execute(
        "SELECT TOP 1000 ID, DateTime, Line, SKUID, ProductName, Barcode, Status, Reject FROM Table_ResultCarton")
    rows = cursor.fetchall()
    print(rows)

    for row in rows:
        ID, DateTime, Line, SKUID, ProductName, Barcode, Status, Reject = row
        sql_data = {
            "ID": str(ID),
            "DateTime": DateTime,
            "Line": Line,
            "SKUID": str(SKUID),
            "ProductName": ProductName,
            "Barcode": str(Barcode),
            "Status": Status,
            "Reject": Reject
        }
        print(sql_data)

    connection.close()
    client.close()
