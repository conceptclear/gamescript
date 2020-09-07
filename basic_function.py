#!/usr/bin/python

"""basic functions used for emulator"""

import win32gui
import win32api
import win32con
import time
import win32ui
import cv2 as cv
import random

rand_num = True


def rand_time():
    return random.uniform(0, 0.5) if rand_num is True else 0


def press_keyboard(handle, key, delay_time):
    """simulate keyboard keys in the background"""
    win32api.PostMessage(handle, win32con.WM_KEYDOWN, key, 0)
    time.sleep(0.2)
    win32api.PostMessage(handle, win32con.WM_KEYUP, key, 0)
    time.sleep(delay_time + rand_time())
    return None


def press_mouse(handle, position, delay_time):
    """simulate mouse press in the background"""
    p_position = win32api.MAKELONG(position[0], position[1])
    win32gui.SendMessage(handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, p_position)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, p_position)
    time.sleep(delay_time + rand_time())
    return None


def get_child_windows(parent):
    """get child handle"""
    if not parent:
        return None
    hwndChildList = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
    return hwndChildList


def get_handle(name):
    """get handle of execute program"""
    hwnd = win32gui.FindWindow(None, name)
    hwnd1 = get_child_windows(hwnd)
    hwnd = hwnd1[0]
    return hwnd


def get_bitmap(handle, width, height, resolution):
    """get background screenshot"""

    width = int(width*resolution)
    height = int(height*resolution)

    hWndDC = win32gui.GetWindowDC(handle)
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
    saveBitMap.SaveBitmapFile(saveDC, "img_check.bmp")
    return None


def template_matching(check_pic, template_pic, resolution, check_area):
    """check the pic whether existing or not"""
    template = cv.imread(template_pic)
    size = template.shape
    target = cv.imread(check_pic)
    if resolution != 0:
        target = cv.resize(target, resolution)
    if check_area != 0:
        target = target[check_area[0]:check_area[1], check_area[2]:check_area[3]]

    result = cv.matchTemplate(target, template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    return [min_val, max_val, min_loc, max_loc, size[0], size[1]]


def save_sliced_binarization_pic(origin_pic, resolution, slicing_area):
    """slice the origin picture to get a binarizational picture"""
    pic = cv.imread(origin_pic)
    pic = cv.resize(pic, resolution)
    pic = pic[slicing_area[0]:slicing_area[1], slicing_area[2]:slicing_area[3]]
    gray = cv.cvtColor(pic, cv.COLOR_RGB2GRAY)
    temp = cv.threshold(gray, 128, 255, cv.THRESH_BINARY)
    cv.imwrite("img_binarization.jpg", temp[1])
    return None
