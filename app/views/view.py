
from app.models.dbmodel import *
from app.controls.query import *
import schedule
import time

def scheduleQuerySqlServer(event=None):
    def run():
        querySqlServer()
        print("loop")
    schedule.every(59).minutes.do(run)

    while True:
        schedule.run_pending()
        time.sleep(60)

def stop_task():
    schedule.clear(schedule.ALL_PENDING)

def homeViewQT():
    """
    desktop view
    """
    from app.templates.index import HomeApp
    root = HomeApp()
    root.bind("<Expose>", scheduleQuerySqlServer)
    root.protocol("WM_DESTROY", stop_task)
    root.mainloop()

#pyinstaller --onefile --hidden-import schedule --hidden-import pyodbc --hidden-import openpyxl --hidden-import pymongo --hidden-import threading --hidden-import pymssql --hidden-import datetime main.py

