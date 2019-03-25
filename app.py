from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import datetime
import datefinder
from itertools import groupby
from operator import itemgetter
from decimal import Decimal

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
## Testing DB
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres123@localhost/weight_tracker"
## Prod DB
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://fpqzadtuibuwiu:877b5633cba5743b4152d40dac4ea9a61c1f1acd90db4abca3a9d43b5138dee2@ec2-54-204-13-34.compute-1.amazonaws.com:5432/der5hc3bs38utn?sslmode=require"
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
    
    # All query
    allRows = (db.session.query(Data).order_by(Data.date_.desc()).all())
    datesList = []
    stonesList = []
    poundsListTen = []

    for i in allRows:
        datesList.append(i.date_.strftime("%d/%m/%Y"))
        stonesList.append(i.stone_)
        poundsListTen.append(i.pounds_)
    
    poundsList = []
    for i in poundsListTen:
        pounds = i/10
        poundsList.append(pounds)

    # print(datesList)
    # print(stonesList)
    # print(poundsList)

    difList = []
    for i, j in zip(stonesList, poundsList):
        stonePounds = i*14
        poundPounds = j
        totalPounds = stonePounds + poundPounds
        initialStones = (stonesList[0]) * 14
        initialPounds = poundsList[0]
        totalInitial = initialStones + initialPounds
        difference = round((totalInitial - totalPounds), 1)
        difList.insert(0, difference)
    print(difList)

    result = zip(datesList, stonesList, poundsList, difList)
    resultsList = list(result)
    # print(resultsList)

    FULL_HTML = ["<tr><th>Date</th><th>Stone</th><th>Pounds</th><th>Lb Change</th></tr>"]
    for date, rows in groupby(resultsList, itemgetter(0)):
        table = []
        for date, value1, value2, value3 in rows:
            table.append("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td><i class='fas fa-times'></i></td></tr>".format(date, value1, value2, value3))
        table = "\n{}\n".format('\n'.join(table))
        FULL_HTML.append(table)
    FULL_HTML = "<table>\n{}\n</table>".format('\n'.join(FULL_HTML))

    return render_template("results.html", table=FULL_HTML)


@app.route("/success", methods=["POST"])
def success():
    if request.method == "POST":
        date = request.form["date_entry"]
        stone = request.form["st_entry"]
        pounds = request.form["lb_entry"]
        pounds = ((float(pounds))*10)
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

