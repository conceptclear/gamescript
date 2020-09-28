#!/usr/bin/python

"""general settings for fgo"""

import random
import sys
import time
import xlrd
import win32gui
import basic_function

check_size = (1280, 720)

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

"""dictionary of button conducted by mouse press"""
press_dict = {
    'A': (66, 571),  # first character first skill
    'B': (169, 571),  # first character second skill
    'C': (260, 571),  # first character third skill
    'D': (383, 571),  # second character first skill
    'E': (480, 571),  # second character second skill
    'F': (575, 571),  # second character third skill
    'G': (709, 571),  # third character first skill
    'H': (798, 571),  # third character second skill
    'I': (898, 571),  # third character third skill
    'J': (1138, 598),  # attack
    'K': (405, 193),  # first character noble phantasm
    'L': (638, 193),  # second character noble phantasm
    'M': (879, 193),  # third character noble phantasm
    'N': (136, 486),  # first card
    'O': (393, 486),  # second card
    'P': (650, 486),  # third card
    'Q': (898, 486),  # forth card
    'R': (1159, 489),  # fifth card
    'S': (1191, 315),  # master skill menu
    'T': (908, 315),  # first master skill
    'U': (999, 315),  # second master skill
    'V': (1085, 315),  # third master skill
    '1': (54, 39),  # first enemy
    '2': (294, 39),  # second enemy
    '3': (524, 39),  # third enemy
    '4': (1190, 678),  # enter (right bottom)
    '5': (851, 130),  # refresh list
    'up': (400, 480, 400, 300),  # draw up
    'chara1': (135, 352),  # character1 in change
    'chara2': (338, 352),  # character2 in change
    'chara3': (540, 352),  # character3 in change
    'chara4': (742, 352),  # character4 in change
    'chara5': (944, 352),  # character5 in change
    'chara6': (1146, 352),  # character6 in change
    'change': (650, 620),  # change character
}


def rand_card(handle, card_num, width, height, delay_num):
    """choose 2 cards in 5 cards"""
    a = [press_dict['N'], press_dict['O'], press_dict['P'], press_dict['Q'], press_dict['R']]
    choice = random.sample(a, card_num)
    for i in range(card_num):
        basic_function.press_mouse(handle, choice[i], [width, height], check_size, 1 + delay_num)
    return None


def continue_attack(handle, action, width, height, delay_num):
    """check whether continue attacking"""
    if not action:
        basic_function.press_mouse(handle, press_dict['E'], [width, height], check_size, 3 + delay_num)
    else:
        basic_function.press_mouse(handle, press_dict['H'], [width, height], check_size, 3 + delay_num)
    return None


def check_fight(handle, width, height, resolution):
    """check which side of the fight"""
    basic_function.get_bitmap(handle, width, height, resolution)
    basic_function.save_sliced_binarization_pic("img_check.bmp", check_size, [5, 45, 860, 890])
    result1 = basic_function.template_matching('img_binarization.jpg', 'source/1.jpg', 0, 0)
    result2 = basic_function.template_matching('img_binarization.jpg', 'source/2.jpg', 0, 0)
    result3 = basic_function.template_matching('img_binarization.jpg', 'source/3.jpg', 0, 0)
    result = max(result1[1], result2[1], result3[1])
    if result < 0.75:
        print('Failed to enter the any side')
        sys.exit()
    else:
        if result == result1[1]:
            return 1
        if result == result2[1]:
            return 2
        if result == result3[1]:
            return 3
        else:
            print('error occurred')
            return None


def check_apple(handle, width, height, resolution, state, delay_num):
    """check whether eat apple"""
    print('Checking whether to eat apple')
    basic_function.get_bitmap(handle, width, height, resolution)
    result1 = basic_function.template_matching('img_check.bmp', 'source/apple.jpg', check_size, 0)
    result2 = basic_function.template_matching('img_check.bmp', 'source/assist.jpg', check_size, 0)
    if result1[1] > 0.95:
        print("eat apple")
        if state:
            basic_function.press_mouse(handle, press_dict['T'], [width, height], check_size, 1 + delay_num)
            basic_function.press_mouse(handle, press_dict['H'], [width, height], check_size, 2 + delay_num)
        else:
            print("end loop")
            sys.exit()
    elif result2[1] > 0.95:
        print("don't need to eat apple")
        return None
    else:
        print("error occurred")
        sys.exit()

    return None


def check_character(handle, width, height, character, equipment, resolution, delay_num):
    """find character in assist"""
    basic_function.get_bitmap(handle, width, height, resolution)
    if character == str(0.0):
        print("don't need to find character")
        if equipment == str(0.0):
            print("don't need to find equipment")
            basic_function.press_mouse(handle, press_dict['T'], [width, height], check_size, 3 + delay_num)
            return None
        else:
            print("finding " + equipment)
            [min_val, max_val, min_loc, max_loc, th, tw] = basic_function.template_matching('img_check.bmp',
                                                                                            'source/' + equipment + '.jpg',
                                                                                            check_size, 0)
            while 1:
                count = 0
                while max_val < 0.95 and count < 10:
                    count += 1
                    basic_function.slide_mouse(handle, press_dict['up'], [width, height], check_size, 1.5 + delay_num)
                    basic_function.get_bitmap(handle, width, height, resolution)
                    [min_val, max_val, min_loc, max_loc, th, tw] = basic_function.template_matching('img_check.bmp',
                                                                                                    'source/' + equipment + '.jpg',
                                                                                                    check_size, 0)
                if max_val >= 0.95:
                    break
                else:
                    time.sleep(10)
                    print('could not find ' + equipment + ', refresh')
                    basic_function.press_mouse(handle, press_dict['5'], [width, height], check_size, 1 + delay_num)
                    basic_function.press_mouse(handle, press_dict['H'], [width, height], check_size, 1 + delay_num)
            print('OK')
    else:
        print('finding ' + character)
        [min_val, max_val, min_loc, max_loc, th, tw] = basic_function.template_matching('img_check.bmp',
                                                                                        'source/' + character + '.jpg',
                                                                                        check_size, 0)

        while 1:
            count = 0
            while max_val < 0.95 and count < 10:
                count += 1
                basic_function.slide_mouse(handle, press_dict['up'], [width, height], check_size, 1.5 + delay_num)
                basic_function.get_bitmap(handle, width, height, resolution)
                [min_val, max_val, min_loc, max_loc, th, tw] = basic_function.template_matching('img_check.bmp',
                                                                                                'source/' + character + '.jpg',
                                                                                                check_size, 0)
            if max_val >= 0.95:
                print('OK')
                if equipment == str(0.0):
                    print("don't need to find equipment")
                    break
                else:
                    print("checking " + equipment)
                    if max_loc[1] + th + 70 > 720:
                        print("equipment did not match")
                        basic_function.slide_mouse(handle, press_dict['up'], [width, height], check_size, 1.5 + delay_num)
                        max_val = 0
                        continue
                    [min_val1, max_val1, min_loc1, max_loc1, th1, tw1] = basic_function.template_matching(
                        'img_check.bmp',
                        'source/' + equipment + '.jpg',
                        check_size,
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
                        basic_function.slide_mouse(handle, press_dict['up'], [width, height], check_size, 1.5 + delay_num)
                        max_val = 0
                        count += 1
                        if count >= 10:
                            print('could not find ' + character + ', refresh')
                            basic_function.press_mouse(handle, press_dict['5'], [width, height], check_size,
                                                       1 + delay_num)
                            basic_function.press_mouse(handle, press_dict['H'], [width, height], check_size,
                                                       1 + delay_num)
                        continue
            else:
                # time.sleep(10)
                print('could not find ' + character + ', refresh')
                basic_function.press_mouse(handle, press_dict['5'], [width, height], check_size, 1 + delay_num)
                basic_function.press_mouse(handle, press_dict['H'], [width, height], check_size, 1 + delay_num)
        print('OK')

    tl = max_loc
    br = (tl[0] + tw, tl[1] + th)

    point = [0, 0]
    point[0] = int((tl[0] + br[0]) / 2)
    point[1] = int((tl[1] + br[1]) / 2)

    basic_function.press_mouse(handle, point, [width, height], check_size, 3 + delay_num)
    return None


def read_strategy(handle, width, height, resolution, delay_num, fight_turn, change_character):
    wb = xlrd.open_workbook('strategy.xlsx')
    for battle in range(fight_turn):
        print("Start fight in side " + str(battle+1))
        side = wb.sheet_by_name('Side' + str(battle + 1))
        for i in range(9):
            if side.cell(2 + i, 1).value != 1:
                continue
            else:
                if side.cell(2 + i, 2).value == 0:
                    basic_function.press_mouse(handle, press_dict[chr(65 + i)], [width, height], check_size, 3 + delay_num)
                elif side.cell(2 + i, 2).value > 6 or side.cell(2 + i, 2).value < 0:
                    print("error input")
                    sys.exit()
                elif side.cell(2 + i, 2).value < 4:
                    basic_function.press_mouse(handle, press_dict[chr(65 + i)], [width, height], check_size, 0.5 + delay_num)
                    basic_function.press_mouse(handle, press_dict[chr(78 + int(side.cell(2 + i, 2).value))], [width, height], check_size,
                                                  3 + delay_num)
                else:
                    basic_function.press_mouse(handle, press_dict[chr(57 + int(side.cell(2 + i, 2).value))], [width, height], check_size,
                                                  0.5 + delay_num)
                    basic_function.press_mouse(handle, press_dict[chr(65 + i)], [width, height], check_size, 3 + delay_num)

        for i in range(3):
            if side.cell(11 + i, 1).value != 1:
                continue
            else:
                basic_function.press_mouse(handle, press_dict['S'], [width, height], check_size, 0.5 + delay_num)
                if i == 2 and change_character == 1:
                    if side.cell(13, 2).value > 3 or side.cell(13, 2).value < 1 or side.cell(13, 3).value > 6 or side.cell(13, 3).value < 4:
                        print("error input")
                        sys.exit()
                    else:
                        basic_function.press_mouse(handle, press_dict['V'], [width, height], check_size,
                                                   0.5 + delay_num)
                        basic_function.press_mouse(handle, press_dict['chara' + str(int(side.cell(13, 2).value))],
                                                   [width, height], check_size,
                                                   0.5 + delay_num)
                        basic_function.press_mouse(handle, press_dict['chara' + str(int(side.cell(13, 3).value))],
                                                   [width, height], check_size,
                                                   0.5 + delay_num)
                        basic_function.press_mouse(handle, press_dict['change'], [width, height], check_size, 5 + delay_num)
                        print("character " + str(int(side.cell(13, 3).value)) + " change character " + str(int(side.cell(13, 2).value)))
                        for j in range(3):
                            if side.cell(14 + j, 1).value != 1:
                                continue
                            else:
                                if side.cell(14 + j, 2).value == 0:
                                    basic_function.press_mouse(handle, press_dict[chr(65 + (int(side.cell(13, 2).value) - 1) * 3 + j)], [width, height],
                                                               check_size, 3 + delay_num)
                                elif side.cell(14 + j, 2).value > 6 or side.cell(14 + j, 2).value < 0:
                                    print("error input")
                                    sys.exit()
                                elif side.cell(14 + j, 2).value < 4:
                                    basic_function.press_mouse(handle, press_dict[chr(65 + (int(side.cell(13, 2).value) - 1) * 3 + j)], [width, height],
                                                               check_size, 0.5 + delay_num)
                                    basic_function.press_mouse(handle,
                                                               press_dict[chr(78 + int(side.cell(14 + j, 2).value))],
                                                               [width, height], check_size,
                                                               3 + delay_num)
                                else:
                                    basic_function.press_mouse(handle,
                                                               press_dict[chr(57 + int(side.cell(14 + j, 2).value))],
                                                               [width, height], check_size,
                                                               0.5 + delay_num)
                                    basic_function.press_mouse(handle, press_dict[chr(65 + (int(side.cell(13, 2).value) - 1) * 3 + j)], [width, height],
                                                               check_size, 3 + delay_num)
                elif side.cell(11 + i, 2).value == 0:
                    basic_function.press_mouse(handle, press_dict[chr(84 + i)], [width, height], check_size, 3 + delay_num)
                elif side.cell(11 + i, 2).value > 4 or side.cell(11 + i, 2).value < 0:
                    print("error input")
                    sys.exit()
                else:
                    basic_function.press_mouse(handle, press_dict[chr(84 + i)], [width, height], check_size, 0.5 + delay_num)
                    basic_function.press_mouse(handle, press_dict[chr(78 + int(side.cell(11 + i, 2).value))], [width, height], check_size,
                                                  3 + delay_num)

        time.sleep(1 + delay_num)
        basic_function.press_mouse(handle, press_dict['J'], [width, height], check_size, 3 + delay_num)
        num_spellcard = 0
        for i in range(3):
            if side.cell(18 + i, 1).value != 1:
                continue
            else:
                if side.cell(18 + i, 2).value == 0:
                    basic_function.press_mouse(handle, press_dict[chr(75 + i)], [width, height], check_size, 0.5 + delay_num)
                    num_spellcard += 1
                elif side.cell(18 + i, 2).value > 4 or side.cell(18 + i, 2).value < 0:
                    print("error input")
                    sys.exit()
                else:
                    basic_function.press_mouse(handle, press_dict[chr(60 + int(side.cell(18 + i, 2).value))], [width, height], check_size,
                                                  0.5 + delay_num)
                    basic_function.press_mouse(handle, press_dict[chr(75 + i)], [width, height], check_size, 0.5 + delay_num)
                    num_spellcard += 1

        rand_card(hwnd, 3-num_spellcard, width, height, delay_num)
        time.sleep(side.cell(21, 1).value)

    for i in range(5):
        basic_function.press_mouse(handle, press_dict['4'], [width, height], check_size, 1 + delay_num)
    print('battle finish')
    return None


if __name__ == '__main__':
    print('可以通过修改strategy.xlsx来实现刷本策略的改变')

    wb = xlrd.open_workbook('strategy.xlsx')
    settings = wb.sheet_by_name('Settings')

    display_resolution = float(settings.cell(1, 1).value)
    repeat_num = int(settings.cell(2, 1).value)
    apple = int(settings.cell(3, 1).value)

    character = str(settings.cell(4, 1).value)
    equipment = str(settings.cell(5, 1).value)

    wait_time = float(settings.cell(6, 1).value)
    delay_number = float(settings.cell(7, 1).value)

    fight_turn = int(settings.cell(8, 1).value)

    hwnd = basic_function.get_handle(settings.cell(9, 1).value)
    change_character = int(settings.cell(10, 1).value)

    left, bottom, right, top = win32gui.GetWindowRect(hwnd)
    hwnd_width = right - left
    hwnd_height = top - bottom

    for repeat in range(repeat_num):
        check_character(hwnd, hwnd_width, hwnd_height, character, equipment, display_resolution, delay_number)
        if repeat == 0:
            basic_function.press_mouse(hwnd, press_dict['4'], [hwnd_width, hwnd_height], check_size, 3 + delay_number)
        time.sleep(wait_time)
        read_strategy(hwnd, hwnd_width, hwnd_height, display_resolution, delay_number, fight_turn, change_character)
        if repeat < repeat_num - 1:
            continue_attack(hwnd, True, hwnd_width, hwnd_height, delay_number)
            if apple == 1:
                check_apple(hwnd, hwnd_width, hwnd_height, display_resolution, True, delay_number)
            else:
                check_apple(hwnd, hwnd_width, hwnd_height, display_resolution, False, delay_number)
            time.sleep(6)
            print("···············")
        else:
            continue_attack(hwnd, False, hwnd_width, hwnd_height, delay_number)
            print("Loop terminated")
    sys.exit()

