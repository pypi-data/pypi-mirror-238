#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/16 9:40
# @Author  : JaySun
# @Site    : 
# @File    : tools.py.py
# @Software: PyCharm

import yaml
import datetime
import os.path
import requests


def get_now_time():
    return datetime.datetime.now()


def get_now_date_time_str():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def format_list():
    # 代码格式化：Ctrl+Alt+L
    my_list = ["a", "b", "c", "d"]
    print(my_list)


def try_except():
    # 快速异常捕获：Ctrl+Alt+T
    try:
        x = 1
    except:
        pass


def annotation():
    # 快速注释/取消注释：Ctrl+/
    a = 1
    b = 2
    c = 3


def indent():
    # 向右缩进Tab
    # 向左缩进Shift+Tab
    try:
        a = 1
    except:
        pass


def insert():
    # 在上方插入新行：Ctrl+Alt+Enter
    # 在下发插入新行：Shift+Enter

    a = 1
    b = 2


def home():
    # 光标定位到代码开头home键
    ...


def end():
    # 光标定位到代码结尾end键
    ...


def get_project_path():
    """
    获取项目绝对路径
    :return:
    """
    # 获取当前路径
    path = os.path.realpath(__file__)
    # # 获取当前路径的上一级
    # up_path = os.path.dirname(os.path.realpath(__file__))
    # # 获取当前路径的上上一级
    upup_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    # 获取当前路径的上上上一级
    # upupup_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    # print(path)
    # print(up_path)
    # print(upup_path)
    # print(upupup_path)
    # project_name = "pytest_framework"
    # file_path = os.path.dirname(__file__)
    # return file_path[:file_path.find(project_name)+len(project_name)]
    return upup_path


def sep(path, add_sep_before=False, add_sep_after=False):
    full_path = os.sep.join(path)
    if add_sep_before:
        full_path = os.sep + full_path
    if add_sep_after:
        full_path = full_path + os.sep
    return full_path


def get_img_path(img_name):
    """
    获取商品图片的路径
    @param img_name:
    @return:
    """
    img_dir_path = get_project_path() + sep(["img", img_name], add_sep_before=True)
    return img_dir_path


def get_daily_wallpaper():
    """
    从bing获取每日壁纸
    @return:
    """
    daily_wallpaper_url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=10&mkt=zh-CN"
    try:
        res = requests.get(url=daily_wallpaper_url)
        wallpaper_url = "https://cn.bing.com" + res.json()["images"][0]["url"][:-7]
        print(res.text)
    except Exception as e:
        print(e)
        wallpaper_url = ""
    return wallpaper_url


def update_date_variable():
    # 生成当前日期
    yaml_file_path = get_project_path() + sep(["config", "environment.yaml"], add_sep_before=True)
    current_date = datetime.date.today()
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    current_day = datetime.datetime.now().day
    current_time = datetime.datetime.now()
    captcha = int('37' + current_date.strftime("%m%d"))

    # 将日期写入YAML文件
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)


    data['variables']['current_date'] = current_date
    data['variables']['current_day'] = current_day
    data['variables']['current_year'] = current_year
    data['variables']['current_month'] = current_month
    data['variables']['current_time'] = current_time
    data['user']['jaysun']['captcha'] = captcha

 # 写入更新后的 YAML 文件
    with open(yaml_file_path, 'w') as file:
        yaml.dump(data, file)

if __name__ == '__main__':
    # print(get_now_time())
    print(get_project_path())
    # sep(["config", "environment.yaml"], add_sep_before=True)
    # print(get_img_path("商品图片一.jpg"))
    # print(get_daily_wallpaper())
    print(get_project_path() + sep(["driver", "chromedriver.exe"], add_sep_before=True))
