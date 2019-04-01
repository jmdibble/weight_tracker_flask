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

## Test DB
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

## INDEX ROUTE
@app.route("/")
def index():
    return render_template("index.html")

## DELETE ROW ROUTE
@app.route("/delete", methods=['POST'])
def delete():
    
    # Delete query
    # (db.session.query(Data).filter(Data.date_.strftime("%d/%m/%Y") == '01/03/2019').delete())
    dateCol = (db.session.query(Data).order_by(Data.date_.desc()).all())
    specDate = (db.session.query(Data).filter(Data.date_ == '01/03/2019').delete())
    db.session.commit()
    print(specDate)
    # for i in dateCol:
    #     dateCol = i.date_.strftime("%d/%m/%Y")
    # print(dateCol)

    return render_template("deleted.html")

## RESULTS ROUTE
@app.route("/results")
def results():
    
    # All query
    allRows = (db.session.query(Data).order_by(Data.date_.desc()).all())
    datesList = []
    stonesList = []
    poundsListTen = []

    # Fill each lists with corresponding column
    for i in allRows:
        datesList.append(i.date_.strftime("%d/%m/%Y"))
        stonesList.append(i.stone_)
        poundsListTen.append(i.pounds_)
    
    # Divide pounds by 100 as they are stored *100 because decimals can't be stored (need to fix this eventually)
    poundsList = []
    for i in poundsListTen:
        pounds = i/100
        poundsList.append(pounds)

    # print(datesList)
    # print(stonesList)
    # print(poundsList)

    # Create a list of all the differences in pounds for each entry compared to the initial weight
    difList = []
    for i, j in zip(stonesList, poundsList):
        stonePounds = i*14
        poundPounds = j
        totalPounds = stonePounds + poundPounds
        initialStones = (stonesList[-1]) * 14
        initialPounds = poundsList[-1]
        totalInitial = initialStones + initialPounds
        difference = round((totalPounds - totalInitial), 2)
        difList.append(difference)
    # print(difList)

    # Link up the delete button to delete a row (Don't think this is needed now, but keeping until sure)
    idTag = []
    for i in range(0, len(difList)):
        idTag.append(i)
    # print(idTag)

    # Change from last entry
    lastList = []
    for i, j in zip(stonesList, poundsList):
        stonePounds1 = i*14
        poundPounds1 = j
        totalPounds1 = stonePounds1 + poundPounds1
        initialStones1 = (stonesList[2]) * 14
        initialPounds1 = poundsList[2]
        totalInitial1 = initialStones1 + initialPounds1
        difference1 = round((totalPounds1 - totalInitial1), 2)
        lastList.append(difference1)

    result = zip(datesList, stonesList, poundsList, difList, idTag, lastList)
    resultsList = list(result)
    # print(resultsList)

    # A disgusting piece of code to build an HTML table of all the results. It turns each list into a column in HTML. Needs cleaning
    FULL_HTML = ["<tr><th>Date</th><th>Stone</th><th>Pounds</th><th>Last Change Lb</th><th>Total Change Lb</th></tr>"]
    for date, rows in groupby(resultsList, itemgetter(0)):
        table = []
        for date, value1, value2, value3, idTag, lastList in rows:
            # table.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a class='button-mini' id='row%s' href='printMe(%s)'><i class='fas fa-times'></i></a></td></tr>" % (date, value1, value2, value3, idTag, date))
            table.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><a class='button-mini' id='%s'><i class='fas fa-times'></i></a></td></tr>" % (date, value1, value2, lastList, value3, date))
        table = "\n{}\n".format('\n'.join(table))
        FULL_HTML.append(table)
    FULL_HTML = "<table>\n{}\n</table>".format('\n'.join(FULL_HTML))

    return render_template("results.html", table=FULL_HTML)


## SUCCESSFUL SUBMISSION ROUTE
@app.route("/success", methods=["POST"])
def success():
    if request.method == "POST":
        date = request.form["date_entry"]
        stone = request.form["st_entry"]
        pounds = request.form["lb_entry"]
        pounds = ((float(pounds))*100)
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


## TO DO
# Clean code
# Modularise code
# Make "x" delete a row
# Turn pounds into stones and pounds
# Make a weekly change column