from flask import Blueprint, render_template, request
from scraper.app import run_scraper
from SQL.VikingsDBConnector import vikings_db
import threading


api = Blueprint("api", __name__, static_folder="static", template_folder="templates")


@api.route("/")
def index():
    return render_template("index.html")


@api.route("/run_vikings_scraper", methods=['GET', 'POST'])
def run_vikings_scraper():
    thread = threading.Thread(target=run_scraper)
    thread.start()
    return {'scraper': 'running'}


@api.route("/insert_entities_to_db", methods=['POST'])
def insert_entities_to_db():
    data = request.json
    vikings_db.insert_entities(data)
    return {'updated_db': 'true'}
