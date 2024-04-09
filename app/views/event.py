from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)
from app.models.dbmodel import *
from app.controls.control import *
import schedule
import time
import signal
import threading
import os


terminate_thread = False
thread_lock = threading.Lock()


def schedule_api_calls():
    global terminate_thread
    while True:
        with thread_lock:
            if terminate_thread:
                break
        processing()
        schedule.run_pending()
        time.sleep(20)

event = Blueprint("event", __name__)


@event.route("/button_click",  methods=["POST", "GET"])
def event_schedule():
    if request.method == "POST":
        global terminate_thread
        with thread_lock:
            terminate_thread = False
        threading.Thread(target=schedule_api_calls).start()
        

@event.route("/button_end",  methods=["POST", "GET"])
def event_end():
    if request.method == "POST":
        global terminate_thread
        with thread_lock:
            terminate_thread = True
