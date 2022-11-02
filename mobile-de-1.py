#def get_all_make_model(mobile_de_eng_base_link="https://www.mobile.de/?lang=en", save_filename="make_and_model_links.csv"):
import pandas as pd
import numpy as np
import re
import os 
import itertools
import time
import pymysql
import mysql.connector
import configparser
from optparse import Values
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from random import randrange
from tqdm import tqdm #progress bar
from datetime import datetime

#fireFoxOptions = Options()
#fireFoxOptions.binary_location = r'C:\Program Files\Firefox Developer Edition\firefox.exe'  # PC"ye Firefox Developer yüklenmelidir.
#fireFoxOptions.add_argument("--headless") 
##fireFoxOptions.add_argument("--window-size=1920,1080")
##fireFoxOptions.add_argument('--start-maximized')
#fireFoxOptions.add_argument('--disable-gpu')
#fireFoxOptions.add_argument('--no-sandbox')

#driver = webdriver.Firefox(options=fireFoxOptions)


options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
service = Service(executable_path='C:/Users/Fatih/Desktop/autoscout24/chromedriver.exe')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

starting_link_to_scrape = "https://www.mobile.de/?lang=en"
driver.get(starting_link_to_scrape)
time.sleep(3)
base_source = driver.page_source
base_soup = BeautifulSoup(base_source, 'html.parser')

make_list = base_soup.findAll('select', {'data-testid': 'qs-select-make'})[0]
one_make = make_list.findAll('option')

#print(one_make)

brand = []
brand_id = []

for i in range(len(one_make)):

    brand.append(one_make[i].text.strip())
    #brand=list(map(lambda x: x.replace(" ", "-"),brand))

    try:
        brand_id.append(one_make[i]['value'])
    except:
        brand_id.append('')

car_base_make_data = pd.DataFrame({
    'brand': brand, 
    'brand_id': brand_id
    })

brand_filter_out = ['Any', 'Other', '']
car_base_make_data = car_base_make_data[~car_base_make_data.brand.isin(brand_filter_out)]
car_base_make_data = car_base_make_data.drop_duplicates()
car_base_make_data = car_base_make_data.reset_index(drop=True)

print(car_base_make_data)
#print(one_make) #with options 
#print(brand) #without options/pure
#print(brand[2]) #BMW

car_base_model_data = pd.DataFrame()

for one_make in tqdm(car_base_make_data['brand'], "Progress: "):

    #make_string = "//select[@id='make']".format(one_make) 
    #driver.find_element(By.XPATH,make_string).click()
    #time.sleep(3)
    
    j=0  
    
    x = 127   # x = 4  yazılırsa eğer  ; ilk 3 arabanın marka-model linkleri db'e kayıt olunur. ( Audi, BMW ve Mercedes-Benz )   # x = 127
  
    
    while j < x:  
        j += 1;
        
        grbf = Select(driver.find_element(By.XPATH,"//body[@class='body']/div[@id='root']/div[@class='hp7JS']/div[@class='_24p6C']/article[@class='RSseD _3LZ_7 _2iEKW']/section[@class='_1ypBX _1G5lv _3Qzoz']/div[@class='_2W31y']/div[@class='UiAUP']/div[@class='_1xQiC']/div[1]/div[1]/select[1]")) #/option[text()='{}']
        grbf.select_by_value(brand_id[j]) #   brand_id[1] = Audi' 
        
        try:
            print(" Sirayla markalar seciliyor, " + brand[j] + " secildi")
            #print(brand[1])
        except:
            print(' Not clicked any make')
        
        
        time.sleep(3) # sayfanın yüklenmesini bekle
        
        base_source = driver.page_source
        base_soup = BeautifulSoup(base_source, 'html.parser')

        model_list = base_soup.findAll('select', {'data-testid': 'qs-select-model'})[0]
        models = model_list.findAll('option')

        #try:
        #    print(models)
        #except:
        #    print("Not listed any model")        
       
        car_model = []
        model_id = []

        for i in range(len(models)):
            
            try:
                car_model.append(models[i].text.strip())
                car_model=list(map(lambda x: x.replace(" ", "-"),car_model))
                #car_model=list(itertools.filterfalse(lambda x: x.endswith('(All)'), car_model))
                car_model=list(filter(lambda x: not x.endswith('(All)'), car_model)) #(All)
            except:
                car_model.append('')
                
            try:
                model_id.append(models[i]['value'])
                model_id=list(filter(lambda x: not x.startswith('g'), model_id))
            except:
                model_id.append('')

        car_base_model_data_aux = pd.DataFrame({
            'car_model': car_model, 
            'model_id': model_id
            })
        
        
        
        car_model_filter_outside = ['Any',' '] 
        car_base_model_data_aux = car_base_model_data_aux[~car_base_model_data_aux.car_model.isin(car_model_filter_outside)]
        car_base_model_data_aux = car_base_model_data_aux.drop_duplicates()
        car_base_model_data_aux = car_base_model_data_aux.reset_index(drop=True)
        
        
        car_base_model_data_aux['brand'] = brand[j]
        
        
        car_base_model_data = pd.concat([car_base_model_data, car_base_model_data_aux], ignore_index=True)
        
        print(car_base_model_data_aux)
        
        #print(car_base_model_data[car_base_model_data['brand'] == "Austin"])
        
        time.sleep(3)
 
        if j == x-1 :
            break
    print("End")
    break 
#print('Out of loop')
       

car_data_base = pd.merge(car_base_make_data, car_base_model_data, left_on=['brand'], right_on=['brand'], how='right')
car_data_base = car_data_base[~car_data_base.model_id.isin([""])]
car_data_base = car_data_base[car_data_base.model_id.apply(lambda x: x.isnumeric())]
car_data_base = car_data_base.drop_duplicates()

#semicolon = ';'

car_data_base['link'] = "https://suchen.mobile.de/fahrzeuge/search.html?cn=DE&dam=0&isSearchRequest=true&ms=" + car_data_base['brand_id'] + ";" + car_data_base['model_id'] + "&ref=quickSearch&sfmr=false&vc=Car&sortOption.sortBy=specifics.mileage&sortOption.sortOrder=ASCENDING" #mileage_asc
car_data_base = car_data_base.reset_index(drop=True)


#if len(save_filename) > 0:
#car_data_base.to_csv(r'C:\Users\Fatih\Desktop\make_and_model_links.csv', encoding='utf-8', index=False)
#return(car_data_base)

#make_model_data = pd.read_csv(r'C:\Users\Fatih\Desktop\make_and_model_links.csv')
#print(make_model_data)


#   Datetime string
now = datetime.now() 
datetime_string = str(now.strftime("%Y%m%d_%H%M%S"))
#   Datetime'ı kolon olarak df'e eklemek için !!!
car_data_base['download_date_time'] = datetime_string


config = configparser.RawConfigParser()
config.read(filenames = 'my.properties')


scrap_db = pymysql.connect(host='localhost',user='root',password='',database='mobile_de',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

cursor = scrap_db.cursor()



sql = """CREATE TABLE carlist_de_mileage_asc(
        
        brand VARCHAR(32),
        brand_id VARCHAR(16),
        model VARCHAR(32),
        model_id VARCHAR(16),
        link VARCHAR(255),
        created_at VARCHAR(32),
        updated_at datetime,
        status tinyint(3)
        )"""
        
cursor.execute(sql)

for row_count in range(0, 1): 
        chunk = car_data_base.iloc[row_count:row_count + 1,:].values.tolist()
        
        #print("-------------------------------------------------------")
        #print(chunk[0])
        #print("-------------------------------------------------------")
        
        brand = ""
        brand_id = ""
        model = ""
        model_id = ""
        link = ""
        created_at = ""
        updated_at = ""
        status = ""
        
        
        #control = "true"
        
        
        len_for_links = len(car_data_base.link)
        
        for l in range(len_for_links):
                        
            if "brand" in car_data_base: 
                try:
                    brand = car_data_base.brand[l]
                except:
                    brand = ""
            
            if "brand_id" in car_data_base:
                try:
                    brand_id = car_data_base.brand_id[l]
                except:
                    brand_id = ""
                    
            if "car_model" in car_data_base:
                try:
                    model = car_data_base.car_model[l]
                except:
                    model = ""
            
            if "model_id" in car_data_base:
                try:
                    model_id = car_data_base.model_id[l]
                except:
                    model_id = ""
                    
            if "link" in car_data_base:
                try:
                    link = car_data_base.link[l]
                except:
                    link = ""
                    
            
            if "download_date_time" in car_data_base:
                try:
                    created_at = car_data_base.download_date_time[l]
                except:
                    created_at = ""
        
            mySql_insert_query = "INSERT INTO carlist_de_mileage_asc (brand,brand_id,model,model_id,link,created_at,updated_at,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (brand,brand_id,model,model_id,link,created_at,updated_at,status)

            #cursor = scrap_db.cursor()
            cursor.execute(mySql_insert_query, val) # cursor.executemany(mySql_insert_query, tuple_of_tuples)
            
            scrap_db.commit()
            print(cursor.rowcount, "Record inserted successfully into *carlist_de_mileage_asc* table")

            #Disconnect from server
            #scrap_db.close()