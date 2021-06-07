from db_oracle.connect import get_connection
import config as cfg
import xlsxwriter
import datetime
import os.path


def format_worksheet(worksheet, common_format):
	worksheet.set_column(0, 0, 7)
	worksheet.set_column(1, 1, 12)
	worksheet.set_column(2, 2, 10)
	worksheet.set_column(3, 3, 19)

	worksheet.write(0, 0, '№', common_format)
	worksheet.write(0, 1, 'Код назначения выплаты', common_format)
	worksheet.write(0, 2, 'Код выплаты', common_format)
	worksheet.write(0, 3, 'Сумма выплаты', common_format)


def rep_bread_winner_0701(id_calc):
	file_name = 'bread_winner_0701_' + str(id_calc) + '.xlsx'
	file_path = cfg.REPORTS_PATH + file_name

	if os.path.isfile(file_path):
		return file_name
	else:
		con = get_connection()
		cursor = con.cursor()
		workbook = xlsxwriter.Workbook(file_path)

		common_format = workbook.add_format({'align': 'center'})
		common_format.set_align('vcenter')
		common_format.set_text_wrap()
		sum_pay_format = workbook.add_format({'num_format': '#,###,##0.00', 'font_color': 'black', 'align': 'vcenter'})

		now = datetime.datetime.now()
		if cfg.Debug:
			print("Начало формирования отчета по потере кормильца с 1 иждивенцем: "+now.strftime("%d-%m-%Y %H:%M:%S"))
		worksheet = workbook.add_worksheet('1 иждивенец')
		format_worksheet(worksheet=worksheet, common_format=common_format)

		cursor.execute(
			"select rownum, al.pnpt_id, al.rfpm_id, al.summ_all from model_calculates al where al.id_calc=:id " +
			"and substr(al.rfpm_id,1,8)='07010101' and al.calc_type='1'", [id_calc])
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

		now = datetime.datetime.now()
		if cfg.Debug:
			print("Начало формирования отчета по потере кормильца с 2 иждивенцами: " + now.strftime("%d-%m-%Y %H:%M:%S"))
		worksheet = workbook.add_worksheet('2 иждивенца')
		format_worksheet(worksheet=worksheet, common_format=common_format)

		cursor.execute(
			"select rownum, al.pnpt_id, al.rfpm_id, al.summ_all from model_calculates al where al.id_calc=:id " +
			"and substr(al.rfpm_id,1,8)='07010102' and al.calc_type='2'", [id_calc])
		row = 0
		for record in cursor:
			col = 0
			for list_val in record:
				if col < 3:
					worksheet.write(row + 1, col, list_val, common_format)
				if col == 3:
					worksheet.write(row + 1, col, list_val, sum_pay_format)
				col += 1
			row += 1
		worksheet.write(row + 1, 3, "=SUM(D2:D" + str(row + 1) + ")", sum_pay_format)

		now = datetime.datetime.now()
		if cfg.Debug:
			print(
				"Начало формирования отчета по потере кормильца с 3 иждивенцами: " + now.strftime("%d-%m-%Y %H:%M:%S"))
		worksheet = workbook.add_worksheet('3 иждивенца')
		format_worksheet(worksheet=worksheet, common_format=common_format)

		cursor.execute(
			"select rownum, al.pnpt_id, al.rfpm_id, al.summ_all from model_calculates al where al.id_calc=:id " +
			"and substr(al.rfpm_id,1,8)='07010103' and al.calc_type='3'", [id_calc])

		row = 0
		for record in cursor:
			col = 0
			for list_val in record:
				if col < 3:
					worksheet.write(row + 1, col, list_val, common_format)
				if col == 3:
					worksheet.write(row + 1, col, list_val, sum_pay_format)
				col += 1
			row += 1
		worksheet.write(row + 1, 3, "=SUM(D2:D" + str(row + 1) + ")", sum_pay_format)

		now = datetime.datetime.now()
		if cfg.Debug:
			print(
				"Начало формирования отчета по потере кормильца с 4 иждивенцами: " + now.strftime("%d-%m-%Y %H:%M:%S"))
		worksheet = workbook.add_worksheet('4 и более')
		format_worksheet(worksheet=worksheet, common_format=common_format)

		cursor.execute(
			"select rownum, al.pnpt_id, al.rfpm_id, al.summ_all from model_calculates al where al.id_calc=:id " +
			"and substr(al.rfpm_id,1,8)='07010104' and al.calc_type='4'", [id_calc])

		row = 0
		for record in cursor:
			col = 0
			for list_val in record:
				if col < 3:
					worksheet.write(row + 1, col, list_val, common_format)
				if col == 3:
					worksheet.write(row + 1, col, list_val, sum_pay_format)
				col += 1
			row += 1
		worksheet.write(row + 1, 3, "=SUM(D2:D" + str(row + 1) + ")", sum_pay_format)

		workbook.close()
		now = datetime.datetime.now()
		print("Формирование отчета завершено: "+now.strftime("%d-%m-%Y %H:%M:%S"))
		con.commit()
		con.close()
		return file_name
