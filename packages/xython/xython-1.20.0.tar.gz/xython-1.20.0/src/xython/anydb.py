# -*- coding: utf-8 -*-
import os  # 내장모듈
import sqlite3  # 내장모듈
import pickle  # 내장모듈


import jfinder, scolor, youtil, basic_data  # xython 모듈


import pandas as pd
import numpy as np
from sqlitedict import SqliteDict


class anydb:
	"""
	database를 사용하기 쉽게 만든것
	table, df의 자료는 [제일 첫컬럼에 컬럼이름을 넣는다]
	"""

	def __init__(self, db_name=""):
		self.db_name = db_name
		self.util = youtil.youtil()
		self.color = scolor.scolor()
		self.easyre = jfinder.jfinder()

		self.table_name = ""
		self.con = ""  # sqlite db에 연결되는 것

		self.common_data = basic_data.basic_data()
		self.vars = self.common_data.vars  # 패키지내에서 공통으로 사용되는 변수

		if self.db_name != "":
			self.con = sqlite3.connect(db_name, isolation_level=None)
			self.cursor = self.con.cursor()

		self.check_db_for_sqlite(db_name)

	def append_df1_df2(self, df_obj_1, df_obj_2):
		"""
		dataframe자료의 뒤에 dataframe자료를 추가하는 것

		:param df_obj_1:
		:param df_obj_2:
		:return:
		"""
		result = pd.concat([df_obj_1, df_obj_2])
		return result

	def change_df_to_dic(self, input_df, style="split"):
		"""
		dataframe자료를 사전형식으로 변경하는것
		dic의 형태중에서 여러가지중에 하나를 선택해야 한다

		입력형태 : data = {"calory": [123, 456, 789], "기간": [10, 40, 20]}
		출력형태 : dataframe
		dict :    {'제목1': {'가로제목1': 1, '가로제목2': 3}, '제목2': {'가로제목1': 2, '가로제목2': 4}}
		list :    {'제목1': [1, 2], '제목2': [3, 4]}
		series :  {열 : Series, 열 : Series}
		split :   {'index': ['가로제목1', '가로제목2'], 'columns': ['제목1', '제목2'], 'data': [[1, 2], [3, 4]]}
		records : [{'제목1': 1, '제목2': 2}, {'제목1': 3, '제목2': 4}]
		index :   {'가로제목1': {'제목1': 1, '제목2': 2}, '가로제목2': {'제목1': 3, '제목2': 4}}

		:param input_df:
		:param style:
		:return:

		"""
		checked_style = style
		if not style in ["split", "list", 'series', 'records', 'index']:
			checked_style = "split"
		result = input_df.to_dict(checked_style)
		return result

	def change_df_to_list(self, df_obj):
		"""
		df자료를 커럼과 값을 기준으로 나누어서 결과를 리스트로 돌려주는 것이다

		:param df_obj: dataframe객체
		:return: [[컬럼리스트], [자료1], [자료2]....]
		"""
		col_list = df_obj.columns.values.tolist()
		value_list = df_obj.values.tolist()
		result = [col_list, value_list]
		return result

	def change_dic_to_list_as_col_value_style(self, dic_data):
		"""
		사전의 자료를 sql에 입력이 가능한 형식으로 만드는 것

		:param dic_data:
		:return: [[컬럼리스트], [자료1], [자료2]....]
		"""
		col_list = list(dic_data[0].keys())
		value_list = []
		for one_col in col_list:
			value_list.append(dic_data[one_col])
		result = [col_list, value_list]
		return result

	def change_insert_data_to_dic(self, input_1, input_2=""):
		"""
		입력되는 자료를 사전형식으로 만드는 것
		입력형태 1 : [["컬럼이름1","컬럼이름2"],[["값1-1","값1-2"], ["값2-1","값2-2"]]]
		입력형태 2 : [[["컬럼이름1","값1"],["컬럼이름2","값2"]], [["컬럼이름1","값11"],["컬럼이름3","값22"]]]]
		입력형태 3 : ["컬럼이름1","컬럼이름2"],[["값1-1","값1-2"], ["값2-1","값2-2"]]

		:param input_1:
		:param input_2:
		:return: [{"컬럼이름1":"값1", "컬럼이름2": "값2"}, {"컬럼이름3":"값31", "컬럼이름2": "값33"}......]
		"""
		input_type = 0
		if input_2:
			input_type = 3
		else:
			if type(input_1[0][0]) == type([]):
				input_type = 2
			elif type(input_1[0][0]) != type([]) and type(input_1[1][0]) != type([]):
				input_type = 1

			result = []
			if input_type == 1:
				for value_list_1d in input_1[1]:
					one_line_dic = {}
					for index, column in enumerate(input_1[0]):
						one_line_dic[column] = value_list_1d[index]
					result.append(one_line_dic)
			elif input_type == 2:
				for value_list_2d in input_1:
					one_line_dic = {}
					for index, list_1d in enumerate(value_list_2d):
						one_line_dic[list_1d[0]] = list_1d[1]
					result.append(one_line_dic)
			elif input_type == 3:
				one_line_dic = {}
				for index, list_1d in enumerate(input_2):
					one_line_dic[input_1[index]] = list_1d[index]
				result.append(one_line_dic)

		return result

	def change_list_to_df(self, col_list="", list2d=""):
		"""
		리스트 자료를 dataframe로 만드는것

		:param col_list: 제목리스트
		:param list2d: 2차원 값리스트형
		:return: dataframe로 바꾼것
		"""
		checked_list2d = self.util.change_list1d_to_list2d(list2d)
		# 컬럼의 이름이 없거나하면 기본적인 이름을 만드는 것이다
		checked_col_list = self.check_input_data(col_list, list2d)
		input_df = pd.DataFrame(data=checked_list2d, columns=checked_col_list)
		return input_df

	def change_sqlite_table_data_to_df(self, table_name, db_name=""):
		"""
		sqlite의 테이블을 df로 변경

		:param table_name: 테이블 이름
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)
		sql = "SELECT * From {}".format(table_name)
		sql_result = self.cursor.execute(sql)
		cols = []
		for column in sql_result.description:
			cols.append(column[0])
		input_df = pd.DataFrame.from_records(data=sql_result.fetchall(), columns=cols)
		return input_df

	def change_sqlite_table_data_to_list(self, table_name, db_name=""):
		"""
		sqlite의 테이블 자료를 리스트로 변경

		:param table_name: 테이블 이름
		:param db_name: 데이터베이스 이름
		:return: [2차원리스트(제목), 2차원리스트(값들)]
		"""
		self.check_db_for_sqlite(db_name)
		sql_result = self.cursor.execute("SELECT * From {}".format(table_name))
		cols = []
		for column in sql_result.description:
			cols.append(column[0])
		temp = []
		for one in sql_result.fetchall():
			temp.append(list(one))
		result = [cols, temp]
		return result

	def change_table_name_for_sqlite(self, table_name_old, table_name_new, db_name=""):
		"""
		현재 db에서 테이블 이름 변경

		:param table_name_old:
		:param table_name_new:
		:param db_name: 데이터베이스 이름
		:return:
		"""

		self.check_db_for_sqlite(db_name)
		sql_sentence = "alter table %s rename to %s" % (table_name_old, table_name_new)
		self.cursor.execute(sql_sentence)

	def check_yname(self, yname):
		"""
		컬럼의 이름으로 쓰이는 것에 이상한 글자들이 들어가지 않도록 확인하는 것이다

		:param yname: y 컬럼이름
		:return:
		"""
		for data1, data2 in [["'", ""], ["/", ""], ["\\", ""], [".", ""], [" ", "_"]]:
			yname = yname.replace(data1, data2)
		return yname

	def check_db_for_sqlite(self, db_name=""):
		"""
		기본적으로 test_db.db를 만든다
		memory로 쓰면, sqlite3를 메모리에 넣도록 한다

		:param db_name: 데이터베이스 이름
		:return:
		"""
		if db_name == "" or db_name == "memory":
			self.con = sqlite3.connect(":memory:")
		elif db_name == "" or db_name == "test":  # 데이터베이스를 넣으면 화일로 만든다
			db_name = "test_db.db"
			self.con = sqlite3.connect(db_name, isolation_level=None)
		else:
			self.con = sqlite3.connect(db_name, isolation_level=None)
		self.cursor = self.con.cursor()

	def check_db_name_in_folder_for_sqlite(self, db_name="", path="."):
		"""
		경로안에 sqlite의 database가 있는지 확인하는 것이다
		database는 파일의 형태이므로 폴더에서 화일이름들을 확인한다

		:param db_name: 데이터베이스 이름
		:param path: 경로
		:return:
		"""
		db_name_all = self.util.read_all_filename_in_folder(path)
		if db_name in db_name_all:
			result = db_name
		else:
			result = ""
		return result

	def check_input_data(self, col_list, data_list):
		"""
		컬럼의 이름이 없으면, 'col+번호'로 컴럼이름을 만드는 것

		:param col_list: y컴럼의 이름들
		:param data_list:
		:return:
		"""
		result = []
		# 컬럼의 이름이 없거나하면 기본적인 이름을 만드는 것이다
		if col_list == "" or col_list == []:
			for num in range(len(data_list)):
				result.append("col" + str(num))
		else:
			result = col_list
		return result

	def check_range_in_df(self, input_value):
		"""
		개인적으로 만든 이용형태를 것으로,
		check로 시작하는 메소드는 자료형태의 변경이나 맞는지를 확인하는 것이다
		dataframe의 영역을 나타내는 방법을 dataframe에 맞도록 변경하는 것이다
		x=["1:2", "1~2"] ===> 1, 2열
		x=["1,2,3,4"] ===> 1,2,3,4열
		x=[1,2,3,4]  ===> 1,2,3,4열
		x=""또는 "all" ===> 전부

		:param input_value:
		:return:
		"""
		one = ""
		if ":" in input_value:
			pass
		elif "~" in input_value:
			one = input_value.replace("~", ":")
			print("======> ", one)
			one = "[" + one + "]"
		elif "all" in input_value:
			one = input_value.replace("all", ":")
			one = "[" + one + "]"
		elif "" in input_value:
			one = input_value.replace("all", ":")
			one = "[" + one + "]"
		return one

	def check_x_index_in_df(self, df_obj, input_index):
		"""
		index가 기본 index인 0부터 시작하는 것이 아닌 어떤 특정한 제목이 들어가 있는경우는
		숫자로 사용할수가 없다. 그래서 그서을 확인후에 기본 index가 아닌경우는 제목으로 변경해 주는
		것을 할려고 한다
		"2~3"  ===>  '인천':'대구'

		:param df_obj: dataframe객체
		:param input_index:
		:return:
		"""
		type_result = "int"
		index_list = df_obj.index
		if len(index_list) > 5:
			for index, one in enumerate(index_list[0:5]):
				if one != index:
					type_result = "string"
		else:
			for index, one in enumerate(index_list):
				if one != index:
					type_result = "string"

		result = input_index
		if ":" == input_index or "all" == input_index or "" == input_index:
			result = ":"
		elif ":" in input_index or "~" in input_index:
			input_index = input_index.replace("~", ":")
			two_data = str(input_index).split(":")
			try:
				if type(int(two_data[0])) == type(1) and type(int(two_data[1])) == type(1):
					if int(two_data[1]) >= len(index_list):
						result = "'" + str(index_list[int(two_data[0])]) + "':"
					else:
						result = "'" + str(index_list[int(two_data[0])]) + "':'" + str(
							index_list[int(two_data[1])]) + "'"
			except:
				result = input_index
		print(input_index, " ===> ", result)
		return result

	def check_y_index_in_df(self, df_obj, input_index):
		"""
		index가 기본 index인 0부터 시작하는 것이 아닌 어떤 특정한 제목이 들어가 있는경우는
		숫자로 사용할수가 없다. 그래서 그것을 확인후에 기본 index가 아닌경우는 제목으로 변경해 주는
		것을 할려고 한다
		"2~3"  ===>  '인천':'대구'

		:param df_obj: dataframe객체
		:param input_index:
		:return:
		"""
		type_result = "int"
		index_list = df_obj.columns
		if len(index_list) > 5:
			for index, one in enumerate(index_list[0:5]):
				if one != index:
					type_result = "string"
		else:
			for index, one in enumerate(index_list):
				if one != index:
					type_result = "string"

		result = input_index
		if ":" == input_index or "all" == input_index or "" == input_index:
			result = ":"
		elif ":" in input_index or "~" in input_index:
			input_index = input_index.replace("~", ":")
			two_data = str(input_index).split(":")
			try:
				if type(int(two_data[0])) == type(1) and type(int(two_data[1])) == type(1):
					if int(two_data[1]) >= len(index_list):
						result = "'" + str(index_list[int(two_data[0])]) + "':"
					else:
						result = "'" + str(index_list[int(two_data[0])]) + "':'" + str(
							index_list[int(two_data[1])]) + "'"
			except:
				result = input_index
		print(input_index, " ===> ", result)
		return result

	def connect_db_for_sqlite(self, db_name=""):
		"""
		database에 연결하기

		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)

	def delete_empty_yline_in_df(self, input_df):
		"""
		dataframe의 빈열을 삭제
		제목이 있는 경우에만 해야 문제가 없을것이다

		:param input_df:
		:return:
		"""
		nan_value = float("NaN")
		input_df.replace(0, nan_value, inplace=True)
		input_df.replace("", nan_value, inplace=True)
		input_df.dropna(how="all", axis=1, inplace=True)
		return input_df

	def delete_empty_yline_in_table_for_sqlite(self, table_name, db_name=""):
		"""
		테이블의 컬럼중에서 아무런 값도 없는 컬럼을 삭제한다

		:param table_name: 테이블 이름
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)
		yname_all = self.read_all_yname_in_table_for_sqlite(table_name, db_name)

		for yname in yname_all:
			sql = ("select COUNT(*) from %s where %s is not null" % (table_name, yname))
			self.cursor.execute(sql)
			if self.cursor.fetchall()[0][0] == 0:
				# 입력값이 없으면 0개이고, 그러면 삭제를 하는 것이다
				sql = ("ALTER TABLE %s DROP COLUMN %s " % (table_name, yname))
				self.cursor.execute(sql)

	def delete_memory_db_for_sqlite(self):
		"""
		memory db는 connection을 close시키면, db가 삭제된다

		:return:
		"""
		self.con.close()

	def delete_table_for_sqlite(self, table_name, db_name=""):
		"""
		입력형태 : 테이블이름

		:param table_name: 테이블 이름
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)
		self.cursor.execute("DROP TABLE " + table_name)

	def delete_yline_in_list_db_by_index(self, input_list_db, input_index_list=[1, 2, 3]):
		"""
		index번호를 기준으로 y라인을 삭제하는것
		list_db의 형태 : [[y_name-1, y_name_2.....],[[a1, a2, a3...], [b1, b2, b3...], ]]

		:param input_list_db:
		:param input_index_list:
		:return:
		"""
		# 맨뒤부터 삭제가 되어야 index가 유지 된다
		checked_input_index_list = input_index_list.reverse()

		for index in checked_input_index_list:
			# y열의 제목을 지우는것
			input_list_db[0].pop(index)

			# 각 항목의 값을 지우는것
			for num in range(len(input_list_db[1])):
				input_list_db[1][num].pop(index)
		return input_list_db

	def delete_yline_in_list_db_by_name(self, input_list_db, input_name_list=["y_name_1, y_name_2"]):
		"""
		y라인 이름을 기준으로 삭제하는것
		list_db의 형태 : [[y_name-1, y_name_2.....],[[a1, a2, a3...], [b1, b2, b3...], ]]

		:param input_list_db:
		:param input_name_list:
		:return:
		"""

		title_dic = {}
		for index in range(len(input_list_db[0])):
			title_dic[input_list_db[0][index]] = index

		input_index_list = []

		for name in input_name_list:
			index = title_dic[name]
			input_index_list.append(index)

		# 맨뒤부터 삭제가 되어야 index가 유지 된다
		result = self.delete_yline_in_list_db_by_index(input_list_db, input_index_list)
		return result

	def delete_yline_in_table_by_yname_for_sqlite(self, table_name, yname_list, db_name=""):
		"""
		컬럼 삭제
		입력형태 : ["col_1","col_2","col_3"]
		yname : 컬럼이름

		:param table_name: 테이블 이름
		:param yname_list:
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)

		if yname_list:
			for yname in yname_list:
				sql = ("ALTER TABLE %s DROP COLUMN %s " % (table_name, yname))
				self.cursor.execute(sql)

	def get_all_y_name_in_table_for_sqlite(self, table_name, db_name=""):
		"""
		해당하는 테이의 컬럼구조를 갖고온다
		입력형태 : 테이블이름
		출력형태 : 컬럼이름들

		:param table_name: 테이블 이름
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)

		self.cursor.execute("PRAGMA table_info('%s')" % table_name)
		sql_result = self.cursor.fetchall()
		result = []
		for one_list in sql_result:
			result.append(one_list[1])
		return result

	def get_columns_data_from_no1_to_no2_in_table_for_sqlite(self, table_name, offset=0, row_count=100, db_name=""):
		"""
		테이블의 자료중 원하는 갯수만 읽어오는 것

		:param table_name: 테이블 이름
		:param offset:
		:param row_count:
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)

		self.cursor.execute(("select * from %s LIMIT %s, %s;") % (table_name, str(offset), str(row_count)))
		result = self.cursor.fetchall()
		return result

	def get_all_db_name_in_path(self, path=".\\"):
		"""
		모든 database의 이름을 갖고온다
		모든이 붙은것은 맨뒤에 all을 붙인다

		:param path: 경로
		:return:
		"""
		result = []
		for fname in os.listdir(path):
			if fname[-3:] == ".db":
				result.append(fname)
		return result

	def get_property_for_y_line_all_in_table_for_sqlite(self, table_name, db_name=""):
		"""
		해당하는 테이블의 컬럼의 모든 구조를 갖고온다

		:param table_name: 테이블 이름
		:param db_name: 데이터베이스 이름
		:return:
		"""

		self.check_db_for_sqlite(db_name)

		self.cursor.execute("PRAGMA table_info('%s')" % table_name)
		result = []
		for temp_2 in self.cursor.fetchall():
			result.append(temp_2)
		return result

	def insert_column_in_sqlite_memory_db(self, table_name, col_data_list_s):
		"""
		memory db에 새로운 컬럼을 넣는다

		:param table_name: 테이블 이름
		:param col_data_list_s:
		:return:
		"""

		# 기존의 테이블의 컬럼이름들을 갖고온다
		all_exist_yname = self.read_all_column_in_sqlite(table_name)

		for one_list in col_data_list_s:
			if type(one_list) == type([]):
				yname = self.check_yname(one_list[0])
				col_type = one_list[1]
			else:
				yname = self.check_yname(one_list)
				col_type = "text"
			if not yname in all_exist_yname:
				self.cursor.execute("alter table %s add column '%s' '%s'" % (table_name, yname, col_type))

	def insert_y_title_in_df(self, df_obj, input_data):
		"""
		df_obj.rename(columns={0: 'TEST', 1: 'ODI', 2: 'T20'}, inplace=True)
		df = pd.DataFrame(data, columns=list_1d)

		:param df_obj: dataframe객체
		:param input_data:
		:return:
		"""
		checked_changed_data = input_data
		if type(input_data) == type({}):
			# {0: 'TEST', 1: 'ODI', 2: 'T20'}
			checked_changed_data = input_data
		elif type(input_data[0]) == type([]) and len(input_data) == 1:
			# 이자료를 [["기존", "바꿀이름"], ["b", "bb"], ["c", "cc"]]
			checked_changed_data = {}
			for one in input_data:
				checked_changed_data[one[0]] = one[1]
		elif type(input_data[0]) == type([]) and len(input_data) == 2:
			# 이자료를 [["기존1", "기존2", "기존3", "기존3"], ["바꿀이름1", "바꿀이름2", "바꿀이름3", "바꿀이름3"]]
			checked_changed_data = {}
			for index, one in enumerate(input_data):
				checked_changed_data[input_data[index]] = input_data[index]
		elif type(input_data[0]) != type([]) and type(input_data) == type([]):
			# 이자료를 ["바꿀이름1", "바꿀이름2", "바꿀이름3", "바꿀이름3"]
			checked_changed_data = {}
			for index, one in enumerate(input_data):
				checked_changed_data[index] = input_data[index]
		df_obj.rename(columns=checked_changed_data, inplace=True)
		return df_obj

	def insert_yline_in_list_db(self, input_list_db, input_yname, input_yline_data):
		"""
		맨끝에, 리스트형태의 자료를 세로열을 하나 추가하는 것

		:param input_list_db:
		:param input_yname: 세로열의 이름
		:param input_yline_data: 세로열을 위한 자료
		:return:
		"""
		input_list_db[0].append(input_yname)
		input_list_db[1].append(input_yline_data)
		return input_list_db

	def insert_yline_in_list_db_by_index(self, input_list_db, input_yname, input_yline_data, input_index):
		"""
		index번호 위치에, 리스트형태의 자료를 세로열을 하나 추가하는 것

		:param input_list_db:
		:param input_yname:
		:param input_yline_data:
		:param input_index:
		:return:
		"""
		input_list_db[0].insert(input_index, input_yname)
		input_list_db[1].insert(input_index, input_yline_data)
		return input_list_db

	def insert_yyline_in_table_for_sqlite(self, table_name, col_data_list_s, db_name=""):
		"""
		(여러줄) 새로운 새로 컬럼을 만든다
		col_data_list_s : [["이름1","int"],["이름2","text"]]
		["이름2",""] => ["이름2","text"]
		1차원리스트가 오면, 전부 text로 만든다

		:param table_name: 테이블 이름
		:param col_data_list_s:
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)

		for one_list in col_data_list_s:
			if type(one_list) == type([]):
				yname = self.check_yname(one_list[0])
				col_type = one_list[1]
			else:
				yname = self.check_yname(one_list)
				col_type = "text"
			self.cursor.execute("alter table %s add column '%s' '%s'" % (table_name, yname, col_type))

	def is_y_names(self, input_list):
		"""
		입력으로 들어온 1 차원 리스트자료가 컬럼이름으로 사용되는것인지 아닌지 확인하는것

		:param input_list:
		:return:
		"""
		result = 1
		result_empty = 0
		result_date_int = 0
		for one_value in input_list:
			if one_value == None or one_value == "":
				result_empty = result_empty + 1
			if type(one_value) == type(1):
				result_date_int = result_date_int + 1
			if result_empty > 0 or result_date_int > 0:
				result = 0
		return result

	def make_cursor_for_sqlite_db(self, db_name=""):
		"""
		커서를 만드는 것
		:param db_name:
		:return:
		"""
		self.check_db_for_sqlite(db_name)

	def make_sql_text_for_dic_data(self, table_name, dic_data):
		"""
		(sql구문 만들기) 사전형의 자료를 기준으로 sql구문 만들기

		:param table_name: 테이블 이름
		:param dic_data: 사전형 자료
		:return:
		"""

		sql_columns = ""
		sql_values = ""
		for one_key in dic_data.keys():
			value = dic_data[one_key]
			sql_columns = sql_columns + str(one_key) + ", "
			if value == None:
				sql_values = sql_values + str(value) + ", "
			elif type(value) == type(123) or type(value) == type(123.4):
				sql_values = sql_values + str(value) + ", "
			else:
				sql_values = sql_values + "'" + str(value) + "', "
		result = "insert into %s (%s) values (%s)" % (table_name, sql_columns[:-2], sql_values[:-2])
		return result

	def make_sql_text_for_insert_by_ynames(self, table_name, col_list):
		"""
		(sql구문 만들기) 컬럼이름을 추가하기위하여 sql구문 만들기

		:param table_name: 테이블 이름
		:param col_list: y컬럼 이름들
		:return:
		"""
		sql_columns = self.util.change_list1d_to_text_with_chainword(col_list, ", ")
		sql_values = "?," * len(col_list)
		result = "insert into %s (%s) values (%s)" % (table_name, sql_columns, sql_values[:-1])
		return result


	def new_db_for_sqlite(self, db_name=""):
		"""
		(새로운 db 만들기) 새로운 데이터베이스를 만든다
		db_name이 이미 있으면 연결되고, 없으면 새로 만듦
		입력형태 : 이름

		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)

	def new_memory_db_for_sqlite(self):
		"""
		(새로운 메모리 db만들기)
		self.cursor.execute("CREATE TABLE " + self.table_name + " (auto_no integer primary key AUTOINCREMENT)")
		memory에 생성하는 것은 바로 connection 이 만들어 진다

		:return:
		"""
		self.check_db_for_sqlite(":memory:")

	def new_table_for_sqlite_memory_db(self, table_name):
		"""
		(새로운 테이블 만들기) 메모리db에 새로운 테이블 만들기

		:param table_name: 테이블 이름
		:return:
		"""
		self.cursor.execute("CREATE TABLE IF NOT EXISTS " + table_name + "(number integer)")

		all_table_name = []
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
		sql_results = self.cursor.fetchall()
		for one in sql_results:
			all_table_name.append(one[0])
		print("모든 테이블 이름 ==> ", all_table_name)

	def new_table_in_db_for_sqlite(self, table_name, db_name=""):
		"""
		(새로운 테이블 만들기) database는 먼저 선택해야 한다
		새로운 테이블을 만든다
		입력형태 : 테이블이름

		:param table_name: 테이블 이름
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)
		# 현재 db안의 테이블에 같은 이름이 없는지 확인 하는 것
		tables = []
		self.cursor.execute("select name from sqlite_master where type = 'table'; ")
		all_table_name = self.cursor.fetchall()
		if not table_name in all_table_name:
			self.cursor.execute("CREATE TABLE " + table_name + " (Item text)")

	def new_table_with_yline_for_sqlite(self, table_name, column_data_list, db_name=""):
		"""
		(새로운 테이블 만들기) 어떤 형태의 자료가 입력이 되어도 테이블을 만드는 sql을 만드는 것이다
		입력형태 1 : 테이블이름, [['번호1',"text"], ['번호2',"text"],['번호3',"text"],['번호4',"text"]]
		입력형태 2 : 테이블이름, ['번호1','번호2','번호3','번호4']
		입력형태 3 : 테이블이름, [['번호1',"text"], '번호2','번호3','번호4']

		:param table_name: 테이블 이름
		:param column_data_list:
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)

		sql_1 = "CREATE TABLE IF NOT EXISTS {}".format(table_name)
		sql_2 = sql_1 + " ("
		for one_list in column_data_list:
			if type(one_list) == type([]):
				if len(one_list) == 2:
					yname = one_list[0]
					col_type = one_list[1]
				elif len(one_list) == 1:
					yname = one_list[0]
					col_type = "text"
			elif type(one_list) == type("string"):
				yname = one_list
				col_type = "text"
			sql_2 = sql_2 + "{} {}, ".format(yname, col_type)
		sql_2 = sql_2[:-2] + ")"
		self.cursor.execute(sql_2)
		return sql_2

	def read_all_yname_for_sqlite_memory_db(self, table_name):
		"""
		(모든 컬럼 이름) 모든 컬럼의 이름을 갖고오는 것, 메모리 db

		:param table_name: 테이블 이름
		:return:
		"""
		self.cursor.execute("PRAGMA table_info('%s')" % table_name)
		sql_result = self.cursor.fetchall()
		result = []
		for one_list in sql_result:
			result.append(one_list[1])
		return result

	def read_all_yname_in_table_for_sqlite(self, table_name, db_name=""):
		"""
		(모든 컬럼 이름) 현재 있는 테이블의 이름에 특수문자들을 지우는 것이다
		공백을 _로 변경하는것, Column의 이름을 변경한다

		:param table_name: 테이블 이름
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)

		all_ynames = self.read_all_yname_in_table_for_sqlite(table_name, db_name)
		for yname in all_ynames:
			yname_new = self.check_yname(yname)
			if not yname_new == yname:
				self.cursor.execute("alter table {} RENAME COLUMN {} to {}".format(table_name, yname, yname_new))

	def read_all_yname_in_table_for_sqlite(self, table_name):
		"""
		(모든 컬럼 이름) 기존의 테이블의 컬럼이름들을 갖고온다

		:param table_name: 테이블 이름
		:return:
		"""
		self.cursor.execute("PRAGMA table_info('%s')" % table_name)
		sql_result = self.cursor.fetchall()
		all_exist_yname = []
		for one_list in sql_result:
			all_exist_yname.append(one_list[1])
		return all_exist_yname

	def read_all_table_data_for_sqlite(self, table_name, db_name=""):
		"""
		(테이블의 모든 값) 테이블의 모든 자료를 읽어온다
		입력형태 : 테이블 이름

		:param table_name: 테이블 이름
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)
		self.cursor.execute(("select * from {}").format(table_name))
		result = self.cursor.fetchall()
		return result

	def read_all_table_name_in_db_for_sqlite(self, db_name=""):
		"""
		(모든 테이블 이름들) 해당하는 테이의 컬럼구조를 갖고온다
		입력형태 : 데이터베이스 이름
		출력형태 : 테이블이름들

		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)
		self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
		result = []
		for temp_2 in self.cursor.fetchall():
			result.append(temp_2[0])
		return result

	def read_data_by_xy_for_sqlite_memory_db(self, table_name, x_no, y_no):
		"""
		(한개의 값)메모리db의 x번째, y번째의 값

		:param table_name: 테이블 이름
		:param x_no:
		:param y_no:
		:return:
		"""
		sql = f"select * from {table_name} where x = {x_no} and y = {y_no}"
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		return result

	def read_data_with_yname_by_xy_for_sqlite_memory_db(self, table_name, x_no, y_no):
		"""
		(한개의 값) 메모리db의 x번째, y번째의 값과 컬럼이름

		:param table_name: 테이블 이름
		:param x_no:
		:param y_no:
		:return:
		"""
		sql = f"select * from {table_name} where x = {x_no} and y = {y_no}"
		self.cursor.execute(sql)
		result = {}
		names = [description[0] for description in self.cursor.description]
		rows = self.cursor.fetchall()
		if rows == []:
			result = {}
		else:
			for row in rows:
				for name, val in zip(names, row):
					result[name] = val
		return result

	def read_data_with_yname_by_xy_for_sqlite_memory_db_except_none_data(self, table_name, x_no, y_no):
		"""
		메모리db의 x번째, y번째의 값과 컬럼이름, 단 None값은 제외한다

		:param table_name: 테이블 이름
		:param x_no:
		:param y_no:
		:return:
		"""
		sql = f"select * from {table_name} where x = {x_no} and y = {y_no}"
		self.cursor.execute(sql)
		result = {}
		names = [description[0] for description in self.cursor.description]
		rows = self.cursor.fetchall()
		for row in rows:
			for name, val in zip(names, row):
				if val != None:
					result[name] = val
		return result

	def read_all_table_data_as_dic_style_for_sqlite(self, table_name):
		"""
		(테이블의 모든 값) 사전형식으로 돌려줌

		:param table_name: 테이블 이름
		:return:
		"""
		sql = f"select * from {table_name}"
		self.cursor.execute(sql)
		names = [description[0] for description in self.cursor.description]

		result = []
		all_lines = self.cursor.fetchall()
		for one_line in all_lines:
			temp = {}
			for index, value in enumerate(one_line):
				temp[names[index]] = value
			result.append(temp)
		return result

	def read_all_table_data_as_dic_style_for_sqlite_except_none(self, table_name):
		"""
		(테이블의 모든 값) 사전형식으로 돌려줌, 단 None값은 제외한다

		:param table_name: 테이블 이름
		:return:
		"""
		sql = f"select * from {table_name}"
		self.cursor.execute(sql)
		names = [description[0] for description in self.cursor.description]
		result = {}
		all_lines = self.cursor.fetchall()
		print(all_lines[-1])
		for one_line in all_lines:
			temp = {}
			for index, value in enumerate(one_line):
				if value:
					temp[names[index]] = value
			if temp["x"] in result.keys():
				result[temp["x"]][temp["y"]] = temp
			else:
				result[temp["x"]] = {}
				result[temp["x"]][temp["y"]] = temp
		# print(result)
		return result

	def read_table_data_by_ynames_at_sqlite(self, yname_s="", condition="all", db_name=""):
		"""
		컬럼이름으로 테이블 값을 갖고오기, 문자는 컬럼이름으로, 숫자는 몇번째인것으로...

		:param yname_s:
		:param condition:
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)
		if yname_s == "":
			sql_columns = "*"
		else:
			sql_columns = self.util.change_list1d_to_text_with_chainword(yname_s, ", ")

		if condition == "all":
			lim_no = 100
		else:
			lim_no = condition
		limit_text = "limit {}".format(lim_no)
		sql = "SELECT {} FROM {} ORDER BY auto_no {}".format(sql_columns, self.table_name, limit_text)
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		return result

	def read_value_by_name_in_df(self, df_obj, x, y):
		"""
		(dataframe의 1개의 값 읽어오기)
		열이나 행의 이름으로 pandas의 dataframe의 일부를 불러오는 것이다
		이것은 리스트를 기본으로 사용한다
		list_x=["가"~"다"] ===> "가"~"다"열
		list_x=["가","나","다","4"] ===> 가,나,다, 4 열
		x=""또는 "all" ===> 전부

		:param df_obj: dataframe객체
		:param x:
		:param y:
		:return:
		"""

		temp = []
		for one in [x, y]:
			if ":" in one[0]:
				changed_one = one[0]
			elif "~" in one[0]:
				ed_one = one[0].split("~")
				changed_one = "'" + str(ed_one[0]) + "'" + ":" + "'" + str(ed_one[1]) + "'"

			elif "all" in one[0]:
				changed_one = one[0].replace("all", ":")
			else:
				changed_one = one
			temp.append(changed_one)
		# 이것중에 self를 사용하지 않으면 오류가 발생한다
		print(temp)
		exec("self.result = df_obj.loc[{}, {}]".format(temp[0], temp[1]))
		return self.result

	def read_value_by_xy_in_df(self, df_obj, xy=[0, 0]):
		"""
		(dataframe의 1개의 값 읽어오기)
		위치를 기준으로 값을 읽어오는 것이다
		숫자를 넣으면 된다

		:param df_obj: dataframe객체
		:param xy:
		:return:
		"""
		result = df_obj.iat[int(xy[0]), int(xy[1])]
		return result

	def read_x_headers_in_df(self, df_obj, x_no=""):
		"""
		컬럼의 x의 index를 읽어오는 것이다

		:param df_obj: dataframe객체
		:param x_no:
		:return:
		"""
		result = df_obj.index
		if x_no != "":
			result = result[x_no]
		return result

	def read_xx_lines_in_df(self, df_obj, x):
		"""
		x의 라인들을 읽어온다

		:param df_obj: dataframe객체
		:param x:
		:return:
		"""

		x_list = self.check_x_index_in_df(df_obj, x)
		exec("self.result = df_obj.loc[{}, {}]".format(x_list, ":"))
		return self.result

	def read_xxyy_lines_in_df(self, df_obj, x, y=""):
		"""
		숫자번호로 pandas의 dataframe의 일부를 불러오는 것
		단, 모든것을 문자로 넣어주어야 한다
		x=["1:2", "1~2"] ===> 1, 2열
		x=["1,2,3,4"] ===> 1,2,3,4열
		x=[1,2,3,4]  ===> 1,2,3,4열
		x=""또는 "all" ===> 전부

		:param df_obj: dataframe객체
		:param x:
		:param y:
		:return:
		"""

		x_list = self.check_x_index_in_df(df_obj, x)
		y_list = self.check_y_index_in_df(df_obj, y)
		print(x_list, y_list)
		exec("self.result = df_obj.loc[{}, {}]".format(x_list, y_list))
		return self.result

	def read_value_by_xyxy_in_df(self, df_obj, xyxy):
		"""
		4각 영역의 번호위치의 값을 읽어오기

		:param df_obj: dataframe객체
		:param xyxy:
		:return:
		"""

		x11, y11, x22, y22 = xyxy

		x1 = min(x11, x22)
		x2 = max(x11, x22)
		y1 = min(y11, y22)
		y2 = max(y11, y22)

		x = str(x1) + ":" + str(x2)
		if x == "0:0":    x = ":"
		y = str(y1) + ":" + str(y2)
		if y == "0:0":    y = ":"

		x_list = self.check_x_index_in_df(df_obj, x)
		y_list = self.check_y_index_in_df(df_obj, y)
		print(x_list, y_list)
		exec("self.result = df_obj.loc[{}, {}]".format(x_list, y_list))
		return self.result

	def read_y_headers_in_df(self, df_obj, y_no=""):
		"""
		컬럼의 y의 컬럼 제목을 읽어오는 것이다

		:param df_obj: dataframe객체
		:param y_no:
		:return:
		"""
		result = df_obj.columns
		if y_no != "":
			result = result[y_no]
		return result

	def read_yy_lines_in_df(self, df_obj, y):
		"""
		y의 라인들을 읽어온다

		:param df_obj: dataframe객체
		:param y:
		:return:
		"""
		y_list = self.check_y_index_in_df(df_obj, y)
		exec("self.result = df_obj.loc[{}, {}]".format(":", y_list))
		return self.result

	def run_sql_for_sqlite(self, sql, db_name=""):
		"""
		sqlite의 sql문을 실행하는 것이다
		fetchall는
		첫번째 : (1, '이름1', 1, '값1')
		두번째 : (2, '이름2', 2, '값2')

		:param sql:
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		self.con.commit()
		return result

	def run_sql_for_sqlite_memory_db(self, sql):
		"""
		(sql실행) sql실행

		:param sql:
		:return:
		"""
		self.cursor.execute(sql)
		result = self.cursor.fetchall()
		self.con.commit()
		return result

	def save_sqlite_memory_db_to_disk_db(self, db_name=""):
		"""
		memory에 저장된것을 화일로 저장하는것
		python 3.7부터는 backup이 가능

		:param db_name: 데이터베이스 이름
		:return:
		"""
		db_disk = sqlite3.connect(db_name)
		self.con.backup(db_disk)

	def set_database(self, db_name=""):
		"""

		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)

	def set_database_for_sqlite(self, db_name=""):
		"""
		db만들기

		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)


	def write_all_table_data_for_sqlite_to_df(self, table_name, db_name=""):
		"""
		sqlite를 df로 만드는것

		:param table_name: 테이블 이름
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)
		sql = "SELECT * From %s" % (table_name)
		query = self.cursor.execute(sql)
		cols = [column[0] for column in query.description]
		input_df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
		return input_df

	def write_data_in_table_for_sqlite(self, table_name, yname_s, col_value_s, db_name=""):
		"""
		값쓰기

		:param table_name: 테이블 이름
		:param yname_s:
		:param col_value_s:
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)
		sql_columns = ""
		sql_values = ""
		for column_data in yname_s:
			sql_columns = sql_columns + column_data + ", "
			sql_values = "?," * len(yname_s)
		sql = "insert into %s(%s) values (%s)" % (table_name, sql_columns[:-2], sql_values[:-1])
		if type(col_value_s[0]) == type([]):
			self.cursor.executemany(sql, col_value_s)
		else:
			self.cursor.execute(sql, col_value_s)
		self.con.commit()

	def write_df_data_to_excel(self, input_df, xy=[1, 1]):
		"""
		df자료를 커럼과 값을 기준으로 나누어서 결과를 돌려주는 것이다

		:param input_df:
		:param xy:
		:return:
		"""
		col_list = input_df.columns.values.tolist()
		value_list = input_df.values.tolist()
		excel = pcell.pcell()
		excel.write_list1d_in_yline("", xy, col_list)
		excel.write_value_in_range_as_speedy("", [xy[0] + 1, xy[1]], value_list)

	def write_df_data_to_sqlite(self, table_name, df_data, db_name=""):
		"""
		df자료를 sqlite에 새로운 테이블로 만들어서 넣는 것

		:param table_name: 테이블 이름
		:param df_data:
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)
		df_data.to_sql(table_name, self.con)

	def write_dic_data_to_sqlite(self, table_name, input_dic, db_name=""):
		"""
		사전형식의 값을 sqlite에 입력하는 것

		:param table_name: 테이블 이름
		:param input_dic:
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)

		for one_col in list(input_dic[0].keys()):
			if not one_col in self.read_all_yname_in_table_for_sqlite(table_name, db_name):
				self.insert_yyline_in_table_for_sqlite(table_name, [one_col], db_name)

		sql = self.make_sql_text_for_insert_by_ynames(table_name, list(input_dic[0].keys()))
		value_list = []
		for one_dic in input_dic:
			value_list.append(list(one_dic.values()))
		self.cursor.executemany(sql, value_list)

	def write_list_1d_data_to_sqlite(self, table_name, yname_s, input_list_1d, db_name=""):
		"""
		리스트의 형태로 넘어오는것중에 y이름과 값을 분리해서 얻는 것이다

		:param table_name: 테이블 이름
		:param yname_s:
		:param list_1d:
		:param db_name: 데이터베이스 이름
		:return:
		"""
		self.check_db_for_sqlite(db_name)
		sql = self.make_sql_text_for_insert_by_ynames(table_name, yname_s)
		self.cursor.executemany(sql, input_list_1d)

	def write_value_in_sqlite(self, table_name, input_1, input_2=""):
		"""
		입력하고싶은 값을 sqlite에 저장하는것

		:param table_name: 테이블 이름
		:param input_1:
		:param input_2:
		:return:
		"""
		list_1d_dic = self.change_insert_data_to_dic(input_1, input_2)
		sql_columns = ""
		sql_values = ""
		for one_dic in list_1d_dic:
			for one_key in one_dic.keys():
				sql_columns = sql_columns + one_key + ", "
				sql_values = sql_values + one_dic[one_key] + ", "
			sql = "insert into %s(%s) values (%s)" % (table_name, sql_columns[:-2], sql_values[:-2])
			self.cursor.execute(sql)
		self.con.commit()

	def write_value_by_xy_in_df(self, df, xy, value):
		"""
		dataframe에 좌표로 값을 저장

		:param df: dataframe
		:param xy:
		:param value:
		:return:
		"""
		x_max = df.index.size
		y_max = df.columns.size
		if xy[1] > y_max:
			for no in range(y_max, xy[1]):
				df[len(df.columns)] = np.NaN
		if xy[0] > x_max:
			data_set = [(lambda x: np.NaN)(a) for a in range(len(df.columns))]
			for no in range(xy[0] - x_max):
				df.loc[len(df.index)] = data_set
		df.iat[int(xy[0]), int(xy[1])] = value

