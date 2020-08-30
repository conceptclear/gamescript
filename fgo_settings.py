#!/usr/bin/python

"""general settings for fgo"""

import random
import sys
import time
import xlrd

import win32gui

import basic_function

"""dictionary of button"""
button_dict = {
    'A': 0x41,  # first character first skill
    'B': 0x42,  # first character second skill
    'C': 0x43,  # first character third skill
    'D': 0x44,  # second character first skill
    'E': 0x45,  # second character second skill
    'F': 0x46,  # second character third skill
    'G': 0x47,  # third character first skill
    'H': 0x48,  # third character second skill
    'I': 0x49,  # third character third skill
    'J': 0x4A,  # attack
    'K': 0x4B,  # first character noble phantasm
    'L': 0x4C,  # second character noble phantasm
    'M': 0x4D,  # third character noble phantasm
    'N': 0x4E,  # first card
    'O': 0x4F,  # second card
    'P': 0x50,  # third card
    'Q': 0x51,  # forth card
    'R': 0x52,  # fifth card
    'S': 0x53,  # master skill menu
    'T': 0x54,  # first master skill
    'U': 0x55,  # second master skill
    'V': 0x56,  # third master skill
    '1': 0x31,  # first enemy
    '2': 0x32,  # second enemy
    '3': 0x33,  # third enemy
    '4': 0x34,  # enter (right bottom)
    '5': 0x35,  # refresh list
    'up': 0x26,  # draw up
}


def rand_card(handle):
    """choose 2 cards in 5 cards"""
    a = [button_dict['N'], button_dict['O'], button_dict['P'], button_dict['Q'], button_dict['R']]
    choice = random.sample(a, 2)
    basic_function.press_keyboard(handle, choice[0], 0.5)
    basic_function.press_keyboard(handle, choice[1], 1)
    return None


def continue_attack(handle, action):
    """check whether continue attacking"""
    if not action:
        basic_function.press_keyboard(handle, button_dict['E'], 3)
    else:
        basic_function.press_keyboard(handle, button_dict['H'], 3)
    return None


def check_apple(handle, width, height, state):
    """check whether eat apple"""
    print('Checking whether to eat apple')
    basic_function.get_bitmap(handle, width, height)
    [min_val1, max_val1, min_loc1, max_loc1, th, tw] = basic_function.template_matching('img_check.bmp',
                                                                                        'source/apple.jpg',
                                                                                        (1280, 720), 0)
    [min_val2, max_val2, min_loc2, max_loc2, th, tw] = basic_function.template_matching('img_check.bmp',
                                                                                        'source/assist.jpg',
                                                                                        (1280, 720), 0)
    if max_val1 > 0.95:
        print("eat apple")
        if state:
            basic_function.press_keyboard(handle, button_dict['T'], 1)
            basic_function.press_keyboard(handle, button_dict['H'], 2)
        else:
            print("end loop")
            sys.exit()
    elif max_val2 > 0.95:
        print("don't need to eat apple")
        return None
    else:
        print("error occurred")
        sys.exit()

    return None


def check_character(handle, width, height, character, equipment):
    """find character in assist"""
    basic_function.get_bitmap(handle, width, height)
    print('finding ' + character)
    [min_val, max_val, min_loc, max_loc, th, tw] = basic_function.template_matching('img_check.bmp',
                                                                                    'source/' + character + '.jpg',
                                                                                    (1280, 720), 0)

    while 1:
        count = 0
        while max_val < 0.95 and count < 10:
            count += 1
            basic_function.press_keyboard(handle, button_dict['up'], 1.5)
            basic_function.get_bitmap(handle, width, height)
            [min_val, max_val, min_loc, max_loc, th, tw] = basic_function.template_matching('img_check.bmp',
                                                                                            'source/' + character + '.jpg',
                                                                                            (1280, 720), 0)
        if max_val >= 0.95:
            print('OK')
            if equipment == 0:
                print("don't need to find equipment")
                break
            else:
                print("checking " + equipment)
                [min_val1, max_val1, min_loc1, max_loc1, th1, tw1] = basic_function.template_matching('img_check.bmp',
                                                                                                      'source/' + equipment + '.jpg',
                                                                                                      (1280, 720),
                                                                                                      [max_loc[1] + th,
                                                                                                       max_loc[
                                                                                                           1] + th + 70,
                                                                                                       max_loc[0] - 20,
                                                                                                       max_loc[
                                                                                                           0] + tw + 20])
                if max_val1 >= 0.95:
                    break
                else:
                    print("equipment did not match")
        else:
            time.sleep(10)
            print('could not find ' + character + ', refresh')
            basic_function.press_keyboard(handle, button_dict['5'], 1)
            basic_function.press_keyboard(handle, button_dict['H'], 1)
    print('OK')

    tl = max_loc
    br = (tl[0] + tw, tl[1] + th)

    point = [0, 0]
    point[0] = int((tl[0] + br[0]) / 2 / 1280 * width)
    point[1] = int((tl[1] + br[1]) / 2 / 720 * height)

    basic_function.press_mouse(handle, point, 3)
    basic_function.press_keyboard(handle, button_dict['4'], 22)
    return None


def read_strategy(handle):
    wb = xlrd.open_workbook('strategy.xlsx')
    for battle in range(3):
        side = wb.sheet_by_name('Side' + str(battle + 1))
        for repeat in range(9):
            if side.cell(2 + repeat, 1).value != 1:
                continue
            else:
                if side.cell(2 + repeat, 2).value == 0:
                    basic_function.press_keyboard(handle, button_dict[chr(65 + repeat)], 3)
                elif side.cell(2 + repeat, 2).value > 6 or side.cell(2 + repeat, 2).value < 0:
                    print("error input")
                elif side.cell(2 + repeat, 2).value < 4:
                    basic_function.press_keyboard(handle, button_dict[chr(65 + repeat)], 0.5)
                    basic_function.press_keyboard(handle, button_dict[chr(78 + int(side.cell(2 + repeat, 2).value))], 3)
                else:
                    basic_function.press_keyboard(handle, button_dict[chr(57 + int(side.cell(2 + repeat, 2).value))],
                                                  0.5)
                    basic_function.press_keyboard(handle, button_dict[chr(65 + repeat)], 3)

        for repeat in range(3):
            if side.cell(11 + repeat, 1).value != 1:
                continue
            else:
                basic_function.press_keyboard(handle, button_dict['S'], 0.5)
                if side.cell(11 + repeat, 2).value == 0:
                    basic_function.press_keyboard(handle, button_dict[chr(84 + repeat)], 3)
                elif side.cell(11 + repeat, 2).value > 4 or side.cell(11 + repeat, 2).value < 0:
                    print("error input")
                else:
                    basic_function.press_keyboard(handle, button_dict[chr(84 + repeat)], 0.5)
                    basic_function.press_keyboard(handle, button_dict[chr(78 + int(side.cell(11 + repeat, 2).value))],
                                                  3)

        basic_function.press_keyboard(handle, button_dict['J'], 3)
        for repeat in range(3):
            if side.cell(15 + repeat, 1).value != 1:
                continue
            else:
                if side.cell(15 + repeat, 2).value == 0:
                    basic_function.press_keyboard(handle, button_dict[chr(75 + repeat)], 0.5)
                elif side.cell(15 + repeat, 2).value > 4 or side.cell(15 + repeat, 2).value < 0:
                    print("error input")
                else:
                    basic_function.press_keyboard(handle, button_dict[chr(60 + int(side.cell(15 + repeat, 2).value))],
                                                  0.5)
                    basic_function.press_keyboard(handle, button_dict[chr(75 + repeat)], 0.5)

        rand_card(hwnd)
        time.sleep(side.cell(18, 1).value)

    for repeat in range(5):
        basic_function.press_keyboard(handle, button_dict['4'], 1)
    print('battle finish')
    return None


if __name__ == '__main__':
    print('This script is based on "网易MuMu模拟器“')
    print('可以通过修改strategy.xlsx来实现刷本策略的改变，默认为狂兰WCBA带04服')
    hwnd = basic_function.get_handle('命运-冠位指定 - MuMu模拟器')
    left, bottom, right, top = win32gui.GetWindowRect(hwnd)
    hwnd_width = right - left
    hwnd_height = top - bottom

    repeat_num = int(input('请输入重复刷本的次数：'))
    apple = int(input('是否需要吃苹果？（1代表是，0代表不是）：'))

    character = input('请输入需要寻找的助战角色(现在提供的有CBA, kongming, merlin, nero, fox)：')
    equipment = input('请输入助战角色身上带的概念礼装（现在提供的有贝拉丽莎（QP），午餐学妹（bondage）：')

    for i in range(repeat_num):
        check_character(hwnd, hwnd_width, hwnd_height, character, equipment)
        read_strategy(hwnd)
        if i < repeat_num - 1:
            continue_attack(hwnd, True)
            if apple == 1:
                check_apple(hwnd, hwnd_width, hwnd_height, True)
            else:
                check_apple(hwnd, hwnd_width, hwnd_height, False)
            time.sleep(6)
            print("···············")
        else:
            continue_attack(hwnd, False)
            print("Loop terminated")
    sys.exit()
