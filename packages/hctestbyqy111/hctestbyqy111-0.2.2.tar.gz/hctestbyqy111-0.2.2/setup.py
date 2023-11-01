from setuptools import setup, find_packages

setup(
    name='hctestbyqy111',
    version='0.2.2',
    packages=find_packages(where='hctestbyqy111'),
    install_requires=[
        "selenium",
        "pyautogui",
        "opencv_python",
        "pytesseract",
        "allure-pytest"
    ],
)
