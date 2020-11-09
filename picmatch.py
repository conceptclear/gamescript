import cv2 as cv
import numpy as np


def template_matching(check_pic, template_pic, resolution, check_area):
    """
    check the pic whether existing or not
    return the position list where the template exsited in the check pic
    """
    threshold = 0.9
    template = cv.imread(template_pic)
    size = template.shape
    target = cv.imread(check_pic)
    if resolution != 0:
        target = cv.resize(target, resolution)
    if check_area != 0:
        target = target[check_area[0]:check_area[1], check_area[2]:check_area[3]]

    result = cv.matchTemplate(target, template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    if max_val < threshold:
        return False
    pos_list = np.array([[max_loc[0], max_loc[0] + size[0], max_loc[1], max_loc[1] + size[1]]])
    location = np.where(result > threshold)
    for i in zip(*location[::-1]):
        for j in range(int(pos_list.size/4)):
            if abs(i[0] - pos_list[j][0]) > 10 or abs(i[1] - pos_list[j][2]) > 10:
                pos_list = np.append(pos_list, [[i[0], i[0] + size[0], i[1], i[1] + size[1]]], axis=0)
    return pos_list


if __name__ == '__main__':
    template_matching('img_check.bmp', 'source/CBA.jpg', (1280, 720), 0)
