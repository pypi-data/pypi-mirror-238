import cv2 as cv  # pip install opencv_python -i https://mirrors.aliyun.com/pypi/simple/

# 这两个只要安装：pip install pytesseract -i https://mirrors.aliyun.com/pypi/simple/
import pytesseract
from PIL import Image


def image_recognition(element_png_file):
    """
    :param element_png_file: 验证码截图存放的截图路径
    :return: 识别到的验证码
    """
    # 原图
    master_drawing = cv.imread(element_png_file)

    # 对图片进行去噪处理
    denoised_picture = cv.pyrMeanShiftFiltering(master_drawing, 10, 100)

    # 对图片进行灰度处理
    grayscale_picture = cv.cvtColor(denoised_picture, cv.COLOR_BGR2GRAY)

    # 对图片进行二值化处理
    threshold_value, binary_picture = cv.threshold(grayscale_picture, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    cv.imwrite("./binary_picture.png", binary_picture)

    # 使用PIL打开图像转化为图像对象，并使用pytesseract进行图像识别
    binary_picture = "binary_picture.png"
    captcha_picture = Image.open(binary_picture)
    verification_code = pytesseract.image_to_string(captcha_picture)
    print("识别到的验证码为: ", verification_code)
    return verification_code
