import datetime
import time
from datetime import datetime as dt
from app.controls.control import *

def queryOptimizationCap(table):
    """
    counter bottles server
    """
    try:
        connection = connectToSqlServer('192.168.2.4', 'Vision_Mas140', 'Control', '123456')
        cursor = connection.cursor()
        end_server = cursorDatabase("Vision_Mas140")
        collection = end_server[table]
        result = collection.delete_many({})
        # Delete all documents in the collection
        result = collection.delete_many({})

        startdate = datetime.datetime(2023, 1, 1, 0, 0, 0)
        query = f"""
        SELECT CONVERT(date, DateTime) AS date,
            DAY(DateTime) AS day,
            MONTH(DateTime) AS month,
            YEAR(DateTime) AS year,
            CASE
                WHEN DATEPART(hh, DateTime) < 6 THEN 1
                WHEN DATEPART(hh, DateTime) < 14 THEN 2
                ELSE 3
            END AS shift,
            FGsCode AS sku,
            Line As line,
            COUNT(*) AS count,
            SUM(CASE WHEN Status = 'Good' THEN 1 ELSE 0 END) AS countGood,
            SUM(CASE WHEN Status = 'Not Good' THEN 1 ELSE 0 END) AS countNotgood
        FROM Table_ResultCap
        GROUP BY CONVERT(date, DateTime), DAY(DateTime), MONTH(DateTime), YEAR(DateTime), Line, FGsCode,
                CASE
                    WHEN DATEPART(hh, DateTime) < 6 THEN 1
                    WHEN DATEPART(hh, DateTime) < 14 THEN 2
                    ELSE 3
                END
        ORDER BY date, shift;
        """
        cursor.execute(query)
        data = cursor.fetchall()
        data_insert = []
        for row in data:
            new_row = {
                "date": row[0],
                "day": row [1],
                "month": row[2],
                "year": row[3],
                "shift": row[4],
                "sku":  row[5],
                "line": row[6],
                "count": row[7],
                "countPass": row[8],
                "countNotgood": row[9],
            }
            data_insert.append(new_row)

        collection.insert_many(data_insert)
        connection.close()
    except Exception as e:
        print("query", {table}, "fail. ", e)

def queryOptimizationCarton(table):
    """
    counter bottles server
    """
    try:
        connection = connectToSqlServer('192.168.2.4', 'Vision_Mas140', 'Control', '123456')
        cursor = connection.cursor()
        end_server = cursorDatabase("Vision_Mas140")
        collection = end_server[table]
        result = collection.delete_many({})
        startdate = datetime.datetime(2023, 1, 1, 0, 0, 0)
        pipeline = f"""
        SELECT CONVERT(date, DateTime) AS date,
            DAY(DateTime) AS day,
            MONTH(DateTime) AS month,
            YEAR(DateTime) AS year,
            CASE
                WHEN DATEPART(hh, DateTime) < 6 THEN 1
                WHEN DATEPART(hh, DateTime) < 14 THEN 2
                ELSE 3
            END AS shift,
            SKUID AS sku,
            Line As line,
            COUNT(*) AS count,
            SUM(CASE WHEN Status = 'Good' THEN 1 ELSE 0 END) AS countGood,
            SUM(CASE WHEN Status = 'WrongCode' THEN 1 ELSE 0 END) AS countWrongCode
        FROM Table_ResultCarton
        GROUP BY CONVERT(date, DateTime), DAY(DateTime), MONTH(DateTime), YEAR(DateTime), Line, SKUID,
                CASE
                    WHEN DATEPART(hh, DateTime) < 6 THEN 1
                    WHEN DATEPART(hh, DateTime) < 14 THEN 2
                    ELSE 3
                END
        ORDER BY date, shift;
        """
        cursor.execute(pipeline)
        group_data = cursor.fetchall()
        data_insert = []
        for row in group_data:
            new_row = {
                "date": row[0],
                "day": row [1],
                "month": row[2],
                "year": row[3],
                "shift": row[4],
                "sku":  row[5],
                "line": row[6],
                "count": row[7],
                "countGood": row[8],
                "countWrongCode": row[9],
            }
            data_insert.append(new_row)

        collection.insert_many(data_insert)
        connection.close()
    except Exception as e:
        print("query", {table}, "fail. ", e)

def queryOptimizationCounter(table):
    """
    counter bottles server
    """
    try:
        connection = connectToSqlServer('192.168.2.4', 'Vision_Mas140', 'Control', '123456')
        cursor = connection.cursor()
        counter_server = cursorDatabase("Vision_Mas140")
        collection = counter_server[table]
        result = collection.delete_many({})
        startdate = datetime.datetime(2023, 1, 1, 0, 0, 0)
        # Define the pipeline string using f-strings for cleaner formatting
        pipeline = f"""
        SELECT CONVERT(date, DateTime) AS date,
            DAY(DateTime) AS day,
            MONTH(DateTime) AS month,
            YEAR(DateTime) AS year,
            CASE
                WHEN DATEPART(hh, DateTime) < 6 THEN 1
                WHEN DATEPART(hh, DateTime) < 14 THEN 2
                ELSE 3
            END AS shift,
            FGsCode AS sku,
            COUNT(*) AS count,
            SUM(CASE WHEN Status = 'Good' THEN 1 ELSE 0 END) AS countPass,
            SUM(CASE WHEN Status = 'NotGood' THEN 1 ELSE 0 END) AS countReject
        FROM Table_ResultCounterBottles
        GROUP BY CONVERT(date, DateTime), DAY(DateTime), MONTH(DateTime), YEAR(DateTime), FGsCode,
            CASE
                WHEN DATEPART(hh, DateTime) < 6 THEN 1
                WHEN DATEPART(hh, DateTime) < 14 THEN 2
                ELSE 3
            END
        ORDER BY date, shift;
        """
        cursor.execute(pipeline)
        group_data = cursor.fetchall()

        data_insert = []
        for row in group_data:
            new_row = {
                "date": row[0],
                "day": row [1],
                "month": row[2],
                "year": row[3],
                "shift": row[4],
                "sku":  row[5],
                "count": row[6],
                "countGood": row[7],
                "countNotGood": row[8],
            }
            #for key, value in new_row.items():
                #if key == "date":
                    #new_row[key] = dt.strftime(value, "%Y-%m-%d")
                #else:
                    #new_row[key] = value if value != float('nan') else ""
            data_insert.append(new_row)

        collection.insert_many(data_insert)
        connection.close()
    except Exception as e:
        print("query", {table}, "fail: ", e)

def querySqlServer():
    print("start session")
    queryOptimizationCap("Table_ResultCap")
    queryOptimizationCarton("Table_ResultCarton")
    queryOptimizationCounter("Table_ResultCounterBottles")
