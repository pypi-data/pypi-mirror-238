from setuptools import setup, find_packages

setup(
    name='hctestbyqy111',
    version='0.2.3',
    packages=find_packages(),
    install_requires=[
        "selenium",
        "pyautogui",
        "opencv_python",
        "pytesseract",
        "allure-pytest"
    ],
)
