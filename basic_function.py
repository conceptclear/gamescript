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


def get_bitmap(handle, width, height):
    """get background screenshot"""
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


def template_matching(handle, width, height, pic, resolution):
    """check the pic whether existing or not"""
    tpl = cv.imread(pic)
    size = tpl.shape
    target = cv.imread("img_check.bmp")
    target = cv.resize(target, resolution)

    result = cv.matchTemplate(target, tpl, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    return [min_val, max_val, min_loc, max_loc, size[0], size[1]]
