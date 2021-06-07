from flask import render_template, request, redirect, g
from flask_login import login_required
# from view import app
from model.aktuar_models import *
import cx_Oracle
import config as cfg
#  Не удалять - неправильно красит среда!!!
from view.routes_calc import *

if cfg.debug_level > 0:
    print("Routes стартовал...")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/')
@app.route('/home')
@app.route('/main')
@app.route('/models')
@app.route('/models_list')
def view_models():
    # print("Static folder: " + app.static_folder)
    print("Static folder: " + url_for('static', filename='styles/main_styles.css'))
    return render_template("models_list.html", cursor=models_list())


@app.route('/model_status/<int:id_model>')
@login_required
def view_model_status(id_model):
    return render_template("model_status.html", id_model=id_model, cursor=model_status(id_model))


@app.route('/model_detail/<int:id_model>')
@login_required
def view_model_detail(id_model):
    if cfg.debug_level > 1:
        print("Model_Detail -> Id_Model = " + str(id_model))
    return render_template("model_detail.html", cursor=model_detail(id_model))


@app.route('/model-create', methods=['POST', 'GET'])
@login_required
def view_model_create():
    if cfg.debug_level > 1:
        print("Добавляем модель !")
    if request.method == "POST":
        if cfg.debug_level > 0:
            print("1. Добавляем!")
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        try:
            if cfg.debug_level > 1:
                print("2. Добавляем!")
                print(title + " : " + intro + " : " + text)
            model_create(title, intro, text)
            if cfg.debug_level > 1:
                print("Успешное завершение добавления модели!")
            return redirect('/models_list')
        except cx_Oracle.IntegrityError as e:
            errorObj, = e.args
            if cfg.debug_level > 1:
                print("Error Code:", errorObj.code)
                print("Error Message:", errorObj.message)
                print("При добавлении модели произошла ошибка")
            return redirect("/models_list")
    else:
        if cfg.debug_level > 0:
            print("Вход по GET: goto model-create.html")
        return render_template("model-create.html")


@app.route('/model_detail/<int:id_model>/del')
@login_required
def view_model_delete(id_model):
    try:
        model_delete(id_model)
        return redirect('/models')
    except cx_Oracle.IntegrityError as e:
        errorObj, = e.args
        if cfg.debug_level >= 0:
            print("Error Code:", errorObj.code)
            print("Error Message:", errorObj.message)
            print("Произошла ошибка при удалении модели: " + str(id_model))
        return redirect('/models')


@app.route('/model_detail/<int:id_model>/upd', methods=['POST', 'GET'])
@login_required
def view_model_update(id_model):
    if cfg.debug_level > 0:
        print("Обновляем модель !")
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        if cfg.debug_level > 0:
            print("POST Update Id = " + str(id_model))
        try:
            model_update(id_model, title, intro, text)
            return redirect("/models_list")
        except cx_Oracle.IntegrityError as e:
            errorObj, = e.args
            print("Error Code:", errorObj.code)
            print("Error Message:", errorObj.message)
            print("При обновлении модели произошла ошибка")
            return redirect("/models_list")
    else:
        if cfg.debug_level > 0:
            print("GET Update Id = " + str(id_model))
            print("Id_model = " + str(id_model))
        return render_template("model_update.html", cursor=model_detail(id_model))


@app.route('/user/<string:name>/<int:id_user>')
def user_page(name, id_user):
    return "User: " + name + " : " + str(id_user)


