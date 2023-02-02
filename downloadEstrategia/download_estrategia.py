from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.FirefoxOptions
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", "/home/leandro/Videos/Banco de dados - conceitos básicos")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

driver = webdriver.Firefox(firefox_profile=profile,executable_path='.\geckodriver')

