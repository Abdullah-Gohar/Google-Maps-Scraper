from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from math import isnan
import time
import traceback
import tkinter as tk




class EmailScraper:
    def __init__(self,driver:webdriver.Chrome=None) -> None:
        
        if driver is None:
            chrome_options = Options()

            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            # chrome_options.add_argument("--headless")
            chrome_options.add_argument("start-maximized")

            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = driver

    def open_website(self, address:str)->None:
        try:
            self.driver.get(address)
        except:
            self.driver.refresh()
        
    def find_email(self):
        mail = None
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located(
            (By.XPATH, '//a[contains(@href, "mailto")]')))
            elem = self.driver.find_element(By.XPATH,'//a[contains(@href, "mailto")]').get_attribute('href')
            mail = elem.split(':')[-1]
            
        except:
            print(traceback.format_exc())
            try:
                contact = self.driver.find_element(By.XPATH,'//a[contains(@href, "contact")]')
                self.driver.get(contact.get_attribute('href'))
                WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located(
                (By.XPATH, '//a[contains(@href, "mailto")]')))
                elem = self.driver.find_element(By.XPATH,'//a[contains(@href, "mailto")]').get_attribute('href')
                mail = elem.split(':')[-1]
            except:
                
                print(traceback.format_exc())      
            
        return mail      
    
    def close(self):
        self.driver.quit()
    
    def pipeline(self,address:str)->str:
        if not address:
            return ""
        self.open_website(address)
        return self.find_email()
    
    def pipeline_with_list(self,addresses:list)->list:
        emails = []
        for address in addresses:
            print(address)
            email = self.pipeline(address)
            emails.append(email)
            
        return email
    
    
if __name__ == '__main__':
    escraper = EmailScraper()
    print(escraper.pipeline("https://miamishome.com/"))