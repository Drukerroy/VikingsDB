from SQL.VikingsDBConnector import vikings_db


class Character(vikings_db.db.Model):
    __tablename__ = 'character'
    characterid = vikings_db.db.Column(vikings_db.db.Integer, primary_key=True)
    firstname = vikings_db.db.Column(vikings_db.db.String(50), nullable=False)
    lastname = vikings_db.db.Column(vikings_db.db.String(50))
    description = vikings_db.db.Column(vikings_db.db.Text)
    tvshow = vikings_db.db.Column(vikings_db.db.Enum('Vikings', 'Norsemen'), nullable=False)
    imagesrc = vikings_db.db.Column(vikings_db.db.Text)
    actorid = vikings_db.db.Column(vikings_db.db.Integer, vikings_db.db.ForeignKey('actor.actorid'))

    actor = vikings_db.db.relationship('Actor')
