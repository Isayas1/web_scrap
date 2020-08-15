'''
    Part of a list of scripts that scrape job boards.
   
    The boards being scraped are Dice, Glassdoor, Indeed, and LinkedIn

    Posititons: Software Developer, Technical Writer, QA Analyst, DBA, Help Desk, AWS Cloud Engineer
'''

# some libraries are were only used in previous versions of this script and are now effectively "deprecated"
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchWindowException
import re
import requests
import bs4
import time
import csv

# firefox webdriver
PATH = "C:\Program Files (x86)\geckodriver.exe"

#what = 'Software Engineer'
#where = 'Washington DC'

positions = ['Software Engineer', 'Data Analyst', 'Help Desk', 'UI/UX']
areas = ['Washington DC', 'Bethesda MD', 'Arlington VA', 'Silver Spring MD']

# only scraping 30% of the returned data for now
with open('indeed_scrape_data_30_percent.csv', 'w', newline = '') as file:
    field_names = ['Title','Company','Location','Link']
    job_write = csv.DictWriter(file, fieldnames=field_names)

    job_write.writeheader()
        
    for i in range(0, len(positions)):

        # obscrution to make selenium bot less detectable, read up on other ways to do this
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument("start-maximized")
        options.add_argument("disabled-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--incognito")


        # firefox unique obstruction 
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", "New User Agent")
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)

        driver = webdriver.Firefox(options=options, executable_path=PATH, firefox_profile=profile)

        what = positions[i]
        where = areas[i]

        # use bot to go to link
        driver.get('https://www.indeed.com/')

        # locate sepecific web elements using different html tags/attributes
        title_input = driver.find_element_by_id('text-input-what')
        location_input = driver.find_element_by_id('text-input-where')
        search_btn = driver.find_element_by_xpath('//*[@id="whatWhereFormId"]/div[3]/button')

        # enter info input field
        title_input.send_keys(what)
        
        # wait to mimic human actions
        time.sleep(0.6)

        for characters in range(0,30):
            time.sleep(0.15)
            location_input.send_keys(Keys.BACK_SPACE)

        # enter info input field
        location_input.send_keys(where)

        search_btn.click()

        current_page = driver.current_url

        # element showing how many jobs have been found
        results_element = driver.find_element_by_id('searchCountPages')

        results = results_element.text.split()

        temp = results[3].replace(',','')

        # 15 results are displayed per page
        limit = int(int(temp)/15)

        #====================================================================

        """with open('indeed_scrape_data_30_percent.csv', 'w', newline = '') as file:
            field_names = ['Title','Company','Location','Link']
            job_write = csv.DictWriter(file, fieldnames=field_names)
            job_write.writeheader()
            """
        
        # only 30% of the result pages are going to be traversed
        temp_limit = int(limit * 0.3)

        for page in range(0,temp_limit):
            time.sleep(2.3)
        
            job_titles = driver.find_elements_by_class_name('jobtitle.turnstileLink')
            companies = driver.find_elements_by_css_selector('span.company')            
            locations = driver.find_elements_by_class_name('location.accessible-contrast-color-location')

            time.sleep(4.3)

            for i in range(0, len(job_titles)):
                job_write.writerow({'Title': job_titles[i].text ,
                                    'Company': companies[i].text,
                                    'Location': locations[i].text,
                                    'Link': job_titles[i].get_attribute('href')
                                    })

            current_page = driver.current_url
            print(current_page)
            
            try:
                next_button = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "*//a[@aria-label='Next']")))
                next_button.click()
            except TimeoutException:
                break
            except StaleElementReferenceException:
                break
            except NoSuchWindowException:
                driver = webdriver.Firefox(options=options, executable_path=PATH, firefox_profile=profile)
                driver.get(current_page)
            except:
                time.sleep(2.3)
                # sometimes the link is blocked by a pop-up element so, just manually go to the next page
                driver.get(next_button.get_attribute('href'))

        #====================================================================
        driver.quit()

        print('\nWaiting to move on to the next job\n')
        time.sleep(6.2)    
    