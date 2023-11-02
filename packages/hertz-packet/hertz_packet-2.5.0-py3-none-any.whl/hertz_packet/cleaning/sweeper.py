# -*- coding: utf-8 -*-

"""
@Project : hertz_packet 
@File    : sweeper.py
@Date    : 2023/11/2 14:46:56
@Author  : zhchen
@Desc    : 
"""
import datetime
import os


def clear_old_file(path, expires=30 * 24 * 60 * 60):
    """清除历史文件, 默认30天"""
    # 获取当前时间
    now = datetime.datetime.now()

    # 遍历目录下的所有文件
    for root, dirs, files in os.walk(path):
        for file in files:
            # 获取文件的最后修改时间
            file_path = os.path.join(root, file)
            modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

            # 计算文件的修改时间与当前时间的差值
            time_diff = now - modified_time

            # 如果差值大于30天，则删除文件
            if time_diff.total_seconds() > expires:
                os.remove(file_path)

    # 获取目录下所有文件夹
    folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    for _folder in folders:
        folder_path = os.path.join(path, _folder)
        # 如果文件夹为空，则删除该文件夹
        if not os.listdir(folder_path):
            os.rmdir(folder_path)


if __name__ == '__main__':
    _path = r'G:\Download\adb-fastboot'
    clear_old_file(_path)
