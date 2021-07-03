from db_oracle.connect import get_connection
import config as cfg
import xlsxwriter
import datetime
import os.path


def rep_resume(id_calc):
    now = datetime.datetime.now()

    file_name = 'resume_' + str(id_calc) + '.xlsx'
    file_path = cfg.REPORTS_PATH + file_name

    if os.path.isfile(file_path):
        return file_name
    else:
        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet('Свод')
        worksheet.set_column(0, 0, 3)
        worksheet.set_column(1, 1, 30)
        worksheet.set_column(2, 2, 12)
        worksheet.set_column(3, 3, 19)

        if cfg.debug_level>2:
            print("Начало сводного расчета: ")

        con = get_connection()
        cursor = con.cursor()

        if cfg.debug_level>2:
            print("\nНачинаем формировать сводный отчет для id_calc: " + str(id_calc) +
                  ",  время: " + now.strftime("%d-%m-%Y %H:%M:%S"))

        cursor.execute("select rownum, case when t.rfpm='0701' then 'По потере кормильца' " +
                       "when t.rfpm='0702' then 'По утрате трудоспособности' " +
                       "when t.rfpm='0703' then 'По потере работы' " +
                       "when t.rfpm='0705' then 'По уходу за ребенком' " +
                       "end rfpm, " +
                       "t.cnt_all, " +
                       "t.sum_all " +
                       "from ( " +
                       "select substr(al.rfpm_id,1,4) rfpm, " +
                       "count(pnpt_id) cnt_all, " +
                       "sum(al.summ_all) sum_all " +
                       "from model_calculates al " +
                       "where al.id_calc=:id " +
                       "and al.calc_type!='W' " +
                       "group by substr(al.rfpm_id,1,4) " +
                       "order by 1 " +
                       ") t", [id_calc])

        common_format = workbook.add_format({'align': 'center'})
        common_format.set_align('vcenter')
        common_format.set_text_wrap()

        first_col_format = workbook.add_format({'align': 'left'})
        first_col_format.set_align('vcenter')

        second_col_format = workbook.add_format({'num_format': '##,###,##0', 'align': 'center'})
        second_col_format.set_align('vcenter')

        sum_pay_format = workbook.add_format({'num_format': '#,###,##0.00 ', 'font_color': 'black', 'align': 'vcenter'})

        worksheet.write(0, 0, '№', common_format)
        worksheet.write(0, 1, 'Выплаты', common_format)
        worksheet.write(0, 2, 'Количество', common_format)
        worksheet.write(0, 3, 'Сумма выплат', common_format)

        row = 0
        for record in cursor:
            col = 0
            for list_val in record:
                if col == 0:
                    worksheet.write(row + 1, col, list_val, common_format)
                if col == 1:
                    worksheet.write(row + 1, col, list_val, first_col_format)
                if col == 2:
                    worksheet.write(row + 1, col, list_val, second_col_format)
                if col == 3:
                    worksheet.write(row + 1, col, list_val, sum_pay_format)
                col += 1
            row += 1

        worksheet.write(row + 1, 3, "=SUM(D2:D" + str(row + 1) + ")", sum_pay_format)
        workbook.close()

        now = datetime.datetime.now()

        if cfg.debug_level>2:
            print("Завершено формирование сводного отчета: " + now.strftime("%d-%m-%Y %H:%M:%S"))

        con.commit()
        con.close()
        return file_name
