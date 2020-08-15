'''
    Create a script that would traverse through the BAH careers site and find job postings based on location
'''

import requests
import bs4
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

PATH = "C:\Program Files (x86)\geckodriver.exe"

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument("start-maximized")
options.add_argument("disabled-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--incognito")

profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", "New User Agent")
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False)

driver = webdriver.Firefox(options=options, executable_path=PATH, firefox_profile=profile)

query = 'Washington DC'#input("Enter location: ")

time.sleep(6)

driver.get('https://careers.boozallen.com/jobs/search')

# https://careers.boozallen.com/jobs/search/?jobOffset= x

#curr_page = driver.current_url

search = driver.find_element_by_id('tpt_search')
search.send_keys(query)

#driver.delete_all_cookies()

search.send_keys(Keys.RETURN)

curr_page = driver.current_url

res = requests.get(curr_page)
soup = bs4.BeautifulSoup(res.text, 'lxml')

jobs = []
locations = []

#span.pagination__legend
results_box1 = driver.find_elements_by_xpath('//*[@id="main"]/div/div/section/div[2]/article/div/div/span')  
results_box2 = driver.find_elements_by_class_name('pagination__legend')
results_box3 = driver.find_elements_by_css_selector('.pagination__legend')

#time.sleep(4)

#print(type(results_box2[0]))

print('1: ',results_box1[0].get_attribute('innerHTML'))
#print('2: ',results_box2[0].get_attribute('innerHTML'))
#print('3: ',results_box3[0].get_attribute('innerHTML'))

results = re.findall(r'\d{3}', results_box1[0].get_attribute("innerHTML"))
#
print('results is ',results,' ',type(results))
# resutlt being is 261 or 263

limit = int(int(results[0]) / 19)

#links = driver.find_elements_by_class_name('link')
#print(links[0].get_attribute('href'))
#print(links[0].text)

links = driver.find_elements_by_class_name('link')

#print(' successful')


#element = WebDriverWait(driver, 40).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'link')))
#links = WebDriverWait(driver, 60).until(EC.presence_of_elements_located((By.CLASS_NAME, 'link')))

print('Success. Going to line 94')

for i in range(0,limit):
    #print(i)
    links = driver.find_elements_by_class_name('link')

    clicker = driver.find_element_by_partial_link_text('Next >>')

    for i in range(0, len(links)-1):
    #if 'accommodations' in i.text:
    #    pass
    #elif 'accommodations' not in i.text:
        try: 
            print(links[i].text)
        except:
            pass
#print(links[0].get_attribute('href'))

    #driver.delete_all_cookies()

    

    """for item in soup.select('div > article > div > table > tbody > tr > td'):
        #print(item.getText().split('\n'))
        temp = item.getText().split('\n')
        
        if len(temp) <= 1:
            #print('==============')
            pos = temp[0].strip()
            jobs.append(pos)
        else:
            loc = temp[1].strip()
            #print(loc)
            locations.append(loc)

    for j in range(0, len(jobs)):
        #if j % 2 > 0 :
        temp = str(jobs[j])
        if 'senior' in temp.lower(): 
            pass
        elif 'lead' in temp.lower():
            pass
        elif 'mid' in temp.lower():
            pass
        else:
            if query in locations[j].lower():
                print('\n {0:35} \t @ \t {1}\n'.format(jobs[j],locations[j]))
    """
    time.sleep(2.3)


    
clicker.click()

print('======================================================================================================================')


#time.sleep(2.3)
driver.quit()