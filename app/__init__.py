import atexit
from flask import (
    Flask,
    url_for,
    redirect,
    request,
    render_template
)
import os
from .controls.control import processing
import threading
import schedule
import time
import signal

terminate_thread = True
thread_lock = threading.Lock()


def schedule_api_calls():
    global terminate_thread
    while True:
        with thread_lock:
            if terminate_thread:
                break
        # Call the processing function here
        processing()
        schedule.run_pending()
        time.sleep(20)



def handle_exit(signum, frame):
    global terminate_thread
    print("Exiting...")
    with thread_lock:
        terminate_thread = True
    os._exit(0)
    
def create_app(test_config=None):
    """ app init

    Args:
        test_config (_type_, optional): _description_. Defaults to None.

    Returns:
        app : Flask app
    """
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
        app.config.from_mapping(SECRET_KEY='unilever',
                                CACHE_TYPE='FileSystemCache',
                                CACHE_DIR='cache',
                                CACHE_THRESHOLD=100000,)
    else:
        app.config.from_mapping(test_config)
    from .views.view import blog
    from .views.event import event
    app.register_blueprint(blog)
    app.register_blueprint(event)

    from .models.dbmodel import db
    db.init_app(app)
    # ensure the instance folder exists 
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def main():
        global terminate_thread
        with thread_lock:
            terminate_thread = False
        threading.Thread(target=schedule_api_calls).start()
        return render_template("index.html")
    
    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)
    
    return app
