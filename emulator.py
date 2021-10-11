import win32gui
import logger
import win32api
import win32con
import time
import random
import win32print
import win32ui
import cv2 as cv
import numpy as np
import fgo_dict


class Emulator:
    """
    模拟器类：
        logger: 生成日志
        name: 模拟器窗口名称
        parent: 父窗口句柄
        handle: 子窗口句柄
        use_rand_time: 使用随机时间
        keyboard_dict: 键盘按键词典
        mouse_dict: 鼠标按键词典
        left: 窗口最左x坐标
        bottom: 窗口最下y坐标
        right: 窗口最右x坐标
        top: 窗口最上y坐标
        width: 窗口宽度
        height: 窗口高度
        resolution: 显示放缩率
    """

    def __init__(self, name, keyboard_dict, mouse_dict, use_rand_time):
        self.logger = logger.Logger(__name__)
        self.name = name
        self.parent = 0
        self.handle = 0
        self.get_handle()
        self.use_rand_time = use_rand_time
        self.keyboard_dict = keyboard_dict
        self.mouse_dict = mouse_dict
        self.left, self.bottom, self.right, self.top = win32gui.GetWindowRect(self.handle)
        self.width = self.right - self.left
        self.height = self.top - self.bottom
        self.resolution = 0
        self.get_resolution()

    def get_handle(self):
        """get handle of execute program"""
        self.parent = win32gui.FindWindow(None, self.name)
        if self.parent == 0:
            self.logger.get_log().error('错误的窗口句柄！无法找到' + self.name)
            return False
        if self.name == '雷电模拟器':
            self.get_child_windows()
        else:
            self.logger.get_log().warn('目前不支持该模拟器，不能保证没有问题')
            self.get_child_windows()
        return None

    def get_child_windows(self):
        """get child handle"""
        if self.parent == 0:
            self.logger.get_log().error('寻找子句柄出错')
            return False
        hwndChildList = []
        win32gui.EnumChildWindows(self.parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
        self.logger.get_log().debug('窗口子句柄为:' + str(hwndChildList[0]))
        self.handle = hwndChildList[0]
        return None

    def get_resolution(self):
        hDC = win32gui.GetDC(0)
        self.resolution = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES) / win32api.GetSystemMetrics(
            win32con.SM_CXSCREEN)
        self.logger.get_log().debug('屏幕分辨率为：' + str(self.resolution))
        return None

    def get_bitmap(self):
        """get background screenshot"""
        width = int(self.width * self.resolution)
        height = int(self.height * self.resolution)

        hWndDC = win32gui.GetWindowDC(self.handle)
        # device description table
        mfcDC = win32ui.CreateDCFromHandle(hWndDC)
        # memory device description table
        saveDC = mfcDC.CreateCompatibleDC()
        # create bitmap
        saveBitMap = win32ui.CreateBitmap()
        # set storage
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        # set screenshot to storage
        saveDC.SelectObject(saveBitMap)
        # save bitmap to memory device description table
        saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
        # save screenshot
        self.logger.get_log().debug('对窗口截图')
        saveBitMap.SaveBitmapFile(saveDC, "img_check.bmp")
        return None

    def press_keyboard(self, key, delay_time):
        """simulate keyboard keys in the background"""
        self.logger.get_log().debug('对窗口按'+key+'键')
        win32api.SendMessage(self.handle, win32con.WM_KEYDOWN, self.keyboard_dict[key], 0)
        win32api.SendMessage(self.handle, win32con.WM_KEYUP, self.keyboard_dict[key], 0)
        time.sleep(delay_time + self.rand_time())
        return None

    def press_mouse_key(self, mouse_key, delay_time):
        """simulate mouse press in the background with dict"""
        point_x = int(self.mouse_dict[mouse_key][0] * self.width / self.mouse_dict['width'])
        point_y = int(self.mouse_dict[mouse_key][1] * self.height / self.mouse_dict['height'])
        self.press_mouse(point_x, point_y, delay_time)
        return None

    def press_mouse(self, point_x, point_y, delay_time):
        """simulate mouse press in the background with given position"""
        # self.logger.get_log().info('鼠标点击（' + str(point_x) + ',' + str(point_y) + '）')
        p_position = win32api.MAKELONG(point_x, point_y)
        win32api.SendMessage(self.handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        win32api.SendMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, p_position)
        time.sleep(0.2)
        win32api.SendMessage(self.handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, p_position)
        time.sleep(delay_time + self.rand_time())
        return None

    def slide_mouse(self, mouse_key1, mouse_key2, delay_time):
        """simulate mouse sliding in the background with dict"""
        point1_x = int(self.mouse_dict[mouse_key1][0] * self.width / self.mouse_dict['width'])
        point1_y = int(self.mouse_dict[mouse_key1][1] * self.height / self.mouse_dict['height'])
        point2_x = int(self.mouse_dict[mouse_key2][0] * self.width / self.mouse_dict['width'])
        point2_y = int(self.mouse_dict[mouse_key2][1] * self.height / self.mouse_dict['height'])
        self.logger.get_log().debug('鼠标拖动（' + str(point1_x) + ',' + str(point1_y) + '）至（'
                                    + str(point2_x) + ',' + str(point2_y) + '）')
        p_position = win32api.MAKELONG(point1_x, point1_y)
        u_position = win32api.MAKELONG(point2_x, point2_y)
        win32gui.SendMessage(self.handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        win32gui.SendMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, p_position)
        time.sleep(0.2)
        steps = 100
        x_add = (point2_x - point1_x)/steps
        y_add = (point2_y - point1_y)/steps
        for i in range(steps):
            win32gui.SendMessage(self.handle, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON,
                                 win32api.MAKELONG(int(point1_x + x_add * i), int(point1_y + y_add * i)))
            time.sleep(0.01)
        win32gui.SendMessage(self.handle, win32con.WM_LBUTTONUP, 0, u_position)
        time.sleep(delay_time + self.rand_time())
        return None

    def rand_time(self):
        """add rand time for each operation"""
        return random.uniform(0, 0.5) if self.use_rand_time is True else 0

    def template_matching(self, check_pic, template_pic, threshold, check_area):
        """
        check the pic whether existing or not
        return the position list where the template exsisted in the check pic
        """
        template = cv.imread(template_pic)
        size = template.shape
        target = cv.imread(check_pic)
        target = cv.resize(target, (self.mouse_dict['width'], self.mouse_dict['height']))
        if check_area != 0:
            target = target[check_area[0]:check_area[1], check_area[2]:check_area[3]]

        result = cv.matchTemplate(target, template, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        if max_val < threshold:
            pos_list = np.array([[]])
            return pos_list
        pos_list = np.array([[max_loc[0], max_loc[0] + size[1], max_loc[1], max_loc[1] + size[0]]])
        location = np.where(result > threshold)
        for i in zip(*location[::-1]):
            for j in range(int(pos_list.size / 4)):
                if abs(i[0] - pos_list[j][0]) > 10 or abs(i[1] - pos_list[j][2]) > 10:
                    pos_list = np.append(pos_list, [[i[0], i[0] + size[1], i[1], i[1] + size[0]]], axis=0)
        return pos_list


if __name__ == '__main__':
    a = Emulator('雷电模拟器', fgo_dict.keyboard_key, fgo_dict.mouse_key, 1)
    a.get_bitmap()
