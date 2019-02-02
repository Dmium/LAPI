from test import db
from test import ma

class People(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key = True)
    Fortnite = db.Column(db.String(100))
    EA = db.Column(db.String(100))
    Geraldo = db.Column(db.String(100))
    Epicness = db.Column(db.Integer)

class People_Schema(ma.ModelSchema):
    class Meta:
        fields = ('id',)

people_schema = People_Schema()
people_schemas = People_Schema(many=True)
