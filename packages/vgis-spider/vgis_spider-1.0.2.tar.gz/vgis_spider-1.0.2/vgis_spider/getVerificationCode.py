#!/usr/bin/python3.9
# -*- coding: utf-8 -*-
from PIL import Image
import pytesseract


# https://www.jb51.net/article/183990.htm
# 针对没有干扰的图片文字能识别处理
# 但是不能识别有干扰的图片
def read_ch_text(text_path):
    """
    传入文本(jpg、png)的绝对路径,读取文本
    :param text_path:
    :return: 文本内容
    """
    # 验证码图片转字符串
    im = Image.open(text_path)
    # 转化为8bit的黑白图片
    imgry = im.convert('L')
    # 二值化，采用阈值分割算法，threshold为分割点
    threshold = 140
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)
    out = imgry.point(table, '1')
    # 识别文本，lang参数改为chi_sim，其他代码与上面的读取验证码代码一致。
    text = pytesseract.image_to_string(out, lang="chi_sim", config='--psm 6')
    return text


def read_en_text(text_path):
    """
    传入文本(jpg、png)的绝对路径,读取文本
    :param text_path:
    :return: 文本内容
    """
    # 验证码图片转字符串
    im = Image.open(text_path)
    # 转化为8bit的黑白图片
    imgry = im.convert('L')
    # 二值化，采用阈值分割算法，threshold为分割点
    threshold = 140
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)
    out = imgry.point(table, '1')
    # 识别文本
    text = pytesseract.image_to_string(out, lang="eng", config='--psm 6')
    return text


if __name__ == '__main__':
    print("图片1：" + read_en_text("E:\\desktop\\response.jpeg"))
    print("图片2：" + read_en_text("E:\\desktop\\wpvvgzigca.png"))
    print("图片3：" + read_en_text("E:\\desktop\\202004020914468.png"))
    print("图片4：" + read_ch_text("E:\\desktop\\2020040209144612.png"))
    print("图片5：" + read_ch_text("E:\\desktop\\2021-12-28_175243.png"))
