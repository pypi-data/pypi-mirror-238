# -*- coding: utf-8 -*-
import re #내장모듈
import basic_data  # xython 모듈

class jfinder:
    def __init__(self):
        # 공통으로 사용할 변수들을 설정하는 것
        self.base_data = basic_data.basic_data()
        self.var = self.base_data.vars  # 패키지내에서 공통으로 사용되는 변수

    def jfinder (self, input_text=""):
        """
        기본저긴 ezre_sql -> re_sql형식으로 만들어 주는것

        :param input_text: 입력되는 text문장
        :return:
		"""

        re_sql = input_text.replace(" ", "")

        setup_list = [
            ["(대소문자무시)", "(?!)"], #re.IGNORECASE 대소문자 무시
            ["(여러줄)", "(?m)"], # re.MULITILINE 여러줄도 실행
            ["(개행문자포함)", "(?s)"], # re.DOTALL 개행문자도 포함
            ]

        for one in setup_list:
            re_sql = re_sql.replace(one[0], one[1])

        basic_list = [
            ["[\[](\d+)[~](\d*)[\]]", "{\\1,\\2}"],  # [3~4] ==> {3,4}
            [":(\d+)[~](\d*)[\]]", "]{\\1,\\2}"],  # :3~4] ==> ]{3,4}

            ["\(back_ok:(.*)\)",                "(?=\\1)" ], #(뒤에있음:(abc)) => (?=abc)
            ["\(back_no:(.*)\)",                "(?!\\1)" ], #(뒤에없음:(abc)) => (?!abc)
            ["\(front_ok:(.*)\)",                "(?<=\\1)"], #(앞에있음:(abc)) => (?<=abc)
            ["\(front_no:(.*)\)",                "(?<!\\1)"], #(앞에없음:(abc)) => (?<!abc)


            ["\(뒤에있음:(.*)\)", "(?=\\1)"],  # (뒤에있음:(abc)) => (?=abc)
            ["\(뒤에없음:(.*)\)", "(?!\\1)"],  # (뒤에없음:(abc)) => (?!abc)
            ["\(앞에있음:(.*)\)", "(?<=\\1)"],  # (앞에있음:(abc)) => (?<=abc)
            ["\(앞에없음:(.*)\)", "(?<!\\1)"],  # (앞에없음:(abc)) => (?<!abc)


            ["([\[]?)영어대문자[&]?([\]]?)",     "\\1A-Z\\2"],
            ["([\[]?)영어소문자[&]?([\]]?)",     "\\1a-z\\2"],
            ["([\[]?)특수문자(.+?)([\]]?)",      "\\1\\2\\3"],
            ["([\[]?)한글모음[&]?([\]]?)",       "\\1ㅏ-ㅣ\\2"], #[ㅏ-ㅣ]
            ["([\[]?)모든문자[&]?([\]]?)",      "\\1.\n\\2"],
            ["([\[]?)일본어[&]?([\]]?)",        "\\1ぁ-ゔ|ァ-ヴー|々〆〤\\2"],
            ["([\[]?)한글[&]?([\]]?)",          "\\1ㄱ-ㅎ|ㅏ-ㅣ|가-힣\\2"],
            ["([\[]?)숫자[&]?([\]]?)",          "\\1\\\d\\2"],
            ["([\[]?)영어[&]?([\]]?)",          "\\1a-zA-Z\\2"],
            ["([\[]?)한자[&]?([\]]?)",          "\\1一-龥\\2"],
            ["([\[]?)문자[&]?([\]]?)",          "\\1.\\2"],
            ["([\[]?)공백[&]?([\]]?)",          "\\1\\\s\\2"],


            ["([\[]?)eng_big[&]?([\]]?)", "\\1A-Z\\2"],
            ["([\[]?)eng_sma[&]?([\]]?)", "\\1a-z\\2"],
            ["([\[]?)special(.+?)([\]]?)", "\\1\\2\\3"],
            ["([\[]?)mo[&]?([\]]?)", "\\1ㅏ-ㅣ\\2"],  # [ㅏ-ㅣ]
            ["([\[]?)all_char[&]?([\]]?)", "\\1.\n\\2"],
            ["([\[]?)jpn[&]?([\]]?)", "\\1ぁ-ゔ|ァ-ヴー|々〆〤\\2"],
            ["([\[]?)kor[&]?([\]]?)", "\\1ㄱ-ㅎ|ㅏ-ㅣ|가-힣\\2"],
            ["([\[]?)num[&]?([\]]?)", "\\1\\\d\\2"],
            ["([\[]?)eng[&]?([\]]?)", "\\1a-zA-Z\\2"],
            ["([\[]?)chi[&]?([\]]?)", "\\1一-龥\\2"],
            ["([\[]?)cha[&]?([\]]?)", "\\1.\\2"],
            ["([\[]?)space[&]?([\]]?)", "\\1\\\s\\2"],


            ["[\[]단어([(].*?[)])([\]]?)",      "\\1"],
            ["[\[]또는([(].*?[)])([\]]?)",      "\\1|"],
            ["[\(]이름<(.+?)>(.+?)[\)]",        "?P<\\1>\\2"], #[이름<abc>표현식]

        ]


        for one in basic_list:
            re_sql = re.sub(one[0], one[1], re_sql)
            re_sql = re_sql.replace(" ", "")

        simple_list = [
            ['[begin]', '^'],
            ['[처음]', '^'], ['[맨앞]', '^'], ['[시작]', '^'],
            ['[맨뒤]', '$'], ['[맨끝]', '$'], ['[끝]', '$'],
            ['[end]', '$'],
            ['[또는]', '|'], ['또는', '|'],['or', '|'],
            ['not', '^'],
            ]

        for one in simple_list:
            re_sql = re_sql.replace(one[0], one[1])

        #최대탐색을 할것인지 최소탐색을 할것인지 설정하는 것이다
        if "(최소찾기)" in re_sql:
            re_sql = re_sql.replace("[1,]","+")
            re_sql = re_sql.replace("[1,]","*")

            re_sql = re_sql.replace("+","+?")
            re_sql = re_sql.replace("*","*?")
            re_sql = re_sql.replace("(최소찾기)","")

        #이단계를 지워도 실행되는데는 문제 없으며, 실행 시키지 않았을때가 약간 더 읽기는 편하다
        high_list = [
            ['[^a-zA-Z0-9]', '\W'],
            ['[^0-9a-zA-Z]', '\W'],
            ['[a-zA-Z0-9]', '\w'],
            ['[0-9a-zA-Z]', '\w'],
            ['[^0-9]', '\D'],
            ['[0-9]', '\d'],
            ['{0,}', '*'],
            ['{1,}', '+'],
            ]

        for one in high_list:
            re_sql = re_sql.replace(one[0], one[1])

        #print ("result ==> ", result)

        if "[.]" in re_sql:
            re_sql = re_sql.replace("[.]", ".")

        return re_sql

    def change_ezre_sql_to_re_sql (self, ezre_sql):
        """
        ezre_sql을 regex스타일로 바꾸는것

        :param ezre_sql: 정규표현식을 쉽게 만들도록 변경한 형태의 문장
        :return:
        """
        result = self.jfinder(ezre_sql)
        return result

    def delete_except_num_eng(self, input_text):
        """
        영문과 숫자와 공백을 제외하고 다 제거를 하는것

        :param input_text: 입력되는 text문장
        :return:
        """
        result = []
        for one_data in input_text:
            temp = ""
            for one in one_data:
                if str(one) in ' 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_':
                    temp = temp + str(one)
            result.append(temp)
        return result

    def delete_eng_num(self, input_text):
        """
        알파벳과 숫자만 삭제하는것

        :param input_text: 입력되는 text문장
        :return:
		"""
        re_com = re.compile("[A-Za-z0-9]*")
        if (re_com.search(input_text) == None):
            new_text = input_text
        else:
            new_text = re_com.sub("", input_text)
        return new_text

    def delete_koren_eng_num(self, input_text):
        """
        한글, 영어, 숫자만 지우는 것

        :param input_text: 입력되는 text문장
        :return:
		"""
        re_com = re.compile("[A-Za-z0-9ㄱ-ㅎㅏ-ㅣ가-힣]*")
        if (re_com.search(input_text) == None):
            new_text = input_text
        else:
            new_text = re_com.sub("", input_text)
        return new_text

    def delete_num_comma(self, input_text):
        """
        숫자중에서 콤마(,)로 분비리된것중에서 ,만 없애는것
        1,234,567 => 1234567

        :param input_text: 입력되는 text문장
        :return:
		"""
        re_com = re.compile("[0-9,]*\.?[0-9]*")
        new_text = re_com.sub("", input_text)
        return new_text

    def delete_special_char(self, input_text):
        """
        공백과 특수문자등을 제외하고 같으면 새로운 y열에 1을 넣는 함수
        리스트의 사이즈를 조정한다

        :param input_text: 입력되는 text문장
        :return:
		"""
        re_com = re.compile("[\s!@#$%^*()\-_=+\\\|\[\]{};:'\",.<>\/?]*")
        if (re_com.search(input_text) == None):
            new_text = input_text
        else:
            new_text = re_com.sub("", input_text)
        return new_text

    def delete_except_special_char(self, input_text):
        """
		공백과 특수문자등을 제외하고 같으면 새로운 y열에 1을 넣는 함수
		리스트의 사이즈를 조정한다

        :param input_text: 입력되는 text문장
        :return:
		"""
        re_com = re.compile("[^\s!@#$%^*()\-_=+\\\|\[\]{};:'\",.<>\/?]*")
        if (re_com.search(input_text) == None):
            new_text = input_text
        else:
            new_text = re_com.sub("", input_text)
        return new_text

    def delete_text_special_letter(self, input_list):
        """
        입력받은 텍스트로된 리스트의 자료를 전부 특수문자를 없앤후 돌려주는 것이다
        입력된 자료가 1차원 리스트인지 판단한다

        :param input_list:
        :return:
		"""
        result = []
        if type(input_list) == type([]) and type(input_list[0]) != type([]):
            for one in input_list:
                if one != "" or one != None:
                    temp = self.delete_except_special_char(one)
                    result.append(temp)
        return result

    def delete_with_ezre_sql (self, ezre_sql, input_text):
        """
        입력자료중 ezre_sql에 맞는 형식을 삭제하는것

        :param ezre_sql: 정규표현식을 쉽게 만들도록 변경한 형태의 문장
        :param input_text: 입력되는 text문장
        :return:
        """
        re_sql = self.jfinder(ezre_sql)
        re.sub(re_sql, "", input_text)
        result = self.search_all_by_ezre_sql(re_sql, input_text)
        return result

    def is_number_only(self, input_text):
        """
        소슷점까지는 포함한것이다

        :param input_text: 입력되는 text문장
        :return:
		"""
        result = False
        temp = re.match("^[0-9.]+$", input_text)
        if temp:
            result = True
        return result

    def is_korean_only(self, input_text):
        """
		모두 한글인지

        :param input_text: 입력되는 text문장
        :return:
		"""
        re_basic = "^[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+$"
        result = False
        temp = re.match(re_basic, input_text)
        if temp : result = True
        return result

    def is_special_char_in(self, input_text):
        """
		특수문자가들어가있는지

        :param input_text: 입력되는 text문장
        :return:
		"""
        re_basic = "^[a-zA-Z0-9]+$"
        result = False
        temp = re.match(re_basic, input_text)
        if temp : result = True
        return result

    def is_handphone_only(self, input_text):
        """
		특수문자가들어가있는지

        :param input_text: 입력되는 text문장
        :return:
    	"""
        re_basic = "^(010|019|011)-\d{4}-\d{4}+$"
        result = False
        temp = re.match(re_basic, input_text)
        if temp : result = True
        return result

    def make_list_on_re_compile(self, re_sql, file_name):
        """
        텍스트화일을 읽어서 re에 맞도록 한것을 리스트로 만드는 것이다
        함수인 def를 기준으로 저장을 하며, [[공백을없앤자료, 원래자료, 시작줄번호].....]

        :param re_sql: 정규표현식으로 만들어진 형태
        :param file_name:
        :return:
		"""
        re_com = re.compile(re_sql)
        f = open(file_name, 'r', encoding='UTF8')
        lines = f.readlines()
        num = 0
        temp = ""
        temp_original = ""
        result = []
        for one_line in lines:
            aaa = re.findall(re_com, str(one_line))
            original_line = one_line
            changed_line = one_line.replace(" ", "")
            changed_line = changed_line.replace("\n", "")

            if aaa:
                result.append([temp, temp_original, num])
                temp = changed_line
                temp_original = original_line
            # print("발견", num)
            else:
                temp = temp + changed_line
                temp_original = temp_original + one_line
        return result

    def replace_with_ezre_sql (self, ezre_sql, replace_word, input_text):
        """
        입력자료를 원하는 문자로 바꾸는것

        :param re_sql: 정규표현식으로 만들어진 형태
        :param replace_word:
        :param input_text: 입력되는 text문장
        :return:
        """
        re_sql = self.jfinder(ezre_sql)
        re.sub(re_sql, replace_word, input_text, flags=re.MULTILINE)
        result = self.search_all_by_ezre_sql(re_sql, input_text)
        return result

    def run_with_ezre_sql (self, ezre_sql, input_text):
        """
        결과값을 얻는것이 여러조건들이 있어서 이것을 하나로 만듦
        [[결과값, 시작순서, 끝순서, [그룹1, 그룹2...], match결과].....]

        :param ezre_sql: 정규표현식을 쉽게 만들도록 변경한 형태의 문장
        :param input_text: 입력되는 text문장
        :return:
		"""
        re_sql = self.jfinder(ezre_sql)
        re_com = re.compile(re_sql)
        result_match = re_com.match(input_text)
        result_finditer = re_com.finditer(input_text)

        final_result = []
        num=0
        for one_iter in result_finditer:
            temp=[]
            #찾은 결과값과 시작과 끝의 번호를 넣는다
            temp.append(one_iter.group())
            temp.append(one_iter.start())
            temp.append(one_iter.end())

            #그룹으로 된것을 넣는것이다
            temp_sub = []
            if len(one_iter.group()):
                for one in one_iter.groups():
                    temp_sub.append(one)
                temp.append(temp_sub)
            else:
                temp.append(temp_sub)

            #제일 첫번째 결과값에 match랑 같은 결과인지 넣는것
            if num == 0: temp.append(result_match)
            final_result.append(temp)
            num+=1
        return final_result

    def search_all_cap(self, input_text):
        """
        모두 알파벳대문자

        :param input_text: 입력되는 text문장
        :return:
		"""
        re_basic = "^[A-Z]+$"
        result = re.findall(re_basic, input_text)
        return result

    def search_handphone(self, input_text):
        """
        특수문자가들어가있는지

        :param input_text: 입력되는 text문장
        :return:
		"""
        re_basic = "^(010|019|011)-\d{4}-\d{4}"
        result = re.findall(re_basic, input_text)
        return result

    def search_ip_address(self, input_text):
        """
        이메일주소 입력

        :param input_text: 입력되는 text문장
        :return:
		"""
        re_basic = "((?:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d))"
        result = re.findall(re_basic, input_text)
        return result

    def search_korean(self, input_text):
        """
        모두 한글인지

        :param input_text: 입력되는 text문장
        :return:
		"""
        re_basic = "[ㄱ-ㅣ가-힣]"
        result = re.findall(re_basic, input_text)
        return result

    def search_special_char(self, input_text):
        """
        특수문자가들어가있는지

        :param input_text: 입력되는 text문장
        :return:
		"""
        re_basic = "^[a-zA-Z0-9]"
        result = re.findall(re_basic, input_text)
        return result

    def search_number_between_len1_len2(self, m, n, input_text):
        """
        m,n개사이인것만 추출

        :param m:
        :param n:
        :param input_text: 입력되는 text문장
        :return:
		"""
        re_basic = "^\d{" + str(m) + "," + str(n) + "}$"
        result = re.findall(re_basic, input_text)
        return result

    def search_dash_date(self, input_text):
        """
        모두 알파벳대문자

        :param input_text: 입력되는 text문장
        :return:
		"""
        re_basic = "^\d{4}-\d{1,2}-\d{1,2}$"
        result = re.findall(re_basic, input_text)
        return result

    def search_email_address(self, input_text):
        """
        이메일주소 입력

        :param input_text: 입력되는 text문장
        :return:
		"""
        re_basic = "^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
        result = re.findall(re_basic, input_text)
        return result

    def search_eng(self, input_text):
        """
        모두 영문인지

        :param input_text: 입력되는 text문장
        :return:
		"""
        re_basic = "^[a-zA-Z]+$"
        result = re.findall(re_basic, input_text)
        return result

    def search_between_len1_len2(self, m, n , input_text):
        """
        문자수제한 : m다 크고 n보다 작은 문자

        :param m:
        :param n:
        :param input_text: 입력되는 text문장
        :return:
		"""
        re_basic = "^.{" + str(m) + "," + str(n) + "}$"
        result = re.findall(re_basic, input_text)
        return result

    def search_num(self, input_text):
        """
		단어중에 나와있는 숫자만 분리하는기능

        :param input_text: 입력되는 text문장
        :return:
		"""
        re_compile = re.compile(r"([0-9]+)")
        result = re_compile.findall(input_text)
        new_result = []
        for dim1_data in result:
            for dim2_data in dim1_data:
                new_result.append(dim2_data)
        return new_result

    def search_between_word1_word2_by_ezre_sql(self, word_a, word_b, input_text):
        """
        두 단어사이의 글자를 갖고오는 것

        :param word_a:
        :param word_b:
        :param input_text: 입력되는 text문장
        :return:
        """
        ezre_sql = "(?<=\\" + str(word_a) + ")(.*?)(?="+str(word_b) + ")"
        result = self.search_all_by_ezre_sql(ezre_sql, input_text)
        return result

    def search_between_brackets_by_ezre_sql(self, input_text):
        """
        괄호안의 문자 갖고오기
        괄호 내부 내용만 추출 : '\(([^)]+)'
        앞 뒤 괄호까지 포함 : '\([^)]+\)'

        :param input_text: 입력되는 text문장
        :return:
        """

        ezre_sql = "(?<=\\()(.*?)(?=\\))"
        result = self.search_all_by_ezre_sql(ezre_sql, input_text)
        return result

    def search_with_ezre_sql (self, ezre_sql, input_text):
        """

        :param ezre_sql: 정규표현식을 쉽게 만들도록 변경한 형태의 문장
        :param input_text: 입력되는 text문장
        :return:
        """
        re_sql = self.jfinder(ezre_sql)
        result = self.search_all_by_ezre_sql(re_sql, input_text)
        return result

    def search_all_by_ezre_sql (self, re_sql, input_text):
        """
        결과값을 얻는것이 여러조건들이 있어서 이것을 하나로 만듦
        [[결과값, 시작순서, 끝순서, [그룹1, 그룹2...], match결과].....]

        :param re_sql: 정규표현식으로 만들어진 형태
        :param input_text: 입력되는 text문장
        :return:
        """
        #print("re문장은 : ", re_sql)
        #print("결과값의 의미 : [[결과값, 시작순서, 끝순서, [그룹1, 그룹2...], match결과].....]")
        re_com = re.compile(re_sql)
        result_match = re_com.match(input_text)
        result_finditer = re_com.finditer(input_text)

        final_result = []
        num=0
        for one_iter in result_finditer:
            temp=[]
            #찾은 결과값과 시작과 끝의 번호를 넣는다
            temp.append(one_iter.group())
            temp.append(one_iter.start())
            temp.append(one_iter.end())

            #그룹으로 된것을 넣는것이다
            temp_sub = []
            if len(one_iter.group()):
                for one in one_iter.groups():
                    temp_sub.append(one)
                temp.append(temp_sub)
            else:
                temp.append(temp_sub)

            #제일 첫번째 결과값에 match랑 같은 결과인지 넣는것
            if num == 0: temp.append(result_match)
            final_result.append(temp)
            num+=1
        return final_result

    def delete_all_explanation(self, input_text):
        """
		py화일의 설명문의 줄들을 제거하는 코드

        :param input_text: 입력되는 text문장
        :return:
		"""
        input_text = re.sub(re.compile(r"[\s]*#.*[\n]"), "\\n", input_text)
        input_text = re.sub(re.compile(r"[\s]*'''.*?'''", re.DOTALL | re.MULTILINE), "\n", input_text)
        input_text = re.sub(re.compile(r'[\s]*""".*?"""', re.DOTALL | re.MULTILINE), "\n", input_text)
        input_text = re.sub(re.compile(r'^[\s]*[\n]'), "", input_text)
        return input_text

    def delete_over_2_empty_lines(self, input_text):
        """

        :param input_text: 입력되는 text문장
        :return:
        """
        input_text = re.sub(re.compile(r"([\s]*\\n){2,}"), "\\n", input_text)
        return input_text

    ####################################################################

    def change_number_to_tel_style(self, input_value):
       """
       전화번호나 핸드폰 번호 스타일을 바꿔주는것
       전화번호를 21345678 =>02-134-5678 로 변경하는 것
       :param input_value:
       :return:
       """

       result = input_value
       value = str(int(input_value))
       if len(value) == 8 and value[0] == "2":
          # 22345678 => 02-234-5678
          result = "0" + value[0:1] +"-"+ value[1:4] +"-"+ value[4:]
       elif len(value) == 9:
          if value[0:2] == "2":
             # 223456789 => 02-2345-6789
             result = "0" + value[0:1] +"-"+ value[1:5] +"-"+ value[5:]
          elif value[0:2] == "11":
             # 113456789 => 011-345-6789
             result = "0" + value[0:2] +"-"+ value[2:5] +"-"+ value[5:]
          else:
             # 523456789 => 052-345-6789
             result = "0" + value[0:2] +"-"+ value[2:5] +"-"+ value[5:]
       elif len(value) == 10:
          # 5234567890 => 052-3456-7890
          # 1034567890 => 010-3456-7890
          result = "0" + value[0:2] +"-"+ value[2:6] +"-"+ value[6:]
       return result

    def data_well_used_re(self):
        """
        잘 사용하는 re코드들
        [이름, 찾을코드, 바꿀코드, 설명

        :return:
        """
        result = self.var["well_used_re"]
        return result

    def delete_no_meaning_words(self, input_list, change_word_dic):
        """

        :param input_list:
        :param change_word_dic:
        :return:
        """
        sql_1 = "[시작][숫자&특수문자:1~][끝]"  # 숫자만있는것을 삭제
        sql_2 = "[시작][숫자:1:5][영어&한글:1:1][끝]"  # 1223개 와 같은것 삭제
        sql_3 = "[시작][한글:1~][끝]"  #
        sql_4 = "[\(][문자:1~][\)]"  # 괄호안의 ㄱ르자

        result = []
        for one in input_list:
            one = str(one).strip()
            if self.check_ok_or_no(sql_3, one):
                if one in list(change_word_dic.keys()):
                    print("발견 ==> 바꿀문자", one)
                    one = change_word_dic[one]

            if self.check_ok_or_no(sql_4, one):
                print("발견 ==> (문자)   :  ", one)
                one = self.delete(sql_4, one)
                print("------------->", one)

            if len(one) <= 1:
                one = ""
            elif self.check_ok_or_no(sql_1, one):
                print("발견 ==> 숫자만", one)
                one = ""
            elif self.check_ok_or_no(sql_2, one):
                print("발견 ==> 숫자+1글자", one)
                one = ""

            if one != "":
                result.append(one)

            result_unique = list(set(result))
        return result_unique

    def data_special_char_set(self):
        """
        특수문자들을 돌려준다

        :return:
        """
        result = ".^$*+?{}[]\\|()"
        return result

    def search_in_result(self, result_list2d, ezre_sql):
        """
        # 결과값으로 넘어온 자료를 다시 검색하해서 결과를 알려주는 것

        :param result_list2d:
        :param ezre_sql: 정규표현식을 쉽게 만들도록 변경한 형태의 문장
        :return:
        """
        result = []
        for list_1d in result_list2d:
            start_no = list_1d[1]
            temp_2d = self.search_all_by_ezre_sql(ezre_sql, list_1d[0])
            if temp_2d:
                for list_1d in temp_2d:
                    list_1d[1] = list_1d[1] + start_no
                    list_1d[2] = list_1d[2] + start_no
                    result.append(list_1d)
        return result

    def change_html_tag_to_re_sql(self, one_tag, option_tag_show=False):
        """
        htm태그안의 값을 갖고오는 것

        :param one_tag:
        :param option_tag_show:
        :return:
        """
        new_tag = ""
        for one in one_tag:
            new_tag = new_tag + "[" + str(one).upper() + str(one).lower() + "]"
        if option_tag_show:
            change_sql = "<" + new_tag + ">.*<\\/" + new_tag + ">"
        else:
            change_sql = "(?<=<" + new_tag + ">).*(?= <\\/" + new_tag + ">)"
        result = change_sql
        return result

    def search_text(self, input_text, start_char, end_char):
        """

        :param input_text:
        :param start_char:
        :param end_char:
        :return:
        """
        start_found = 0
        end_found = 0
        temp = ""
        result = []
        ""
        temp_list = ["", 0]
        for index, one in enumerate(input_text):
            if one == start_char:
                start_found = 1
                temp_list[1] = index
            elif one == end_char:
                end_found = 1
            if start_found and not end_found:
                temp = temp + one
            elif start_found and end_found:
                temp_list[0] = temp + one
                result.append(temp_list)
                temp_list = ["", 0]
                temp = ""
                start_found = 0
                end_found = 0
        return result
