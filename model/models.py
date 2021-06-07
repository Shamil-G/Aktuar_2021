from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column

from main_app import app


db = SQLAlchemy(app)
print("Модель стартовала...")


class Models:
    id_model = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    dat = db.Column(db.DateTime)


class ModelsF(object):
    def __init__(self, id_model, title, intro, text, dat):
        self.id_model = id_model
        self.title = title
        self.intro = intro
        self.text = text
        self.dat = dat


class ModelStatusCalculated:
    id_calc = db.Column(db.Integer, primary_key=True, unique=True)
    date_calc = db.Column(db.DateTime, nullable=False)
    id_models = db.Column(db.Integer, nullable=False)
    st_0701 = db.Column(db.String(1), nullable=True)
    st_0702 = db.Column(db.String(1), nullable=True)
    st_0703 = db.Column(db.String(1), nullable=True)
    st_0705 = db.Column(db.String(1), nullable=True)


class ModelStatusCalculatedF:
    def __init__(self, id_calc, date_calc, id_model, st_0701, st_0702, st_0703, st_0705):
        self.id_calc = id_calc
        self.date_calc = date_calc
        self.id_model = id_model
        self.st_0701 = st_0701
        self.st_0702 = st_0702
        self.st_0703 = st_0703
        self.st_0705 = st_0705


class ModelCalculated:
    id_calc = db.Column(db.Integer, primary_key=True, unique=True)
    rfpm_id = db.Column(db.String(8), nullable=False)
    pnpt_id = db.Column(db.Integer, nullable=False)
    date_stop = db.Column(db.DateTime)
    sum_all = db.Column(db.DECIMAL, nullable=False)


class ModelCalculatedF(object):
    def __init__(self, id_calc, rfpm_id, pnpt_id, date_stop, sum_all):
        self.id_calc = id_calc
        self.rfpm_id = rfpm_id
        self.pnpt_id = pnpt_id
        self.date_stop = date_stop
        self.sum_all = sum_all
