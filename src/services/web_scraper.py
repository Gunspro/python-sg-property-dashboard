import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

from sqlalchemy.orm import Session
from src.repositories.PropertyRepository import PropertyRepository
from src.db.database import SessionLocal
from src.model.property import PropertyData

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def scrape_data():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://www.99.co/singapore/sale?main_category=hdb")
    page = driver.page_source
    my_html = BeautifulSoup(page, "html.parser")
    lists_of_items = my_html.findAll('div', '_19sj7')
    property_list = []
    pagenum = 0
    cnt = 0
    while True:
        for items in lists_of_items:   
            list_items = items.find_all('div', '_1zvu5') #update if anti-webscraper is in place
            pagenum += 1

            for item in list_items:
                cnt += 1 
                property_info = {}

                price_element = item.find('li', {'class': 'JlU_W'}) #update if anti-webscraper is in place
                year_element = item.find('li', {'itemprop': 'yearbuilt'}) #update if anti-webscraper is in place
                block_address_element = item.find('h2', {'itemprop': 'name'}) #update if anti-webscraper is in place
                room_element = item.find('li', {'class': '_1LPAx'}) #update if anti-webscraper is in place

                property_info['id'] = cnt
                property_info['price'] = price_element.text if price_element else "N/A"
                property_info['yearbuilt'] = year_element.text if year_element else "N/A"
                property_info['block_and_address'] = block_address_element.text if block_address_element else "N/A"
                property_info['number_of_rooms'] = room_element.text if room_element else "N/A"

                property_list.append(property_info)

            try:
                next_button = driver.find_element(By.XPATH, "//a[text()='Next']")
                if next_button.is_enabled():
                    next_button.click()
                    print('Page:', pagenum)
            except:
                break
        if pagenum >= 2:  # Break the loop after scraping the 2nd page
            break

        return property_list

def store_property_data(data: PropertyData):
    db = SessionLocal()
    property_data = PropertyRepository(db)
    property_data.truncate_properties()
    property_data.create_properties(data)
    db.close()

    return {"message": "Property data stored successfully"}