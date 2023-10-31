# -*- coding: utf-8 -*-
import sys #내장모듈
import datetime #내장모듈

import basic_data  # my 모듈
import mygrid_sample_data_01  # my 모듈

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import pyperclip
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, QRect, Qt
from PyQt5 import QtCore



# 코드 전체에서 사용할 변수를 설정한다
common_var = mygrid_sample_data_01.setup_data()

class make_table_datas():
	"""
	모든 자료를 먼저 만들고 싶은만큼 빈 2차원 빈 cell객체를 넣는다
	이후에 각 리스트안에 원하는 값들을 cell객체의 내용을 변경한다
	"""

	def __init__(self, parent=None):
		# 기본 설정한 가로세로에 맞는 2차원 리스트에 cell객체를 넣는다
		self.cell_sets = [[basic_data.basic_cell_class() for j in range(common_var["grid_y_len"])] for i in
						  range(common_var["grid_x_len"])]

	def get_cell_sets(self):
		"""
		2차원의 빈 cell객체에 값을 넣고 2차원의 객체를 돌려준다
		외부에서도 바꿔서 사용할수있도록하기위해 2개의 리스트형태로 만들었다
		"""
		# 이것처름 쓰면 본인이 만든것을 쉽게 넣을수도 있다
		my_values = mygrid_sample_data_01.write_data()

		# 모든 2차원 자료를 확인하면서 동일하게 만들것을 적용한다
		for one_value in my_values:
			x = one_value["x"]
			y = one_value["y"]
			self.cell_sets[x][y].values.update(one_value)
		return self.cell_sets

class TableModel(QAbstractTableModel):

    def __init__(self, table_data, parent=None):
        super().__init__(parent)
        self.table_data = table_data

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self.table_data.shape[0]

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self.table_data.shape[1]

    def data(self, index, role):
        print("Display Role")
        """
        각 셀별로 자료를 표현할 때마다 이것이 실행되는 것이다
        모든 것을 각 셀마다 다르게 설정할수가 있다
        화면을 움직이거나 하면 매번 다시 실행된다
        """
        # print("data-all")
        x = index.row()
        y = index.column()
        cell_obj = self.grid_cell_values[x][y]
        cell_values = cell_obj.values

        if role == Qt.DisplayRole:
            # 0 : 문자를 표현하는 방법 (QString)
            # print("data-display-role")

            if cell_values["kind_2"] == "date" and cell_values["kind_2"] == "=today()":
                return "2022-08-20"
            elif type(cell_values["text"]) == type(1):
                return "숫자 : " + str(cell_values["text"])

            elif cell_values["kind_2"] == "date" and isinstance(cell_values["value"], datetime):
                return cell_values["value"].strftime('%Y-%m-%d')
            else:
                return cell_values["text"]

        if role == Qt.DecorationRole:
            # 1   셀안에 값의 앞부분에 나타나는 아이콘같은 모양의 그림 (QColor, QIcon or QPixmap)

            if cell_values["kind_2"] == "date" and isinstance(cell_values["value"], datetime):
                return QIcon('calendar.png')
            elif cell_values["kind_2"] == "date" and cell_values["value"] == "=today()":
                return QIcon('calendar.png')
            elif str(cell_values["text"]) == "=":
                return QIcon('calendar.png')

        if role == Qt.EditRole:
            # 2   The data in a form suitable for editing in an editor. (QString)
            # 수정할때 나타나는 것
            return cell_values["text"]

        if role == Qt.ToolTipRole:
            # 3   각 셀마다 툴팁을 설정할수있는것. (QString)
            if cell_values["kind_1"] == "tool_tip":
                return cell_values["tool_tip"]
        if role == Qt.StatusTipRole:
            # 4   status bar에 나타나는것 (QString)
            pass

        if role == Qt.WhatsThisRole:
            # 5   The data displayed for the item in "What's This?" mode. (QString)
            pass

        if role == Qt.FontRole:
            # 6   The font used for items rendered with the default delegate. (QFont)
            font = QFont()
            font.setPixelSize(12)
            return Qt.QVariant(font)

        if role == Qt.TextAlignmentRole:
            # 7   The alignment of the text for items rendered with the default delegate. (Qt.AlignmentFlag)
            return Qt.QVariant(int(Qt.AlignLeft | Qt.AlignBottom))

        if role == Qt.BackgroundColorRole:
            # 8   The background brush used for items rendered with the default delegate. (QBrush)
            color = cell_values["background_color"]
            if color:
                return Qt.QVariant(QColor(color[0], color[1], color[2]))

        if role == Qt.ForegroundRole:
            # 9   The foreground brush (text color, typically) used for items rendered with the default delegate. (QBrush)
            font_color = cell_values["font_dic"]["color"]
            if font_color:
                return Qt.QVariant(QColor(font_color[0], font_color[1], font_color[2]))
            pass

        if role == Qt.CheckStateRole:
            # 10  This role is used to obtain the checked state of an item. (Qt.CheckState)
            pass
        #	if self.grid_cell_values[row][column].isChecked():
        #		return QVariant(Qt.Checked)
        #	else:
        #		return QVariant(Qt.Unchecked)

        if role == Qt.AccessibleTextRole:
            # 11  The text to be used by accessibility extensions and plugins, such as screen readers. (QString)
            pass

        if role == Qt.AccessibleDescriptionRole:
            # 12  A description of the item for accessibility purposes. (QString)
            pass

        if role == Qt.SizeHintRole:
            # 13  The size hint for the item that will be supplied to views. (QSize)
            pass

        if role == Qt.InitialSortOrderRole:
            # 14  This role is used to obtain the initial sort order of a header view section. (Qt.SortOrder). This role was introduced in Qt 4.8.
            pass

        if role == Qt.UserRole:
            # 32  The first role that can be used for application-specific purposes.
            pass

    def setData(self, index, value, role=Qt.EditRole):
        """
		셀에서 값을 바꾸면 실행되는 코드
		editor가 실행을 마치고 넘어오는 value값이 저장되는 것이다
		"""
        # print("data-setdata")
        x = index.row()
        y = index.column()
        cell_obj = self.grid_cell_values[x][y]
        cell_values = cell_obj.values

        if role == Qt.EditRole:
            try:
                text = int(cell_values["text"])
                text = "숫자 : " + str(text)
            except:
                pass

            self.grid_cell_values[x][y].values["text"] = text

            self.dataChanged.emit(index, index)
            return True

        if role == Qt.DecorationRole:
            # 1   셀안에 값의 앞부분에 나타나는 아이콘같은 모양의 그림 (QColor, QIcon or QPixmap)
            if isinstance(cell_values["text"], datetime):
                return QIcon('calendar.png')
            if cell_values["fun"]:
                if cell_values["fun"][0] == "date" and cell_values["fun"][2] == "=today()":
                    return QIcon('calendar.png')

        if role == Qt.CheckStateRole and y == 0:
            self.grid_cell_values[x][y] = QCheckBox('')
            if cell_values["text"] == Qt.Checked:
                self.grid_cell_values[x][y].setChecked(True)
            else:
                self.grid_cell_values[x][y].setChecked(False)
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return str(self.table_data.columns[section])

    def setColumn(self, col, array_items):
        """Set column data"""
        self.table_data[col] = array_items
        # Notify table, that data has been changed
        self.dataChanged.emit(QModelIndex(), QModelIndex())

    def getColumn(self, col):
        """Get column data"""
        return self.table_data[col]

class CreateTable(QTableWidget): # QTableWidget

    def __init__(self, row, col): # Index, ColumnHeaders
        super(CreateTable, self).__init__()

        self.cliptext = [] # undo가가능하도록 하는것
        self.history = []
        self.x = ""
        self.y = ""
        self.xy = ""
        self.xx= [0, 0]
        self.yy = [0, 0]
        self.xyxy = [0, 0, 0, 0]

        self.old_item = ""
        self.old_cell = ""
        self.old_text = ""

        self.selected_xyxy = ""
        self.usedrange = [0, 0]

        self.max_x = 1
        self.max_y = 1
        self.max_x_len = row
        self.max_y_len = col

        self.cell_drag_t = 10
        self.cell_drag_h = 20
        self.cell_drag_w = 20

        #기본적인 설정을 하는 곳
        self.var = {}
        self.var["odd_y_colored"] = True # 반복되는 행의 색깔을 지정하는 코드
        self.var["one_page_no"] = 25 # page up/down을 누르면 변하는 갯수들
        self.var["basic_cell_width"] = 85
        self.var["basic_cell_height"] = 10
        self.var["mouse_tracking"] = True

        self.var["line_select"] = False #1줄씩 선택하도록 하는 것
        self.var["cell_edit_no"] = False #모든셀의 수정을 못하게 하는것
        self.var["no_grid_line"] = False #그리드라인을 안보이게
        self.var["no_header_x"] = False # 열번호 안나오게 하는 코드
        self.var["no_header_y"] = False # 행번호 안나오게 하는 코드

        stylesheet_1 = "::section{Background-color:rgb(255,236,236)}"
        stylesheet_2 = "::section{Background-color:rgb(236,247,255)}"

        self.setMouseTracking(True)
        self.setRowCount(row)
        self.setColumnCount(col)
        self.horizontalHeader().setStyleSheet(stylesheet_1)
        self.verticalHeader().setStyleSheet(stylesheet_2)

        #header설정에 대한것
        #self.header().setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        #header에서 마우스오른쪽을 누르면 나타나는메뉴
        self.horizontalHeader().customContextMenuRequested.connect(self.menu_header_y)
        self.verticalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        #header에서 마우스오른쪽을 누르면 나타나는메뉴
        self.verticalHeader().customContextMenuRequested.connect(self.menu_header_x)

        self.set_basic_setting()
        #화면에 나오게 하기 위해 설정이 필요


        # 기본적인 event에 대한 설정하는 부분
        self.currentCellChanged.connect(self.action_current_cell_changed)
        self.currentItemChanged.connect(self.action_current_item_changed)
        self.cellChanged.connect(self.action_cell_changed)
        self.cellEntered.connect(self.action_cell_entered)
        self.cellActivated.connect(self.action_cell_activated)
        self.itemChanged.connect(self.action_item_changed)
        self.itemSelectionChanged.connect(self.action_item_selection_changed)
        self.itemClicked.connect(self.action_item_clicked)

    def action_cell_activated(self, now_x, now_y):
        #셀이 활성화되면 실행되는것
        print("action_cell_activated", now_x, now_y)

    def action_current_cell_changed(self, x, y, old_x, old_y):
        """
        이젠에 선택된 셀에서 다른 셀이 선택되었을때, 같은셀이 선택되면 실행되지 않는다
        Item이 있고 없고는 상관없음
        range를 선택하면, 마지막셀만 나타내고, old_x, old_y는 드래그하는동안의 주소가 넘어간다
        마우스클릭이 된것을 파악해서 정리해야 함
        """
        self.currunt_x = x
        self.currunt_y = y
        self.old_x = old_x
        self.old_y = old_y
        #print("현재위치 ==> ", x, y, "이전위치 ==> ", old_x, old_y)

    def action_current_item_changed(self, item):
        """
        item이 다른것으로 선택되었을때, 같은것을 다시한번 클릭하면 적용이 않된다
        self.select_item_changed = "yes"
        1개가 아닌 여러 영역을 선택하면 제일 마지막 셀만 위치만 가리키며
        1개의 셀 위치만 나타냄
        새로운 item이 넘어오는 것이다
        """
        if item:
            x = item.row()
            y = item.column()
            self.select_item_xy = [x, y]
            self.item = item
            print("action_current_item_changed", x, y)

    def action_cell_changed(self, x, y):
        """
        셀값이 변경되었을때,
        None셀이던 아니던 상관없음
        """
        try:
            self.value = self.item(x, y).text()
            print("action_cell_changed", x, y)

            # cells = self.read_attribute_in_range([x, y])
            # self.old_cell = {"type": "change", "range": [x, y], "cells": cells}
            # self.check_max_xy(x, y)
            #print("입력값이 변경되었네요", (x, y), input_text)
            #셀에 입력이 "="으로 입력되었을때 적용하는것
            #if input_text == "=1":
            #    self.add_combo_in_cell([2, 2], ["abc", "def", "xyz"])
            #elif input_text == "=2":
                #print("=2 를 입력했네요")
            #    self.add_combo_in_cell([3, 3], ["111abc", "222def", "333xyz"])
        except:
            pass

    def action_item_selection_changed(self ):
        """
        셀이 선택되면 실행
        어떤 형태의 셀이라도 좋음
        """
        selected_range = self.read_address_in_selection()[0]
        seleted_items = self.selectedItems()
        #print("action_item_selection_changed ==> ", selected_range)
        #print("selection_item ==> ", seleted_items)

        #self.setSelection()

    def action_item_clicked(self, item):
        """
        1. item이있는 셀을 클릭이나 더블클릭하면 실행되는것
        2. 빈셀에 입력을위해 더블클릭해서 들어가는 순간에 입력을 하던 아니던 item이 만들어 진것이고, 만약 다시 그곳을 클릭하면 실행됨
        여러영역이 선택되어질때는 실행되지 않는다
        """
        x = item.row()
        y = item.column()
        self.old_item = item
        print("item이 있는 셀을 클락했읍니다", [x,y])

    def action_item_changed(self, item):
        """
        마우스가 셀위를 움직일때, 선택한것은 아니며, item이있는 셀만 알려준다
        기본 item을 변경하는 것이 적용될때
        1. item의 선택이 바뀔때 (마우스로)
        2. item안의 값이 바뀔때 실행된다
        """
        self.item = item
        self.x = item.row()
        self.y = item.column()
        print("item이 변경됨")


            #print(input_text)
            #셀에 입력이 "="으로 입력되었을때 적용하는것
        #    if input_text[0:2] == "=1":
        #        self.add_combo_in_cell(2, 2, ["abc", "def", "xyz"])
        #    elif input_text[0:2] == "=2":
        #        self.add_combo_in_cell(3, 3, ["111abc", "222def", "333xyz"])
        #except:
        #    pass

    def action_cell_entered(self, now_x, now_y):
        """
        마우스가 셀에 접근하면 실행되는 코드를 만들수 있다
        너무 많이 실행되서 pass로 만든다
        """
        #print("마우스가 셀안으로 이동 ==> ",now_x+1, now_y+1)
        pass

    def add_checkbox_in_cell(self, xy, title = "입력값", checked = 0):
        """
        셀에 체크박스를 넣는 것이다
        """
        cbox = QCheckBox(str(title))
        cbox.setChecked(int(checked))
        if xy[0] < self.max_x_len - 1 and xy[1] < self.max_y_len - 1:
            self.setCellWidget(xy[0], xy[1], cbox)

    def add_combo_in_cell(self, xy, combo_list):
        """
        # tablewidget은 셀에 객체의 형식으로 넣어야 들어간다
        # 즉, 값, 색깔, 위치등을 지정해 주어야 들어가는 것이다
        #self.check_usedrange(xy)
        """
        combo_object = QComboBox()
        for one in combo_list:
            combo_object.addItem(str(one))
        if xy[0] < self.max_x_len - 1 and xy[1] < self.max_y_len - 1:
            self.setCellWidget(xy[0], xy[1], combo_object)

    def add_calendar_in_cell(self, xy):
        dateedit = QDateEdit(calendarPopup=True)
        #self.menuBar().setCornerWidget(self.dateedit, Qt.TopLeftCorner)
        dateedit.setDateTime(QDateTime.currentDateTime())
        if xy[0] < self.max_x_len - 1 and xy[1] < self.max_y_len - 1:
            self.setCellWidget(xy[0], xy[1], dateedit)

    def add_radiobutton_in_cell(self, xy, input_list=""):
        """
        # tablewidget은 셀에 객체의 형식으로 넣어야 들어간다
        # 즉, 값, 색깔, 위치등을 지정해 주어야 들어가는 것이다
        #self.check_usedrange(xy)
        """

        groupBox = QGroupBox("시간 단위", self)
        lay = QVBoxLayout()

        radio1 = QRadioButton("일봉", self)
        radio1.setChecked(True)
        #self.radio1.clicked.connect(self.radioButtonClicked)
        lay.addWidget(radio1)

        radio2 = QRadioButton("주봉", self)
        #self.radio2.clicked.connect(self.radioButtonClicked)
        lay.addWidget(radio2)

        radio3 = QRadioButton("월봉", self)
        #self.radio3.clicked.connect(self.radioButtonClicked)
        lay.addWidget(radio3)

        groupBox.setLayout(lay)
        groupBox.show()

        if xy[0] < self.max_x_len - 1 and xy[1] < self.max_y_len - 1:
            self.setCellWidget(xy[0], xy[1], groupBox)

    def add_progressbar_in_cell(self, xy, value=50):
        """
        프로그래스 바를 만드는 것이다
        """
        progress = QProgressBar()
        progress.setValue(int(value))
        if xy[0] < self.max_x_len - 1 and xy[1] < self.max_y_len - 1:
            self.setCellWidget(xy[0], xy[1], progress)

    def add_cols(self, xyxy):
        xyxy = self.read_select_address()[0]
        for x in (xyxy[0], xyxy[2]):
            self.InsertCols(x)
        self.add_history({"type": "add_cols", "range": [xyxy[0], 0, xyxy[2], 0], "cells": ""})

    def add_rows(self, xyxy):
        xyxy = self.read_select_address()[0]
        for y in range(xyxy[1], xyxy[3]):
            self.insertRow(y)
        self.add_history({"type": "add_rows", "range": [0, xyxy[1], 0, xyxy[3]], "cells": ""})

    def add_history(self, change):
        self.history.append(change)

    def contextMenuEvent(self, event):
        """
        마우스 오른쪽으로 누르면 나타나는 메뉴를 만드는 것
        """
        menu = QMenu(self)
        aaa = menu.addAction("test")
        copy_action = menu.addAction("복사하기")
        quit_action = menu.addAction("Quit")
        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == quit_action:
            qApp.quit()
        elif action == copy_action:
            print("copy...")
        elif action == aaa:
            print("test...")

    def check_usedrange(self, xyxy):
        if len(xyxy) == 2:
            self.usedrange[0] = max(xyxy[0], self.usedrange[0])
            self.usedrange[1] = max(xyxy[0], self.usedrange[1])
        else:
            self.usedrange[0] = max(xyxy[0], self.usedrange[0], self.usedrange[2])
            self.usedrange[1] = max(xyxy[0], self.usedrange[1], self.usedrange[3])

    def check_address(self, xyxy):
        """
        주소를 확인하는 코드
        입력값 : [x0, y0, x1, y1], [x0, y0]
        결과값 : [x0, y0, x1, y1]
        아무것도 없으면 [0, 0, 0, 0]이 나타난다
        """
        if len(xyxy) ==2:
            x0, y0, x1, y1 = [xyxy[0], xyxy[1], xyxy[0], xyxy[1]]
        elif len(xyxy) ==4:
            x0, y0, x1, y1 = [xyxy[0], xyxy[1], xyxy[2], xyxy[3]]
        elif xyxy == []:
            x0, y0, x1, y1 = [0, 0, 0, 0]

        #최소와 최대의 위치를 변경하는 것이다
        x0_checked = min(x0, x1)
        x1_checked = max(x0, x1)
        y0_checked = min(y0, y1)
        y1_checked = max(y0, y1)
        x0, y0, x1, y1 = x0_checked, x1_checked, y0_checked, y1_checked
        result = [x0, y0, x1, y1]

        return result

    def copy_item_object_in_xxline(self, xx):
        #선택한 영역의 1개의 item객체를 복사하는 것이다
        #복사를 하기위해서는 clone을 이용해야 한다

        result = []
        y_no = self.max_y_len
        #print("y_no",y_no)

        for x in range(xx[0], xx[1]+1):
            temp = []
            for y in range(0, y_no):
                self.old_item = self.item(x, y)
                one_item = self.old_item.clone()
                temp.append(one_item)
            result.append(temp)
        return result

    def copy_item_object_in_cell(self, xy):
        """
        선택한 영역의 1개의 item객체를 복사하는 것이다
        복사를 하기위해서는 clone을 이용해야 한다
        """
        self.old_item = self.item(xy[0], xy[1])
        result = self.old_item.clone()
        return result

    def check_data_limit(self, xyxy, input_data):
        """
        자료가 넘어온것이 범위를 넘어가지 않는지를 확인하는것
        """
        input_data_status = "good"
        input_xyxy_status = "good"

        #xyxy의 값을 확인한다
        x0, y0, x1, y1 = 0,0,0,0
        if len(xyxy) == 2 :
            x0, y0, x1, y1 = xyxy[0], xyxy[1], xyxy[0], xyxy[1]
        elif  len(xyxy) == 4 :
            x0, y0, x1, y1 = xyxy[0], xyxy[1], xyxy[2], xyxy[3]
        else:
            input_xyxy_status = "error"

        if input_xyxy_status == "good":
            x0_checked = min(x0, x1)
            x1_checked = max(x0, x1)
            y0_checked = min(y0, y1)
            y1_checked = max(y0, y1)
            x0, y0, x1, y1 = x0_checked, x1_checked, y0_checked, y1_checked

        #input_data의 갯수를 확인한다
        input_data_x_max = len(input_data)
        input_data_y_max = 1
        if type(input_data) == type("123") or type(input_data) == type(123):
            input_data_x_max = 1
            input_data_y_max = 1
        elif type(input_data) == type([123]) or type(input_data) == type((123)):
            input_data_x_max = len(input_data)
            for no in input_data:
                if type(input_data[no]) == type([123]) or type(input_data[no]) == type((123)):
                    input_data_y_max = max(input_data_y_max, len(input_data[no]))
                elif type(input_data) == type("123") or type(input_data) == type(123):
                    input_data_y_max = 1
                else:
                    input_data_status = "error"
        else:
            input_data_status = "error"


        x0_new = x0 + input_data_x_max
        x1_new = x1 + input_data_y_max
        y0_new = y0 + input_data_x_max
        y1_new = y1 + input_data_y_max


        if x0_new > self.max_x_len - 1:
            if x0 > self.max_x_len - 1:
                input_data_status = "error"
            else:
                input_xyxy_status = "good"
        elif int(x0) < self.max_x_len - 1 and int(x1) > self.max_x_len - 1:
            x1 = self.max_x_len - 1
            input_range_status = "error"
        elif int(x0) > self.max_x_len - 1 and int(x1) > self.max_x_len - 1:
            x1 = self.max_x_len - 1
            input_range_status = "error"
        elif int(x0) > self.max_x_len - 1 and int(x1) > self.max_x_len - 1:
            x1 = self.max_x_len
            input_range_status = "error"

        if int(y0) > self.max_x_len - 1: result = "error"
        if int(x0) < self.max_x_len - 1 and int(x1) > self.max_x_len - 1:
            x1 = self.max_x_len

        return result

    def check_max_xy(self, x, y):
        #usedrange를 확정하기위해 사용되는것
        if x !="":
            self.max_x = max(x, self.max_x)
        if y !="":
            self.max_y = max(y, self.max_y)

    def check_used_range(self, xyxy):
        if len(xyxy) == 2:
            self.usedrange[0] = max(xyxy[0], self.usedrange[0])
            self.usedrange[1] = max(xyxy[0], self.usedrange[1])
        else:
            self.usedrange[0] = max(xyxy[0], self.usedrange[0], self.usedrange[2])
            self.usedrange[1] = max(xyxy[0], self.usedrange[1], self.usedrange[3])

    def delete_range_select(self, many_range):
        # selected ranges
        #print("delete action")
        for xyxy in many_range:
            for x in range(xyxy[0], xyxy[2]+1):
                for y in range(xyxy[1], xyxy[3]+1):
                    self.setItem(x, y, QTableWidgetItem(""))

    def delete_cell_attribute(self, xy):
        # tablewidget은 셀에 객체의 형식으로 넣어야 들어간다
        # 즉, 값, 색깔, 위치등을 지정해 주어야 들어가는 것이다
        self.removeCellWidget(xy[0], xy[1])

    def delete_cols(self, xyxy):
        xyxy = self.read_select_address()[0]
        cells = self.read_attribute_in_xxline(xyxy)
        for y in range(xyxy[2], xyxy[0], -1):
            self.removeColumn(y)
        self.add_history({"type": "delete_cols", "range": [xyxy[0], 0, xyxy[2], 0], "cells": cells})

    def delete_rows(self, xyxy):
        xyxy = self.read_select_address()[0]
        cells = self.read_attribute_in_yyline(xyxy)
        for y in range(xyxy[3], xyxy[1], -1):
            self.removeRow(y)
        self.add_history({"type": "delete_rows", "range": [0, xyxy[1], 0, xyxy[3]], "cells": cells})

    def delete_yyline_in_range(self, yy=""):
        self.model = QStandardItemModel()
        """
        yy열을 삭제하는 것이다
        """
        #print("delete yy")
        if yy =="":
            aa = self.read_address_in_selection()[0]
            yy = [aa[1], aa[3]]
        #print("delete yy", aa)

        if len(yy) == 4:
            y0 = yy[1]
            y1 = yy[3]
        elif len(yy) == 2:
            y0 = yy[0]
            y1 = yy[1]

        y0_checked = min(y0, y1)
        y1_checked = max(y0, y1)
        #selected_rows = self.selectionModel().selectedColumns()

        #model = self.model
        #indices = self.tableView.selectionModel().selectedRows()
        #for index in sorted(indices):
        #    model.removeColumn(index.column(), Qt.QModelIndex())

        indexes = self.selectionModel().selectedColumns()
        for index in reversed(sorted(indexes)):
            #print('Column %d is selected' % index.column())
            self.removeColumn(3)


        #for each_row in reversed(sorted(selected_rows)):
        #    print(each_row.column())
        #    self.model.removeColumn(each_row.column())
            #self.removeColumn(each_row.column())

        #for y in range(y0_checked, y1_checked + 1):
                #if y < self.max_y_len - 1:
                #aa = self.setItem(0, y,"")

        #        print("삭제할 y열은 ==>", y)
                #item1 = self.itemFromIndex(y)
                # if y < self.max_y_len - 1:
                #self.insertColumn(item1.column())
                #self.clearSelection()
        #        self.removeColumn(item1.column())
            #self.add_history({"action": "delete_yyline_in_range", "range": [0, xyxy[1], 0, xyxy[3]], "cells": cells})

    def delete_value_in_range(self, input_2drange):
        """
        영역의 값만을 삭제하는 것이다
        2차원 영역이 입력되어야 한다
        입력값 : [[1,2,3,4], [5,6,7,8]]
        """
        #혹시 1차원의 리스트가 들어오면 2차원으로 만들어 주는 것이다
        if type(input_2drange[0]) !=type([]):
            input_2drange = [input_2drange]

        for xyxy in input_2drange:
            xyxy = self.check_address(xyxy)
            for x in range(xyxy[0], xyxy[2]+1):
                if x < self.max_x_len - 1:
                    for y in range(xyxy[1], xyxy[3]+1):
                        if y < self.max_y_len - 1:
                            self.delete_value_in_cell([x, y])

    def delete_value_in_cell(self, xy):
        # 선택된 셀의 item의 text를 ""으로 만드는 것이다
        # 다른 속성은 그대로 유지한다

        if xy[0] < self.max_x_len - 1 and xy[1] < self.max_y_len - 1:
            old_item = self.item(xy[0], xy[1])
            if old_item:
                pass
            else:
                old_item = self.item(xy[0], xy[1])
                old_item.text = ""
                self.setItem(xy[0], xy[1], old_item)

    def delete_widget_in_cell(self, xy):
        """
        tablewidget은 셀에 객체의 형식으로 넣어야 들어간다
        즉, 값, 색깔, 위치등을 지정해 주어야 들어가는 것이다
        """
        if xy[0] < self.max_x_len - 1 and xy[1] < self.max_y_len - 1:
            self.removeCellWidget(xy[0], xy[1])

    def delete_item_object_in_cell(self, xy):
        """
        tablewidget은 셀에 객체의 형식으로 넣어야 들어간다
        즉, 값, 색깔, 위치등을 지정해 주어야 들어가는 것이다
        """
        if xy[0] < self.max_x_len - 1 and xy[1] < self.max_y_len - 1:
            self.setItem(xy[0], xy[1], QTableWidgetItem())

    def delete_xxline_in_range(self, xx=""):
        """
        xx열을 삭제하는 것이다
        """

        #print("delete_xxline_in_range")
        if xx =="":
            aa = self.read_address_in_selection()[0]
            #print("선택영역은", aa)
            xx = [aa[0], aa[2]]
        if len(xx) ==4:
            x0 = xx[0]
            x1 = xx[2]
        elif len(xx) ==2:
            x0 = xx[0]
            x1 = xx[1]

        x0_checked = min(x0, x1)
        x1_checked = max(x0, x1)

        for x in range(x1_checked, x0_checked-1, -1):
            if x < self.max_x_len - 1:
                self.removeRow(x)
                #self.removeColumn(x)
            #self.add_history({"action": "delete_xxline_in_range", "range": [xyxy[0], 0, xyxy[2], 0], "cells": cells})

    def get_colordialog_color(self):
        """
        프로그래스 바를 만드는 것이다
        """
        result = QColorDialog.getColor()
        return result

    def get_all_attribute_in_item(self, item):
        """
        넘어온 item의 속성을 저장하는 것인데, 이것은 차후에 그냥 Item을 Clone해서 저장을 하여도 된다
        """
        item_dic = {"background" : item.background(), #배경색
                    "column": item.column(),  #y열
                    "flags": item.flags(),
                    "font": item.font(), #폰트
                    "icon": item.icon(),
                    "isselected": item.isSelected(), #선택되었을때
                    "row": item.row(), #x열
                    "text": item.text(), #텍스트값
                    "textalignment": item.textAlignment(), #텍스트 정렬
                    "textcolor": item.textColor(), #텍스트색
                    "tooltip": item.toolTip(),
                    "type": item.type(),
                    }
        return item_dic

    def isPrintable(key):
        printable = [
            Qt.Key_Space, Qt.Key_Exclam, Qt.Key_QuoteDbl, Qt.Key_NumberSign, Qt.Key_Dollar,
            Qt.Key_Percent, Qt.Key_Ampersand, Qt.Key_Apostrophe, Qt.Key_ParenLeft, Qt.Key_ParenRight,
            Qt.Key_Asterisk, Qt.Key_Plus, Qt.Key_Comma, Qt.Key_Minus, Qt.Key_Period, Qt.Key_Slash,
            Qt.Key_0, Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6, Qt.Key_7, Qt.Key_8, Qt.Key_9,
            Qt.Key_Colon, Qt.Key_Semicolon, Qt.Key_Less,
            Qt.Key_Equal, Qt.Key_Greater,
            Qt.Key_Question, Qt.Key_At,
            Qt.Key_A, Qt.Key_B, Qt.Key_C, Qt.Key_D, Qt.Key_E, Qt.Key_F, Qt.Key_G, Qt.Key_H, Qt.Key_I, Qt.Key_J,
            Qt.Key_K, Qt.Key_L, Qt.Key_M, Qt.Key_N, Qt.Key_O, Qt.Key_P, Qt.Key_Q, Qt.Key_R, Qt.Key_S, Qt.Key_T,
            Qt.Key_U, Qt.Key_V, Qt.Key_W, Qt.Key_X, Qt.Key_Y, Qt.Key_Z,
            Qt.Key_BracketLeft, Qt.Key_Backslash, Qt.Key_BracketRight, Qt.Key_AsciiCircum,
            Qt.Key_Underscore, Qt.Key_QuoteLeft, Qt.Key_BraceLeft, Qt.Key_Bar,
            Qt.Key_BraceRight, Qt.Key_AsciiTilde, Qt.Key_Insert, Qt.Key_PageUp,
            Qt.Key_PageDown, Qt.Key_End, Qt.Key_Home,
        ]
        if key in printable:
            return True
        else:
            return False

    def insert_xxline_in_range(self, xx=""):
        """
        xx열을 삽입하는 것이다
        """
        if xx =="":
            aa = self.read_address_in_selection()[0]
            xx = [aa[0], aa[2]]

        if len(xx) ==4:
            x0 = xx[0]
            x1 = xx[2]
        elif len(xx) ==2:
            x0 = xx[0]
            x1 = xx[1]

        x0_checked = min(x0, x1)
        x1_checked = max(x0, x1)


        for x in (x0_checked, x1_checked+1):
            if x < self.max_x_len - 1:
                self.insertRow(x)
            #self.add_history({"action": "insert_xxline_in_range", "range": xyxy})

    def insert_yyline_in_range(self, yy=""):
        """
        yy열을 삽입하는 것이다
        """
        if yy =="":
            aa = self.read_address_in_selection()[0]
            yy = [aa[1], aa[3]]

        if len(yy) ==4:
            y0 = yy[1]
            y1 = yy[3]
        elif len(yy) ==2:
            y0 = yy[0]
            y1 = yy[1]

        y0_checked = min(y0, y1)
        y1_checked = max(y0, y1)

        #item = self.itemAt(event.pos())
        #item_x = self.row(item)
        #item_y = self.column(item)


        #xyxy = self.read_address_in_selection()[0]
        #cells = self.read_attribute_in_yyline(xyxy)
        for y in range(y0_checked, y1_checked+1):
            if y < self.max_y_len - 1:
                self.insertColumn(y)
            #self.add_history({"action": "delete_yyline_in_range", "range": [0, xyxy[1], 0, xyxy[3]], "cells": cells})

    def paint_color_in_cell(self, xy, input_rgb=[123,123,123]):
        now_item = self.item(xy[0], xy[1])
        if now_item:
            pass
        else:
            now_item = QTableWidgetItem()
        now_item.setBackground(QColor(input_rgb[0], input_rgb[1], input_rgb[2]))
        self.setItem(xy[0], xy[1], now_item)

        #value = self.read_value_in_cell(xy)
        #aaa = self.setItem(xy[0], xy[1], QTableWidgetItem())
        #aaa.setBackground(input_color)
        #item1 = QTableWidgetItem(value)
        #item1.setBackground(QColor(input_color[0], input_color[1], input_color[2]))
        #self.setItem(xy[0], xy[1], item1)
        #self.setItem(xy[0], xy[1], QTableWidgetItem())
        #self.item(xy[0], xy[1]).setBackground(QColor(255, 128, 128))
        #self.setStyleSheet("QTableWidget::item::selected { background-color:#F9F6F5 ; color:black; border: 3px  solid black;}")

    def keyPressEvent(self, e):

        #x0, y0 = self.read_first_xy_in_selection()

        x0, y0 = self.x, self.y

        ctrl_key = ""
        shift_key = ""
        alt_key = ""

        if e.modifiers() & Qt.ControlModifier: ctrl_key = "on"
        if e.modifiers() & Qt.ShiftModifier: shift_key = "on"
        if e.modifiers() & Qt.AltModifier: alt_key = "on"

        if ctrl_key == "" and shift_key == "" and alt_key == "":
            if e.key() == Qt.Key_Delete:
                print('press key : Delete')
                # self.press_delete_key()
            elif e.key() == Qt.Key_Backspace:
                print('press key : Backspace')
            elif e.key() in [Qt.Key_Return, Qt.Key_Enter]:
                print('press key : Enter')
                # self.press_enter_key()
            elif e.key() == Qt.Key_Escape:
                print('press key : Escape')
                self.clearSelection()
            elif e.key() == Qt.Key_Right:
                print('press key : Right')
                if y0 + 1 > self.max_y_len - 1: y0 = y0 - 1
                self.setCurrentCell (x0, y0+1)
            elif e.key() == Qt.Key_Left:
                if y0 - 1 < 0: y0 = 1
                print('press key : Left')
                self.setCurrentCell (x0, y0-1)
            elif e.key() == Qt.Key_Up:
                print('press key : Up')
                if x0 - 1 < 0: x0 = 1
                self.setCurrentCell(x0 - 1, y0)
            elif e.key() == Qt.Key_Down:
                print('press key : Down')
                if x0 + 1 > self.max_x_len - 1: x0 = x0 - 1
                self.setCurrentCell(x0 + 1, y0)
            elif e.key() == Qt.Key_Insert:
                print('press key : Insert')
            elif e.key() == Qt.Key_PageUp:
                print('press key : PageUp')
                if x0 - self.var["one_page_no"] < 0 :
                    x0 = 0
                else:
                    x0 = x0 - 25
                self.setCurrentCell(x0, y0)
            elif e.key() == Qt.Key_PageDown:
                print('press key : PageDown')
                if x0 + self.var["one_page_no"] > self.max_x_len - 1:
                    x0 = self.max_x_len - 1
                else:
                    x0 = x0 + 25
                self.setCurrentCell(x0, y0)

            elif e.key() == Qt.Key_Home:
                print('press key : Home')
                self.clearSelection()
                self.setCurrentCell(x0, 0)
            elif e.key() == Qt.Key_End:
                print('press key : End')
            else:
                pass

        if ctrl_key == "" and shift_key == "on" and alt_key == "":
            print('press key : Shift')

        if ctrl_key == "" and shift_key == "" and alt_key == "on":
            print('press key : Alt')

        if ctrl_key == "on" and shift_key == "" and alt_key == "":
            if e.key() == Qt.Key_A:
                print("press key : Ctrl + A")
                self.selectAll()
            elif e.key() == Qt.Key_B:
                print("press key : Ctrl + B")
            elif e.key() == Qt.Key_C:
                print("press key : Ctrl + C")
                # self.press_copy_key()
            elif e.key() == Qt.Key_V:
                print("press key : Ctrl + V")
                # self.press_paste_key()
            elif e.key() == Qt.Key_X:
                print("press key : Ctrl + X")
                # self.paste_cut_key()
            elif e.key() == Qt.Key_Z:
                print("press key : Ctrl + Z")
                # self.undo()
            elif e.key() == Qt.Key_Right:
                self.clearSelection()
                print('press key : Ctrl + Right')
                self.setCurrentCell(x0, self.max_y_len - 1)
            elif e.key() == Qt.Key_Left:
                print('Ctrl + Left')
                self.clearSelection()
                self.setCurrentCell(x0, 0)
            elif e.key() == Qt.Key_Up:
                self.clearSelection()
                print('Ctrl + Up')
                self.setCurrentCell(0, y0)
            elif e.key() == Qt.Key_Down:
                self.clearSelection()
                print('Ctrl + Down')
                self.setCurrentCell(self.max_x_len - 1, y0)
            else:
                pass

    def mouseMoveEvent(self, event):
        """
        마우스가 움직이면 자동으로 실행되는 기본 이벤트
        """
        super(CreateTable, self).mouseMoveEvent(event)

        mouse_xpx = event.x()
        mouse_ypx = event.y()

        #item = self.itemAt(event.pos())
        #item_x = self.row(item)
        #item_y = self.column(item)

        cell = self.indexAt(event.pos())
        cell_rect = self.visualRect(cell)

        #x : computer x,  컴퓨터에서사용하는 x로 0부터시작하는것, px : person x (사람을 위한것만 px로 사용하자)
        #cell_x = cell.row()
        #cell_y = cell.column()

        #cell_x_width = cell_rect.width()
        #cell_y_height = cell_rect.height()

        cell_x0px = cell_rect.x()
        cell_y0px = cell_rect.y()

        cell_x1px = cell_x0px + cell_rect.width()
        cell_y1px = cell_y0px + cell_rect.height()

        cell_x2px = cell_x1px - self.cell_drag_w
        cell_y2px = cell_y1px - self.cell_drag_t

        cell_x3px = cell_x1px - self.cell_drag_t
        cell_y3px = cell_y1px - self.cell_drag_h

        #오른쪽 하단에 마우스가 오면 십자모양으로 커서가 변경되게 하였다
        if (cell_x2px < mouse_xpx and cell_x1px > mouse_xpx and cell_y2px < mouse_ypx and cell_y1px > mouse_ypx) \
            or (cell_x3px < mouse_xpx and cell_x1px > mouse_xpx and cell_y3px < mouse_ypx and cell_y1px > mouse_ypx):
            self.setCursor(Qt.CursorShape.CrossCursor)
        else:
            self.setCursor(Qt.CursorShape.PointingHandCursor)

    def menu_header_x(self, pos):
        """
        Header에서 마우스 오른쪽으로 누르면 나타나는 메뉴를 만드는 것
        """
        global_pos = self.mapToGlobal(pos)
        menu = QMenu()
        ddd = menu.addAction("x해드의 1번을 누르세요")
        delete_xx_action = menu.addAction("xx삭제하기")
        quit_action = menu.addAction("Quit")

        selected_menu = menu.exec_(global_pos)
        if selected_menu == quit_action:
            print("Quit을 눌렀네요")
        elif selected_menu == delete_xx_action:
            self.delete_xxline_in_range()
        elif selected_menu == ddd:
            print("1번을 눌렀네요")

    def menu_header_y(self, pos):
        """
        Header에서 마우스 오른쪽으로 누르면 나타나는 메뉴를 만드는 것
        """
        global_pos = self.mapToGlobal(pos)
        menu = QMenu()
        ddd = menu.addAction("y해드의 1번을 누르세요")
        del_yy_action = menu.addAction("yy삭제하기")
        quit_action = menu.addAction("Quit")

        selected_menu = menu.exec_(self.viewport().mapToGlobal(pos))
        if selected_menu == quit_action:
            print("Quit을 눌렀네요")
        elif selected_menu == del_yy_action:
            self.delete_yyline_in_range()
        elif selected_menu == ddd:
            print("1번을 눌렀네요")

    def paste_item_object_in_xxline(self, xx, input_2ditem):
        #선택한 영역의 1개의 item객체를 복사하는 것이다
        #복사를 하기위해서는 clone을 이용해야 한다

        for x in range(xx[0], xx[1]+1):
            y_no = len(input_2ditem[x-xx[0]])
            for y in range(0, y_no):
                self.setItem(x, y, input_2ditem[x-xx[0]][y])

    def paste_item_object_in_cell(self, xy, old_item):
        """
        복사한것을 붙여넣기 하는 것이다
        """
        if xy[0] < self.max_x_len - 1 and xy[1] < self.max_y_len - 1:
            self.setItem(xy[0], xy[1], old_item)

    def press_cut_key(self):
        self.press_copy_key()
        self.press_delete_key()

    def press_paste_key(self):
        input_text = pyperclip.paste()
        result = []
        semi_list = input_text.split("\n")
        for one_text in semi_list:
            temp = one_text.split("\t")
            result.append(temp)

        xyxy = self.read_address_in_selection()[0]
        self.write_value_in_range(result, [xyxy[0][0], xyxy[0][1]])

    def press_copy_key(self):
        self.cliptext = []
        xyxy = self.read_address_in_selection()[0]
        #print("press_copy_key ==>", xyxy)
        result = ""
        if len(xyxy)==2:
            xyxy = [xyxy[0], xyxy[1], xyxy[0], xyxy[1]]

        for x in range(xyxy[0], xyxy[2]+1):
            temp = []
            for y in range(xyxy[1], xyxy[3]+1):
                item_temp = self.item(x, y)
                if item_temp is not None:
                    value = item_temp.text()
                else:
                    value = ""
                temp.append(value)
                result = result+value +"\t"
            result = result[:-2]+"\n"
            self.cliptext.append(temp)
        #print("press_copy_key, cliptext ==>", self.cliptext)
        pyperclip.copy(result[:-2])
        return result

    def merge_range(self, xy, x_count, y_count):
        """
        1차원자료를 입력하면 셀에 입력하는것
        처음시작할 위치를 알아낸다
        xy는 시작위치
        x_count : 아래쪽으로 몇개까지 병합될지
        y_count : 오른쪽으로 몇개까지 병합될지

        x나 y가 0이면 header를 뜻한다
        """
        if xy[0]+x_count < self.max_x_len - 1 and xy[1]+y_count < self.max_y_len - 1:
            self.setSpan(xy[0], xy[1], x_count, y_count)


    def press_delete_key(self):
        #print("delete")
        xyxy_s = self.read_address_in_selection()[0]
        cells = []
        for xyxy in xyxy_s:
            cell = self.read_attribute_in_range(xyxy)
            cells.append(cell)
        self.delete_value_in_range(xyxy_s)
        self.add_history({"action": "delete", "range": xyxy_s, "cells": cells})

    def press_enter_key(self):
        current = self.currentIndex()
        nextIndex = current.sibling(current.row() + 1, current.column())
        self.setItem(current.row() + 1, current.column(), QTableWidgetItem(str("")))
        if nextIndex.isValid():
            self.setCurrentCell(current.row() + 1, current.column())
            self.edit(nextIndex)

    def read_attribute_in_range(self, xyxy):
        """
        선택한영역의 주소와 속성을 하나씩 저장하는 것이다
        결과물 = [[x,y,값]....]
        """
        result = []
        if len(xyxy) == 2:
            xyxy = [xyxy[0], xyxy[1], xyxy[0], xyxy[1]]

        for x in range(xyxy[0], xyxy[2]):
            for y in range(xyxy[1], xyxy[3]):
                result.append([x, y, self.item(x, y).text()])
        return result

    def read_attribute_in_yyline(self, xyxy):
        """
        세로를 삭제하였을때 값과 속성을 하나씩 저장하는 것이다
        """
        old_xyxy = self.read_address_in_selection()[0]
        end_xy = self.usedrange
        xyxy = [0, old_xyxy[1], end_xy[0], old_xyxy[3]]
        result = []
        for x in range(xyxy[0], xyxy[2]):
            temp = {}
            for y in range(xyxy[1], xyxy[3]):
                # 추가로 속성을 넣을수있도록 만든것이다
                temp["x"] = x
                temp["y"] = y
                temp["value"] = self.item(x, y).text()
            result.append(temp)
        return result

    def read_attribute_in_xxline(self, xyxy):
        # 가로를 삭제하였을때 값과 속성을 하나씩 저장하는 것이다
        old_xyxy = self.read_address_in_selection()[0]
        end_xy = self.usedrange
        xyxy = [old_xyxy[0], 0, old_xyxy[2], end_xy[1]]
        result = []
        for x in range(xyxy[0], xyxy[2]):
            temp = {}
            for y in range(xyxy[1], xyxy[3]):
                # 추가로 속성을 넣을수있도록 만든것이다
                temp["x"] = x
                temp["y"] = y
                temp["value"] = self.item(x, y).text()
            result.append(temp)
        return result

    def read_value_in_cell(self, xy):
        """
        cell의 값을 읽어오는것
        만약 Item이 없으면
        """
        xy = self.check_address(xy)
        try:
            result = self.item(xy[0], xy[1]).text()
        except:
            result = ""
        return result

    def read_value_in_range(self, xyxy):
        """
        영역안의 값을 읽어오는것
        item이 아닌것만 갖고오는 것이다
        """
        result = []
        for x in range(xyxy[0], xyxy[2]):
            temp = []
            for y in range(xyxy[1], xyxy[3]):
                try:
                    value = self.item(x, y).text()
                except:
                    value = ""
                temp.append(value)
            result.append(temp)
        self.max_x = max(xyxy[2], self.max_x)
        self.max_y = max(xyxy[3], self.max_y)
        return result

    def read_address_in_all_selection(self):
        """
        현재 선택된것이 아니고 전에 선택되어졌던 영역을 돌려준다
        선택한 여러영역의 좌표를 돌려준다 ===> [[1,2,7,4],[5,6,7,8],[9,10,11,12]]
        만약 영역이 선택되어있지 않으면 [[]]를 돌려준다
        """
        selected_range = self.selectedRanges()
        result = []
        if selected_range:
            for idx, sel in enumerate(selected_range):
                [x0, y0, x1, y1] = [sel.topRow(), sel.leftColumn(), sel.bottomRow(), sel.rightColumn()]
                if self.max_x_len == x1 + 1: x1 = 0
                if self.max_y_len == y1 + 1: y1 = 0
                result.append([x0, y0, x1, y1])
        else:
            result = [[]]
        return result

    def read_address_in_selection(self):
        """
        현재 선택된 영역을 돌려 준다
        """
        result = []
        range_s = self.selectedRanges()
        for range in range_s:
            result.append([range.topRow(), range.leftColumn(), range.bottomRow(), range.rightColumn()])
        return result

    def read_items_in_range(self, xyxy_list):
        """
        선택된 영역의 item을 돌려준다
        여러곳을 선택할수가 있어서
        final_result = [[2ditem_자료들, xyxy], [2ditem_자료들, xyxy], ]
        """

        final_result = []
        result = []

        for xyxy_one in xyxy_list:
            x0, y0, x1, y1 = self.check_address(xyxy_one)
            for x in range(x0, x1+1):
                temp = []
                for y in range(y0, y1+1):
                    self.old_item = self.item(x, y)
                    one_item = self.old_item.clone()
                    temp.append(one_item)
                result.append(temp)
            final_result.append([result, xyxy_one])
        self.old_item = final_result
        return result

    def read_first_xy_in_selection(self):
        """
        선택한 영역의 제일 처음 좌표를 알려주는 것이다
        아무런 영역도 지정을하지 않았다면 [0, 0]을 돌려준다
        """
        range_list = self.read_address_in_selection()[0]
        if range_list:
            result = [range_list[0][0], range_list[0][1]]
        else:
            result = [0,0]
        return result

    def sort_by_no(self, x):
        """
        """
        # x 번재 자리에 column 삽입
        self.sortItems(x, Qt.DescendingOrder)

    def set_basic_setting(self):
        """
        """
        #처음의 시작시의 설정을 하도록 한다
        if self.var["line_select"] : self.setSelectionBehavior(QAbstractItemView.SelectRows)
        if self.var["cell_edit_no"] : self.setEditTriggers(QAbstractItemView.NoEditTriggers) # 셀 edit 금지
        if self.var["no_grid_line"]: self.setShowGrid(False)
        if self.var["no_header_x"]: self.verticalHeader().setVisible(False) # 행번호 안나오게 하는 코드
        if self.var["no_header_y"]: self.horizontalHeader().setVisible(False) # 열번호 안나오게 하는 코드
        if self.var["basic_cell_width"]: self.horizontalHeader().setDefaultSectionSize(self.var["basic_cell_width"]) # 열번호 안나오게 하는 코드
        if self.var["basic_cell_height"]: self.verticalHeader().setDefaultSectionSize(self.var["basic_cell_height"]) # 열번호 안나오게 하는 코드
        if self.var["odd_y_colored"]:
            self.setAlternatingRowColors(True)  # 행마다 색깔을 변경 하는 코드
            self.gui_palette = QPalette()  # 반복되는 행의 색깔을 지정하는 코드
            self.gui_palette.setColor(QPalette.AlternateBase, QColor(0, 0, 0, 0))  # 반복되는 행의 색깔을 지정하는 코드
        if self.var["mouse_tracking"]:
            self.setMouseTracking(True)
        else:
            self.setMouseTracking(False)

    def sort_range_byno(self, x):
        """
        x 번재 자리에 column 삽입
        """
        self.sortItems(x, Qt.DescendingOrder)

    def undo(self):
        """
        실행 취소를 누르면 취소되는 기능
        """
        if len(self.history):
            action = self.history.pop()
            xyxy = action["range"]
            value_s = action["cells"]
            #print("undo 실행", action["action"], xyxy, value_s)

            if action["action"] == "change" or action["action"] == "delete":
               self.write_range_attribute(action)

            elif action["action"] == "delete_yyline_in_range":
                self.insert_yyline_in_range(xyxy)
                for row, col, attribute in value_s:
                    self.write_value_in_cell([row, col], attribute["value"])

            elif action["action"] == "delete_xxline_in_range":
                self.insert_xxline_in_range(xyxy)
                for row, col, attribute in value_s:
                    self.write_value_in_cell([row, col], attribute["value"])

            elif action["action"] == "insert_yyline_in_range":
                self.del_rows(xyxy)

            elif action["action"] == "insert_xxline_in_range":
                self.del_cols(xyxy)
            else:
                return

    def update_usedrange(self, x, y):
        """
        usedrange를 확정하기위해 사용되는것
        이것은 usedrange가 없으므로 이것을 만드는 것이다
        """
        if x < self.max_x_len:
            self.usedrange[0] = max(x, self.usedrange[0])
        if y < self.max_y_len:
            self.usedrange[1] = max(y, self.usedrange[1])

    def write_calendar_in_cell(self, xy):
        """
        calendar객체를 넣는것
        """
        dateedit = QDateEdit(calendarPopup=True)
        dateedit.setDateTime(QDateTime.currentDateTime())
        if xy[0] < self.max_x_len - 1 and xy[1] < self.max_y_len - 1:
            self.setCellWidget(xy[0], xy[1], dateedit)


    def write_radio_button_in_cell(self, xy, title="group box", group_list="", output_xy=[2,3]):
        """
        """
        self.groupbox_output_xy = output_xy

        self.groupbox = QGroupBox(title)
        self.group_obj = []

        for index, name in enumerate(group_list):
            exec(f"self.radio{index} = QRadioButton('{name}')")
            exec(f"self.group_obj.append(self.radio{index})")
            exec(f"self.radio{index}.clicked.connect(self.action_radio_button)")
        self.group_obj[0].setChecked(True)

        vbox = QVBoxLayout()
        for one_obj in self.group_obj:
            vbox.addWidget(one_obj)
        self.groupbox.setLayout(vbox)
        self.setCellWidget(xy[0], xy[1], self.groupbox)

    def action_radio_button(self):
        """
        radio_button 객체가 click가 되었을때 실행되는것
        """
        for one_obj in self.group_obj:
            if one_obj.isChecked():
                self.groupbox_output = one_obj.text()
        self.write_value_in_cell(self.groupbox_output_xy, self.groupbox_output)

    def write_checkbox_in_cell(self, xy, value = 1):
        """
        checkbox객체를 넣는것
        """
        cbox = QCheckBox("I have a Cat")
        cbox.setChecked(int(value))
        self.setCellWidget(xy[0], xy[1], cbox)

    def write_cell_button(self, xy, action, caption):
        """
        셀에 버튼을 만들어서 넣는 것이다
        """
        self.write_button_in_cell(xy, action, caption)

    def write_button_in_cell(self, xy, action, caption = "abc"):
        """
        button객체를 넣는것
        """
        # tablewidget은 셀에 객체의 형식으로 넣어야 들어간다
        # 즉, 값, 색깔, 위치등을 지정해 주어야 들어가는 것이다
        btnRun = QPushButton(caption, self)  # 버튼 텍스트
        btnRun.clicked.connect(action)
        btnRun.setFont(QFont('Malgun Gothic', 10))
        btnRun.setStyleSheet("QPushButton { text-align: left;font-color:black}")
        self.setCellWidget(xy[0], xy[1], btnRun)

    def write_combo_in_cell(self, xy, combo_list, output_xy=[2,3]):
        """
        combo객체를 넣는것
        """
        self.combo = QComboBox()
        for one in combo_list:
            self.combo.addItem(str(one))

        self.combo.currentTextChanged.connect(self.action_combo)

        self.setCellWidget(xy[0], xy[1], self.combo)

    def action_combo(self, text):
        """
        dial 객체가 click가 되었을때 실행되는것
        """
        self.write_value_in_cell(self.groupbox_output_xy, text)

    def write_groupbox_in_cell(self, xy, title="group box", group_list="", output_xy=[2,3]):
        """
        groupbox객체를 넣는것
        """
        self.groupbox_output_xy = output_xy

        self.groupbox = QGroupBox(title)
        self.group_obj = []

        for index, name in enumerate(group_list):
            exec(f"self.radio{index} = QRadioButton('{name}')")
            exec(f"self.group_obj.append(self.radio{index})")
            exec(f"self.radio{index}.clicked.connect(self.action_groupbox)")
        self.group_obj[0].setChecked(True)

        vbox = QVBoxLayout()
        for one_obj in self.group_obj:
            vbox.addWidget(one_obj)
        self.groupbox.setLayout(vbox)
        self.setCellWidget(xy[0], xy[1], self.groupbox)

    def action_groupbox(self):
        """
        groupbox 객체가 click가 되었을때 실행되는것
        """
        for one_obj in self.group_obj:
            if one_obj.isChecked():
                self.groupbox_output = one_obj.text()
        self.write_value_in_cell(self.groupbox_output_xy, self.groupbox_output)

    def write_file_dialog_in_cell(self, xy, caption="file dialog", output_xy=[2,3]):
        """
        file_dialog객체를 넣는것
        """
        btnRun = QPushButton(caption, self)  # 버튼 텍스트
        self.output_xy = output_xy
        btnRun.clicked.connect(self.action_file_dialog)
        btnRun.setFont(QFont('Malgun Gothic', 10))
        btnRun.setStyleSheet("QPushButton { text-align: left;font-color:black}")
        self.setCellWidget(xy[0], xy[1], btnRun)

    def action_file_dialog(self):
        """
        dial 객체가 click가 되었을때 실행되는것
        """
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        self.write_value_in_cell(self.output_xy, fname[0])

    def write_color_dialog_in_cell(self, xy, caption="color dialog", output_xy=[4,3]):
        """
        color_dialog객체를 넣는것
        """
        self.output_xy = output_xy
        btnRun = QPushButton(caption, self)  # 버튼 텍스트
        btnRun.clicked.connect(self.action_color_dialog)
        btnRun.setFont(QFont('Malgun Gothic', 10))
        btnRun.setStyleSheet("QPushButton { text-align: left;font-color:black}")
        self.setCellWidget(xy[0], xy[1], btnRun)


    def action_color_dialog(self):
        """
        dial 객체가 click가 되었을때 실행되는것
        """
        col = QColorDialog.getColor()
        self.write_value_in_cell(self.output_xy, col.rgb())

    def write_slider_in_cell(self, xy, output_xy=None):
        """
        slider객체를 넣는것
        """
        if output_xy == "":
            self.slider_output_xy = [xy[0], xy[1]+1]
        elif output_xy == None:
            self.slider_output_xy = None
        else:
            self.slider_output_xy = output_xy
        self.check_used_range(xy)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.move(30, 30)
        self.slider.setRange(0, 50)
        self.slider.setSingleStep(2)

        self.slider.setPageStep(10)
        self.slider.setTickPosition(QSlider.TickPosition.TicksAbove)

        self.slider.valueChanged.connect(self.action_slider)
        self.setCellWidget(xy[0], xy[1], self.slider)

    def action_slider(self):
        """
        dial 객체가 click가 되었을때 실행되는것
        """
        if self.slider_output_xy == None:
            pass
        else:
            self.slider_output = self.dial.value()
        self.write_value_in_cell(self.slider_output_xy, self.slider_output)

    def write_dial_in_cell(self, xy, output_xy=None):
        """
        dial객체를 넣는것
        """
        if output_xy == "":
            self.dial_output_xy = [xy[0], xy[1]+1]
        elif output_xy == None:
            self.dial_output_xy = None
        else:
            self.dial_output_xy = output_xy

        self.check_used_range(xy)
        self.dial = QDial()
        self.dial.move(20, 80)
        self.dial.setRange(0, 100)
        self.dial.setNotchesVisible(True)
        self.dial.valueChanged.connect(self.action_dial)
        self.setCellWidget(xy[0], xy[1], self.dial)

    def action_dial(self):
        """
        dial 객체가 click가 되었을때 실행되는것
        """
        if self.dial_output_xy == None:
            pass
        else:
            self.dial_output = self.dial.value()
        self.write_value_in_cell(self.dial_output_xy, self.dial_output)

    def write_progressbar_in_cell(self, xy, value=50):
        """
        tablewidget은 셀에 객체의 형식으로 넣어야 들어간다
        즉, 값, 색깔, 위치등을 지정해 주어야 들어가는 것이다
        """
        self.check_used_range(xy)

        combo = QProgressBar()
        combo.setValue(int(value))
        self.setCellWidget(xy[0], xy[1], combo)

    def write_value_in_cell(self, xy, input_text):
        """
        셀하나에 값을 넣는것이다
        """
        if xy[0] < self.max_x_len - 1 and xy[1] < self.max_y_len - 1:
            self.setItem(xy[0], xy[1], QTableWidgetItem(str(input_text)))
            self.check_max_xy(xy[0], xy[1])

    def write_attribute(self, action):
        """
        """
        action_type = action["type"]
        xyxy = action["range"]
        value_s = action["cells"]
        for one_list in value_s:
            for x, y, value in one_list:
                self.setItem(x, y, QTableWidgetItem(str(value)))

    def write_value(self, xy, input_list):
        """
        값을 쓰는것
        """
        self.check_used_range(xy)
        if type([]) != type(input_list[0]):
            input_list = [input_list]

        for x in range(len(input_list)):
            for y in range(len(input_list[0])):
                self.setItem(xy[0]+x, xy[1]+y, QTableWidgetItem(str(input_list[x][y])))
        self.check_max_xy(xy[0]+len(input_list), xy[1]+len(input_list[0]))

    def write_value_for_list1d(self, input_list):
        """
        1차원리스트의 값을 넣는것
        """
        for y in range(len(input_list)):
                self.setItem(1, y, QTableWidgetItem(str(input_list[y])))

    def write_value_in_range(self, xy, input_2dlist):
        """
        2차원자료 형태의 것을 입력하는 것이다
        """
        if type([]) != type(input_2dlist[0]):
            input_2dlist = [input_2dlist]

        for x in range(len(input_2dlist)):
            if xy[0] + x < self.max_x_len - 1:
                for y in range(len(input_2dlist[0])):
                    if xy[1] + y < self.max_y_len - 1:
                        self.setItem(xy[0]+x, xy[1]+y, QTableWidgetItem(str(input_2dlist[x][y])))

    def write_range_1dvalue(self, xy, input_list):
        """
        1차원자료를 입력하면 셀에 입력하는것
        처음시작할 위치를 알아낸다
        """
        if xy[0] < self.max_x_len - 1 and xy[1] < self.max_y_len - 1:
            for y in range(len(input_list)):
                if xy[1]+y < self.max_y_len - 1:
                    self.setItem(xy[0], xy[1]+y, QTableWidgetItem(str(input_list[y])))

    def write_merge_in_range(self, xy, x_count, y_count):
        """
        1차원자료를 입력하면 셀에 입력하는것
        처음시작할 위치를 알아낸다
        xy는 시작위치
        x_count : 아래쪽으로 몇개까지 병합될지
        y_count : 오른쪽으로 몇개까지 병합될지
        """
        if xy[0]+x_count < self.max_x_len - 1 and xy[1]+y_count < self.max_y_len - 1:
            self.setSpan(xy[0], xy[1], x_count, y_count)

class mygrid_main(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        grid = CreateTable(30,30)
        self.create_menubar()

        self.resize(500,500)

        grid.write_slider_in_cell([1,1])

        grid.write_dial_in_cell([2,1])

        grid.write_color_dialog_in_cell([3,1])

        grid.write_file_dialog_in_cell([4,1])

        grid.write_groupbox_in_cell([6,1],"그룹 박스",  ["a", "b", "c", "d"], [6,4])

        grid.write_combo_in_cell([7,1], ["a", "b", "c", "d"], [7,4])

        self.setCentralWidget(grid)

        self.show()

    def create_menubar(self):
        # 메뉴바를 만드는 것
        menubar = self.menuBar()
        menu_1 = menubar.addMenu("사용법")

        menu_1_1 = QAction('내부실행용', self)
        menu_1_1.triggered.connect(self.text_manual)
        menu_1.addAction(menu_1_1)

        menu_1_2 = QAction('외부화일 실행용', self)
        menu_1_2.triggered.connect(self.text_manual)
        menu_1.addAction(menu_1_2)

        menu_1_3 = QAction(QIcon("save.png"), '참고사이트', self)
        menu_1_3.triggered.connect(self.text_manual)
        menu_1.addAction(menu_1_3)

        menu_2 = menubar.addMenu("Made by")

        menu_2_1 = QAction('누가 만들었나요 ?', self)
        menu_2_1.triggered.connect(self.text_manual)
        menu_2.addAction(menu_2_1)

        menu_2_2 = QAction('Logo의 의미', self)
        menu_2_2.triggered.connect(self.text_manual)
        menu_2.addAction(menu_2_2)

        menu_3 = menubar.addMenu("끝내기")

        menu_3_1 = QAction(QIcon('exit.png'), 'Exit', self)
        menu_3_1.triggered.connect(qApp.quit)
        menu_3.addAction(menu_3_1)

    def text_manual(self):
        print("메뉴의 테스트")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mygrid_main = mygrid_main()
    sys.exit(app.exec_())