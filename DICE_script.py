'''
    Part of a script that scrapes job boards.
   
    The boards being scraped are Dice, Glassdoor, Indeed, and LinkedIn

    Posititons: Software Developer, Technical Writer, QA Analyst, DBA, Help Desk, AWS Cloud Engineer
'''

# import necessary libraries
import requests
import bs4
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import re
import csv
import pandas as pd


# set a variable for the web driver path 
CPATH = "C:\Program Files (x86)\chromedriver.exe"
FPATH = "C:\Program Files (x86)\geckodriver.exe"


#driver = webdriver.Firefox(options=options, executable_path=PATH, firefox_profile=profile)

#driver.get('https://www.dice.com/')

# use a loop to perform the automated scripting action for each position
position = ['Junior Software Engineer',
            'asdf',
            'Technical Writer',
            'asdf',
            'Data Analyst',
            'asdf',
            'Junior Database Administrator',
            'asdf',
            'Junior Cloud Engineer']

locations = ['Silver Spring MD',    # 10 mi
             'Washington DC',       # 10 mi
             'Bethesda MD',         # 10 mi
             'Alexandria VA',       #  5 mi
             'Rockville MD']        # 10 mi


with open('dice_scrape_data.csv', 'w', newline='') as file:
    field_names = ['Title','Location','Company']
    job_writer = csv.DictWriter(file, fieldnames=field_names)

    for i in range(0, len(position)): # mean to be used for different positions

        #time.sleep(5)

        job_writer.writeheader()
        for j in range(0, len(locations)):

            time.sleep(3.6)

            if i % 2 > 0:

                options = webdriver.FirefoxOptions()
                options.add_argument("--headless")
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-gpu')
                options.add_argument("start-maximized")
                options.add_argument("disabled-infobars")
                options.add_argument("--disable-extensions")
                #options.add_argument("--incognito")

                profile = webdriver.FirefoxProfile()
                profile.set_preference("general.useragent.override", "New User Agent")
                profile.set_preference("browser.cache.disk.enable", False)
                profile.set_preference("browser.cache.memory.enable", False)
                profile.set_preference("browser.cache.offline.enable", False)
                profile.set_preference("network.http.use-cache", False)

                driver = webdriver.Firefox(options=options, executable_path=FPATH, firefox_profile=profile)

                driver.get('https://www.dice.com/')

                time.sleep(2.6)
                clicker = driver.find_element_by_id('submitSearch-button')

                #position_search = driver.find_element_by_css_selector('input.form-control-ng-tns-c31-0.ng-star-inserted')
                #position_search = driver.find_elements_by_css_selector('input.form-control.ng-tns-c31-0.ng-star-inserted')
                position_search = driver.find_element_by_xpath('//*[@id="searchInput-div"]/form/div/div[1]/div/dhi-new-typeahead-input/div/input')
                position_search.send_keys(position[i])

                location_search = driver.find_element_by_xpath('//*[@id="google-location-search"]')
                
                for characters in range(0,30):
                    time.sleep(0.15)
                    location_search.send_keys(Keys.BACK_SPACE)

                location_search.send_keys(locations[j])
                time.sleep(1.6)

                clicker.click()
                curr_page = driver.current_url
                time.sleep(3.5)

                #select_fr = Select(driver.find_element_by_id("pageSize_2")) 
                #select_fr.select_by_index(3)
                
                time.sleep(3.6)

                total_results = driver.find_element_by_id('totalJobCount')
                results = total_results.text
                #results = 100
                limit = int(int(results)/100)

                print('\n**********************   {0:20}   @   {1:}   **********************\n'.format(position[i],locations[j]))
                print('Jobs found: {0:10}'.format(results))

                for k in range(0, limit):
                    try:
                        element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, '»')))
                        time.sleep(2.6)
                        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        pos = driver.find_elements_by_class_name('card-title-link.bold')               
                        comp = driver.find_elements_by_xpath('//*[@id="searchDisplay-div"]/div[2]/dhi-search-cards-widget/div/dhi-search-card[1]/div/div[1]/div/div[2]/div[1]/div/a')
                        location = driver.find_element_by_xpath('//*[@id="searchResultLocation"]')


                        for i in range(0, len(pos)):
                            #time.sleep(0.5)
                            #print(job.text)
                            job_writer.writerow({'Title':pos[i].text,
                                                'Location': location[i].text,
                                                'Company':comp[i].text
                                                })
                                
                        
                        time.sleep(2.5)
                        time.sleep(1.5)
                        print('\n                   i: {} @ j: {}                   '.format(i,j))
                        print('\n==================================================\n')
                        element.click()

                    except:
                        driver.quit()

                    #time.sleep(randint(3,8))
                    
                    # go to home here
                    #driver.get('https://www.dice.com/')
                #driver.get('https://www.dice.com/')
                driver.delete_all_cookies()
                driver.quit()
            elif i % 2 == 0:
                
                options2 = webdriver.FirefoxOptions()
                options2.add_argument("--headless")
                options2.add_argument('--no-sandbox')
                options2.add_argument('--disable-gpu')
                options2.add_argument("start-maximized")
                options2.add_argument("disabled-infobars")
                options2.add_argument("--disable-extensions")
                #options.add_argument("--incognito")

                profile2 = webdriver.FirefoxProfile()
                profile2.set_preference("general.useragent.override", "New User Agent")
                profile2.set_preference("browser.cache.disk.enable", False)
                profile2.set_preference("browser.cache.memory.enable", False)
                profile2.set_preference("browser.cache.offline.enable", False)
                profile2.set_preference("network.http.use-cache", False)

                driver = webdriver.Firefox(options=options2, executable_path=FPATH, firefox_profile=profile2)

                driver.get('https://www.dice.com/')

                time.sleep(2.6)
                clicker = driver.find_element_by_id('submitSearch-button')

                #position_search = driver.find_element_by_css_selector('input.form-control-ng-tns-c31-0.ng-star-inserted')
                #position_search = driver.find_elements_by_css_selector('input.form-control.ng-tns-c31-0.ng-star-inserted')
                position_search = driver.find_element_by_xpath('//*[@id="searchInput-div"]/form/div/div[1]/div/dhi-new-typeahead-input/div/input')
                position_search.send_keys(position[i])

                location_search = driver.find_element_by_xpath('//*[@id="google-location-search"]')
                
                for characters in range(0,30):
                    time.sleep(0.15)
                    location_search.send_keys(Keys.BACK_SPACE)

                location_search.send_keys(locations[j])
                time.sleep(1.6)

                clicker.click()
                curr_page = driver.current_url
                time.sleep(3.5)

                #select_fr = Select(driver.find_element_by_id("pageSize_2")) 
                #select_fr.select_by_index(3)
                
                time.sleep(3.6)

                total_results = driver.find_element_by_id('totalJobCount')
                results = total_results.text
                #results = 100
                limit = int(int(results)/100)

                print('\n**********************   {0:20}   @   {1:}   **********************\n'.format(position[i],locations[j]))
                print('Jobs found: {0:10}'.format(results))

                for k in range(0, limit):
                    try:
                        element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, '»')))
                        time.sleep(2.6)
                        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        pos = driver.find_elements_by_class_name('card-title-link.bold')               
                        comp = driver.find_elements_by_xpath('//*[@id="searchDisplay-div"]/div[2]/dhi-search-cards-widget/div/dhi-search-card[1]/div/div[1]/div/div[2]/div[1]/div/a')
                        location = driver.find_element_by_xpath('//*[@id="searchResultLocation"]')


                        for i in range(0, len(pos)):
                            #time.sleep(0.5)
                            #print(job.text)
                            job_writer.writerow({'Title':pos[i].text,
                                                'Location': location[i].text,
                                                'Company':comp[i].text
                                                })
                                
                        
                        time.sleep(3.2)
                        time.sleep(1.5)
                        print('\n                   i: {} @ j: {}                   '.format(i,j))
                        print('\n==================================================\n')
                        element.click()

                    except:
                        driver.quit()

                    #time.sleep(randint(3,8))
                    
                    # go to home here
                    #driver.get('https://www.dice.com/')
                #driver.get('https://www.dice.com/')
                driver.delete_all_cookies()
                driver.quit()