from setuptools import setup, find_packages

setup(
    name='hctestbyqy',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        "selenium",
        "pyautogui",
        "opencv_python",
        "pytesseract",
        "allure-pytest"
    ],
)
