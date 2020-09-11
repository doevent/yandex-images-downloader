from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver import ActionChains
import time

from urllib.request import urlretrieve
from urllib.parse import urlparse

import os
import datetime


        
print('Just enter a keywords:')
keyword = input()  # считываем строку и кладём её в переменную name
print('Enter the number of files (e.g. 300):')
num_files = int(input(">> "))

save_urls = time.strftime("%Y%m%d-%H%M%S") + ".txt"

months={
	1:"JAN",
	2:"FEB",
	3:"MAR",
	4:"APR",
	5:"MAY",
	6:"JUN",
	7:"JUL",
	8:"AUG",
	9:"SEP",
	10:"OCT",
	11:"NOV",
	12:"DEC"
	}

now = datetime.datetime.now()
ls_day = now.day
if ls_day < 10: 
	str_day = "0" + str(ls_day)
else:
	str_day = str(ls_day)
savedir = str_day + "-" + str(months.get(now.month))
if not os.path.exists(savedir):
	os.makedirs(savedir)
	print ("Created directory: " , savedir)
print (savedir)


options = webdriver.ChromeOptions() 
options.add_argument("disable-infobars")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

with webdriver.Chrome(options=options) as driver:
        # no head browser
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
        """
        })

    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browser1"}})

    
    driver.get("https://yandex.ru/images/")
    driver.implicitly_wait(10) # seconds
    time.sleep(10)

    driver.find_element_by_class_name("input__control").send_keys(keyword + Keys.RETURN)
    time.sleep(4)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(10)
    driver.find_element_by_class_name('serp-item__link').click()
    time.sleep(10)
    file1 = open(f'{savedir}/{save_urls}', "a", encoding="utf-8") # open 2 write
    
    for links in range(0, num_files):
        tpt = driver.find_element_by_class_name('MMButton-RightIcon').click()
        time.sleep(4)
        link = driver.find_element_by_css_selector('[class="MMViewerButtons-ImageSizesListItem"]').get_attribute("href")
        print(link)
        try:
            # print()
            filept = f'{savedir}/{os.path.basename(urlparse(link).path)}'
            urlretrieve(link, filept)
            file1.write(link + '\n')
        except Exception as e:
            print(e)
        else:
            file1.write(link + '\n')
            print(links ," >>>  ", link)
            print(links ," >>>  ",filept, " image file saved\n")
       	time.sleep(5)
        
        
        driver.find_elements_by_class_name('CircleButton-Icon')[-1].click() # next image
        time.sleep(1)
    file1.close()
    driver.close()
        
    
