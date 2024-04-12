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
from app import terminate_thread


# Import other necessary modules (dbmodel, control, etc.)

event = Blueprint("event", __name__)

# Initialize terminate_thread as a global variable
thread_lock = threading.Lock()

def schedule_api_calls():
    while True:
        with thread_lock:
            if terminate_thread:
                break
        processing()
        schedule.run_pending()
        time.sleep(20)
        

@event.route("/home", methods=["POST", "GET"])
def home():
    global terminate_thread
    if request.method == "POST":
        print("click")
        from app import terminate_thread
        if request.values.get('button') == 'start':
            terminate_thread = False
            threading.Thread(target=schedule_api_calls).start()
        elif request.values.get('button') == 'start':
            terminate_thread = True
    return render_template("index.html")


@event.route("/button_click", methods=["POST", "GET"])
def event_schedule():
    print("click")
    if request.method == "POST":
        terminate_thread = False
        threading.Thread(target=schedule_api_calls).start()


@event.route("/button_end", methods=["POST", "GET"])
def event_end():
    print("click")
    if request.method == "POST":
        terminate_thread = True

# Add other routes and functionality as needed
# ...

# Example usage:
# - When the client sends a POST request to "/button_click", it starts the thread.
# - When the client sends a POST request to "/button_end", it
