import time
import pyautogui  # pip install pyautogui -i https://mirrors.aliyun.com/pypi/simple/


def file_upload(driver, file_locatio=1):
    """
    :param driver: 浏览器对象
    :param file_locatio: mac系统想要上传的第几个文件，从左上角开始
    :return: 文件上传操作
    """
    driver.maximize_window()
    # 点击"文稿"
    pyautogui.moveTo(2130, 507)
    time.sleep(2)
    pyautogui.click()

    # 点击"图片"
    pyautogui.moveTo(2797, 357)
    time.sleep(2)
    pyautogui.click()

    # 点击"打开"(因为mac系统有权限问题，可能双击不成功，所以采取最原始的方式)
    pyautogui.moveTo(2823, 648)
    pyautogui.click()

    # 判断传入页面第几个文件，从左到右
    x, y = 2291, 353
    try:
        if file_locatio == 0:
            pass
        elif file_locatio == 1:
            x += 125
        elif file_locatio == 2:
            x += 125 * 2
        elif file_locatio == 3:
            x += 125 * 3
        elif file_locatio == 4:
            x += 125 * 4
        elif file_locatio == 5:
            x += 125 * 5
        elif file_locatio == 6:
            y += 130
        elif file_locatio == 7:
            x += 125
            y += 130
        elif file_locatio == 8:
            x += 125 * 2
            y += 130
        elif file_locatio == 9:
            x += 125 * 3
            y += 130
        elif file_locatio == 10:
            x += 125 * 4
            y += 130
        else:
            print("输入有误!")
    except Exception as e:
        print("找不到该图片！")

    # 选择上传的文件
    pyautogui.moveTo(x, y)
    pyautogui.click()

    # 点击"打开"(因为mac系统有权限问题，可能双击不成功，所以采取最原始的方式)
    pyautogui.moveTo(2823, 648)
    pyautogui.click()
