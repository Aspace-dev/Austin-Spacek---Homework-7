from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hawaii.sqlite'
db = SQLAlchemy(app)

class DictMixIn:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(getattr(self, column.name), datetime.datetime)
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }

class Measurement(db.Model, DictMixIn):
    id = db.Column(db.Integer(), primary_key=True)
    station = db.Column(db.String())
    date = db.Column(db.String())
    prcp = db.Column(db.Float())
    tobs = db.Column(db.Float())

class Station(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    station = db.Column(db.String())
    name = db.Column(db.String())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    elevation = db.Column(db.Float())


@app.before_first_request
def init_app():
    db.create_all()
    db.session.commit()


@app.route('/')
def index():
    return (
        f"Welcome to my first API!<br/>"
        f"Here are the all available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def show_all():
    measurements = db.session.query(Measurement.prcp, Measurement.date).\
    filter(Measurement.date <= "2017-08-23").filter(Measurement.date >= "2016-08-23").all()
    return jsonify([Measurement.to_dict() for Measurement in measurements])


if __name__ == "__main__":
    app.run(debug=True)