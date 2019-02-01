from flask_table import Table, Col

class Results(Table):
    def __init__(self, date, stone, pounds):
        self.date=date
        self.stone=stone
        self.pounds=pounds
        date = Col('date_')
        stone = Col('stone_')
        pounds = Col('pounds')