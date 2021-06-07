from db_oracle.connect import get_connection
from model.models import ModelsF, ModelStatusCalculatedF
from flask import redirect, url_for, request
import config as cfg
import cx_Oracle


def models_list():
    if cfg.debug_level > 0:
        print('List_models ...')
    con = get_connection()
    cursor = con.cursor()
    cursor.execute('select id_model, title, intro, text, dat  from aktuar_models order by 1 desc')
#    cursor.execute('select * from aktuar_models order by 1 desc')
    cursor.rowfactory = ModelsF
    if cfg.debug_level > 0:
        print('Models list have got...')
    return cursor


def model_status(id_model):
    if cfg.debug_level > 0:
        print('Model status ...'+str(id_model))
    con = get_connection()
    cursor = con.cursor()
    cursor.execute('select id_calc, date_calc, id_model, st_0701, st_0702, st_0703, st_0705  from model_status_calculates where id_model=:id order by 1 desc', [id_model])
    cursor.rowfactory = ModelStatusCalculatedF
    if cfg.debug_level > 0:
        print('Model status have got...')
    return cursor


def model_detail(id_model):
    if cfg.debug_level > 0:
        print("Id = " + str(id_model))
    print("Model_Detail -> Id_Model = " + str(id_model))
    con = get_connection()
    cursor = con.cursor()
    cursor.execute('select id_model, title, intro, text, dat  from aktuar_models where id_model=:id order by 1 desc', [id_model])
    cursor.rowfactory = ModelsF
    record = cursor.fetchone()
    if cfg.debug_level > 0:
        print('Model_detail have got...')
    return record


def model_create(title, intro, text):
    if cfg.debug_level > 0:
        print("Model " + title + " : " + intro + " : " + text)
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.callproc('models.model_new', [title, intro, text])
        cursor.close()
        con.close()
        if cfg.debug_level > 0:
            print("Успешное завершение добавления Модели!")
    except cx_Oracle.IntegrityError as e:
        errorObj, = e.args
        print("Error Code:", errorObj.code)
        print("Error Message:", errorObj.message)
        print("При добавлении статьи произошла ошибка")
        return


def model_calc_new(id_model, date_calc):
    if cfg.debug_level > 0:
        print("Model " + str(id_model) + ', date_calc: ' + str(date_calc))
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.callproc('models.model_calc_new', [id_model, date_calc])
        cursor.close()
        con.close()
        if cfg.debug_level > 0:
            print("Успешное завершение добавления расчета Модели!")
        return
    except cx_Oracle.IntegrityError as e:
        errorObj, = e.args
        print("Error Code:", errorObj.code)
        print("Error Message:", errorObj.message)
        print("При добавлении статьи произошла ошибка")
        return redirect(url_for('login_page') + '?next=' + request.url)


def model_calc_del(id_calc):
    if cfg.debug_level > 0:
        print("Model_calc_del. id_calc " + str(id_calc))
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.callproc('models.model_calc_del', [id_calc])
        cursor.close()
        con.close()
        if cfg.debug_level > 0:
            print("Успешное удаление расчета Модели!")
        return
    except cx_Oracle.IntegrityError as e:
        errorObj, = e.args
        print("Error Code:", errorObj.code)
        print("Error Message:", errorObj.message)
        print("При удалении модели произошла ошибка")
        return redirect(url_for('login_page') + '?next=' + request.url)


def model_delete(id_model):
    if cfg.debug_level > 0:
        print("Model_delete. id_model " + str(id_model))
    try:
        con = get_connection()
        cursor = con.cursor()
        cursor.callproc('models.model_del', [id_model])
        cursor.close()
        con.close()
        return
    except cx_Oracle.IntegrityError as e:
        errorObj, = e.args
        print("Error Code:", errorObj.code)
        print("Error Message:", errorObj.message)
        print("Произошла ошибка при удалении Модели: " + str(id_model))
        return


def model_update(id_model, title, intro, text):
    con = get_connection()
    cursor = con.cursor()
    cursor.callproc('models.model_upd', [id_model, title, intro, text])
    if cfg.debug_level > 0:
        print("Успешное обновление!")
    cursor.close()
    con.close()
    return

