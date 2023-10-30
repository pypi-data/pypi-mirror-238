# -*- coding: utf-8 -*-
import re, time, calendar  # 내장모듈
from datetime import datetime, time, date, timedelta  # 내장모듈
import datetime

import jfinder, scolor, youtil, basic_data  # xython 모듈

from korean_lunar_calendar import KoreanLunarCalendar

class pynal():
	"""
	datetime 객체를 기준으로 하여도 된다
	시간을 다루기 위한 모듈
	기본적으로 날짜의 변환이 필요한 경우는 utc 시간을 기준으로 변경하도록 하겠읍니다
	음력의 자료는 KoreanLunarCalendar모듈을 사용한다
	주일의 시작은 월요일이다
	"""

	def __init__(self):
		self.easyre = jfinder.jfinder()
		self.color = scolor.scolor()
		self.util = youtil.youtil()

		self.lunar_calendar = KoreanLunarCalendar() #음력
		self.base_data = basic_data.basic_data()
		self.var = self.base_data.vars
		self.var_common = {"timezone": "seoul", "week_no_7_start": 0}

	def change_any_text_time_to_dt_obj(self, input_text_time):
		"""
		기존의 자료를 다른 형태러 만들어 본것
		어떤 문자열의 시간이 오더라도 datetime형으로 돌려주는것

		:param input_text_time:
		:return:
		"""
		result = {}

		result["year"] = 0
		result["mon"] = 0
		result["day"] = 0
		result["hour"] = 0
		result["min"] = 0
		result["sec"] = 0
		result["week"] = 0
		result["bellow_sec"] = 0
		result["utc_+-"] = 0
		result["utc_h"] = 0
		result["utc_m"] = 0
		mon_l = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8,
		         'september': 9, 'october': 10, 'november': 11, 'december': 12}
		mon_s = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10,
		         'nov': 11, 'dec': 12}
		day_th = {'1st': 1, '2nd': 2, '3rd': 3, '4th': 4, '5th': 5, '6th': 6, '7th': 7, '8th': 8, '9th': 9, '10th': 10,
		          '11th': 11, '12th': 12, '13th': 13, '14th': 14, '15th': 15, '16th': 16, '17th': 17, '18th': 18,
		          '19th': 19, '20th': 20, '21st': 21, '22nd': 22, '23RD': 23, '24th': 24, '25th': 25, '26th': 26,
		          '27th': 27, '28th': 28, '29th': 29, '30th': 30, '31st': 31}
		week_l = {'monday': 1, 'tuesday': 2, 'wendsday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7}
		week_s = {'mon': 1, 'tue': 2, 'wen': 3, 'thu': 4, 'fri': 5, 'sat': 6, 'sun': 7}

		# 전처리를 실시
		dt_string = (str(input_text_time).strip()).lower()
		dt_string = dt_string.replace("/", "-")
		dt_string = dt_string.replace("#", "-")

		ymd_sql = []

		# 아래의 자료 형태들을 인식하는 것이다
		# '2022-03-04'
		# '3/12/2018' => '3-12-2018'
		# '20220607'
		# "180919 015519"
		# 'Jun 28 2018 7:40AM',
		# 'Jun 28 2018 at 7:40AM',
		# 'September 18, 2017, 22:19:55',
		# 'Mon, 21 March, 2015',
		# 'Tuesday , 6th September, 2017 at 4:30pm'
		# '2023-09-09 00:00:00+00:00'
		# 'Sun, 05/12/1999, 12:30PM', => 'Sun, 05-12-1999, 12:30PM',
		# '2023-03-01T10:01:23.221000+09:00'

		# +00:00 을 찾아내는것
		resql_result = self.easyre.search_all_by_easyre_sql("[+-:1~1][숫자:2~2]:[숫자:2~2]", dt_string)
		if resql_result and len(resql_result) > 1:
			temp = resql_result[0][0].split(":")
			result["current_+-"] = temp[0][0]
			result["current_h"] = temp[0][1:3]
			result["current_m"] = temp[1]
			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()

		# "2022-03-04"
		# "3-12-2018"
		# "20220607"
		# "180919 015519"
		# 'Jun 28 2018 7:40AM',
		# 'Jun 28 2018 at 7:40AM',
		# 'September 18, 2017, 22:19:55',
		# 'Mon, 21 March, 2015',
		# 'Tuesday , 6th September, 2017 at 4:30pm'
		# "2023-09-09 00:00:00"
		# 'Sun, 05-12-1999, 12:30PM',
		# '2023-03-01T10:01:23.221000'

		# 7:40AM
		resql = "[숫자:1~2]:[숫자:2~2][공백&apm:2~3]"
		resql_result = self.easyre.search_all_by_easyre_sql(resql, dt_string)
		ampm = ""
		if resql_result and len(resql_result) > 1:
			searched_data = resql_result[0][0]

			if "am" in searched_data:
				ampm = "am"
				searched_data = searched_data.replace("am", "")
			if "pm" in searched_data:
				ampm = "pm"
				searched_data = searched_data.replace("pm", "")

			temp = searched_data.split(":")
			result["hour"] = str(temp[0]).strip()
			result["min"] = str(temp[1]).strip()

			if ampm == "pm" and int(result["hour"]) <= 12:
				result["hour"] = int(result["hour"]) + 12

			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()

		# "2022-03-04"
		# "3-12-2018"
		# "20220607"
		# "180919 015519"
		# 'Jun 28 2018',
		# 'September 18, 2017, 22:19:55',
		# 'Mon, 21 March, 2015',
		# 'Tuesday , 6th September, 2017'
		# "2023-09-09 00:00:00"
		# 'Sun, 05-12-1999,'
		# '2023-03-01T10:01:23.221000'

		# 17:08:00
		resql_result = self.easyre.search_all_by_easyre_sql("[숫자:2~2]:[숫자:2~2]:[숫자:2~2]", dt_string)
		if resql_result and len(resql_result) > 1:
			searched_data = resql_result[0][0]

			temp = resql_result[0][0].split(":")
			result["hour"] = temp[0]
			result["min"] = temp[1]
			result["sec"] = temp[2]

			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.replace("at", "")
			dt_string = dt_string.strip()

		# "2022-03-04"
		# "3-12-2018"
		# "20220607"
		# "180919 015519"
		# 'Jun 28 2018',
		# 'September 18, 2017,',
		# 'Mon, 21 March, 2015',
		# 'Tuesday , 6th September, 2017'
		# 'Sun, 05-12-1999,'
		# '2023-03-01T.221000'

		# 2022-03-04
		if self.easyre.search_all_by_easyre_sql("[숫자:4~4]-[숫자:1~2]-[숫자:1~2]", dt_string):
			resql_result = self.easyre.search_all_by_easyre_sql("[숫자:4~4]-[숫자:1~2]-[숫자:1~2]", dt_string)

			temp = resql_result[0][0].split("-")
			result["year"] = temp[0]
			result["mon"] = temp[1]
			result["day"] = temp[2]

			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()

		# "3-12-2018"
		# "20220607"
		# "180919 015519"
		# 'Jun 28 2018',
		# 'September 18, 2017,',
		# 'Mon, 21 March, 2015',
		# 'Tuesday , 6th September, 2017'
		# 'Sun, 05-12-1999,'
		# 'T.221000'

		# 18/09/19 => 18-09-19
		resql_result = self.easyre.search_all_by_easyre_sql("[숫자:2~2][-/_:1~1][숫자:1~2][-/_:1~1][숫자:1~2]", dt_string)
		if resql_result and len(dt_string) > 1:
			# print("18/09/19 형식입니다")
			temp = resql_result[0][0].split("-")
			result["year"] = temp[2]
			if int(temp[0]) > 12:
				result["mon"] = temp[1]
				result["day"] = temp[0]
			elif int(temp[1]) > 12:
				result["mon"] = temp[0]
				result["day"] = temp[1]
			else:
				result["mon"] = temp[0]
				result["day"] = temp[1]

			if int(result["year"]) > 50:
				result["year"] = "19" + result["year"]
			else:
				result["year"] = "20" + result["year"]

			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()

		# "20220607"
		# "180919 015519"
		# 'Jun 28 2018',
		# 'September 18, 2017,',
		# 'Mon, 21 March, 2015',
		# 'Tuesday , 6th September, 2017'
		# 'Sun'

		# 20220607
		resql_result = self.easyre.search_all_by_easyre_sql("[20|19][숫자:6~6]", dt_string)
		if resql_result and len(dt_string) > 1:
			result["year"] = resql_result[0][0][0:4]
			result["mon"] = resql_result[0][0][4:6]
			result["day"] = resql_result[0][0][6:8]

			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()
		# "180919 015519"
		# 'Jun 28 2018',
		# 'September 18, 2017,',
		# 'Mon, 21 March, 2015',
		# 'Tuesday , 6th September, 2017'
		# 'Sun'

		for one_value in list(week_l.keys()):
			if one_value in dt_string:
				result["week"] = week_l[one_value]
				dt_string = dt_string.replace(one_value, "")
				dt_string = dt_string.strip()

		for one_value in list(week_s.keys()):
			if one_value in dt_string:
				result["week"] = week_s[one_value]
				dt_string = dt_string.replace(one_value, "")
				dt_string = dt_string.strip()

		# "180919 015519"
		# 'Jun 28 2018',
		# 'September 18, 2017,',
		# ', 21 March, 2015',
		# ', 6th September, 2017'

		# "180919 015519"
		resql_result = self.easyre.search_all_by_easyre_sql("[숫자:6~6][공백:1~1][숫자:6~6]", dt_string)
		if resql_result:
			result["day"] = resql_result[0][0][0:2]
			result["mon"] = resql_result[0][0][2:4]
			result["year"] = resql_result[0][0][4:6]
			result["bellow_sec"] = resql_result[0][0][:-6]

			if int(result["year"]) > 50:
				result["year"] = "19" + result["year"]
			else:
				result["year"] = "20" + result["year"]

			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()

		# 'Jun 28 2018',
		# 'September 18, 2017,',
		# ', 21 March, 2015',
		# ', 6th September, 2017'

		resql_result = self.easyre.search_all_by_easyre_sql("[영어:3~9][공백&,:1~3][숫자:1~2][공백&,:1~3][숫자:4~4]", dt_string)
		if resql_result:
			found_text = resql_result[0][0]

			bbb = self.easyre.search_all_by_easyre_sql("[영어:3~9]", found_text)
			for num in range(len(mon_l)):
				if bbb[0][0] in mon_l[num]:
					result["mon"] = num + 1
			found_text = found_text.replace(bbb[0][0], "")

			ccc = self.easyre.search_all_by_easyre_sql("[숫자:4~4]", found_text)
			result["year"] = ccc[0][0]
			found_text = found_text.replace(ccc[0][0], "")

			ddd = self.easyre.search_all_by_easyre_sql("[숫자:2~2]", found_text)
			result["day"] = ddd[0][0]

			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()

		# ', 21 March, 2015',
		# ', 6th September, 2017'

		#	'Tuesday , 6th September, 2017 at 4:30pm'
		resql_result = self.easyre.search_all_by_easyre_sql("[숫자:1~2][영어:0~3][공백&,:1~3][영어:3~9][공백&,:0~3][숫자:4~4]", dt_string)
		if resql_result:
			found_text = resql_result[0][0]

			bbb = self.easyre.search_all_by_easyre_sql("[영어:3~9]", found_text)
			# print(bbb)
			for num in range(len(mon_l)):
				if bbb[0][0] in mon_l[num]:
					result["mon"] = num + 1
			found_text = found_text.replace(bbb[0][0], "")
			# print(found_text)

			ccc = self.easyre.search_all_by_easyre_sql("[숫자:4~4]", found_text)
			result["year"] = ccc[0][0]
			found_text = found_text.replace(ccc[0][0], "")

			ddd = self.easyre.search_all_by_easyre_sql("[숫자:1~2]", found_text)
			result["day"] = ddd[0][0]

			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()

		resql_result = self.easyre.search_all_by_easyre_sql("\.[숫자:6~6]", dt_string)
		if resql_result:
			dt_string = dt_string.replace(resql_result[0][0], "")
			# .586525
			# 초단위 이하의 자료
			result["bellow_sec"] = resql_result[0][0]

		# 여태 걸린것주에 없는 4가지 숫자는 연도로 추측한다
		resql_result = self.easyre.search_all_by_easyre_sql("[숫자:4~4]", dt_string)
		if resql_result:
			# print(resql_result)
			result["year"] = resql_result[0][0]
			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()

		# 여태 걸린것 없는 2가지 숫자는 날짜로 추측한다
		resql_result = self.easyre.search_all_by_easyre_sql("[숫자:2~2]", dt_string)
		if resql_result:
			result["day"] = resql_result[0][0]
			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()

		resql_result = self.easyre.search_all_by_easyre_sql("pm[또는]am", dt_string)
		if resql_result:
			# print(resql_result)
			if resql_result[0][0] == "pm" and int(result["hour"]) <= 12:
				result["hour"] = int(result["hour"]) + 12
			dt_string = dt_string.replace(resql_result[0][0], "")
			dt_string = dt_string.strip()

		result["year"] = int(result["year"])
		result["mon"] = int(result["mon"])
		result["day"] = int(result["day"])
		result["hour"] = int(result["hour"])
		result["min"] = int(result["min"])
		result["sec"] = int(result["sec"])

		try:
			result = datetime(result["year"], result["mon"], result["day"], result["hour"], result["min"],
			                  result["sec"])
		except:
			result = "error"

		return result

	def change_any_time_to_dt_obj(self, input_text_time):
		"""
		어떤 시간의 형태로된 문자열을 날짜 객체로 만드는 것

		:param input_text_time:
		:return:
		"""
		result = self.check_input_time(input_text_time)
		return result

	def change_ymd_list_to_dt_obj(self, input_text_time):
		"""
		datetime객체는 최소한 년/월/일은 들어가야 생성된다
		dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")

		:param input_text_time:
		:return:
		"""
		dt_obj = self.check_input_time(input_text_time)
		return dt_obj

	def change_dt_obj_to_text_time_as_input_format(self, input_dt_obj, input_format):
		"""
		입력형식으로 되어있는 시간자료를 dt객체로 인식하도록 만드는 것이다
		dt = datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")

		:param input_dt_obj: 날짜 객체
		:param input_format:
		:return:
		"""
		result = input_dt_obj.strptime(input_format)
		return result

	def get_all_infomation_for_dt_obj(self, input_dt_obj):
		"""
		입력된 시간에 대한 왠만한 모든 형식의 날짜 표현을 사전형식으로 돌려준다

		:param input_dt_obj: 날짜 객체
		:return:
		"""

		result = {}
		# s는 short, e는 english, l은 long
		result["year_s"] = input_dt_obj.strftime('%y')  # 22
		result["year"] = input_dt_obj.strftime('%Y')  # 2023
		result["yyyy"] = result["year"]

		result["mon"] = input_dt_obj.strftime('%m')  # 1
		result["mm"] = result["mon"]
		result["mon_eng_s"] = input_dt_obj.strftime('%b')  # jan
		result["mon_eng_l"] = input_dt_obj.strftime('%B')  # january

		result["day_s"] = input_dt_obj.strftime('%d')  # 1
		result["d"] = input_dt_obj.strftime('%d')  # 1
		result["day"] = input_dt_obj.strftime('%j')  # 01
		result["dd"] = result["d"]

		result["week"] = input_dt_obj.strftime('%w')  # 6
		result["yearweek"] = input_dt_obj.strftime('%W')  # 34, 1년중에 몇번째 주인지
		result["week_eng_s"] = input_dt_obj.strftime('%a')  # mon
		result["week_eng_l"] = input_dt_obj.strftime('%A')  # monday

		result["hour_s"] = input_dt_obj.strftime('%I')  # 1
		result["hour"] = input_dt_obj.strftime('%H')  # 13

		result["ampm"] = input_dt_obj.strftime('%p')
		result["min"] = input_dt_obj.strftime('%M')
		result["sec"] = input_dt_obj.strftime('%S')
		return result

	def change_dt_obj_to_timestamp(self, input_text_time):
		"""
		날짜객체를 timestamp로 만드는 것
		*용어 : timestamp : 1960년부터 1로계산된 시간
		* text_time : 시간이나 날짜를 나타내는 형태의 문자열

		:param input_text_time:
		:return:
		"""
		utf_time = self.check_input_time(input_text_time)
		result = utf_time.timestamp()
		return result

	def change_dt_obj_to_utc(self, input_dt_obj):
		"""

		:param input_dt_obj: 날짜 객체
		:return:
		"""
		result = int(input_dt_obj.timestamp())
		return result

	def change_dt_obj_to_ymd_list(self, input_dt_obj):
		"""
		날짜객체를 년월일의 리스트로 돌려주는 것

		:param input_dt_obj: 날짜 객체
		:return:
		"""

		utc_str = self.change_dt_obj_to_text_time_set_as_dic(input_dt_obj)
		result = [int(utc_str["yyyy"]), int(utc_str["mm"]), int(utc_str["dd"])]
		return result


	def change_dt_obj_to_ymd_style_with_connect_char(self, input_dt_obj, connect_str="-"):
		"""
		입력문자를 기준으로 yyyy-mm-dd이런 스타일로 만드는 것이다
		시간객체 => 년-월-일

		:param input_dt_obj: 날짜 객체
		:param connect_str:
		:return:
		"""
		utc_str = self.change_dt_obj_to_text_time_set_as_dic(input_dt_obj)
		result = utc_str["yyyy"] + connect_str + utc_str["mm"] + connect_str + utc_str["dd"]
		return result

	def change_hms_list_to_sec(self, input_hms_list=""):
		"""
		hms_list : [시, 분, 초]
		input_data = "14:06:23"
		출력값 : 초
		입력값으로 온 시분초를 초로 계산한것

		:param input_hms_list:
		:return:
		"""
		re_compile = re.compile("\d+")
		result = re_compile.findall(input_hms_list)
		total_sec = int(result[0]) * 3600 + int(result[1]) * 60 + int(result[2])
		return total_sec

	def change_iso_format_to_dt_obj(self, input_iso_format="2023-03-01"):
		"""
		date 클래스의 isoformat() - YYYY-MM-DD의 형태를 말합니다
		ISO형식 : 2023-03-01T10:01:23.221000
				 2023-03-01T10:01:23.221000+09:00
		         2023-03-01

		:param input_iso_format:
		:return:
		"""
		dt_obj = datetime.fromisoformat(input_iso_format)
		return dt_obj

	def change_lunar_day_to_solar_day(self, input_ymd):
		"""
		음력 -> 양력으로 변환시 (음력은 윤달인지 아닌지에대한 기준이 필요하다)
		결과값 : [평달일때의 양력, 윤달일때의 양력]

		:param input_ymd:
		:return:
		"""
		self.lunar_calendar.setLunarDate(input_ymd[0], input_ymd[1], input_ymd[2], False)
		moon_day_1 = self.lunar_calendar.SolarIsoFormat()

		moon_day_2 = ""
		try:
			# 윤달이 없는 달이면, 평달의 날짜를 돌려준다
			self.lunar_calendar.setLunarDate(input_ymd[0], input_ymd[1], input_ymd[2], True)
			moon_day_2 = self.lunar_calendar.SolarIsoFormat()
		except:
			pass
		return [moon_day_1, moon_day_2]

	def change_lunar_day_to_solar_day_1(self, input_data):
		"""

		:param input_data:
		:return:
		"""
		result = []
		for one in input_data:
			if one[3] == "양":
				result.append(one)
			elif one[3] == "음":
				if one[2] == "말일":
					result.append(one)
					input_data[1] = self.check_last_day_for_lunar_ym_list([one[0], one[1:]])
					self.lunar_calendar.setLunarDate(one[0], input_data[0], input_data[1], False)
					moon_day_1 = self.lunar_calendar.SolarIsoFormat()
					ymd_list = moon_day_1.split("-")
					one = ymd_list + one[3:]
				for num in range(int(one[4])):
					self.lunar_calendar.setLunarDate(one[0], one[1] + num, one[2], False)
					moon_day_1 = self.lunar_calendar.SolarIsoFormat()
					ymd_list = moon_day_1.split("-")
					result.append(ymd_list + ["음", 1] + one[5:])
		return result

	def change_lunar_to_solar(self, input_ymd_list, yoon_or_not=True):
		"""
		음력을 양력으로 만들어 주는것

		:param input_ymd_list:
		:param yoon_or_not:
		:return:
		"""
		self.lunar_calendar.setLunarDate(int(input_ymd_list[0]), int(input_ymd_list[1]), int(input_ymd_list[2]),
		                                 yoon_or_not)
		dt_obj = self.change_any_text_time_to_dt_obj(self.lunar_calendar.SolarIsoFormat())
		result = self.change_dt_obj_to_ymd_list(dt_obj)
		return result

	def change_next_day_of_sunday(self, holiday_list, input_list_2d):
		"""
		대체공휴일을 확인하는것
		일요일인것만, 리스트로 만들어 준다

		:param holiday_list:
		:param input_list_2d:
		:return:
		"""
		result = []
		if holiday_list == "all":
			for list_1d in input_list_2d:
				temp = []
				sunday = 0
				for one in list_1d:
					if one[3] == 0:    sunday = 1
					one[2] = int(one[2]) + sunday
					temp.append(one)
				result.append(temp)
		else:
			for list_1d in input_list_2d:
				temp = []
				if list_1d in holiday_list:
					sunday = 0
					for one in list_1d:
						if one[3] == 0:  # 일요일의 값인 0이 있다면...
							sunday = 1
						one[2] = int(one[2]) + sunday
						temp.append(one)
					result.append(temp)
				else:
					result.append(list_1d)

		return result

	def change_sec_to_dhms_list(self, input_sec_no=""):
		"""
		초 => 날자
		1000초 => 2일3시간10분30초
		:param input_data:
		:return:
		"""
		step_1 = divmod(int(input_sec_no), 60)
		step_2 = divmod(step_1[0], 60)
		day = int(input_sec_no) / (60 * 60 * 24)
		result = [day, step_2[0], step_2[1], step_1[1]]
		return result

	def change_sec_to_hms_list(self, input_sec_no=""):
		"""
		초로 넘어온 자료를 기간으로 돌려주는 것
		입력값 : 123456

		:param input_data:
		:return:
		"""
		step_1 = divmod(int(input_sec_no), 60)
		step_2 = divmod(step_1[0], 60)
		final_result = [step_2[0], step_2[1], step_1[1]]
		return final_result

	def change_solar_day_to_lunar_day(self, input_ymd_list):
		"""
		양력 -> 음력으로 변환시
		결과값 : [음력, 윤달여부]

		:param input_ymd:
		:return:
		"""
		self.lunar_calendar.setLunarDate(input_ymd_list[0], input_ymd_list[1], input_ymd_list[2], False)
		moon_day_1 = self.lunar_calendar.LunarIsoFormat()
		yoon_or_not = self.lunar_calendar.isIntercalation()

		return [moon_day_1, yoon_or_not]

	def change_text_time_n_format_to_dt_obj(self, input_text_time, input_format):
		"""
		입력한 시간 문자열과 문자열의 형식을 넣어주면 datetime객체를 만들어 준다
		날짜와 시간(datetime) -> 문자열로 : strftime
		날짜와 시간 형식의 문자열을 -> datetime으로 : strptime

		:param input_text_time:
		:param input_format:
		:return:
		"""
		dt_obj = datetime.strptime(input_text_time, input_format)
		return dt_obj

	def change_text_time_to_another_text_time_by_format(self, input_text_time, input_time_format):
		"""
		입력시간을 utc로 바꾸는 것

		:param input_time_format:
		:param input_format:
		:return:
		"""
		cheked_input_text_time = self.check_input_time(input_text_time)
		result = time.strptime(cheked_input_text_time, input_time_format)
		return result

	def change_text_time_to_dt_obj(self, input_text_time):
		"""
		어떤 시간의 형태로된 문자열을 날짜 객체로 만드는 것

		:param input_text_time:
		:return:
		"""
		result = self.check_input_time(input_text_time)
		return result

	def change_text_time_to_ymd_list(self, input_text_time):
		"""
		날짜객체를 년월일의 리스트로 돌려주는 것

		:param input_text_time: 문자열로된 시간
		:return:
		"""
		utc = self.check_input_time(input_text_time)
		utc_str = self.change_dt_obj_to_text_time_set_as_dic(utc)
		result = [int(utc_str["yyyy"]), int(utc_str["mm"]), int(utc_str["dd"])]
		return result

	def change_text_time_to_ymd_style(self, input_text_time, connect_str="-"):
		"""
		입력시간을 년월일을 특수 문자로 연결하여 돌려주는 것

		:param input_text_time:
		:param connect_str:
		:return:
		"""
		utc = self.check_input_time(input_text_time)
		utc_str = self.change_dt_obj_to_text_time_set_as_dic(utc)
		result = utc_str["yyyy"] + connect_str + utc_str["mm"] + connect_str + utc_str["dd"]
		return result

	def change_timestamp_to_utc(self, input_text_time):
		"""
		숫자형으로된 시간을 utc로 바꾸는 것

		:param input_text_time:
		:return:
		"""
		result = time.gmtime(input_text_time)
		return result

	def change_utc_by_format(self, input_utc, input_format):
		"""

		:param input_utc:
		:param input_format:
		:return:
		"""
		result = time.strftime(input_format, input_utc)
		return result

	def change_utc_to_day_list(self, input_utc=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		일 -----> ['05']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_data:
		:return:
		"""
		utc_local_time = self.check_input_time(input_utc)
		day = time.strftime('%d', utc_local_time)
		day_l = time.strftime('%j', utc_local_time)
		result = [day, day_l]
		return result

	def change_utc_to_dt_obj(self, input_utc=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		분 -----> ['07']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_utc:
		:return:
		"""
		result = self.check_input_time(input_utc)
		return result

	def change_utc_to_hour_list(self, input_utc=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		시 -----> ['10', '22']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_utc:
		:return:
		"""
		utc_local_time = self.check_input_time(input_utc)
		hour = time.strftime('%I', utc_local_time)
		hour_l = time.strftime('%H', utc_local_time)
		result = [hour, hour_l]
		return result

	def change_utc_to_min_list(self, input_utc=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		분 -----> ['07']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_utc:
		:return:
		"""
		utc_local_time = self.check_input_time(input_utc)
		min = time.strftime('%M', utc_local_time)
		result = [min]
		return result

	def change_utc_to_month_list(self, input_utc=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		월 -----> ['04', Apr, April]
		닞은숫자 -> 많은글자 순으로 정리

		:param input_utc:
		:return:
		"""
		utc_local_time = self.check_input_time(input_utc)
		mon = time.strftime('%m', utc_local_time)
		mon_e = time.strftime('%b', utc_local_time)
		mon_e_l = time.strftime('%B', utc_local_time)
		result = [mon, mon_e, mon_e_l]
		return result

	def change_utc_to_sec_list(self, input_utc=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		초 -----> ['48']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_utc:
		:return:
		"""
		utc_local_time = self.check_input_time(input_utc)
		sec = time.strftime('%S', utc_local_time)
		result = [sec]
		return result

	def change_utc_to_week_list(self, input_utc=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		주 -----> ['5', '13', 'Fri', 'Friday']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_utc:
		:return:
		"""
		utc_local_time = self.check_input_time(input_utc)
		week_no = time.strftime('%w', utc_local_time)
		yearweek_no = time.strftime('%W', utc_local_time)
		week_e = time.strftime('%a', utc_local_time)
		week_e_l = time.strftime('%A', utc_local_time)
		result = [week_no, yearweek_no, week_e, week_e_l]
		return result

	def change_utc_to_weekno(self, input_utc=""):
		"""
		시간이 들어온면
		입력값 : 년도, 위크번호
		한 주의 시작은 '월'요일 부터이다

		:param input_utc:
		:return:
		"""
		lt = self.check_input_time(input_utc)
		# print("lt", lt)
		result = time.strftime('%W', lt)  # 34, 1년중에 몇번째 주인지
		return result

	def change_utc_to_year_list(self, input_utc=""):
		"""
		년 -----> ['22', '2022']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_utc:
		:return:
		"""
		utc_local_time = self.check_input_time(input_utc)
		year_s = time.strftime('%y', utc_local_time)
		year = time.strftime('%Y', utc_local_time)
		result = [year_s, year]
		return result

	def change_utc_to_ymd_dash(self, input_utc=""):
		"""
		utc를 2023-2-2형태로 돌려주는 것

		:param input_utc:
		:return:
		"""
		lt = self.change_any_text_time_to_dt_obj(input_utc)
		result = lt.format("YYYY-MM-DD")
		return result

	def change_utc_to_ymd_list(self, input_utc=""):
		"""

		:param input_utc:
		:return:
		"""
		utc_local_time = self.check_input_time(input_utc)
		year = time.strftime('%Y', utc_local_time)
		month = time.strftime('%m', utc_local_time)
		day = time.strftime('%d', utc_local_time)
		result = [year, month, day]
		return result

	def change_utc_timeformat(self, input_utc, format_a):
		"""

		:param input_utc:
		:param format_a:
		:return:
		"""
		result = time.strftime(format_a, input_utc)
		return result

	def change_windows_time_to_dt_obj(self):
		"""
		1601년 1월1일을 0으로하여 계산하는 윈도우의 시간을 dt_obj로 만드는것

		:return:
		"""
		pass

	def change_ymd_list_to_sec(self, input_list=[0, 0, 1]):
		"""
		몇년 몇월 몇일을 초로 바꾸는 것
		입력형태 : [몇년, 몇월, 몇일]
		현재일자를 기준으로
		월은 30일 기준으로 계산한다
		기준날짜에서 계산을 하는 것이다

		:param input_list:
		:return:
		"""
		total_sec = int(input_list[0]) * 60 * 60 * 24 * 365 + int(input_list[1]) * 60 * 60 * 24 * 30 + int(
			input_list[2]) * 60 * 60 * 24
		return total_sec

	def check_day_or_not(self, input_list):
		"""
		입력된 자료들이 년을 나타내는 자료인지를 확인하는것

		:param input_list:
		:return:
		"""
		result = []
		alphabet = "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".upper()
		if type(input_list[0]) == type([]):
			changed_input_list = input_list
		else:
			changed_input_list = []
			for one in input_list:
				changed_input_list.append([one])

		for one_list in changed_input_list:
			if str(one_list[0])[0] in alphabet:
				# 알파벳으로 사용하는것은 월밖에 없다
				result.append(False)
			else:
				if len(str(one_list[0])) == 4:
					# 4개의 숫자는 년도를 나타내는 것
					result.append(False)
				elif len(one_list[0]) <= 2:
					result.append(True)

				if int(one_list[0]) > 31:
					# 31보다 크면, 년도이다
					result.append(False)
				else:
					# 12보다 크면, 월을 나타내는것이 아니다
					result.append(True)

		total_num = 0
		for one in result:
			total_num = total_num + one

		# 전체중에서 1보다 넘으면 년을 쓰인것으로 본다
		# 숫자가 2개이하인것과 12이상일때, 두번 True로 만들기때문에...
		if total_num / len(result) > 1:
			month_or_not = True
		else:
			month_or_not = False
		return month_or_not

	def check_holiday(self, input_year, input_data):
		"""
		입력받은 공휴일 자료중에서 양력으로 된것은 그대로 저장하고
		음력으로 된것을 양력 날짜로 바꾸는것

		:param input_year:
		:param input_data:
		:return:
		"""
		result = []
		if input_data[2] == "양":
			dt_obj = self.change_ymd_list_to_dt_obj([input_year, input_data[0], input_data[1]])
		elif input_data[2] == "음":
			if input_data[1] == "말일":
				input_data[1] = self.check_last_day_for_lunar_ym_list([input_year, input_data[0]])

			self.lunar_calendar.setLunarDate(input_year, input_data[0], input_data[1], False)
			dt_obj = self.change_any_text_time_to_dt_obj(self.lunar_calendar.SolarIsoFormat())

		week_no_7 = self.get_one_week_no_7_for_dt_obj(dt_obj)
		new_ymd_list = self.change_dt_obj_to_ymd_list(dt_obj)
		for index in range(int(input_data[3])):
			checked_ymd_list = self.check_ymd_list([new_ymd_list[0], new_ymd_list[1], int(new_ymd_list[2]) + index])
			result.append(
				[checked_ymd_list[0], checked_ymd_list[1], checked_ymd_list[2], divmod(int(week_no_7) + index, 7)[1],
				 input_data[-1]])
		return result

	def check_input_time(self, input_text_time=""):
		"""
		어떤 형태가 들어오더라도 datetime으로 돌려주는 것

		:param input_text_time:
		:return:
		"""
		if input_text_time == "":
			# 아무것도 입력하지 않으면 local time 으로 인식한다
			result = datetime.now()

		elif type(input_text_time) == type(datetime.now()):
			# 만약 datetime객체일때
			result = input_text_time

		elif type(input_text_time) == type(float(123.00)) or type(input_text_time) == type(int(123.00)):
			# timestamp로 인식
			result = datetime.fromtimestamp(input_text_time)

		elif type("string") == type(input_text_time):
			#  만약 입력형태가 문자열이면 : "202201O", "22/mar/01","22mar01"
			result = self.change_any_text_time_to_dt_obj(input_text_time)

		elif type(input_text_time) == type([]):
			# 리스트 형태의 경우
			if len(input_text_time) >= 3:
				self.year, self.month, self.day = int(input_text_time[0]), int(input_text_time[1]), int(input_text_time[2])
				result = datetime(self.year, self.month, self.day)
		else:
			result = datetime.now()
		return result

	def check_last_day_for_lunar_ym_list(self, input_ym_list, yoon_or_not=True):
		"""
		음력으로 입력된 것중에 말일이라고 된것의 양력날짜를 구하는 것
		yoon_or_not : 윤달인지 아닌지에 대한 설정

		:param input_ym_list:
		:param yoon_or_not:
		:return:
		"""
		for num in range(27, 31):
			try:
				# 윤달이 아닌 날짜를 기준으로 확인
				self.lunar_calendar.setLunarDate(int(input_ym_list[0]), int(input_ym_list[1]), num, yoon_or_not)
				dt_obj = self.change_any_text_time_to_dt_obj(self.lunar_calendar.SolarIsoFormat())
				ymd_list = self.change_dt_obj_to_ymd_list(dt_obj)
			except:
				break
		return ymd_list

	def check_last_day_for_lunar_ym_list_1(self, input_ym_list):
		"""
		음력으로 말일을 찾는것

		:param input_ym_list:
		:return:
		"""
		result = 26
		for nun in range(27, 31):
			self.lunar_calendar.setLunarDate(input_ym_list[0], input_ym_list[1], nun, False)
			temp = self.lunar_calendar.SolarIsoFormat()
			ymd_list = temp.split("-")
			if int(ymd_list[2]) >= result:
				print("말일 찾기 ==> ", result)
				result = int(ymd_list[2])
			else:
				break
		return result

	def check_month_or_not(self, input_list):
		"""
		입력된 자료들이 월을 나타내는 자료인지를 확인하는것

		:param input_list:
		:return:
		"""
		result = []
		alphabet = "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".upper()
		if type(input_list[0]) == type([]):
			changed_input_list = input_list
		else:
			changed_input_list = []
			for one in input_list:
				changed_input_list.append([one])

		for one_list in changed_input_list:
			if str(one_list[0])[0] in alphabet:
				# 알파벳으로 사용하는것은 월밖에 없다
				result.append(True)
			else:
				if len(str(one_list[0])) == 4:
					# 4개의 숫자는 년도를 나타내는 것
					result.append(False)
				elif int(one_list[0]) > 31:
					# 31보다 크면, 년도이다
					result.append(False)
				elif int(one_list[0]) > 12 and int(one_list[0]) <= 31:
					# 12보다 크면, 월을 나타내는것이 아니다
					result.append(True)
		total_num = 0
		for one in result:
			total_num = total_num + one

		# 전체중에서 70%가 넘으면 월로쓰인것으로 본다
		if total_num / len(result) > 0.9:
			month_or_not = True
		else:
			month_or_not = False

		return month_or_not

	def check_year_or_not(self, input_list):
		"""
		입력된 자료들이 년을 나타내는 자료인지를 확인하는것

		:param input_list:
		:return:
		"""
		result = []
		alphabet = "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".upper()
		if type(input_list[0]) == type([]):
			changed_input_list = input_list
		else:
			changed_input_list = []
			for one in input_list:
				changed_input_list.append([one])

		for one_list in changed_input_list:
			if str(one_list[0])[0] in alphabet:
				# 알파벳으로 사용하는것은 월밖에 없다
				result.append(False)
			else:
				if len(str(one_list[0])) == 4:
					# 4개의 숫자는 년도를 나타내는 것
					result.append(True)
				elif int(one_list[0]) > 31:
					# 31보다 크면, 년도이다
					result.append(True)
				elif int(one_list[0]) > 12 and int(one_list[0]) <= 31:
					# 12보다 크면, 월을 나타내는것이 아니다
					result.append(False)
		total_num = 0
		for one in result:
			total_num = total_num + one

		# 전체중에서 70%가 넘으면 년을 쓰인것으로 본다
		if total_num / len(result) > 0.5:
			month_or_not = True
		else:
			month_or_not = False
		return month_or_not

	def check_ymd_list(self, input_ymd_list):
		"""
		YMD리스트로 들어온값이 월과 일을 넘는 숫자이면 이것을 고치는것
		[2000, 14, 33] ==> [2001, 3, 31]

		:param input_ymd_list:
		:return:
		"""
		year = int(input_ymd_list[0])
		month = int(input_ymd_list[1])
		day = int(input_ymd_list[2])
		if month > 12:
			year = year + divmod(month, 12)[0]
			month = divmod(month, 12)[1]
			if month == 0:
				year = year - 1
				month = 12

		if day > 25:
			delta_day = day - 25
			dt_obj = self.change_ymd_list_to_dt_obj([year, month, 25])
			dt_obj = self.shift_dt_obj_by_day(dt_obj, delta_day)
		else:
			dt_obj = self.change_ymd_list_to_dt_obj([year, month, day])

		result = self.change_dt_obj_to_ymd_list(dt_obj)
		return result

	def combine_date_obj_and_time_obj(self, input_date_obj, input_time_obj):
		"""
		날짜객체와 시간객체를 하나로 만드는 것

		:param input_date_obj:
		:param input_time_obj:
		:return:
		"""
		dt_obj = datetime.combine(input_date_obj, input_time_obj)
		return dt_obj

	def data_holiday_nation(self):
		"""
		휴일기준

		:return:
		"""
		self.var_common["holiday_common"] = ["0101", "0301", "0505", "0606", "0815", "1001", "1225", 1.3]
		self.var_common["holiday_company"] = ["0708"]

	def data_national_holiday_in_year(self, input_ymd_list1, input_ymd_list2):
		"""
		입력한 해의 국정공휴일을 반환해 주는 것이다
		[공휴일지정 시작일, 공휴일지정 끝나는날],[공휴일 월, 일, 음/양, 몇일간 연속된것인지, 윤달여부, 공휴일의 이름]

		:param input_ymd_list1:
		:param input_ymd_list2:
		:return:
		"""

		holiday_list2d = self.var["holiday_list"]

		# 전체적으로 사용되는 변수들
		result_sun = []
		end_ymd_list_moon = self.shift_ymd_list_by_day(input_ymd_list2, 62)
		base_start_no = int(input_ymd_list1[0]) * 10000 + int(input_ymd_list1[1]) * 100 + int(input_ymd_list1[2])
		base_end_no = int(input_ymd_list2[0]) * 10000 + int(input_ymd_list2[1]) * 100 + int(input_ymd_list2[2])

		# 양력의 자료에 대해서 구한것
		period_list_sun = self.split_period_as_year_basis(input_ymd_list1, input_ymd_list2)
		for start_ymd_list, end_ymd_list in period_list_sun:
			year = int(start_ymd_list[0])
			for one_holiday in holiday_list2d:
				# 위의 자료를 모두 확인해서, 입력한 년도와 관계있는것만 골라내는 것
				if one_holiday[1][2] == "양":
					holiday_no = year * 10000 + int(one_holiday[1][0]) * 100 + int(one_holiday[1][1])
					if base_start_no <= holiday_no and base_end_no >= holiday_no and one_holiday[0][0] <= holiday_no and \
							one_holiday[0][1] >= holiday_no:
						result_sun.append([year, int(one_holiday[1][0]), int(one_holiday[1][1])] + one_holiday[1])

		# 음력중 평달인것만 구한것
		# 음력을 변환했을때의 양력날짜는 양력의 날짜보다 클수가 없다. 그래서 음력의 기간을 다시 설정하는 것이다
		period_list_moon = self.split_period_as_year_basis(input_ymd_list1, end_ymd_list_moon)

		for start_ymd_list, end_ymd_list in period_list_moon:
			year = int(start_ymd_list[0])

			for one_holiday in holiday_list2d:
				# 위의 자료를 모두 확인해서, 입력한 년도와 관계있는것만 골라내는 것
				if one_holiday[1][2] == "음":
					if one_holiday[1][1] == "말일":
						ymd_list_moon = self.check_last_day_for_lunar_ym_list([year, one_holiday[1][0]])
					else:
						ymd_list_moon = [year, one_holiday[1][0], one_holiday[1][1]]

					self.lunar_calendar.setLunarDate(int(ymd_list_moon[0]), int(ymd_list_moon[1]),
					                                 int(ymd_list_moon[2]), True)
					ymd_list_sun = self.change_lunar_to_solar(ymd_list_moon)
					holiday_no = int(ymd_list_sun[0]) * 10000 + int(ymd_list_sun[1]) * 100 + int(ymd_list_sun[2])

					if base_start_no <= holiday_no and base_end_no >= holiday_no and one_holiday[0][0] <= holiday_no and \
							one_holiday[0][1] >= holiday_no:
						result_sun.append(ymd_list_sun + one_holiday[1])
		return result_sun

	def delta_2_date(self, date_1, date_2):
		"""
		두날짜의 빼기

		:param date_1:
		:param date_2:
		:return:
		"""
		time_big = 1  # ymd_cls(date_1)
		time_small = 2  # ymd_cls(date_2)
		if time_big.lt_utc > time_small.lt_utc:
			pass
		else:
			time_big, time_small = time_small, time_big
		time_big.last_day = self.get_month_range(time_big.year, time_big.month)[3]
		time_small.last_day = self.get_month_range(time_small.year, time_small.month)[3]

		delta_year = abs(time_big.year - time_small.year)
		delta_day = int(abs(time_big.lt_utc - time_small.lt_utc) / (24 * 60 * 60))
		# 실제 1 년의 차이는 365 일 5 시간 48 분 46초 + 0.5초이다 (2 년에 1 번씩 윤초를 실시》
		actual_delta_year = int(abs(time_big.lt_utc - time_small.lt_utc) / (31556926 + 0.5))
		delta_month = abs((time_big.year * 12 + time_big.month) - (time_small.year * 12 + time_small.month))
		if time_big.day > time_small.day:
			actual_delta_month = delta_month - 1
		else:
			actual_delta_month = delta_month
		actual_delta_day = delta_day
		return [delta_year, delta_month, delta_day, actual_delta_year, actual_delta_month, actual_delta_day]

	def delta_date0_date1(self, input_date1, input_date2):
		"""
		두날짜의 빼기

		:param input_date1:
		:param input_date2:
		:return:
		"""
		utc1 = self.change_any_text_time_to_dt_obj(input_date1)
		utc2 = self.change_any_text_time_to_dt_obj(input_date2)
		result = abs((float(utc1) - float(utc2)) / (60 * 60 * 24))
		return result

	def delta_date0_date1_as_sec(self, input_date1, input_date2):
		"""
		두날짜의 빼기

		:param input_date1:
		:param input_date2:
		:return:
		"""
		utc1 = self.change_any_text_time_to_dt_obj(input_date1)
		utc2 = self.change_any_text_time_to_dt_obj(input_date2)
		result = abs((float(utc1) - float(utc2)) / (60 * 60 * 24))
		return result

	def delta_date1_date2(self, date_1, date_2):
		"""
		두날짜의 빼기

		:param date_1:
		:param date_2:
		:return:
		"""
		time_big = 1  # ymd_cls(date_1)
		time_small = 2  # ymd_cls(date_2)
		if time_big.lt_utc > time_small.lt_utc:
			pass
		else:
			time_big, time_small = time_small, time_big
		time_big.last_day = self.get_month_range(time_big.year, time_big.month)[3]
		time_small.last_day = self.get_month_range(time_small.year, time_small.month)[3]

		delta_year = abs(time_big.year - time_small.year)
		delta_day = int(abs(time_big.lt_utc - time_small.lt_utc) / (24 * 60 * 60))
		# 실제 1 년의 차이는 365 일 5 시간 48 분 46초 + 0.5초이다 (2 년에 1 번씩 윤초를 실시》
		actual_delta_year = int(abs(time_big.lt_utc - time_small.lt_utc) / (31556926 + 0.5))
		delta_month = abs((time_big.year * 12 + time_big.month) - (time_small.year * 12 + time_small.month))
		if time_big.day > time_small.day:
			actual_delta_month = delta_month - 1
		else:
			actual_delta_month = delta_month
		actual_delta_day = delta_day
		return [delta_year, delta_month, delta_day, actual_delta_year, actual_delta_month, actual_delta_day]

	def delta_hms_list_1_and_hms_list_2(self, input_hms_1, input_hms_2):
		"""
		hms_list : [시, 분, 초]
		두 시간에 대한 차이를 hms 형태로 돌려주는 것

		:param input_hms_1:
		:param input_hms_2:
		:return:
		"""
		sec_1 = self.change_hms_list_to_sec(input_hms_1)
		sec_2 = self.change_hms_list_to_sec(input_hms_2)
		delta_sec = abs(int(sec_2 - sec_1))
		result = self.change_sec_to_hms_list(delta_sec)
		return result

	def delta_input_ymd1_and_input_ymd2(self, input_date1, input_date2):
		"""

		:param input_date1:
		:param input_date2:
		:return:
		"""
		dt_obj1 = self.check_input_time(input_date1)
		dt_obj2 = self.check_input_time(input_date2)
		print("datetime객체 ==> ", dt_obj1, dt_obj2)
		temp = (dt_obj1 - dt_obj2)
		print("-----", int(temp.total_seconds() / 60 * 60 * 24))
		return temp

	def delta_two_hms_list(self, input_hms_list_1, input_hms_list_2):
		"""
		hms_list : [시, 분, 초]
		두 시간에 대한 차이를 hms 형태로 돌려주는 것

		:param input_hms_list_1:
		:param input_hms_list_2:
		:return:
		"""
		sec_1 = self.change_hms_list_to_sec(input_hms_list_1)
		sec_2 = self.change_hms_list_to_sec(input_hms_list_2)
		delta_sec = abs(int(sec_2 - sec_1))
		result = self.change_sec_to_hms_list(delta_sec)
		return result

	def differance_dt_obj1_with_dt_obj2(self, input_dt_obj_1, input_dt_obj_2):
		"""
		날짜의 차이

		:param input_dt_obj_1:
		:param input_dt_obj_2:
		:return:
		"""
		if input_dt_obj_1 > input_dt_obj_2:
			input_dt_obj_2, input_dt_obj_1 = input_dt_obj_1, input_dt_obj_2

		base_ymd_list = self.change_dt_obj_to_ymd_list(input_dt_obj_1)
		day_no_for_one_month_before = self.get_last_day_of_month_for_ym_list([base_ymd_list[0], base_ymd_list[1] - 1])
		ymd_list_2 = self.change_dt_obj_to_ymd_list(input_dt_obj_2)

		if base_ymd_list[2] - ymd_list_2[2] <= 0:
			base_ymd_list[2] = base_ymd_list[2] + day_no_for_one_month_before
			base_ymd_list[1] = base_ymd_list[1] - 1

	def get_1st_day_N_last_day_for_ym_list(self, input_ym_list):
		"""
		[2023, 05] => [(1,31), 1, 31]

		:param input_ym_list:
		:return:
		"""
		date = datetime(year=input_ym_list[0], month=input_ym_list[1], day=1).date()
		monthrange = calendar.monthrange(date.year, date.month)
		first_day = calendar.monthrange(date.year, date.month)[0]
		last_day = calendar.monthrange(date.year, date.month)[1]
		return [date, monthrange, first_day, last_day]

	def get_7_days_list_for_weekno(self, year, week_no_year):
		"""
		월요일부터 시작하는 7 개의 날짜를 돌려준다
		2023-07-24 : f'{year} {week_no_year} 0' => f'{year} {week_no_year} 1'

		:param year:
		:param week_no_year:
		:return:
		"""
		str_datetime = f'{year} {week_no_year} 1'  # 1은 월요일 이다
		# 문자열형태로 입력받아서, 시간객체로 만들어 주는것
		startdate = datetime.strptime(str_datetime, '%Y %W %w')
		dates = []
		for i in range(1, 8):
			day = startdate + timedelta(days=i)
			dates.append(day.strftime("%Y-%m-%d"))
		return dates

	def get_all_day_list_for_year_month(self, input_year, input_month):
		"""
		년과 월을 주면, 한달의 리스트를 알아내는것
		월요일부터 시작

		:param input_year:
		:param input_month:
		:return:
		"""
		result = []
		week_no = []
		date_obj = datetime(year=input_year, month=input_month, day=1).date()
		first_day_wwek_no = calendar.monthrange(date_obj.year, date_obj.month)[0]
		last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
		if first_day_wwek_no == 0:
			pass
		else:
			for no in range(first_day_wwek_no):
				week_no.append("")
		for num in range(1, int(last_day) + 1):
			if len(week_no) == 7:
				result.append(week_no)
				week_no = [num]
			else:
				week_no.append(num)
		if week_no:
			result.append(week_no)
		return result

	def get_date_of_monday_for_weekno(self, year, week_no):
		"""
		입력값 : 년도, 위크번호
		한 주의 시작은 '월'요일 부터이다

		:param year:
		:param week_no:
		:return:
		"""

		utc_local_time = self.check_input_time([year, 1, 1])
		base = 1 if utc_local_time.isocalendar()[1] == 1 else 8
		temp = utc_local_time + datetime.timedelta(days=base - utc_local_time.isocalendar()[2] + 7 * (int(week_no) - 1))
		days = str(temp).split("-")

	# input_utf_time_no = nal.change_ymd_list_to_utc([2022, 1, 1])
	# return [str(temp), temp, input_utf_time_no]

	def get_day_from_utc(self, input_text_time=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		일 -----> ['05']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_text_time:
		:return:
		"""
		utc_local_time = self.check_input_time(input_text_time)
		day = time.strftime('%d', utc_local_time)
		return day

	def get_dt_obj_for_last_day_of_text_time(self, input_text_time):
		"""
		입력한 날의 월의 마지막 날짜를 계산
		입력받은 날자에서 월을 1나 늘린후 1일을 마이너스 한다
		0:2023-04-19 -> 2023-05-01 -> 2023-05-01 - 12 -> 2023-04-30

		:param input_text_time:
		:return:
		"""
		dt_obj = self.check_input_time(input_text_time)
		if dt_obj.month == 12:
			year = dt_obj.year + 1
			month = 1
		else:
			year = dt_obj.year
			month = dt_obj.month + 1
		dt_obj_1 = datetime(year, month, 1)
		dt_obj_2 = dt_obj_1 + timedelta(days=-1)
		result = dt_obj_2.day
		return result

	def get_dt_obj_for_last_day_of_ym_list(self, input_ym_list=[2002, 3]):
		"""
		입력월의 마지막날을 돌려준다


		:param input_list:
		:return:
		"""
		any_day = datetime.date(input_ym_list[0], input_ym_list[1], 1)
		next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
		result = next_month - datetime.timedelta(days=next_month.day)
		return result

	def get_dt_obj_for_monday_of_weekno(self, year, week_no):
		"""
		입력값:년도, 위크번호
		한주의 시작은 '월'요일 부터이다

		:param year:
		:param week_no:
		:return:
		"""
		utf_local_time = self.check_input_time([year, 1, 1])
		base = 1 if utf_local_time.isocalendar0[1] == 1 else 8
		temp = utf_local_time + datetime.timedelta(days=base - utf_local_time.isocalendar0[2] + 7 * (int(week_no) - 1))
		days = str(temp).split("-")


	def get_dt_obj_with_date_obj_and_time_obj(self, input_date_obj, input_time_obj):
		"""
		날짜객체와 시간객체를 하나로 만드는 것

		:param input_date_obj:
		:param input_time_obj:
		:return:
		"""
		dt_obj = datetime.combine(input_date_obj, input_time_obj)
		return dt_obj

	def get_end_day_for_input_month(self, input_text_time):
		"""
		입력한 날의 월의 마지막 날짜를 계산
		입력받은 날자에서 월을 1나 늘린후 1일을 마이너스 한다
		예: 2023-04-19 -> 2023-05-01 -> 2023-05-01 - 1일 -> 2023-04-30

		:param input_text_time:
		:return:
		"""
		dt_obj = self.check_input_time(input_text_time)
		if dt_obj.month == 12:
			year = dt_obj.year + 1
			month = 1
		else:
			year = dt_obj.year
			month = dt_obj.month + 1
		dt_obj_1 = datetime(year, month, 1)
		dt_obj_2 = dt_obj_1 + timedelta(days=-1)
		result = dt_obj_2.day
		return result

	def get_holiday_between_day1_and_day2(self, input_ymd_list1, input_ymd_list2):
		"""
		날짜사이의 휴일의 리스트 얻기

		:param input_ymd_list1:
		:param input_ymd_list2:
		:return:
		"""
		holiday = self.var["holiday_list"]

		start_day = int(input_ymd_list1[0]) * 10000 + int(input_ymd_list1[1]) * 100 + int(input_ymd_list1[2])
		input_ymd_list2 = self.shift_ymd_list_by_day(input_ymd_list2, 60)
		end_day = int(input_ymd_list2[0]) * 10000 + int(input_ymd_list2[1]) * 100 + int(input_ymd_list2[2])

		result = []
		for list1d in holiday:
			if list1d[0][0] <= start_day and list1d[0][1] >= end_day:
				temp_year = [str(list1d[0][0])[0:4]]
				result.append(temp_year + list1d[1])
		return result

	def get_holiday_list_for_year(self, input_year):
		"""
		특정년도의 휴일을 돌려 줍니다

		:param input_year:
		:return:
		"""
		result = []
		temp = []
		for year in [input_year - 1, input_year, input_year + 1]:
			aaa = self.data_national_holiday_in_year(year)
			for one in aaa:
				bbb = self.check_holiday(year, one)
				for one in bbb:
					temp.append(one)
			print(year, temp)

		for one in temp:
			if int(one[0]) == int(input_year):
				result.append(one)
		return result

	def get_hour_from_utc(self, input_text_time=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		시 -----> ['10', '22']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_text_time:
		:return:
		"""
		utc_local_time = self.check_input_time(input_text_time)
		hour = time.strftime('%I', utc_local_time)
		return hour

	def get_last_day_for_ym_list(self, input_ym_list):
		"""
		양력날짜에서 월의 마지막날을 찾는것
		입력 : [2023, 05]
		출력 : [날짜객체, [1,31], 1, 31]

		:param input_ym_list:
		:return:
		"""
		date = datetime(year=input_ym_list[0], month=input_ym_list[1], day=1).date()
		monthrange = calendar.monthrange(date.year, date.month)
		last_day = calendar.monthrange(date.year, date.month)[1]
		return last_day

	def get_last_day_of_month_for_ym_list(self, input_list=[2002, 3]):
		"""
		입력값 : datetime.date(2012, month, 1)
		결과값 : 원하는 년과 월의 마지막날을 알아내는것

		:param input_list:
		:return:
		"""
		any_day = datetime.date(input_list[0], input_list[1], 1)
		next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail
		result = next_month - timedelta(days=next_month.day)
		return result

	def get_monday_for_year_weekno(self, year, weekno):
		"""
		입력값 : 년도, 위크번호
		한 주의 시작은 '월'요일 부터이다

		:param year:
		:param weekno:
		:return:
		"""

		utc_local_time = self.check_input_time([year, 1, 1])
		base = 1 if utc_local_time.isocalendar()[1] == 1 else 8
		temp = utc_local_time + datetime.timedelta(days=base - utc_local_time.isocalendar()[2] + 7 * (int(weekno) - 1))
		days = str(temp).split("-")

	# input_utf_time_no = nal.change_ymd_list_to_utc([2022, 1, 1])
	# return [str(temp), temp, input_utf_time_no]

	def get_month_from_utc(self, input_text_time=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		월 -----> ['04', Apr, April]
		닞은숫자 -> 많은글자 순으로 정리

		:param input_text_time:
		:return:
		"""
		utc_local_time = self.check_input_time(input_text_time)
		mon = time.strftime('%m', utc_local_time)
		return mon

	def get_month_list_for_year_month(self, input_year, input_month):
		"""
		년과 월을 주면, 한달의 리스트를 알아내는것
		월요일부터 시작

		:param input_year:
		:param input_month:
		:return:
		"""
		result = []
		week_no = []
		date_obj = datetime(year=input_year, month=input_month, day=1).date()
		first_day_wwek_no = calendar.monthrange(date_obj.year, date_obj.month)[0]
		last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
		if first_day_wwek_no == 0:
			pass
		else:
			for no in range(first_day_wwek_no):
				week_no.append("")
		for num in range(1, int(last_day) + 1):
			if len(week_no) == 7:
				result.append(week_no)
				week_no = [num]
			else:
				week_no.append(num)
		if week_no:
			result.append(week_no)
		return result

	def get_month_range_for_ym_list(self, input_ym_list=[2002, 3]):
		"""
		입력월의 첫날과 끝날을 알려주는 것

		:param year:
		:param month:
		:return:
		"""
		date = datetime(year=input_ym_list[0], month=input_ym_list[1], day=1).date()
		monthrange = calendar.monthrange(date.year, date.month)
		first_day = 1
		last_day = calendar.monthrange(date.year, date.month)[1]
		return [first_day, last_day]

	def get_now_as_dt_obj(self):
		"""
		기본인 datetime 객체를 돌려주는 것은 별도로 표기하지 않는다

		:return:
		"""
		dt_obj = datetime.now()
		return dt_obj

	def get_now_as_utc(self):
		"""
		현재의 시간을 utc로 바꿉니다

		:return:
		"""
		time_stamp = time.time()
		result = time.gmtime(time_stamp)
		return result

	def get_one_week_no_7_for_dt_obj(self, input_dt_obj):
		"""
		날짜객체의 week_no_7을 알아내는것
		주의 7번째요일인 일요일의 날짜를 돌려줍니다

		:param input_dt_obj: 날짜 객체
		:return:
		"""
		result = input_dt_obj.strftime('%w')  # 6
		return result

	def get_one_week_no_for_dt_obj(self, input_dt_obj):
		"""
		dt객체에 대한 한해의 몇번째 주인지를 알아낸다

		:param input_dt_obj: 날짜 객체
		:return:
		"""
		result = input_dt_obj.strftime('%w')  # 6
		return result

	def get_sec_from_utc(self, input_text_time=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		초 -----> ['48']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_text_time:
		:return:
		"""
		utc_local_time = self.check_input_time(input_text_time)
		sec = time.strftime('%S', utc_local_time)
		return sec

	def get_time_format(self, input_text_time=""):
		"""

		:param input_text_time:
		:return:
		"""
		self.check_input_time(input_text_time)
		return self.var_common["utc"]

	def get_today_as_dt_obj(self):
		"""
		날짜와 시간(datetime) -> 문자열로 : strftime
		날짜와 시간 형식의 문자열을 -> datetime으로 : strptime

		:return:
		"""
		dt_obj = datetime.now()
		return dt_obj

	def get_today_as_ymd_dash(self):
		"""
		오늘 날짜를 yyyy-mm-dd형식으로 돌려준다
		지금의 날짜를 돌려준다
		입력값 : 없음
		출력값 : 2022-03-01,

		:return:
		"""
		just_now = self.check_input_time("")
		result = just_now.format("YYYY-MM-DD")
		return result

	def get_today_as_yyyy_mm_dd_style(self):
		"""
		날짜와 시간(datetime) -> 문자열로 : strftime
		날짜와 시간 형식의 문자열을 -> datetime으로 : strptime

		:return:
		"""
		dt_obj = datetime.now()
		result = dt_obj.strftime("%Y-%m-%d")
		return result

	def get_week_from_utc(self, input_text_time=""):
		"""
		입력값 : utf시간숫자, 1640995200.0 또는 ""
		주 -----> ['5', '13', 'Fri', 'Friday']
		닞은숫자 -> 많은글자 순으로 정리

		:param input_text_time:
		:return:
		"""
		utc_local_time = self.check_input_time(input_text_time)
		week_no_7 = time.strftime('%w', utc_local_time)
		return week_no_7

	def get_week_no_for_1st_day_of_ym_list(self, input_ym_list):
		"""
		week_no : 1~7까지의 요일에 대한 숫자
		입력한 월의 1일이 무슨요일인지 알아 내는것
		입력 : [2023, 05]
		출력 : 0 ==> 월요일

		:param input_ym_list:
		:return:
		"""
		date = datetime(year=input_ym_list[0], month=input_ym_list[1], day=1).date()
		monthrange = calendar.monthrange(date.year, date.month)
		first_day = calendar.monthrange(date.year, date.month)[0]
		return first_day

	def get_week_no_for_dt_obj(self, input_dt_obj):
		"""
		week_no : 1~7까지의 요일에 대한 숫자
		요일에대한 숫자를, 일요일이 0이다

		:param input_dt_obj: 날짜 객체
		:return:
		"""
		result = input_dt_obj.strftime('%w')
		return result

	def get_week_no_from_utc(self, input_text_time=""):
		"""
		시간이 들어온면
		입력값 : 년도, 위크번호
		한 주의 시작은 '월'요일 부터이다

		:param input_text_time:
		:return:
		"""
		lt = self.check_input_time(input_text_time)
		result = time.strftime('%W', lt)  # 34, 1년중에 몇번째 주인지
		return result

	def get_weekno_for_today(self):
		"""
		weekno : 1년에서 몇번째 주인지 아는것
		입력한날의 week 번호를	계산
		입력값 : 날짜

		:return:
		"""
		today = self.get_today_as_yyyy_mm_dd_style()
		year, month, day = today.split("-")
		utc_local_time = self.check_input_time([year, month, day])
		result = int(utc_local_time.strftime("%W"))
		return result

	def get_weekno_for_ymd_list(self, input_date=""):
		"""
		weekno : 1년에서 몇번째 주인지 아는것
		입력한날의 week 번호를	계산
		입력값 : 날짜

		:param input_date:
		:return:
		"""
		if input_date == "":
			today = self.get_today_as_yyyy_mm_dd_style()
			print(today)
			year, month, day = today.split("-")
			utc_local_time = self.check_input_time([year, month, day])
		else:
			utc_local_time = self.change_any_text_time_to_dt_obj(input_date)
		result = int(utc_local_time.strftime("%W"))
		return result

	def get_ymd_of_monday_for_week_no(self, year, week_no_7):
		"""
		입력값 : 년도, 위크번호
		한 주의 시작은 '월'요일 부터이다

		:param year:
		:param week_no_7:
		:return:
		"""
		first = date(year, 1, 1)
		base = 1 if first.isocalendar()[1] == 1 else 8
		temp = first + timedelta(days=base - first.isocalendar()[2] + 7 * (int(week_no_7) - 1))
		days = str(temp).split("-")

	# input_utf_time_no = nal.change_ymd_utc([2022, 1, 1])
	# return [str(temp), temp, input_utf_time_no]

	def get_ymd_of_monday_for_weekno(self, year, week_no):
		"""
		입력값 : 년도, 위크번호
		한 주의 시작은 '월'요일 부터이다

		:param year:
		:param week_no:
		:return:
		"""
		first = date(year, 1, 1)
		base = 1 if first.isocalendar()[1] == 1 else 8
		temp = first + timedelta(days=base - first.isocalendar()[2] + 7 * (int(week_no) - 1))
		days = str(temp).split("-")

	# input_utf_time_no = nal.change_ymd_utc([2022, 1, 1])
	# return [str(temp), temp, input_utf_time_no]

	def make_time_list_between_2_hsm_list_by_step(self, start_hsm_list, end_hsm_list, step=30):
		"""
		시작과 종료시간을 입력하면, 30분간격으로 시간목록을 자동으로 생성시키는것

		:param start_hsm_list:
		:param end_hsm_list:
		:param step:
		:return:
		"""
		result = []
		hour, min, sec = start_hsm_list
		hour_end, min_end, sec_end = end_hsm_list
		result.append([hour, min, sec])
		while 1:
			min = min + step
			over_min, min = divmod(min, 60)
			if over_min > 0:
				hour = hour + over_min
			hour = divmod(hour, 24)[1]
			if int(hour) * 60 + int(min) > int(hour_end) * 60 + int(min_end):
				break
			result.append([hour, min, sec])
		return result

	def make_time_list_by_step(self, start_hsm_list, step=30, cycle=20):
		"""
		시작과 종료시간을 입력하면, 30분간격으로 시간목록을 자동으로 생성시키는것

		:param start_hsm_list:
		:param step:
		:param cycle:
		:return:
		"""
		result = []
		hour, min, sec = start_hsm_list
		result.append([hour, min, sec])
		for one in range(cycle):
			min = min + step
			over_min, min = divmod(min, 60)
			if over_min > 0:
				hour = hour + over_min
			hour = divmod(hour, 24)[1]
			result.append([hour, min, sec])
		return result

	def make_time_list_by_step_with_start_end(self, start_hsm_list, end_hsm_list, step=30):
		"""
		시작과 종료시간을 입력하면, 30분간격으로 시간목록을 자동으로 생성시키는것

		:param start_hsm_list:
		:param end_hsm_list:
		:param step:
		:return:
		"""
		result = []
		hour, min, sec = start_hsm_list
		hour_end, min_end, sec_end = end_hsm_list
		result.append([hour, min, sec])
		while 1:
			min = min + step
			over_min, min = divmod(min, 60)
			if over_min > 0:
				hour = hour + over_min
			hour = divmod(hour, 24)[1]
			if int(hour) * 60 + int(min) > int(hour_end) * 60 + int(min_end):
				break
			result.append([hour, min, sec])
		return result

	def make_time_list_for_hsm_list_by_step_cycle(self, start_hsm_list, step=30, cycle=20):
		"""
		시작과 종료시간을 입력하면, 30분간격으로 시간목록을 자동으로 생성시키는것

		:param start_hsm_list:
		:param step:
		:param cycle:
		:return:
		"""
		result = []
		hour, min, sec = start_hsm_list
		result.append([hour, min, sec])
		for one in range(cycle):
			min = min + step
			over_min, min = divmod(min, 60)
			if over_min > 0:
				hour = hour + over_min
			hour = divmod(hour, 24)[1]
			result.append([hour, min, sec])
		return result

	def make_unique_words(self, input_list2d):
		"""
		입력으로 들어온 자료들을 단어별로 구분하기위해서 만든것이며 /,&-등의 문자는 없앨려고 하는것이다

		:param input_list2d:
		:return:
		"""

		list1d = []
		for one in input_list2d:
			list1d.extend(one)
		temp_result = []
		for one in list1d:
			one = str(one).lower()
			one = one.replace("/", " ")
			one = one.replace(",", " ")
			one = one.replace("&", " ")
			one = one.replace("-", " ")
			temp_result.extend(one.split(" "))
		result = list(set(temp_result))
		return result

	def minus_date0_date1(self, input_date1, input_date2):
		"""
		두날짜의 빼기


		:param input_date1:
		:param input_date2:
		:return:
		"""
		utc1 = self.change_any_text_time_to_dt_obj(input_date1)
		utc2 = self.change_any_text_time_to_dt_obj(input_date2)
		result = abs((float(utc1) - float(utc2)) / (60 * 60 * 24))
		return result

	def replace_holiday_for_sunday(self, input_data):
		"""
		대체공휴일의 날짜를 확인하는 것이다
		input_data : [2009, 5, 5, 5, 5, '양', 1, '', '어린이날']
		[시작일], [끝나는날],[월, 일, 음/양, 몇일간, 윤달여부],[요일 - 대체적용일], [설명]

		:param input_data:
		:return:
		"""
		holiday_replace = [
			[[19590327, 19601230], ["all"], [6], ["대체공휴일제도"]],  # 모든공휴일에 대해서 대체공휴일 적용(일요일)
			[[19890301, 19901130], ["all"], [6], ["대체공휴일제도"]],  # 모든공휴일에 대해서 대체공휴일 적용(일요일)

			[[20131105, 99991231], [12, "말일", "음", 1, "윤달"], [6], ["설날", "대체공휴일제도"]],
			[[20131105, 99991231], [1, 1, "음", 2, "평달"], [6], ["신정", "대체공휴일제도"]],
			[[20131105, 99991231], [5, 5, "양", 1, ""], [5, 6], ["어린이날", "대체공휴일제도"]],  # 토/일요일
			[[20131105, 99991231], [8, 14, "음", 3, "평달"], [6], ["추석", "대체공휴일제도"]],

			[[20210715, 99991231], [3, 1, "양", 1, ""], [6], ["31절", "대체공휴일제도"]],
			[[20210715, 99991231], [10, 3, "양", 1, ""], [6], ["개천절", "대체공휴일제도"]],
			[[20210715, 99991231], [10, 9, "양", 1, ""], [6], ["한글날", "대체공휴일제도"]],

			[[20230504, 99991231], [12, 25, "양", 1, ""], [6], ["기독탄신일", "대체공휴일제도"]],
			[[20230504, 99991231], [4, 8, "음", 1, "평달"], [6], ["부처님오신날", "대체공휴일제도"]],
		]

		result = []
		dt_obj = self.change_ymd_list_to_dt_obj(input_data[0:3])
		week_no_7 = self.get_week_no_7_for_dt_obj(dt_obj)
		day_no = int(input_data[0]) * 10000 + int(input_data[1]) * 100 + int(input_data[2])

		for list1d in holiday_replace:
			change_day = False
			if list1d[0][0] <= day_no and list1d[0][1] >= day_no:
				if list1d[1][0] == "all" and week_no_7 in list1d[3]:
					# 대체휴일적용대상임
					change_day = True
				elif input_data[-1] == list1d[-1][0] and week_no_7 in list1d[3]:
					change_day = True

			if change_day:
				# print("대체공휴일 적용 =====> ")
				new_dt_obj = dt_obj + timedelta(days=1)
				new_ymd_list = self.change_dt_obj_to_ymd_list(new_dt_obj)
				result = new_ymd_list + input_data[3:] + ["대체공휴일적용", ]

		return result

	def replace_time(self, dt_obj, input_dic):
		"""
		datetime.replace(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo, *, fold=0)
		입력된 시간의 특정 단위를 바꿀수있다
		즉, 모든 년을 2002로 바꿀수도 있다는 것이다

		:param dt_obj: 날짜 객체
		:param input_dic:
		:return:
		"""
		new_dt_obj = dt_obj.replace(input_dic)
		return new_dt_obj

	def shift_dt_obj_by_day(self, dt_obj, input_no):
		"""
		날짜를 이동

		:param dt_obj: 날짜 객체
		:param input_no:
		:return:
		"""
		new_dt_obj = dt_obj + timedelta(days=input_no)
		return new_dt_obj

	def shift_dt_obj_by_hour(self, dt_obj, input_no):
		"""
		시간을 이동

		:param dt_obj: 날짜 객체
		:param input_no:
		:return:
		"""
		new_dt_obj = dt_obj + timedelta(hours=input_no)
		return new_dt_obj

	def shift_dt_obj_by_min(self, dt_obj, input_no):
		"""
		분을 이동

		:param dt_obj: 날짜 객체
		:param input_no:
		:return:
		"""
		new_dt_obj = dt_obj + timedelta(minutes=input_no)
		return new_dt_obj

	def shift_dt_obj_by_month(self, dt_obj, input_month_no):
		"""
		월을 이동

		:param dt_obj: 날짜 객체
		:param input_month_no:
		:return:
		"""

		original_mon = dt_obj.month
		original_year = dt_obj.year

		delta_year, delta_month = divmod(input_month_no, 12)

		if original_mon <= delta_month * -1 and 0 > delta_month:
			original_mon = original_mon + 12
			original_year = original_year - 1

		new_month = original_mon + delta_month
		new_year = original_year + delta_year

		delta_year_1, delta_month_1 = divmod(new_month, 12)
		final_new_year = original_year + delta_year_1

		new_dt_obj = dt_obj.replace(year=final_new_year)
		new_dt_obj = new_dt_obj.replace(month=delta_month_1)
		return new_dt_obj

	def shift_dt_obj_by_sec(self, dt_obj, input_no):
		"""
		날짜객체를 초단위로 이동시키는 것

		:param dt_obj: 날짜 객체
		:param input_no:
		:return:
		"""
		new_dt_obj = dt_obj + timedelta(seconds=input_no)
		return new_dt_obj

	def shift_dt_obj_by_year(self, dt_obj, input_year_no):
		"""
		년을 이동

		:param dt_obj: 날짜 객체
		:param input_year_no:
		:return:
		"""
		new_year = dt_obj.year + input_year_no
		new_dt_obj = dt_obj.replace(year=new_year)
		return new_dt_obj

	def shift_text_time_by_month(self, input_text_time, input_month_no):
		"""
		기준날짜에서 월을 이동시키는것

		:param input_text_time:
		:param input_month_no:
		:return:
		"""
		utf_time = self.check_input_time(input_text_time)

		input_list = self.change_text_time_to_ymd_style(utf_time)
		year = int(input_list[0])
		month = int(input_list[1])
		day = int(input_list[2])

		add_year, remain_month = divmod((month + int(input_month_no)), 12)
		if remain_month == 0:
			add_year = add_year - 1
			remain_month = 12
		result = [year + int(add_year), remain_month, day]
		return result

	def shift_ymd_list_as_ymd_list(self, ymd_list_1, ymd_list_2):
		"""
		ymd_list형식의 입력값을 3년 2개월 29일을 이동시킬때 사용하는것

		:param ymd_list_1:
		:param ymd_list_2:
		:return:
		"""
		dt_obj = self.change_ymd_list_to_dt_obj(ymd_list_1)
		changed_dt_obj = self.shift_dt_obj_by_day(dt_obj, ymd_list_2[2])
		changed_dt_obj = self.shift_dt_obj_by_month(changed_dt_obj, ymd_list_2[1])
		changed_dt_obj = self.shift_dt_obj_by_year(changed_dt_obj, ymd_list_2[0])
		result = self.change_dt_obj_to_ymd_list(changed_dt_obj)
		return result

	def shift_ymd_list_by_day(self, input_text_time="", input_no=""):
		"""
		입력한 날짜리스트를 기준으로 날을 이동시키는것
		아무것도 입력하지 않으면 현재 시간
		입력값 : [2022, 03, 02]
		출력값 : 2022-01-01

		:param input_text_time:
		:param input_no:
		:return:
		"""
		utc_local_time = self.check_input_time(input_text_time)
		dt_obj = utc_local_time.shift(days=int(input_no))
		result = self.change_dt_obj_to_ymd_list(dt_obj)
		return result

	def shift_ymd_list_by_month(self, input_text_time="", input_month=3):
		"""
		기준날짜에서 월을 이동시키는것

		:param input_text_time:
		:param input_month:
		:return:[2022, 3, 1]
		"""
		utc_local_time = self.check_input_time(input_text_time)
		dt_obj = utc_local_time.shift(months=int(input_month))
		result = self.change_dt_obj_to_ymd_list(dt_obj)
		return result

	def shift_ymd_list_by_year(self, input_ymd_list="", input_year=3):
		"""
		기준날짜에서 년을 이동시키는것
		입력형태 : [2022, 3, 1]

		:param input_ymd_list: [2022, 3, 1]
		:param input_year:
		:return:
		"""
		utc_local_time = self.check_input_time(input_ymd_list)
		dt_obj = utc_local_time.shift(years=int(input_year))
		result = self.change_dt_obj_to_ymd_list(dt_obj)
		return result

	def split_period_as_year_basis(self, input_ymd_list1, input_ymd_list2):
		"""
		날짜기간이 년이 다른경우 같은 year들로 리스트형태로 기간을 만들어 주는것
		입력값을 확인하는 것이다

		:param input_ymd_list1:
		:param input_ymd_list2:
		:return:
		"""
		dt_obj1 = self.check_input_time(input_ymd_list1)
		input_ymd_list1 = self.change_dt_obj_to_ymd_list(dt_obj1)

		dt_obj2 = self.check_input_time(input_ymd_list2)
		input_ymd_list2 = self.change_dt_obj_to_ymd_list(dt_obj2)

		# 2가지의 날짜가 들어오면, 1년단위로 시작과 끝의 날짜를 만들어 주는 것이다
		start_1 = int(input_ymd_list1[0]) * 10000 + int(input_ymd_list1[1]) * 100 + int(input_ymd_list1[2])
		end_1 = int(input_ymd_list2[0]) * 10000 + int(input_ymd_list2[1]) * 100 + int(input_ymd_list2[2])
		result = []

		# 날짜가 늦은것을 뒤로가게 만드는 것이다
		start_ymd = input_ymd_list1
		end_ymd = input_ymd_list2
		if start_1 > end_1:
			start_ymd = input_ymd_list2
			end_ymd = input_ymd_list1

		# 만약 년도가 같으면, 그대로 돌려준다
		if int(start_ymd[0]) == int(end_ymd[0]):
			result = [[start_ymd, end_ymd]]
		# 만약 1년의 차이만 나면, 아래와 같이 간단히 만든다
		elif int(end_ymd[0]) - int(start_ymd[0]) == 1:
			result = [
				[start_ymd, [start_ymd[0], 12, 31]],
				[[end_ymd[0], 1, 1], end_ymd],
			]
		# 2년이상이 발생을 할때 적용하는 것이다
		else:
			result = [[start_ymd, [start_ymd[0], 12, 31]], ]
			for year in range(int(start_ymd[0]) + 1, int(end_ymd[0])):
				result.append([[year, 1, 1], [year, 12, 31]])
			result.append([[end_ymd[0], 1, 1], end_ymd])
		return result


	def time_list_by_step(self, start_hsm_list, step=30, cycle=20):
		"""
		시작과 종료시간을 입력하면, 30분간격으로 시간목록을 자동으로 생성시키는것

		:param start_hsm_list:
		:param step:
		:param cycle:
		:return:
		"""
		result = []
		hour, min, sec = start_hsm_list
		result.append([hour, min, sec])
		for one in range(cycle):
			min = min + step
			over_min, min = divmod(min, 60)
			if over_min > 0:
				hour = hour + over_min
			hour = divmod(hour, 24)[1]
			result.append([hour, min, sec])
		return result

	def time_list_by_step_with_start_end(self, start_hsm_list, end_hsm_list, step=30):
		"""
		시작과 종료시간을 입력하면, 30분간격으로 시간목록을 자동으로 생성시키는것

		:param start_hsm_list:
		:param end_hsm_list:
		:param step:
		:return:
		"""
		result = []
		hour, min, sec = start_hsm_list
		hour_end, min_end, sec_end = end_hsm_list
		result.append([hour, min, sec])
		while 1:
			min = min + step
			over_min, min = divmod(min, 60)
			if over_min > 0:
				hour = hour + over_min
				hour = divmod(hour, 24)[1]
			if int(hour) * 60 + int(min) > int(hour_end) * 60 + int(min_end):
				break
			result.append([hour, min, sec])
		return result

