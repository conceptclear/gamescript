import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.Qt import QThread, QMutex
from PyQt5.QtGui import QIntValidator
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QHeaderView, QAbstractItemView
import qt_fgo_main
import qt_fgo_settings
import qt_fgo_about
import qt_fgo_fight
import fgo
import json

qmut_1 = QMutex()


class Thread_1(QThread):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def run(self):
        qmut_1.lock()
        this_fgo_fight = fgo.Fgo(self.filename)
        this_fgo_fight.repeat_fight()
        qmut_1.unlock()


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))


class WindowFgoMain(QtWidgets.QWidget, qt_fgo_main.Ui_MainWidget):
    def __init__(self):
        super(WindowFgoMain, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('source/favicon.ico'))
        self.dialog_fgo_settings = WindowFgoSettings()
        self.dialog_fgo_about = WindowFgoAbout()
        self.dialog_fgo_fight = WindowFgoFight()
        self.filename = None
        """
        self.setcomboBox()
        with open('settings/fgosettings1.json', 'r') as f_read:
            self.fgo_settings = json.load(f_read)
        fight_text = codecs.open('settings/fight1.json', 'r', encoding='utf-8').read()
        self.fight_list = np.array(json.loads(fight_text))
        """
        # 下面将输出重定向到textEdit中
        sys.stdout = EmittingStream(textWritten=self.outputWritten)
        sys.stderr = EmittingStream(textWritten=self.outputWritten)

    # 接收信号str的信号槽
    def outputWritten(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def file_open(self):
        filename, filetype = QFileDialog.getOpenFileName(
            self, "选择文件", "settings/", "Json Files (*.json)")
        if len(filename) == 0:
            return
        self.label_2.setText(filename)
        self.filename = filename

    def change_fgo_settings_click(self):
        if self.filename is None:
            return
        self.dialog_fgo_settings.set_settings(self.filename)
        self.dialog_fgo_settings.show()

    def change_fgo_fight(self):
        if self.filename is None:
            return
        self.dialog_fgo_fight.set_fight_list(self.filename)
        self.dialog_fgo_fight.show()

    def open_about(self):
        self.dialog_fgo_about.show()

    def start_script(self):
        if self.filename is not None:
            self.thread = Thread_1(self.filename)
            self.thread.start()

    def end_script(self):
        sys.exit()


class WindowFgoSettings(QtWidgets.QWidget, qt_fgo_settings.Ui_Dialog):
    def __init__(self):
        super(WindowFgoSettings, self).__init__()
        self.setupUi(self)
        self.filename = None
        self.fgo_settings = None
        self.buttonGroup1 = QtWidgets.QButtonGroup()
        self.buttonGroup1.addButton(self.radioButton)
        self.buttonGroup1.addButton(self.radioButton_2)
        self.buttonGroup2 = QtWidgets.QButtonGroup()
        self.buttonGroup2.addButton(self.radioButton_3)
        self.buttonGroup2.addButton(self.radioButton_4)
        self.comboBox.addItem("不吃苹果")
        self.comboBox.addItem("吃金苹果")
        self.comboBox.addItem("吃银苹果")
        self.comboBox.addItem("吃铜苹果")
        self.comboBox.addItem("吃彩苹果")
        self.comboBox_2.addItem('1')
        self.comboBox_2.addItem('2')
        self.comboBox_2.addItem('3')
        self.comboBox_3.addItem('孔明')
        self.comboBox_3.addItem('斯卡哈·斯卡蒂')
        self.comboBox_3.addItem('梅林')
        self.comboBox_3.addItem('花嫁尼禄')
        self.comboBox_3.addItem('玉藻前')
        self.comboBox_3.addItem('阿尔托莉雅·卡斯特')
        self.comboBox_3.addItem('无')
        self.comboBox_4.addItem('午茶学妹')
        self.comboBox_4.addItem('小达芬奇')
        self.comboBox_4.addItem('无')
        self.comboBox_5.addItem('1')
        self.comboBox_5.addItem('2')
        self.comboBox_5.addItem('3')
        self.comboBox_6.addItem('1')
        self.comboBox_6.addItem('2')
        self.comboBox_6.addItem('3')
        self.comboBox_7.addItem('4')
        self.comboBox_7.addItem('5')
        self.comboBox_7.addItem('6')
        self.lineEdit.setValidator(QIntValidator(0, 65535))
        self.lineEdit_2.setValidator(QIntValidator(0, 65535))
        self.lineEdit_4.setValidator(QIntValidator(0, 65535))
        self.lineEdit_5.setValidator(QIntValidator(0, 65535))
        self.lineEdit_6.setValidator(QIntValidator(0, 65535))
        self.lineEdit_7.setValidator(QIntValidator(0, 65535))

    def set_settings(self, filename):
        self.filename = filename
        with open(filename, 'r') as f_read:
            self.fgo_settings = json.load(f_read)
        self.lineEdit.setText(str(self.fgo_settings['repeat_num']))
        self.lineEdit_2.setText(str(self.fgo_settings['delay_time']))
        self.lineEdit_3.setText(str(self.fgo_settings['emulator_name']))
        self.lineEdit_4.setText(str(self.fgo_settings['round_wait_time'][0]))
        self.lineEdit_5.setText(str(self.fgo_settings['round_wait_time'][1]))
        self.lineEdit_6.setText(str(self.fgo_settings['round_wait_time'][2]))
        self.lineEdit_7.setText(str(self.fgo_settings['wait_time']))

        if self.fgo_settings['apple'] == 1:
            self.comboBox.setCurrentIndex(1)
        elif self.fgo_settings['apple'] == 2:
            self.comboBox.setCurrentIndex(2)
        elif self.fgo_settings['apple'] == 3:
            self.comboBox.setCurrentIndex(3)
        elif self.fgo_settings['apple'] == 1000:
            self.comboBox.setCurrentIndex(4)
        else:
            self.comboBox.setCurrentIndex(0)

        if self.fgo_settings['fight_turn'] == 1:
            self.comboBox_2.setCurrentIndex(0)
        elif self.fgo_settings['fight_turn'] == 2:
            self.comboBox_2.setCurrentIndex(1)
        elif self.fgo_settings['fight_turn'] == 3:
            self.comboBox_2.setCurrentIndex(2)
        else:
            sys.exit()

        if self.fgo_settings['character'] == 'kongming':
            self.comboBox_3.setCurrentIndex(0)
        elif self.fgo_settings['character'] == 'CBA':
            self.comboBox_3.setCurrentIndex(1)
        elif self.fgo_settings['character'] == 'merlin':
            self.comboBox_3.setCurrentIndex(2)
        elif self.fgo_settings['character'] == 'nero':
            self.comboBox_3.setCurrentIndex(3)
        elif self.fgo_settings['character'] == 'fox':
            self.comboBox_3.setCurrentIndex(4)
        elif self.fgo_settings['character'] == 'CAB':
            self.comboBox_3.setCurrentIndex(5)
        elif str(self.fgo_settings['character']) == '0':
            self.comboBox_3.setCurrentIndex(6)
        else:
            sys.exit()

        if self.fgo_settings['equipment'] == 'bondage':
            self.comboBox_4.setCurrentIndex(0)
        elif self.fgo_settings['equipment'] == 'QP':
            self.comboBox_4.setCurrentIndex(1)
        elif str(self.fgo_settings['equipment']) == '0':
            self.comboBox_4.setCurrentIndex(2)
        else:
            sys.exit()

        if self.fgo_settings['use_rand_time'] == 1:
            self.radioButton.setChecked(True)
            self.radioButton_2.setChecked(False)
        else:
            self.radioButton.setChecked(False)
            self.radioButton_2.setChecked(True)

        if self.fgo_settings['change_character'] != 0:
            self.radioButton_3.setChecked(True)
            self.radioButton_4.setChecked(False)
            self.comboBox_5.setCurrentIndex(self.fgo_settings['change_character'][0] - 1)
            self.comboBox_6.setCurrentIndex(self.fgo_settings['change_character'][1] - 1)
            self.comboBox_7.setCurrentIndex(self.fgo_settings['change_character'][2] - 4)
        else:
            self.radioButton_3.setChecked(False)
            self.radioButton_4.setChecked(True)
            self.comboBox_5.setCurrentIndex(0)
            self.comboBox_6.setCurrentIndex(0)
            self.comboBox_7.setCurrentIndex(0)

    def accept(self):
        self.fgo_settings['repeat_num'] = int(self.lineEdit.text())

        if self.comboBox.currentIndex() == 0:
            self.fgo_settings['apple'] = 0
        elif self.comboBox.currentIndex() == 1:
            self.fgo_settings['apple'] = 1
        elif self.comboBox.currentIndex() == 2:
            self.fgo_settings['apple'] = 2
        elif self.comboBox.currentIndex() == 3:
            self.fgo_settings['apple'] = 3
        elif self.comboBox.currentIndex() == 4:
            self.fgo_settings['apple'] = 1000
        else:
            sys.exit()

        if self.comboBox_3.currentIndex() == 0:
            self.fgo_settings['character'] = 'kongming'
        elif self.comboBox_3.currentIndex() == 1:
            self.fgo_settings['character'] = 'CBA'
        elif self.comboBox_3.currentIndex() == 2:
            self.fgo_settings['character'] = 'merlin'
        elif self.comboBox_3.currentIndex() == 3:
            self.fgo_settings['character'] = 'nero'
        elif self.comboBox_3.currentIndex() == 4:
            self.fgo_settings['character'] = 'fox'
        elif self.comboBox_3.currentIndex() == 5:
            self.fgo_settings['character'] = 'CAB'
        elif self.comboBox_3.currentIndex() == 6:
            self.fgo_settings['character'] = 0
        else:
            sys.exit()

        if self.comboBox_4.currentIndex() == 0:
            self.fgo_settings['equipment'] = 'bondage'
        elif self.comboBox_4.currentIndex() == 1:
            self.fgo_settings['equipment'] = 'QP'
        elif self.comboBox_4.currentIndex() == 2:
            self.fgo_settings['equipment'] = 0
        else:
            sys.exit()

        self.fgo_settings['wait_time'] = int(self.lineEdit_7.text())
        self.fgo_settings['delay_time'] = int(self.lineEdit_2.text())
        if self.comboBox_2.currentIndex() == 0:
            self.fgo_settings['fight_turn'] = 1
        elif self.comboBox_2.currentIndex() == 1:
            self.fgo_settings['fight_turn'] = 2
        elif self.comboBox_2.currentIndex() == 2:
            self.fgo_settings['fight_turn'] = 3
        else:
            sys.exit()

        self.fgo_settings['round_wait_time'] = [
            int(self.lineEdit_4.text()), int(self.lineEdit_5.text()), int(self.lineEdit_6.text())]
        if self.radioButton_3.isChecked():
            self.fgo_settings['change_character'] = [
                self.comboBox_5.currentIndex() + 1,
                self.comboBox_6.currentIndex() + 1,
                self.comboBox_7.currentIndex() + 4]
        else:
            self.fgo_settings['change_character'] = 0
        self.fgo_settings['emulator_name'] = self.lineEdit_3.text()

        if self.radioButton.isChecked():
            self.fgo_settings['use_rand_time'] = 1
        else:
            self.fgo_settings['use_rand_time'] = 0

        with open(self.filename, 'w') as f_write:
            json.dump(self.fgo_settings, f_write, sort_keys=True, indent=4, separators=(',', ': '))
        self.close()

    def reject(self):
        self.close()


class WindowFgoFight(QtWidgets.QWidget, qt_fgo_fight.Ui_Dialog):
    def __init__(self):
        super(WindowFgoFight, self).__init__()
        self.setupUi(self)
        self.filename = None
        self.fgo_settings = None
        for i in range(3):
            for j in range(3):
                self.comboBox.addItem("角色"+str(i+1)+"技能"+str(j+1))
        for i in range(3):
            self.comboBox.addItem("御主技能"+str(i+1))
            self.comboBox_3.addItem("宝具"+str(i+1))
        for i in range(5):
            self.comboBox_3.addItem("攻击卡"+str(i+1))

        self.comboBox_2.addItem("全体或自身")
        self.comboBox_4.addItem("全体或自身")
        for i in range(3):
            self.comboBox_2.addItem("敌方角色"+str(i+1))
            self.comboBox_4.addItem("敌方角色"+str(i+1))
        for i in range(3):
            self.comboBox_2.addItem("我方角色"+str(i+1))

        self.lineEdit.setValidator(QIntValidator(0, 65535))
        self.lineEdit.setText(str(3))
        self.lineEdit_2.setValidator(QIntValidator(0, 65535))
        self.lineEdit_2.setText(str(3))

        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels(["技能选择", "应用对象", "延迟时间"])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_2.setHorizontalHeaderLabels(["攻击选择", "应用对象", "延迟时间"])
        self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.key_dict = {
            "A": "角色1技能1",
            "B": "角色1技能2",
            "C": "角色1技能3",
            "D": "角色2技能1",
            "E": "角色2技能2",
            "F": "角色2技能3",
            "G": "角色3技能1",
            "H": "角色3技能2",
            "I": "角色3技能3",
            "T": "御主技能1",
            "U": "御主技能2",
            "V": "御主技能3",
            "K": "宝具1",
            "L": "宝具2",
            "M": "宝具3",
            "N": "攻击卡1",
            "O": "攻击卡2",
            "P": "攻击卡3",
            "Q": "攻击卡4",
            "R": "攻击卡5",
            "角色1技能1": "A",
            "角色1技能2": "B",
            "角色1技能3": "C",
            "角色2技能1":"D",
            "角色2技能2": "E",
            "角色2技能3": "F",
            "角色3技能1": "G",
            "角色3技能2": "H",
            "角色3技能3": "I",
            "御主技能1": "T",
            "御主技能2": "U",
            "御主技能3": "V",
            "宝具1": "K",
            "宝具2": "L",
            "宝具3": "M",
            "攻击卡1": "N",
            "攻击卡2": "O",
            "攻击卡3": "P",
            "攻击卡4": "Q",
            "攻击卡5": "R",
        }

    def set_fight_list(self, filename):
        self.filename = filename
        with open(filename, 'r') as f_read:
            self.fgo_settings = json.load(f_read)
        round_count = self.comboBox_5.count()
        if round_count < self.fgo_settings['fight_turn']:
            for i in range(self.fgo_settings['fight_turn'] - round_count):
                self.comboBox_5.addItem(str(round_count + i + 1))
                self.comboBox_6.addItem(str(round_count + i + 1))
        elif round_count > self.fgo_settings['fight_turn']:
            for i in range(self.fgo_settings['fight_turn'], round_count):
                self.comboBox_5.removeItem(i)
                self.comboBox_6.removeItem(i)
        self.tableWidget.setRowCount(
            len(self.fgo_settings['fight']['fight_round'+str(self.comboBox_5.currentIndex()+1)]['skill']))
        for i in range(len(self.fgo_settings['fight']['fight_round'+str(self.comboBox_5.currentIndex()+1)]['skill'])):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(
                self.key_dict[self.fgo_settings['fight']['fight_round' + str(self.comboBox_5.currentIndex() + 1)][
                    'skill']['operation' + str(i + 1)]['button']]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(
                self.comboBox_2.itemText(
                    int(self.fgo_settings['fight']['fight_round' + str(self.comboBox_5.currentIndex() + 1)]['skill'][
                         'operation' + str(i + 1)]['object']) - 1)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(
                    str(self.fgo_settings['fight']['fight_round' + str(self.comboBox_5.currentIndex() + 1)]['skill'][
                        'operation' + str(i + 1)]['delay_time'])))

        self.tableWidget_2.setRowCount(
            len(self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack']))
        for i in range(
                len(self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack'])):
            self.tableWidget_2.setItem(i, 0, QTableWidgetItem(
                self.key_dict[
                    self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack'][
                        'operation' + str(i + 1)]['button']]))
            self.tableWidget_2.setItem(i, 1, QTableWidgetItem(
                self.comboBox_4.itemText(
                    int(self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack'][
                            'operation' + str(i + 1)]['object']) - 1)))
            self.tableWidget_2.setItem(i, 2, QTableWidgetItem(
                str(self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack'][
                        'operation' + str(i + 1)]['delay_time'])))
        return

    def round_change_skill(self):
        self.tableWidget.setRowCount(
            len(self.fgo_settings['fight']['fight_round' + str(self.comboBox_5.currentIndex() + 1)]['skill']))
        for i in range(
                len(self.fgo_settings['fight']['fight_round' + str(self.comboBox_5.currentIndex() + 1)]['skill'])):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(
                self.key_dict[self.fgo_settings['fight']['fight_round' + str(self.comboBox_5.currentIndex() + 1)][
                    'skill']['operation' + str(i + 1)]['button']]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(
                self.comboBox_2.itemText(
                    int(self.fgo_settings['fight']['fight_round' + str(self.comboBox_5.currentIndex() + 1)]['skill'][
                            'operation' + str(i + 1)]['object']) - 1)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(
                str(self.fgo_settings['fight']['fight_round' + str(self.comboBox_5.currentIndex() + 1)]['skill'][
                        'operation' + str(i + 1)]['delay_time'])))
        return

    def round_change_attack(self):
        self.tableWidget_2.setRowCount(
            len(self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack']))
        for i in range(
                len(self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack'])):
            self.tableWidget_2.setItem(i, 0, QTableWidgetItem(
                self.key_dict[
                    self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack'][
                        'operation' + str(i + 1)]['button']]))
            self.tableWidget_2.setItem(i, 1, QTableWidgetItem(
                self.comboBox_4.itemText(
                    int(self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack'][
                            'operation' + str(i + 1)]['object']) - 1)))
            self.tableWidget_2.setItem(i, 2, QTableWidgetItem(
                str(self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack'][
                        'operation' + str(i + 1)]['delay_time'])))
        return

    def add_skill(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(
            self.tableWidget.rowCount()-1, 0, QTableWidgetItem(self.comboBox.itemText(self.comboBox.currentIndex())))
        self.tableWidget.setItem(
            self.tableWidget.rowCount()-1, 1, QTableWidgetItem(self.comboBox_2.itemText(self.comboBox_2.currentIndex())))
        self.tableWidget.setItem(
            self.tableWidget.rowCount()-1, 2, QTableWidgetItem(self.lineEdit.text()))

        self.fgo_settings['fight']['fight_round' + str(self.comboBox_5.currentIndex() + 1)]['skill'][
            'operation' + str(self.tableWidget.rowCount())] = {'button': 0, 'object': 0, 'delay_time': 0}
        self.fgo_settings['fight']['fight_round' + str(self.comboBox_5.currentIndex() + 1)]['skill'][
            'operation' + str(self.tableWidget.rowCount())]['button'] = \
            self.key_dict[self.comboBox.itemText(self.comboBox.currentIndex())]
        self.fgo_settings['fight']['fight_round' + str(self.comboBox_5.currentIndex() + 1)]['skill'][
            'operation' + str(self.tableWidget.rowCount())]['object'] = \
            self.comboBox_2.currentIndex()+1
        self.fgo_settings['fight']['fight_round' + str(self.comboBox_5.currentIndex() + 1)]['skill'][
            'operation' + str(self.tableWidget.rowCount())]['delay_time'] = \
            int(self.lineEdit.text())
        return

    def delete_skill(self):
        delrow = self.tableWidget.currentRow()
        self.tableWidget.removeRow(delrow)

        for i in range(delrow, len(self.fgo_settings['fight']['fight_round' + str(self.comboBox_5.currentIndex() + 1)][
                                       'skill'])-1):
            self.fgo_settings['fight']['fight_round' + str(self.comboBox_5.currentIndex() + 1)]['skill'][
                'operation' + str(i+1)] = self.fgo_settings['fight'][
                'fight_round' + str(self.comboBox_5.currentIndex() + 1)]['skill']['operation' + str(i+2)]
        self.fgo_settings['fight']['fight_round' + str(self.comboBox_5.currentIndex() + 1)]['skill'].pop(
            'operation' + str(len(self.fgo_settings['fight'][
                                      'fight_round' + str(self.comboBox_5.currentIndex() + 1)]['skill'])))
        return

    def add_attack(self):
        self.tableWidget_2.insertRow(self.tableWidget_2.rowCount())
        self.tableWidget_2.setItem(
            self.tableWidget_2.rowCount() - 1, 0,
            QTableWidgetItem(self.comboBox_3.itemText(self.comboBox_3.currentIndex())))
        self.tableWidget_2.setItem(
            self.tableWidget_2.rowCount() - 1, 1,
            QTableWidgetItem(self.comboBox_4.itemText(self.comboBox_4.currentIndex())))
        self.tableWidget_2.setItem(
            self.tableWidget_2.rowCount() - 1, 2, QTableWidgetItem(self.lineEdit_2.text()))

        self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack'][
            'operation' + str(self.tableWidget_2.rowCount())] = {'button': 0, 'object': 0, 'delay_time': 0}
        self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack'][
            'operation' + str(self.tableWidget_2.rowCount())]['button'] = \
            self.key_dict[self.comboBox_3.itemText(self.comboBox_3.currentIndex())]
        self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack'][
            'operation' + str(self.tableWidget_2.rowCount())]['object'] = \
            self.comboBox_4.currentIndex() + 1
        self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack'][
            'operation' + str(self.tableWidget_2.rowCount())]['delay_time'] = \
            int(self.lineEdit_2.text())
        return

    def delete_attack(self):
        delrow = self.tableWidget_2.currentRow()
        self.tableWidget_2.removeRow(delrow)

        for i in range(delrow, len(self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)][
                                       'attack']) - 1):
            self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack'][
                'operation' + str(i + 1)] = self.fgo_settings['fight'][
                'fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack']['operation' + str(i + 2)]
        self.fgo_settings['fight']['fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack'].pop(
            'operation' + str(len(self.fgo_settings['fight'][
                                      'fight_round' + str(self.comboBox_6.currentIndex() + 1)]['attack'])))
        return

    def accept(self):
        with open(self.filename, 'w') as f_write:
            json.dump(self.fgo_settings, f_write, sort_keys=True, indent=4, separators=(',', ': '))
        self.close()
        return

    def reject(self):
        self.close()


class WindowFgoAbout(QtWidgets.QWidget, qt_fgo_about.Ui_Dialog):
    def __init__(self):
        super(WindowFgoAbout, self).__init__()
        self.setupUi(self)

    def accept(self):
        self.close()


def start():
    fgo_window = WindowFgoMain()
    fgo_window.show()
    return fgo_window


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = start()
    sys.exit(app.exec_())
