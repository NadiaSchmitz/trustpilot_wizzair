from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
#from selenium.webdriver import Chrome
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.support.ui import WebDriverWait as wait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import NoSuchElementException
import requests
#import re
import time

# URL
url = 'https://de.trustpilot.com/review/www.wizzair.com'

# Response
url_response = requests.get(url)



browser = webdriver.Chrome()
browser.get(url)
browser.maximize_window()

try:
    cookies_button = browser.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
    cookies_button.click()
    time.sleep(3)
except:
    print("There is no cookies_button")

try:
    filter_button = browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/div/main/div/div[4]/section/div[2]/div[3]/button')
    filter_button.click()
    time.sleep(3)
except:
    print("There is no filter_button")

try:
    lang_input = browser.find_element(By.XPATH, '//*[@id="language-option-all"]')
    lang_input.click()
    time.sleep(3)
except:
    print("There is no lang_input")

try:
    filter_confirm_button = browser.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[3]/div/button[2]')
    filter_confirm_button.click()
    time.sleep(3)
except:
    print("There is no filter_confirm_button")

# URL aktuell ermitteln
url_actual = browser.current_url

# Response
url_response_actual = requests.get(url_actual)

# Soup erstellen
url_soup = BeautifulSoup(url_response_actual.text, "lxml")

# Anzahl der Seiten ermitteln
page_number = int(url_soup.find('a', attrs={'name': 'pagination-button-last'}).find('span').text)
print(page_number)

reviews_data = []

try:
    for page in range(2, (page_number + 1)):
        url = url_actual
        url_response_actual = requests.get(url)
        time.sleep(3)
        url_soup = BeautifulSoup(url_response_actual.text, "lxml")
        reviews = url_soup.findAll('div', class_='styles_cardWrapper__LcCPA')
        print(page)
        for review in reviews:
            country = review.find('div', 'typography_body-m__xgxZ_').find('span').text
            rating = int(review.find('div', class_='styles_reviewHeader__iU9Px').attrs['data-service-review-rating'])
            date_review = review.find('time').attrs['datetime'][0:10]
            review_title = review.find('h2').text
            review_body = review.find('p', 'typography_body-l__KUYFJ').text
            reviews_data.append([country, rating, date_review, review_title, review_body])
        url = url + '&page=' + str(page)
except:
    print("Parsing was not successful")

header_csv = ['country', 'rating', 'date_review', 'review_title', 'review_body']

df = pd.DataFrame(reviews_data, columns=header_csv)
df.to_csv('/Users/DAA/Desktop/Daten/wizzair/wizzair.csv', sep=';')

print("Parsing was successful. Data saved and available C:/Users/DAA/Desktop/Daten/wizzair/wizzair.csv")