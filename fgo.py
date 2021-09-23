import fgo_dict
import emulator
import logger
import json
import random
import sys
import time


class FgoBasic:
    """
    Data Class for basic settings in fgo

    logger: 生成日志
    repeat_num: 重复刷本次数
    apple: 是否吃苹果
    character: 助战角色
    equipment: 助战角色所带礼装
    wait_time: 选完角色后进入第一面开始刷本所需要时间
    delay_time: 延迟按键时间（针对于运算速度比较慢的电脑做的动态调整）
    fight_turn: 战斗面数
    change_character: 使用换人礼装，为一个list，第0位确定第几面换人，第1位为前三个角色中一个，第2位为后三个角色中一个
    round_wait_time: 三面释放宝具后等待时间
    emulator_name: 模拟器窗口名称
    use_rand_time: 使用随机延迟时间
    fight: 按键序列
    count_character: 检测助战角色拖动界面次数
    """

    def __init__(self, repeat_num, apple, character, equipment, wait_time, delay_time,
                 fight_turn, round_wait_time, emulator_name, use_rand_time, change_character, fight):
        self.repeat_num = repeat_num
        self.apple = apple
        self.character = character
        self.equipment = equipment
        self.wait_time = wait_time
        self.delay_time = delay_time
        self.fight_turn = fight_turn
        self.round_wait_time = round_wait_time
        self.emulator = emulator.Emulator(emulator_name, fgo_dict.keyboard_key, fgo_dict.mouse_key, use_rand_time)
        self.change_character = change_character
        self.fight = fight
        self.count_character = 0


class Fgo:
    """
    Fgo class for automation
    """

    def __init__(self, settings_name):
        with open(settings_name, 'r') as f_read:
            self.fgo_settings = dict2fgobasic(json.load(f_read))
        self.logger = logger.Logger(__name__)

    def save_fgo_settings(self, settings_name):
        """
        保存fgo设定
        :param settings_name: 保存名称
        :return:
        """
        with open(settings_name, 'w') as f_write:
            json.dump(fgobasic2dict(self.fgo_settings), f_write, sort_keys=True, indent=4, separators=(',', ': '))

    def rand_card(self, card_num):
        """choose 2 cards in 5 cards"""
        card = ['N', 'O', 'P', 'Q', 'R']
        choice = random.sample(card, card_num)
        for i in range(card_num):
            self.fgo_settings.emulator.press_mouse_key(choice[i], 1 + self.fgo_settings.delay_time)
        return None

    def continue_attack(self, action):
        """check whether continue attacking"""
        if not action:
            self.fgo_settings.emulator.press_mouse_key('E', 5 + self.fgo_settings.delay_time)
        else:
            self.fgo_settings.emulator.press_mouse_key('H', 5 + self.fgo_settings.delay_time)
        return None

    def check_apple(self):
        """check whether eat apple"""
        self.logger.get_log().debug('判断是否进入吃苹果界面')
        self.fgo_settings.emulator.get_bitmap()
        result1 = self.fgo_settings.emulator.template_matching('img_check.bmp', 'source/apple.jpg', 0.9, 0)
        result2 = self.fgo_settings.emulator.template_matching('img_check.bmp', 'source/assist.jpg', 0.9, 0)
        if result1.size:
            self.logger.get_log().debug('已进入吃苹果判断界面')
            if self.fgo_settings.apple == 1:
                self.logger.get_log().debug('吃金苹果')
                self.fgo_settings.emulator.press_mouse_key('T', 1 + self.fgo_settings.delay_time)
                self.fgo_settings.emulator.press_mouse_key('H', 2 + self.fgo_settings.delay_time)
            elif self.fgo_settings.apple == 2:
                self.logger.get_log().debug('吃银苹果')
                self.fgo_settings.emulator.press_mouse_key('P', 1 + self.fgo_settings.delay_time)
                self.fgo_settings.emulator.press_mouse_key('H', 2 + self.fgo_settings.delay_time)
            elif self.fgo_settings.apple == 3:
                self.logger.get_log().debug('吃铜苹果')
                self.fgo_settings.emulator.slide_mouse('up1', 'up2', 1.5 + self.fgo_settings.delay_time)
                self.fgo_settings.emulator.press_mouse_key('P', 1 + self.fgo_settings.delay_time)
                self.fgo_settings.emulator.press_mouse_key('H', 2 + self.fgo_settings.delay_time)
            elif self.fgo_settings.apple == 1000:
                self.logger.get_log().debug('吃彩苹果')
                self.fgo_settings.emulator.press_mouse_key('L', 1 + self.fgo_settings.delay_time)
                self.fgo_settings.emulator.press_mouse_key('H', 2 + self.fgo_settings.delay_time)
            else:
                self.logger.get_log().debug('不吃苹果，结束循环')
                sys.exit()
        elif result2.size:
            self.logger.get_log().debug('进入选取助战界面')
            return None
        else:
            self.logger.get_log().error('在判断是否需要吃苹果界面发生错误')
            sys.exit()
        return None

    def character_skill(self, fight_round, operation):
        """
        :param fight_round: 战斗面数
        :param operation: 操作编号
        :return: None
        """
        if self.fgo_settings.fight[fight_round]["skill"][operation]["object"] == 1:
            self.fgo_settings.emulator.press_mouse_key(
                self.fgo_settings.fight[fight_round]["skill"][operation]["button"],
                self.fgo_settings.fight[fight_round]["skill"][operation]["delay_time"]
                + self.fgo_settings.delay_time)
        elif self.fgo_settings.fight[fight_round]["skill"][operation]["object"] > 7 \
                or self.fgo_settings.fight[fight_round]["skill"][operation]["object"] < 0:
            self.logger.get_log().error('技能选择释放对象出错')
            sys.exit()
        elif self.fgo_settings.fight[fight_round]["skill"][operation]["object"] > 4:
            self.fgo_settings.emulator.press_mouse_key(
                self.fgo_settings.fight[fight_round]["skill"][operation]["button"],
                0.5 + self.fgo_settings.delay_time)
            self.fgo_settings.emulator.press_mouse_key(
                chr(74 + self.fgo_settings.fight[fight_round]["skill"][operation]["object"]),
                self.fgo_settings.fight[fight_round]["skill"][operation]["delay_time"]
                + self.fgo_settings.delay_time)
        else:
            self.fgo_settings.emulator.press_mouse_key(
                chr(47 + self.fgo_settings.fight[fight_round]["skill"][operation]["object"]),
                0.5 + self.fgo_settings.delay_time)
            self.fgo_settings.emulator.press_mouse_key(
                self.fgo_settings.fight[fight_round]["skill"][operation]["button"],
                self.fgo_settings.fight[fight_round]["skill"][operation]["delay_time"]
                + self.fgo_settings.delay_time)
        return None

    def master_skill(self, fight_round, operation):
        """
        御主技能
        :param fight_round: 战斗面数
        :param operation: 操作编号
        :return: None
        """
        if self.fgo_settings.change_character != 0 and \
                self.fgo_settings.fight[fight_round]["skill"][operation]["button"] == 'V':
            this_fight_round = int(fight_round[-1])
            if self.fgo_settings.change_character[0] == this_fight_round:
                self.logger.get_log().debug('使用换人功能')
                self.fight_change_character(fight_round, operation)
                return None
            else:
                self.logger.get_log().error("已使用过换人")
                sys.exit()
        if self.fgo_settings.fight[fight_round]["skill"][operation]["object"] == 0:
            return None
        else:
            self.fgo_settings.emulator.press_mouse_key('S', 0.5 + self.fgo_settings.delay_time)
            self.character_skill(fight_round, operation)
        return None

    def skill_check(self, fight_round, operation):
        if self.fgo_settings.fight[fight_round]["skill"][operation]["button"] == "T" or \
                self.fgo_settings.fight[fight_round]["skill"][operation]["button"] == "U" or\
                self.fgo_settings.fight[fight_round]["skill"][operation]["button"] == "V":
            self.master_skill(fight_round, operation)
        else:
            self.character_skill(fight_round, operation)

    def fight_change_character(self, fight_round, operation):
        self.fgo_settings.emulator.press_mouse_key('S', 0.5 + self.fgo_settings.delay_time)
        if self.fgo_settings.change_character[1] > 3 or self.fgo_settings.change_character[1] < 1 \
                or self.fgo_settings.change_character[2] > 6 or self.fgo_settings.change_character[2] < 4:
            self.logger.get_log().error('换人中选人错误，应该是前三个角色中一个更换后三个角色中一个')
            sys.exit()
        self.fgo_settings.emulator.press_mouse_key('V', 1.5 + self.fgo_settings.delay_time)
        self.fgo_settings.emulator.press_mouse_key(
            'chara' + str(self.fgo_settings.change_character[1]), 0.5 + self.fgo_settings.delay_time)
        self.fgo_settings.emulator.press_mouse_key(
            'chara' + str(self.fgo_settings.change_character[2]), 0.5 + self.fgo_settings.delay_time)
        self.fgo_settings.emulator.press_mouse_key(
            'change', self.fgo_settings.fight[fight_round]["skill"][operation]["delay_time"]
            + self.fgo_settings.delay_time)
        self.logger.get_log().debug('角色' + str(self.fgo_settings.change_character[2]) +
                                    '更换角色' + str(self.fgo_settings.change_character[1]))

    def spell_card(self, fight_round, operation):
        """
        释放宝具
        :param fight_round: 战斗面数
        :param operation: 操作编号
        :return: 宝具释放次数
        """
        if self.fgo_settings.fight[fight_round]["attack"][operation]["object"] == 0:
            return 0
        else:
            if self.fgo_settings.fight[fight_round]["attack"][operation]["object"] == 1:
                self.fgo_settings.emulator.press_mouse_key(
                    self.fgo_settings.fight[fight_round]["attack"][operation]["button"],
                    self.fgo_settings.fight[fight_round]["attack"][operation]["delay_time"]
                    + self.fgo_settings.delay_time)
            elif self.fgo_settings.fight[fight_round]["attack"][operation]["object"] > 4 \
                    or self.fgo_settings.fight[fight_round]["attack"][operation]["object"] < 0:
                self.logger.get_log().error('释放宝具选取对象错误')
                sys.exit()
            else:
                self.fgo_settings.emulator.press_mouse_key(
                    chr(47 + self.fgo_settings.fight[fight_round]["attack"][operation]["object"]),
                    0.5 + self.fgo_settings.delay_time)
                self.fgo_settings.emulator.press_mouse_key(
                    self.fgo_settings.fight[fight_round]["attack"][operation]["button"],
                    self.fgo_settings.fight[fight_round]["attack"][operation]["delay_time"]
                    + self.fgo_settings.delay_time)
        return 1

    def set_fight(self):
        for battle in range(self.fgo_settings.fight_turn):
            self.logger.get_log().debug('开始第' + str(battle + 1) + '面的战斗')
            fight_round = "fight_round" + str(battle+1)
            for i in range(len(self.fgo_settings.fight[fight_round]["skill"])):
                operation = "operation" + str(i+1)
                self.skill_check(fight_round, operation)
            num_attack_card = len(self.fgo_settings.fight[fight_round]["attack"])
            self.fgo_settings.emulator.press_mouse_key('J', 3 + self.fgo_settings.delay_time)
            for i in range(num_attack_card):
                operation = "operation" + str(i+1)
                self.spell_card(fight_round, operation)
            self.rand_card(3 - num_attack_card)
            time.sleep(self.fgo_settings.round_wait_time[battle])
        for i in range(5):
            self.fgo_settings.emulator.press_mouse_key('4', 1 + self.fgo_settings.delay_time)
        self.logger.get_log().debug('战斗结束')
        return None

    def find_assist(self, assist, threshold):
        self.logger.get_log().debug('寻找' + assist)
        if assist != "CAB":
            assist_pos = self.fgo_settings.emulator.template_matching(
                'img_check.bmp', 'source/' + assist + '.jpg', threshold, 0)
        else:
            assist_pos = self.fgo_settings.emulator.template_matching(
                'img_check.bmp', 'source/' + assist + '1.jpg', threshold, 0)
            if assist_pos.size == 0:
                assist_pos = self.fgo_settings.emulator.template_matching(
                    'img_check.bmp', 'source/' + assist + '2.jpg', threshold, 0)
        while 1:
            while assist_pos.size == 0 and self.fgo_settings.count_character < 10:
                self.fgo_settings.count_character += 1
                self.fgo_settings.emulator.slide_mouse('up1', 'up2', 1.5 + self.fgo_settings.delay_time)
                self.fgo_settings.emulator.get_bitmap()
                if assist != "CAB":
                    assist_pos = self.fgo_settings.emulator.template_matching(
                        'img_check.bmp', 'source/' + assist + '.jpg', threshold, 0)
                else:
                    assist_pos = self.fgo_settings.emulator.template_matching(
                        'img_check.bmp', 'source/' + assist + '1.jpg', threshold, 0)
                    if assist_pos.size == 0:
                        assist_pos = self.fgo_settings.emulator.template_matching(
                            'img_check.bmp', 'source/' + assist + '2.jpg', threshold, 0)
            if assist_pos.size != 0:
                break
            else:
                time.sleep(5)
                self.logger.get_log().debug('无法找到' + assist + '，刷新助战列表')
                self.fgo_settings.emulator.press_mouse_key('5', 1 + self.fgo_settings.delay_time)
                self.fgo_settings.emulator.press_mouse_key('H', 1 + self.fgo_settings.delay_time)
                self.fgo_settings.count_character = 0
        self.logger.get_log().debug('已找到')
        return assist_pos

    def check_equipment(self, assist_pos):
        """check whether equipment match"""
        self.logger.get_log().debug('检测助战角色所带礼装是否符合要求')
        for i in range(int(assist_pos.size / 4)):
            if assist_pos[i][3] + 20 > 720:
                continue
            equip_pos = self.fgo_settings.emulator.template_matching(
                'img_check.bmp', 'source/' + self.fgo_settings.equipment + '.jpg', 0.95,
                [assist_pos[i][2], assist_pos[i][3] + 20, assist_pos[i][0] - 220, assist_pos[i][0]])
            if equip_pos.size == 0:
                continue
            else:
                self.logger.get_log().debug('符合要求')
                return i
        self.fgo_settings.emulator.slide_mouse('up1', 'up2', 1.5 + self.fgo_settings.delay_time)
        self.fgo_settings.count_character += 1
        self.fgo_settings.emulator.get_bitmap()
        self.logger.get_log().debug('不符合要求')
        return -1

    def check_character(self):
        """find character in assist"""
        self.fgo_settings.emulator.get_bitmap()
        status = 0
        if self.fgo_settings.character == 0:
            self.logger.get_log().debug("不需要寻找助战从者")
            if self.fgo_settings.equipment == 0:
                self.logger.get_log().debug("不需要寻找礼装")
                self.logger.get_log().warning('不设置助战从者也不设置寻找礼装，则会默认点击第一个助战从者的位置，若开启筛选可能会出错')
                self.fgo_settings.emulator.press_mouse_key('T', 3 + self.fgo_settings.delay_time)
                return None
            else:
                self.fgo_settings.count_character = 0
                assist_pos = self.find_assist(self.fgo_settings.equipment, 0.95)
        else:
            self.fgo_settings.count_character = 0
            assist_pos = self.find_assist(self.fgo_settings.character, 0.9)
            if self.fgo_settings.equipment == 0:
                self.logger.get_log().debug("不需要寻找礼装")
            else:
                status = self.check_equipment(assist_pos)
                while status == -1:
                    assist_pos = self.find_assist(self.fgo_settings.character, 0.9)
                    status = self.check_equipment(assist_pos)

        point_x = int((assist_pos[status][0] + assist_pos[status][1]) / 2 *
                      self.fgo_settings.emulator.width / self.fgo_settings.emulator.mouse_dict['width'])
        point_y = int((assist_pos[status][2] + assist_pos[status][3]) / 2 *
                      self.fgo_settings.emulator.height / self.fgo_settings.emulator.mouse_dict['height'])
        self.fgo_settings.emulator.press_mouse(point_x, point_y, 3 + self.fgo_settings.delay_time)
        return None

    def repeat_fight(self):
        for repeat in range(self.fgo_settings.repeat_num):
            self.check_character()
            if repeat == 0:
                self.fgo_settings.emulator.press_mouse_key('4', 5 + self.fgo_settings.delay_time)
            time.sleep(self.fgo_settings.wait_time)
            self.set_fight()
            if repeat < self.fgo_settings.repeat_num - 1:
                self.continue_attack(True)
                self.check_apple()
                time.sleep(6)
                self.logger.get_log().debug('完成刷本' + str(repeat + 1) + '次')
            else:
                self.continue_attack(False)
                self.logger.get_log().debug('完成刷本，关闭脚本')
        sys.exit()


def fgobasic2dict(fgobasic):
    return {
        'repeat_num': fgobasic.repeat_num,
        'apple': fgobasic.apple,
        'character': fgobasic.character,
        'equipment': fgobasic.equipment,
        'wait_time': fgobasic.wait_time,
        'delay_time': fgobasic.delay_time,
        'fight_turn': fgobasic.fight_turn,
        'round_wait_time': fgobasic.round_wait_time,
        'change_character': fgobasic.change_character,
        "emulator_name": fgobasic.emulator.name,
        'use_rand_time': fgobasic.emulator.use_rand_time,
        'fight': fgobasic.fight
    }


def dict2fgobasic(dict):
    return FgoBasic(
        dict['repeat_num'],
        dict['apple'],
        dict['character'],
        dict['equipment'],
        dict['wait_time'],
        dict['delay_time'],
        dict['fight_turn'],
        dict['round_wait_time'],
        dict['emulator_name'],
        dict['use_rand_time'],
        dict['change_character'],
        dict['fight']
    )


if __name__ == '__main__':
    fgo = Fgo('settings/fgo1.json')
    fgo.repeat_fight()
