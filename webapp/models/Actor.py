from SQL.VikingsDBConnector import vikings_db


class Actor(vikings_db.db.Model):
    __tablename__ = 'actor'
    actorid = vikings_db.db.Column(vikings_db.db.Integer, primary_key=True)
    firstname = vikings_db.db.Column(vikings_db.db.String(50), nullable=False)
    lastname = vikings_db.db.Column(vikings_db.db.String(50))
    description = vikings_db.db.Column(vikings_db.db.Text)
