import pywintypes
import json
import win32api

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from math import isnan
import time
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import threading
import traceback




class Scraper:
    
    def __init__(self,address = None) -> None:
        chrome_options = Options()

        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("start-maximized")

        self.driver = webdriver.Chrome(options=chrome_options)
        # self.open_maps(address)
        # self.test()
        
    def open_maps(self,address):
        try:
            self.driver.get(address)
        except:
            self.driver.refresh()
    def get_hrefs(self):
        elem = None
        # elem = self.driver.find_element(By.XPATH,'//body')
        # try:
        # WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
        #     (By.XPATH, '//div[contains(@class, "L1xEbb")]')))
        # self.driver.find_element(By.XPATH,'//div[contains(@class, "L1xEbb")]').click()
        
        # except:
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//div[contains(@class, "Nv2PK")]')))
        elem = self.driver.find_element(By.XPATH,'//div[contains(@class, "Nv2PK")]')
        elem.click()
        
        elems = self.driver.find_elements(By.XPATH,'//div[contains(@class, "Nv2PK")]')
        prev_len = 0
        attempt = 0
        current_len = len(elems)
        action = ActionChains(self.driver)
        try:
            # while prev_len != current_len:
            while True:
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '//div[contains(@class, "Nv2PK")]')))
                elem = self.driver.find_element(By.XPATH,'//div[contains(@class, "Nv2PK")]')
                elem.click()
                print(current_len)
                if current_len == prev_len:
                    attempt += 1
                    if attempt == 4:
                        time.sleep(7)
                    if attempt ==5:
                        break
                else:
                    attempt = 0
                prev_len = current_len
                action.send_keys(Keys.END)
                action.perform()
                time.sleep(2)
                current_len = len(self.driver.find_elements(By.XPATH,'//div[contains(@class, "Nv2PK")]'))
                
        except Exception as e:
            print(e)
            traceback.print_exc()
        
        hrefs = []
        elems = self.driver.find_elements(By.XPATH,'//div[contains(@class, "Nv2PK")]')
        for elem in elems:
            hrefs.append(elem.find_element(By.XPATH,'.//a').get_attribute('href'))
        with open('hrefs.csv','w') as f:
            f.write('\n'.join(hrefs))
        print(current_len)            
        print("Done")
        
        return hrefs
    
    def get_details(self):
        name,address,website,reviews = None,None,None,None
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//h1')))
            name = self.driver.find_element(By.XPATH,'//h1').text
            print(name)
        except Exception as e:
            print(e)
            traceback.print_exc()
        try:
            address = self.driver.find_element(By.XPATH,'//button[@data-item-id="address"]/div/div[2]').text
            print(address)
            
        except:
            pass
            
        try:
            website = self.driver.find_element(By.XPATH,'//a[@data-tooltip="Open website"]/div/div[2]').text
            print(website)
        except:
            pass
            # input()
            
        try:
            reviews = self.driver.find_element(By.XPATH,'//button[contains(@class, "HHrUdb")]/span').text
        except:
            print(traceback.format_exc())
            reviews = 0
            
        return [name,address,website,reviews]
        
    
    def test(self):
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()
        
    def pipeline(self, address):
        self.open_maps(address)
        hrefs = self.get_hrefs()
        with open('hrefs.csv','r') as f:
            hrefs = f.read().split('\n')
            
        total_details = []
        columns = ['Name','Address','Website','Maps_Url','Reviews']
        for i,href in enumerate(hrefs):
            print(i+1,'/',len(hrefs))
            print(href)
            self.open_maps(href)
            details = self.get_details()
            details.append(href)
            total_details.append(details)
        try:
            with open("data.txt",'w',encoding='utf-8') as f:
                f.write(str(total_details))
        except:
            print(traceback.print_exc())
        df = pd.DataFrame(total_details,columns=columns)
        file_name = self.get_file_name(address)
        df.to_excel(f"{file_name}.xlsx",index=False)
    
    def get_file_name(self,url):
        search_query = url.split('search/')[-1]
        name = search_query.split('/')[0]
        name_words = name.split('+')
        name = '_'.join(name_words)
        
        return name
    
    def exit(self):
        self.driver.quit()
        
if __name__ == '__main__':
    sc = Scraper()
    sc.pipeline("https://www.google.com/maps/search/contractors+rawalpindi+Pakistan/")
    # sc.pipeline("https://www.google.com/maps/search/physiotherapist+MELBOURNE+VIC+australia")
    # sc.open_maps("https://www.google.com/maps/search/physiotherapist+MELBOURNE+VIC+australia/@-37.8175956,144.9681828,14z/data=!3m1!4b1?entry=ttu")
    # hrefs = sc.get_hrefs()
    
    # sc.open_maps(r"https://www.google.com/maps/place/Harley+House+Osteopathy/data=!4m7!3m6!1s0x6ad642c7d327d5c3:0xe246c71260394d8c!8m2!3d-37.8133329!4d144.9729292!16s%2Fg%2F1tx8tbqt!19sChIJw9Un08dC1moRjE05YBLHRuI?authuser=0&hl=en&rclk=1")
    # sc.get_details()
    # sc = Scraper("https://www.google.com/maps/search/physiotherapist+ST-KILDA-ROAD-CENTRAL+VIC+australia/")
    input()
    sc.exit()
# fontTitleLarge
# Nv2PK