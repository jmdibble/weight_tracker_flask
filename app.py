from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import datetime
import datefinder

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres123@localhost/weight_tracker"
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    date_ = db.Column(db.Date, unique=True)
    stone_ = db.Column(db.Integer)
    pounds_ = db.Column(db.Integer)

    def __init__(self, date_, stone_, pounds_):
        self.date_ = date_
        self.stone_ = stone_
        self.pounds_ = pounds_


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/results")
def results():
    ##
    dates = db.session.query(Data.date_).all()
    result = [str(i) for i in dates]
    ls = []
    for i in result:
        matches = datefinder.find_dates(i)
        for match in matches:
            match = match.date()
            match = match.strftime("%d/%m/%Y")
            ls.append(match)
    print(ls)
    return render_template("results.html", dates=ls)


@app.route("/success", methods=["POST"])
def success():
    if request.method == "POST":
        date = request.form["date_entry"]
        stone = request.form["st_entry"]
        pounds = request.form["lb_entry"]
        # print(date)
        if db.session.query(Data).filter(Data.date_ == date).count() == 0:
            data = Data(date, stone, pounds)
            db.session.add(data)
            db.session.commit()
            return render_template("success.html")
        return render_template("index.html", text="You've already got an entry for that date")


if __name__ == "__main__":
    app.debug = True
    app.run()
