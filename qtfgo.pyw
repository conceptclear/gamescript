import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.Qt import QThread, QMutex
from PyQt5.QtGui import QIntValidator
from PyQt5.QtGui import QIcon
import qt_fgo_main
import qt_fgo_settings
import qt_fgo_about
import qt_fgo_fight
import fgo
import json
import numpy as np
import codecs

qmut_1 = QMutex()


class Thread_1(QThread):
    def __init__(self, script):
        super().__init__()
        self.script = script

    def run(self):
        qmut_1.lock()
        this_fgo_fight = fgo.Fgo('settings/fgosettings' + self.script + '.json')
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
        self.setcomboBox()
        with open('settings/fgosettings1.json', 'r') as f_read:
            self.fgo_settings = json.load(f_read)
        fight_text = codecs.open('settings/fight1.json', 'r', encoding='utf-8').read()
        self.fight_list = np.array(json.loads(fight_text))
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

    def setcomboBox(self):
        self.comboBox.addItem("脚本1")
        self.comboBox.addItem("脚本2")
        self.comboBox.addItem("脚本3")
        self.comboBox.addItem("脚本4")
        self.comboBox.addItem("脚本5")

    def change_fgo_settings_click(self):
        with open('settings/fgosettings' + str(self.comboBox.currentIndex() + 1) + '.json', 'r') as f_read:
            self.fgo_settings = json.load(f_read)
        self.dialog_fgo_settings.set_settings(self.fgo_settings, self.comboBox.currentIndex() + 1)
        self.dialog_fgo_settings.show()

    def change_fgo_fight(self):
        fight_text = codecs.open(
            'settings/fight' + str(self.comboBox.currentIndex() + 1) + '.json', 'r', encoding='utf-8').read()
        self.fight_list = np.array(json.loads(fight_text))
        self.dialog_fgo_fight.set_fight_list(self.fight_list, self.comboBox.currentIndex() + 1)
        self.dialog_fgo_fight.show()

    def open_about(self):
        self.dialog_fgo_about.show()

    def start_script(self):
        self.thread = Thread_1(str(self.comboBox.currentIndex() + 1))
        self.thread.start()

    def end_script(self):
        sys.exit()


class WindowFgoSettings(QtWidgets.QWidget, qt_fgo_settings.Ui_Dialog):
    def __init__(self):
        super(WindowFgoSettings, self).__init__()
        self.setupUi(self)
        self.setting_file = 1
        self.buttonGroup1 = QtWidgets.QButtonGroup()
        self.buttonGroup1.addButton(self.radioButton)
        self.buttonGroup1.addButton(self.radioButton_2)
        self.buttonGroup2 = QtWidgets.QButtonGroup()
        self.buttonGroup2.addButton(self.radioButton_3)
        self.buttonGroup2.addButton(self.radioButton_4)
        self.comboBox.addItem('不吃苹果')
        self.comboBox.addItem('吃金苹果')
        self.comboBox.addItem('吃银苹果')
        self.comboBox.addItem('吃彩苹果')
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

    def set_settings(self, fgo_settings, setting_file):
        self.setting_file = setting_file
        self.lineEdit.setText(str(fgo_settings['repeat_num']))
        self.lineEdit_2.setText(str(fgo_settings['delay_time']))
        self.lineEdit_3.setText(str(fgo_settings['emulator_name']))
        self.lineEdit_4.setText(str(fgo_settings['side_wait_time'][0]))
        self.lineEdit_5.setText(str(fgo_settings['side_wait_time'][1]))
        self.lineEdit_6.setText(str(fgo_settings['side_wait_time'][2]))
        self.lineEdit_7.setText(str(fgo_settings['wait_time']))

        if fgo_settings['apple'] == 1:
            self.comboBox.setCurrentIndex(1)
        elif fgo_settings['apple'] == 2:
            self.comboBox.setCurrentIndex(2)
        elif fgo_settings['apple'] == 1000:
            self.comboBox.setCurrentIndex(3)
        else:
            self.comboBox.setCurrentIndex(0)

        if fgo_settings['fight_turn'] == 1:
            self.comboBox_2.setCurrentIndex(0)
        elif fgo_settings['fight_turn'] == 2:
            self.comboBox_2.setCurrentIndex(1)
        elif fgo_settings['fight_turn'] == 3:
            self.comboBox_2.setCurrentIndex(2)
        else:
            sys.exit()

        if fgo_settings['character'] == 'kongming':
            self.comboBox_3.setCurrentIndex(0)
        elif fgo_settings['character'] == 'CBA':
            self.comboBox_3.setCurrentIndex(1)
        elif fgo_settings['character'] == 'merlin':
            self.comboBox_3.setCurrentIndex(2)
        elif fgo_settings['character'] == 'nero':
            self.comboBox_3.setCurrentIndex(3)
        elif fgo_settings['character'] == 'fox':
            self.comboBox_3.setCurrentIndex(4)
        elif fgo_settings['character'] == 'CAB':
            self.comboBox_3.setCurrentIndex(5)
        elif str(fgo_settings['character']) == '0':
            self.comboBox_3.setCurrentIndex(6)
        else:
            sys.exit()

        if fgo_settings['equipment'] == 'bondage':
            self.comboBox_4.setCurrentIndex(0)
        elif fgo_settings['equipment'] == 'QP':
            self.comboBox_4.setCurrentIndex(1)
        elif str(fgo_settings['equipment']) == '0':
            self.comboBox_4.setCurrentIndex(2)
        else:
            sys.exit()

        if fgo_settings['use_rand_time'] == 1:
            self.radioButton.setChecked(True)
            self.radioButton_2.setChecked(False)
        else:
            self.radioButton.setChecked(False)
            self.radioButton_2.setChecked(True)

        if fgo_settings['change_character'] != 0:
            self.radioButton_3.setChecked(True)
            self.radioButton_4.setChecked(False)
            self.comboBox_5.setCurrentIndex(fgo_settings['change_character'][0] - 1)
            self.comboBox_6.setCurrentIndex(fgo_settings['change_character'][1] - 1)
            self.comboBox_7.setCurrentIndex(fgo_settings['change_character'][2] - 4)
        else:
            self.radioButton_3.setChecked(False)
            self.radioButton_4.setChecked(True)
            self.comboBox_5.setCurrentIndex(0)
            self.comboBox_6.setCurrentIndex(0)
            self.comboBox_7.setCurrentIndex(0)

    def accept(self):
        fgo_settings = {'repeat_num': int(self.lineEdit.text())}

        if self.comboBox.currentIndex() == 0:
            fgo_settings['apple'] = 0
        elif self.comboBox.currentIndex() == 1:
            fgo_settings['apple'] = 1
        elif self.comboBox.currentIndex() == 2:
            fgo_settings['apple'] = 2
        elif self.comboBox.currentIndex() == 3:
            fgo_settings['apple'] = 1000
        else:
            sys.exit()

        if self.comboBox_3.currentIndex() == 0:
            fgo_settings['character'] = 'kongming'
        elif self.comboBox_3.currentIndex() == 1:
            fgo_settings['character'] = 'CBA'
        elif self.comboBox_3.currentIndex() == 2:
            fgo_settings['character'] = 'merlin'
        elif self.comboBox_3.currentIndex() == 3:
            fgo_settings['character'] = 'nero'
        elif self.comboBox_3.currentIndex() == 4:
            fgo_settings['character'] = 'fox'
        elif self.comboBox_3.currentIndex() == 5:
            fgo_settings['character'] = 'CAB'
        elif self.comboBox_3.currentIndex() == 6:
            fgo_settings['character'] = 0
        else:
            sys.exit()

        if self.comboBox_4.currentIndex() == 0:
            fgo_settings['equipment'] = 'bondage'
        elif self.comboBox_4.currentIndex() == 1:
            fgo_settings['equipment'] = 'QP'
        elif self.comboBox_4.currentIndex() == 2:
            fgo_settings['equipment'] = 0
        else:
            sys.exit()

        fgo_settings['wait_time'] = int(self.lineEdit_7.text())
        fgo_settings['delay_time'] = int(self.lineEdit_2.text())
        if self.comboBox_2.currentIndex() == 0:
            fgo_settings['fight_turn'] = 1
        elif self.comboBox_2.currentIndex() == 1:
            fgo_settings['fight_turn'] = 2
        elif self.comboBox_2.currentIndex() == 2:
            fgo_settings['fight_turn'] = 3
        else:
            sys.exit()

        fgo_settings['side_wait_time'] = [
            int(self.lineEdit_4.text()), int(self.lineEdit_5.text()), int(self.lineEdit_6.text())]
        if self.radioButton_3.isChecked():
            fgo_settings['change_character'] = [
                self.comboBox_5.currentIndex() + 1,
                self.comboBox_6.currentIndex() + 1,
                self.comboBox_7.currentIndex() + 4]
        else:
            fgo_settings['change_character'] = 0
        fgo_settings['emulator_name'] = self.lineEdit_3.text()

        if self.radioButton.isChecked():
            fgo_settings['use_rand_time'] = 1
        else:
            fgo_settings['use_rand_time'] = 0
        fgo_settings['fight'] = 'settings/fight' + str(self.setting_file) + '.json'

        with open('settings/fgosettings' + str(self.setting_file) + '.json', 'w') as f_write:
            json.dump(fgo_settings, f_write)
        self.close()

    def reject(self):
        self.close()


class WindowFgoFight(QtWidgets.QWidget, qt_fgo_fight.Ui_Dialog):
    def __init__(self):
        super(WindowFgoFight, self).__init__()
        self.setupUi(self)
        self.setting_file = 1
        self.comboBoxDict = {
            1: self.comboBox, 2: self.comboBox_2,
            3: self.comboBox_3, 4: self.comboBox_4,
            5: self.comboBox_5, 6: self.comboBox_6,
            7: self.comboBox_7, 8: self.comboBox_8,
            9: self.comboBox_9, 10: self.comboBox_10,
            11: self.comboBox_11, 12: self.comboBox_12,
            13: self.comboBox_13, 14: self.comboBox_14,
            15: self.comboBox_15, 16: self.comboBox_16,
            17: self.comboBox_17, 18: self.comboBox_18,
            19: self.comboBox_19, 20: self.comboBox_20,
            21: self.comboBox_21, 22: self.comboBox_22,
            23: self.comboBox_23, 24: self.comboBox_24,
            25: self.comboBox_25, 26: self.comboBox_26,
            27: self.comboBox_27, 28: self.comboBox_28,
            29: self.comboBox_29, 30: self.comboBox_30,
            31: self.comboBox_31, 32: self.comboBox_32,
            33: self.comboBox_33, 34: self.comboBox_34,
            35: self.comboBox_35, 36: self.comboBox_36,
            37: self.comboBox_37, 38: self.comboBox_38,
            39: self.comboBox_39, 40: self.comboBox_40,
            41: self.comboBox_41, 42: self.comboBox_42,
            43: self.comboBox_43, 44: self.comboBox_44,
            45: self.comboBox_45, 46: self.comboBox_46,
            47: self.comboBox_47, 48: self.comboBox_48,
            49: self.comboBox_49, 50: self.comboBox_50,
            51: self.comboBox_51, 52: self.comboBox_52,
            53: self.comboBox_53, 54: self.comboBox_54,
        }
        for i in range(3):
            for j in range(18):
                self.comboBoxDict[18 * i + j + 1].addItem('不用技能')
                self.comboBoxDict[18 * i + j + 1].addItem('全体或自身技能')
                self.comboBoxDict[18 * i + j + 1].addItem('对敌方角色1用技能')
                self.comboBoxDict[18 * i + j + 1].addItem('对敌方角色2用技能')
                self.comboBoxDict[18 * i + j + 1].addItem('对敌方角色3用技能')
            for j in range(15):
                self.comboBoxDict[18 * i + j + 1].addItem('对己方角色1用技能')
                self.comboBoxDict[18 * i + j + 1].addItem('对己方角色2用技能')
                self.comboBoxDict[18 * i + j + 1].addItem('对己方角色3用技能')

    def set_fight_list(self, fight_list, setting_file):
        self.setting_file = setting_file
        for i in range(3):
            for j in range(18):
                self.comboBoxDict[i * 18 + j + 1].setCurrentIndex(fight_list[i][j])

    def accept(self):
        fight_list = np.empty([3, 18], dtype=int)
        for i in range(3):
            for j in range(18):
                fight_list[i][j] = self.comboBoxDict[18 * i + j + 1].currentIndex()
        fight_text = fight_list.tolist()
        json.dump(fight_text, codecs.open(
            'settings/fight' + str(self.setting_file) + '.json', 'w', encoding='utf-8'),
                  separators=(',', ':'), sort_keys=True, indent=4)
        self.close()

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
