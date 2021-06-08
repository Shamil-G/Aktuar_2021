from main_app import app
from flask_login import login_required
from flask import request, redirect, render_template, url_for
from model.aktuar_models import *
from model.utils import *
from datetime import date
from reports.childcare_0705 import *
from reports.unemployment_0703 import *
from reports.disability_0702 import *
from reports.bread_winner_0701 import *
from reports.rep_resume import *
import config as cfg


@app.route('/model-calc/<int:id_model>/new', methods=['POST', 'GET'])
@login_required
def view_model_calc_new(id_model):
    if 'Operator AKTUAR' in g.user.roles or \
            'Admin' in g.user.roles:
        if cfg.debug_level > 0:
            print("Добавляем расчет! "+str(id_model))
            print("Метод запроса: "+request.method)
        if request.method == "POST":
            date_calc = request.form['date_calc']
            if cfg.debug_level > 0:
                print("Добавляем расчет! id_mod: "+str(id_model)+",date_calc: "+str(date_calc))
            if date_calc:
                model_calc_new(id_model, date_calc)
                if cfg.debug_level > 0:
                    print("Успешное завершение добавления расчета!")
                return redirect(url_for('view_model_status', id_model=id_model))
        else:
            today = date.today()
            return render_template('model-calc-new.html', id_model=id_model, date_calc=today)
    return render_template("models_list.html", cursor=models_list())


@app.route('/model-status/<int:id_model>/<int:id_calc>/del')
@login_required
def view_model_calc_del(id_model, id_calc):
    if 'Operator AKTUAR' in g.user.roles or \
            'Admin' in g.user.roles:
        if cfg.debug_level >= 0:
            print("Удаляем расчет! "+str(id_calc))
        if id_calc:
            if cfg.debug_level > 1:
                print("1. Удаляем расчет! id_model: "+str(id_model)+", ид расчета: "+str(id_calc))
            model_calc_del(id_calc)
            if cfg.debug_level >= 0:
                print("2. Успешное удаление расчета!")
            return redirect(url_for('view_model_status', id_model=id_model))
    return render_template("models_list.html", cursor=models_list())


@app.route('/model-status/<int:id_model>/<int:id_calc>/report_0705')
def view_report_0705(id_model, id_calc):
    if cfg.debug_level > 2:
        print("Выдаем отчет-расчет! "+str(id_calc))
    if id_calc:
        if cfg.debug_level > 2:
            print("1. Формируем отсчет! ид расчета: "+str(id_calc))
        new_path = rep_childcare_0705(id_calc)
        if cfg.debug_level > 1:
            print("2. Отчет: "+str(new_path))

        return redirect(url_for('uploaded_file', filename=new_path))
    return redirect(url_for('view_model_status', id_model=id_model))


@app.route('/model-status/<int:id_model>/<int:id_calc>/report_0703')
def view_report_0703(id_model, id_calc):
    if cfg.debug_level > 2:
            print("Выдаем отчет расчет! "+str(id_calc))
    if id_calc:
        if cfg.debug_level > 2:
            print("1. Формируем отсчет! ид расчета: "+str(id_calc))
        new_path = rep_unemployment_0703(id_calc)
        if cfg.debug_level > 1:
            print("2. Успешное передача отчета!")
        return redirect(url_for('uploaded_file', filename=new_path))
    return redirect(url_for('view_model_status', id_model=id_model))


@app.route('/model-status/<int:id_model>/<int:id_calc>/report_0702')
def view_report_0702(id_model, id_calc):
    if cfg.debug_level > 2:
        print("Выдаем отчет расчет! "+str(id_calc))
    if id_calc:
        if cfg.debug_level > 2:
            print("1. Формируем отсчет! ид расчета: "+str(id_calc))
        new_path = rep_disability_0702(id_calc)
        if cfg.debug_level > 1:
            print("2. Успешное передача отчета!")
        return redirect(url_for('uploaded_file', filename=new_path))
    return redirect(url_for('view_model_status', id_model=id_model))


@app.route('/model-status/<int:id_model>/<int:id_calc>/report_0701')
def view_report_0701(id_model, id_calc):
    if cfg.debug_level > 2:
        print("Выдаем отчет расчет! "+str(id_calc))
    if id_calc:
        if cfg.debug_level > 2:
            print("1. Формируем отсчет! ид расчета: "+str(id_calc))
        new_path = rep_bread_winner_0701(id_calc)
        if cfg.debug_level > 1:
            print("2. Успешное передача отчета!")
        return redirect(url_for('uploaded_file', filename=new_path))
    return redirect(url_for('view_model_status', id_model=id_model))


@app.route('/model-status/<int:id_model>/<int:id_calc>/report_resume')
def view_report_resume(id_model, id_calc):
    if cfg.debug_level > 2:
        print("Выдаем отчет-расчет! "+str(id_calc))
    if id_calc:
        if cfg.debug_level > 2:
            print("1. Формируем отчет! ид расчета: "+str(id_calc))
        new_path = rep_resume(id_calc)
        if cfg.debug_level > 1:
            print("2. Успешное передача отчета!")
        return redirect(url_for('uploaded_file', filename=new_path))
    return redirect(url_for('view_model_status', id_model=id_model))
