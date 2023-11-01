from setuptools import setup, find_packages

setup(
    name='huaceqiye',
    version='0.1.0',
    packages=find_packages(where='src'),
    install_requires=[
        "selenium",
        "pyautogui",
        "opencv_python",
        "pytesseract",
        "allure-pytest"
    ],
)
