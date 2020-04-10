from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
# options.add_argument('--headless')



## this path may depend on what you're using and where
driver = webdriver.Chrome('/usr/local/bin/chromedriver', options = options)
#driver = webdriver.Chrome(ChromeDriverManager().install(), options=options) #part of a possible fix


## modifying the query here
url = 'https://www.nseindia.com'


driver.get(url)

print('Page loaded')

# //product-template/div/div[4]/div[3]/div/div[1]/h4/span[2]/span
# //product-template/div/div[4]/div[1]/a

elementname = driver.find_element(By.XPATH, '/html/body/div[7]/div[1]/section[1]/div/div/div/div/div[1]/div[2]/div/div/nav/div/div/a[1]/div/p[2]')

time.sleep(5)
element = driver.find_elements_by_xpath('/html/body/div[7]/div[1]/section[1]/div/div/div/div/div[1]/div[2]/div/div/nav/div/div/a[1]/div/p[2]')

print(element[0].text)
