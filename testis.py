import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains

os.environ['PATH'] += 'C:\\Users\\PC\\Desktop\\python'
driver = webdriver.Chrome()
driver.get('https://orteil.dashnet.org/cookieclicker/')
driver.implicitly_wait(15)
lang_button = driver.find_element(By.ID, value ='langSelect-EN')
lang_button.click()

nogomet = driver.find_element(By.ID, value='bigCookie')
cookie_count = driver.find_element(by=By.ID, value="cookies").text

actions = ActionChains(driver)
actions.click(nogomet)

for i in range(80):
	actions.perform()
	count = cookie_count
	print(count)




