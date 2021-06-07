from db_oracle.connect import get_connection
import config as cfg
import xlsxwriter
import datetime
import os.path


def rep_childcare_0705(id_calc):
	now = datetime.datetime.now()

	file_name = 'childcare_0705_'+str(id_calc)+'.xlsx'
	file_path = cfg.REPORTS_PATH + file_name

	if os.path.isfile(file_path):
		return file_name
	else:
		workbook = xlsxwriter.Workbook(file_path)
		worksheet = workbook.add_worksheet()
		worksheet.set_column(0, 0, 7)
		worksheet.set_column(1, 1, 12)
		worksheet.set_column(2, 2, 10)
		worksheet.set_column(3, 3, 19)

		if cfg.Debug:
			print("Начало расчета по уходу за ребенком : "+now.strftime("%d-%m-%Y %H:%M:%S"))

		con = get_connection()
		cursor = con.cursor()

		if cfg.Debug:
			print("\nНачинаем  формировать отчет для id_calc: "+str(id_calc))
		cursor.execute(
			"select rownum, al.pnpt_id, al.rfpm_id, al.summ_all from model_calculates al where al.id_calc=:id " +
			"and substr(al.rfpm_id,1,4)='0705'", [id_calc])

		common_format = workbook.add_format({'align': 'center'})
		common_format.set_align('valign')
		common_format.set_text_wrap()
		sum_pay_format = workbook.add_format({'num_format': '#,###,##0.00', 'font_color': 'black', 'align': 'vcenter'})

		worksheet.write(0, 0, '№', common_format)
		worksheet.write(0, 1, 'Код назначения выплаты', common_format)
		worksheet.write(0, 2, 'Код выплаты', common_format)
		worksheet.write(0, 3, 'Сумма выплаты', common_format)

		row = 0
		for record in cursor:
			col = 0
			for list_val in record:
				if col < 3:
					worksheet.write(row+1, col, list_val, common_format)
				if col == 3:
					worksheet.write(row+1, col, list_val, sum_pay_format)
				col += 1
			row += 1

		worksheet.write(row+1, 3, "=SUM(D2:D"+str(row+1)+")", sum_pay_format)
		workbook.close()

		now = datetime.datetime.now()

		if cfg.Debug:
			print("Завершен расчет по уходу за ребенком: "+now.strftime("%d-%m-%Y %H:%M:%S"))

		con.commit()
		con.close()
		return file_name
