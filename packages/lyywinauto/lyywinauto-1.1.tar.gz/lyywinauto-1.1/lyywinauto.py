# -*- coding: utf-8 -*-

#pyinstaller --noconfirm -D -w -n win_on_top  --distpath  "D:/Soft/_lyytools" D:\UserData\Documents\BaiduSyncdisk\2024-test\testwin32gui.py

import pyautogui
import sys

# 设置标题的关键词
title_keyword = "交易师"


def bring_window_to_front(title_keyword):
    """
    根据关键字查找窗口并置顶。
    优点是不用完整标题也不用开始文字，也不用考虑大小写。
    缺点是：用到pyautogui库，且文件较大接近100MB。
    
    """
    try:
        # 获取当前所有窗口的标题
        windows = pyautogui.getAllTitles()

        # 遍历窗口标题，查找以指定关键词开头的窗口
        for window_title in windows:
            print(window_title)
            if title_keyword.lower() in window_title.lower():
                print("# 找到匹配的窗口，激活并置顶", window_title)
                pyautogui.getWindowsWithTitle(window_title)[0].activate()

                break
    except Exception as e:
        print(f"出现错误：{e}")


if len(sys.argv) == 1:
    print("请输入窗口标题关键词,默认为交易师")
    bring_window_to_front("交易师")
elif len(sys.argv) > 1:
    if sys.argv[1] == "/?" or sys.argv[1] == "--help":
        print("请输入窗口标题关键词,默认为交易师。可输入多个参数，会依次置顶")
        sys.exit()
    print(f"有{ len(sys.argv) }个参数")
    for argv in sys.argv[1:]:
        bring_window_to_front(argv)
