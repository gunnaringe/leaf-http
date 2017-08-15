from flask import Flask
from flask import request, Response
import pycarwings2
from functools import wraps
from pycarwings2 import CarwingsError

app = Flask(__name__)

def authenticate():
    return Response(
    'Please verify your credentials',
    401,
    {'WWW-Authenticate': 'Basic realm="Leaf"'})

def get_leaf(auth):
        if auth is None: return None
        session = pycarwings2.Session(auth.username, auth.password , "NE")
        try:
            return session.get_leaf()
        except CarwingsError as e:
            return None

@app.route('/climate/start', methods=['POST'])
def start_climate_control():
    leaf = get_leaf(request.authorization)
    if leaf is None: return authenticate()

    leaf.start_climate_control()
    return "Starting climate control"

@app.route('/climate/stop', methods=['POST'])
def stop_climate_control():
    leaf = get_leaf(request.authorization)
    if leaf is None: return authenticate()

    leaf.stop_climate_control()
    return "Stopping climate control"

@app.route('/climate/status', methods=['GET'])
def get_climate_status():
    leaf = get_leaf(request.authorization)
    if leaf is None: return authenticate()

    is_running = leaf.get_latest_hvac_status().is_hvac_running
    status = "on" if is_running else "off"
    return "Climate control: %s" % status
