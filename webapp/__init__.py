from flask import Flask
from SQL.VikingsDBConnector import vikings_db
from webapp.views.views import views
from webapp.views.rest_api import api


def create_app():
    app = Flask(__name__, static_url_path='/static')

    app.register_blueprint(views, url_prefix="")
    app.register_blueprint(api, url_prefix="/api")
    # 'postgres://vikingsdatabase_user:ehYdAjcULaUASBTNLJ1iOx1tkqRvAR4Q@dpg-ciohtolph6elhbt6oru0-a/vikingsdatabase'
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://vikingsdatabase_user:ehYdAjcULaUASBTNLJ1iOx1tkqRvAR4Q@dpg-ciohtolph6elhbt6oru0-a/vikingsdatabase'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    vikings_db.db.init_app(app)

    return app
