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

positions = ['Software Engineer', 'Data Analyst', 'Help Desk', 'UI/UX', 'Junior DBA', 'AWS Cloud Engineer']
areas = ['Washington DC', 'Bethesda MD', 'Arlington VA', 'Silver Spring MD']
job_types = ['SE','DA','HD','UX','DBA', 'CE']

# only scraping 30% of the returned data for now
with open('indeed_scrape_data_50_percent.csv', 'w', newline = '') as file:
    field_names = ['Title','Company','Location','Type','Link']
    job_write = csv.DictWriter(file, fieldnames=field_names)

    job_write.writeheader()
        
    # job title would be used for the outer loop
    # look for a job in the locations proided within the areas list
    for i in range(0, len(positions)):
        
        what = positions[i]
        jt = job_types[i]

        for j in range(0, len(areas)):
            
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

            #where = areas[i]
            where = areas[j]

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
                time.sleep(0.08)
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
            
            # only 50% of the result pages are going to be traversed
            # it's IMPORTANT to note that the higher the percentage, the more likely it's to be detected
            # (in which case, specific changes need to be made to make the bot mimic human-like actions)
            temp_limit = int(limit * 0.50)

            for page in range(0,temp_limit):
                time.sleep(1.2)
            
                job_titles = driver.find_elements_by_class_name('jobtitle.turnstileLink')
                companies = driver.find_elements_by_css_selector('span.company')            
                locations = driver.find_elements_by_class_name('location.accessible-contrast-color-location')

                time.sleep(1.8)

                for i in range(0, len(job_titles)):
                    try:
                        job_write.writerow({'Title': job_titles[i].text ,
                                            'Company': companies[i].text,
                                            'Type': jt,
                                            'Location': locations[i].text,
                                            'Link': job_titles[i].get_attribute('href')
                                            })
                    except StaleElementReferenceException:
                        continue
                    except:
                        break

                current_page = driver.current_url
                # just to show the script's progression on the terminal
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
                    time.sleep(2.25)
                    # sometimes the link is blocked by a pop-up element so, just manually go to the next page
                    # achor links have the link to the next page in the href attribute
                    driver.get(next_button.get_attribute('href'))

            #====================================================================
            driver.quit()

            print('\nWaiting to move on to the next position and/or location\n')
            time.sleep(1.8)    
        