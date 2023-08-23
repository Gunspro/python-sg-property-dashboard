import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import random
import time

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


def generate_listing_id():
    random_number = random.randint(100000, 999999)  # Generating a random 6-digit number
    listing_id = f"L{random_number}"
    return listing_id

def process_property_list(prop_list):
    block_address = {}

    filtered_prop_list = []

    for info in prop_list:
        block_and_address = info['block_and_address']
        block_and_address = block_and_address.strip()

        price = info['price']
        price = price.strip()

        if block_and_address not in block_address:
            
            filtered_prop_list.append(info)
            block_address[block_and_address] = True
        else:
            if price != "Make an offer":
                for item in filtered_prop_list:
                    if item["block_and_address"] == True:
                        item['price'] = price
                        break
            else:
                for item in filtered_prop_list:
                    if item["block_and_address"] == True:
                        if item['price'] < price:
                            item['price'] = price
                            break
                        break
    
    return filtered_prop_list

def scrape_data():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://www.99.co/singapore/sale?main_category=hdb")
    property_list = []
    pagenum = 0
    cnt = 0
    while True:
        page = driver.page_source
        my_html = BeautifulSoup(page, "html.parser")
        # lists_of_items = my_html.findAll('div', '_19sj7')
        list_items = my_html.findAll('div', '_1zvu5') #update if anti-webscraper is in place
        
        for item in list_items:
            random_listing_id = generate_listing_id()
            property_info = {}

            price_element = item.find('li', {'class': 'JlU_W'}) #update if anti-webscraper is in place
            year_element = item.find('li', {'itemprop': 'yearbuilt'}) #update if anti-webscraper is in place
            block_address_element = item.find('h2', {'itemprop': 'name'}) #update if anti-webscraper is in place
            room_element = item.find('li', {'class': '_1LPAx'}) #update if anti-webscraper is in place
            floor_element = item.find('li', {'itemprop': 'floorSize'})

            property_info['id'] = random_listing_id
            property_info['timestamp'] = datetime.datetime.now()
            property_info['price'] = price_element.text if price_element else "N/A"
            property_info['yearbuilt'] = year_element.text if year_element else 2018
            property_info['block_and_address'] = block_address_element.text if block_address_element else "N/A"
            property_info['number_of_rooms'] = room_element.text if room_element else "N/A"
            property_info['floor_size'] = floor_element.text if floor_element else "N/A"

            property_list.append(property_info)

        pagenum += 1
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        next_button = driver.find_element(By.XPATH, "//a[text()='Next']")
        if next_button.is_enabled():
            next_button.click()
            print('Page:', pagenum)

        if pagenum >= 10:  # Break the loop after scraping the 2nd page
            break

    property_list = process_property_list(property_list)
    return property_list

def store_property_data(data: PropertyData):
    db = SessionLocal()
    property_data = PropertyRepository(db)
    property_data.create_properties(data)
    db.close()

    return {"message": "Property data stored successfully"}