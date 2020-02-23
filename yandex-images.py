from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
import time
from urllib.request import urlretrieve
from urllib.error import HTTPError
from urllib.error import URLError
import os
import datetime

def get_extension_from_link(link, default='jpg'):
    splits = str(link).split('.')
    if len(splits) == 0:
        return default
    ext = splits[-1].lower()
    if ext == 'jpg' or ext == 'jpeg' or ext == 'jpe':
        return 'jpg'
    elif ext == 'gif':
        return 'gif'
    elif ext == 'png':
        return 'png'
    elif ext == 'ico':
        return 'ico'
    elif ext == 'jfif':
        return 'jfif'
    elif ext == 'bmp':
        return 'bmp'
    elif ext == 'svg':
        return 'svg'
    elif ext == 'webp':
        return 'webp'
    else:
        return default
        
print('Just enter a keywords:')
keyword = input()
save_urls = time.strftime("%Y%m%d-%H%M%S") + ".txt"
print('Enter the number of files (e.g. 300):')
num_files = int(input())


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


with webdriver.Chrome() as driver:
    driver.get("https://yandex.ru/images/")
    driver.implicitly_wait(10) # seconds
    time.sleep(10)
    wait = WebDriverWait(driver, 10)
    WebDriverWait(driver, 10)
    driver.find_element_by_class_name("input__control").send_keys(keyword + Keys.RETURN)
    driver.find_element_by_class_name('serp-item__preview').click()
   
    file1 = open(save_urls, "a", encoding="utf-8") # open 2 write
    
    for links in range(0, num_files):
        WebDriverWait(driver, 10)
        link= driver.find_element_by_class_name('MMViewerButtons-OpenImageSizes').find_element_by_css_selector('a').get_attribute("href")

        
        
       	timestr = time.strftime("%Y%m%d-%H%M%S")
       	savefilename = "./" + savedir + "/img_" + timestr + "." + get_extension_from_link(link)
        try:
            urlretrieve(link, savefilename)
        except HTTPError:
            print("\n Forbidden\n")
        except URLError:
            print("\nURLError\n")
        except:
            print("OthersError")
        else:
            file1.write(link + '\n')
            print(links ,": ", link)
            print("\n" , savefilename , " image file saved")
       	time.sleep(5)
        
        
        driver.find_elements_by_class_name('CircleButton-Icon')[-1].click() # next image
        time.sleep(1)
    file1.close()
    driver.close()
        
    
