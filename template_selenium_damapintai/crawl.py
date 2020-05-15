from dama import indentify
from selenium import webdriver
import requests
import time
#实例化driver
driver = webdriver.Chrome()
driver.get("https://2046pro.com/forum.php")

#实例化session
session = requests.session()
cookies = driver.get_cookies()
cookies = {i["name"]:i["value"] for i in cookies}


driver.find_element_by_xpath("//button[@tabindex='904']").click()
driver.switch_to_default_content()
driver.find_element_by_xpath("//div/table/tbody/tr[2]/td[2]/div[1]/div[1]/form/div/div[1]//input")
#a = driver.find_element_by_xpath("//div/table/tbody/tr[2]/td[2]/div[1]/div[1]/form/div/div[1]//input").send_keys("zimu123")
#driver.find_element_by_xpath("//div/table/tbody/tr[2]/td[2]/div[1]/div[1]/form/div/div[2]//input").send_keys("140302lhp")
#cap = driver.find_element_by_xpath("//img[contains(@width,'100')]").get_attribute("src")
'''a = driver.find_element_by_xpath('//*[@id="kw"]').send_keys("python")
driver.find_element_by_xpath('//*[@id="su"]').click()'''
time.sleep(3)
driver.quit()
#print(cap)
