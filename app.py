from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
import datetime
import pandas as pd
from sqlalchemy import func

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Data/hawaii.sqlite"
db = SQLAlchemy(app)


class Measurement(db.Model):
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


@app.route("/")
def index():
    return (
        f"Welcome to my first API!<br/>"
        f"Here are the all available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_end_type"
    )


@app.route("/api/v1.0/precipitation")
def last_year_prcp():
    measurements = (
        db.session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date <= "2017-08-23")
        .filter(Measurement.date >= "2016-08-23")
        .all()
    )
    precip_df = pd.DataFrame(measurements).sort_index(axis=1, ascending=False)
    precip_dict = precip_df.to_dict(orient="index")
    return jsonify(precip_dict)


@app.route("/api/v1.0/stations")
def stations_list():
    stations = db.session.query(Station.station).all()
    stations_df = pd.DataFrame(stations)
    stations_dict = stations_df.to_dict(orient="list")
    return jsonify(stations_dict)


@app.route("/api/v1.0/tobs")
def last_year_tobs():
    ly_tobs = (
        db.session.query(Measurement.date, Measurement.tobs)
        .filter(Measurement.date <= "2017-08-23")
        .filter(Measurement.date >= "2016-08-23")
        .all()
    )
    ly_tobs_df = pd.DataFrame(ly_tobs)
    ly_tobs_dict = ly_tobs_df.to_dict(orient="index")
    return jsonify(ly_tobs_dict)


# To search this route copy and paste the route, then type: ?start="%Y-%m-%d" If you want an end date also, then add: &end="%Y-%m-%d"
@app.route("/api/v1.0/start_end_type")
def start_type():
    request_start = request.args.get("start")
    request_end = request.args.get("end")

    try:
        base_cmd = db.session.query(
            func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs),
        )

        if request_start:
            base_cmd = base_cmd.filter(
                Measurement.date
                >= datetime.datetime.strptime(request_start, "%Y-%m-%d")
            )

        if request_end:
            base_cmd = base_cmd.filter(
                Measurement.date <= datetime.datetime.strptime(request_end, "%Y-%m-%d")
            )

        data = base_cmd.all()

        return jsonify(data)

    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
