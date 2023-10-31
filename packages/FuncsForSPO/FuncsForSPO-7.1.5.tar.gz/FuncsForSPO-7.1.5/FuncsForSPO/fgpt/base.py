from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager
from FuncsForSPO.fpython.functions_for_py import *
from FuncsForSPO.fselenium.functions_selenium import *
from FuncsForSPO.fwinotify.fwinotify import *
from FuncsForSPO.fregex.functions_re import *
from FuncsForSPO.fpdf.focr.orc import *
from FuncsForSPO.fpysimplegui.functions_for_sg import *
import pandas as pd
import re
import json
import os

class BotMain:    
    def __init__(self, headless) -> None:
        # --- CHROME OPTIONS --- #
        self._options = ChromeOptions()
        
        if headless == True:
            self._options.add_argument('--headless')
            self._options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
            self._options.add_experimental_option('useAutomationExtension', False)
            self._options.add_argument("--window-size=1920,1080")
            self._options.add_argument('--kiosk-printing')
        else:
            self._options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
            self._options.add_experimental_option('useAutomationExtension', False)
            self._options.add_argument("--window-size=1920,1080")
            self._options.add_argument('--kiosk-printing')

        
        self.__service = Service(ChromeDriverManager().install())
        
        # create DRIVER
        self.DRIVER = Chrome(service=self.__service, options=self._options)

        self.WDW3 = WebDriverWait(self.DRIVER, timeout=3)
        self.WDW5 = WebDriverWait(self.DRIVER, timeout=5)
        self.WDW7 = WebDriverWait(self.DRIVER, timeout=7)
        self.WDW10 = WebDriverWait(self.DRIVER, timeout=10)
        self.WDW30 = WebDriverWait(self.DRIVER, timeout=30)
        self.WDW130 = WebDriverWait(self.DRIVER, timeout=130)
        self.WDW330 = WebDriverWait(self.DRIVER, timeout=330)
        self.WDW = self.WDW7

        self.DRIVER.maximize_window()
        return self.DRIVER
