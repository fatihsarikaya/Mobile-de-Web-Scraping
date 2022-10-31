##############################################################################################################################
# 2. BÜTÜN MARKALAR İÇİN MAX. 20 SAYFADAN GELEN 400 ARABANIN DETAY LİNKLERİNİ (ADD_LINKS) TOPLAMA  (Part 2)
from tkinter import E
from xml.etree.ElementTree import QName
import bs4
import urllib.request
import pandas as pd
#import lxml
#import cchardet
import pymysql
import mysql.connector
import configparser
import concurrent.futures
import re
import numpy as np
import time
from datetime import datetime
from tqdm import tqdm #progress bar
from urllib.request import urlopen
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
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
import glob
import os
import datetime
import time
import pandas as pd
import numpy as np
import re
import itertools
from selenium.webdriver.firefox.options import Options

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mobile_de"
)
mycursor = mydb.cursor()

sql = "SELECT * FROM carlist_de_mileage_asc"

mycursor.execute(sql)

columns = [desc[0] for desc in mycursor.description]

data_df = pd.DataFrame(mycursor.fetchall(), columns=columns)

data_dict = data_df.to_dict(orient="list")

dataframe = pd.DataFrame(data_dict)

#print("dataframe:",dataframe)



make_model_data = dataframe

#print("make_model_data:",make_model_data)

x=1  # Buradaki x=1 , db'de -> id = 2 ye denk gelir. ( Audi - 200 linkinden gelen ilanlarin adlinks'lerini toplayacaktır. (6 adet ilanın linkleri veritabanına kaydedilir.)
y=2  # Buradaki y=2 , db'de -> id = 3 e denk gelir. Fakat id = 3 scraping'e dahil değildir
#
#number = np.arange(x,y)

print(dataframe.link[x:y])

def fonksiyon(i):

    global x
    global y

#for i in  tqdm(number):
    make_model_input_link = make_model_data.link[i]

    sleep = 1
    make_model_input_data = make_model_data
    save_to_csv = False

    fireFoxOptions = Options()
    #fireFoxOptions.binary_location = r'C:\Program Files\Firefox Developer Edition\firefox.exe'
    fireFoxOptions.add_argument("--headless")
    #fireFoxOptions.add_argument("--window-size=1920,1080")
    #fireFoxOptions.add_argument('--start-maximized')
    fireFoxOptions.add_argument('--disable-gpu')
    fireFoxOptions.add_argument('--no-sandbox')

    driver = webdriver.Firefox(options=fireFoxOptions)

#    options = Options()
#    options = webdriver.ChromeOptions()

    #options.set_headless = True
    #options.add_argument('--disable-gpu')
    #options.add_argument("--window-size=1920x1080")

#    options.headless = True
#    options.add_argument("--headless")

    prefs = {"profile.managed_default_content_settings.images": 2}
#   options.add_experimental_option("prefs", prefs)

    #start a driver
    #service = Service(executable_path='C:/Users/Fatih/Desktop/autoscout24/chromedriver.exe')
#    driver = webdriver.Chrome(options=options)
#    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    #get the number of pages
    driver.get(make_model_input_link)
    make_model_link_lastpage_source = driver.page_source
    make_model_link_soup = BeautifulSoup(make_model_link_lastpage_source, 'lxml')

    last_button = make_model_link_soup.findAll('span', {'class': 'btn btn--secondary btn--l'}) ### SONRASINA BAK

    # Eğer sadece 1 sayfa varsa, error alırız, bundan dolayı sayfa sayısını kontrol etmek durumundayız !!!
    try:
        print("-Bulunan sayfa sayisi: ", last_button[len(last_button)-1].text)
        last_button_number = last_button[len(last_button)-1].text
        last_button_number = int(last_button_number)
    except:
        last_button_number = int(1)

    driver.close()

    # Linkleri kazımaya başlıyoruz !!!

    links_on_multiple_pages = []

    for i in tqdm(range(1, last_button_number + 1)):

        #Her seferinde web driver i yeniden başlatıyoruz ki captcha ya takılıp block olmayalım !!!

        fireFoxOptions = Options()
        #fireFoxOptions.binary_location = r'C:\Program Files\Firefox Developer Edition\firefox.exe'
        fireFoxOptions.add_argument("--headless")
        #fireFoxOptions.add_argument("--window-size=1920,1080")
        #fireFoxOptions.add_argument('--start-maximized')
        fireFoxOptions.add_argument('--disable-gpu')
        fireFoxOptions.add_argument('--no-sandbox')

        driver = webdriver.Firefox(options=fireFoxOptions)

       #options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
#       options.add_experimental_option("prefs", prefs)

        #start a driver
        #service = Service(executable_path='C:/Users/Fatih/Desktop/autoscout24/chromedriver.exe')
#       driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # Sırayla sayfalara (1 den 20 ye) gitmemiz gerekiyor !!!  #
        one_page_link = make_model_input_link + "&pageNumber=" + str(i)

        driver.get(one_page_link)
        time.sleep(sleep)
        base_source = driver.page_source
        base_soup = BeautifulSoup(base_source, 'lxml')

        # Her araç için (detaylara gidebilmek adına) link topluyoruz !!!
        cars_add_list_all = base_soup.findAll('a', {'class': re.compile('link--muted no--text--decoration result-item')})

        links_on_one_page = []

        for i in range(len(cars_add_list_all)):

            link = cars_add_list_all[i]['href']

            if not link.endswith('SellerAd&ref=srp'):
                #   'SellerAd' ile biten bağlantıları filtreliyoruz (bunlar reklam bağlantıları olduğundan ihtiyacımız yok) !!!
                links_on_one_page.append(link)

        for elements in links_on_one_page:
            links_on_multiple_pages.append(elements) # Peşpeşe linkler alt alta eklenir !!!

        driver.close() #close the driver

    links_on_one_page_df = pd.DataFrame({'ad_link' : links_on_multiple_pages}) # Dataframe oluşturulur !!!
    #drop duplicates
    links_on_one_page_df = links_on_one_page_df.drop_duplicates()

    links_on_one_page_df['make_model_link'] = make_model_input_link # Bu sayede linklerin hangi marka ve modele ait olduğunu görebiliriz !!!

    #datetime string
    now = datetime.datetime.now()
    datetime_string = str(now.strftime("%Y%m%d_%H%M%S"))

    links_on_one_page_df['download_date_time'] = datetime_string

    #   Marka ve modelin D.F.'de olup olmadığını kontrol eder !!!
    if isinstance(make_model_input_data, pd.DataFrame):
        #join the dataframes to get make and model information
        links_on_one_page_df = pd.merge(links_on_one_page_df, make_model_input_data, how = 'left', left_on= ['make_model_link'], right_on = ['link'])

    #   save_to_csv True ise DataFrame'i kaydeder !!!
#    if save_to_csv:
#        #   Klasörün var olup olmadığını kontrol eder ve yoksa oluşturur !!!
#        if not os.path.exists(r'C:\Users\Fatih\Desktop\mobile-de\data\make_model_ads_links'):
#            os.makedirs(r'C:\Users\Fatih\Desktop\mobile-de\data\make_model_ads_links')
#
#        links_on_one_page_df.to_csv(str(r'C:\Users\Fatih\Desktop\mobile-de\data\make_model_ads_links\links_on_one_page_df' + datetime_string + '.csv'), index = False)
#
#    return(links_on_one_page_df)
#scrape_links_for_one_make_model

#link_on_multiple_pages_data = scrape_links_for_one_make_model(make_model_input_link = 'https://suchen.mobile.de/fahrzeuge/search.html?dam=0&isSearchRequest=true&ms=22900;13&ref=quickSearch&sfmr=false&vc=Car',make_model_input_data = make_model_data,save_to_csv=True)
#print(link_on_multiple_pages_data)


    try:
        brand_and_model = base_soup.find('li', {'class': ('u-text-truncate')}).get_text()
    except:
        brand_and_model = ""
    #######
    print("brand_and_model:",brand_and_model)


    links_on_one_page_df['brand_model'] = brand_and_model
    

    links_on_one_page_df['link'] = make_model_data.link

#def multiple_link_on_multiple_pages_data(make_model_input_links = [], sleep = 1, make_model_input_data = make_model_data, save_to_csv = True):

    make_model_input_links = []
    sleep = 0
    make_model_input_data = make_model_data
    save_to_csv = False

    multiple_make_model_data = pd.DataFrame()

    for one_make_model_link in make_model_input_links:

        one_page_adds = links_on_one_page_df

        make_model_input_link = one_make_model_link
        #sleep = sleep
        #make_model_input_data = make_model_input_data

        multiple_make_model_data = pd.concat([multiple_make_model_data, one_page_adds], ignore_index=True)

        #print("multiple_make_model_links: ",multiple_make_model_data)
        #return(multiple_make_model_data)

    config = configparser.RawConfigParser()
    config.read(filenames = 'my.properties')
    #print(config.sections())

    scrap_db = pymysql.connect(host='localhost',user='root',password='',database='mobile_de',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

    cursor = scrap_db.cursor()

    # Drop table as per requirement

    #cursor.execute('DROP TABLE IF EXISTS CARS')

    # Create table as per requirement

    sql = """CREATE TABLE adlinks_de_mileage_asc(
        
        count int(11),
        carlist_id int(11),
        brand_model VARCHAR(32),
        ad_link VARCHAR(255),
        link VARCHAR(255),
        created_at VARCHAR(32),
        updated_at datetime,
        status tinyint(3)
        )"""

    cursor.execute(sql)   #Save data to the table

    #control = "false"

    for row_count in range(0, 1):
        chunk = links_on_one_page_df.iloc[row_count:row_count + 1,:].values.tolist()

        #print("-------------------------------------------------------")
        #print(chunk[0])
        #print("-------------------------------------------------------")

        count = ""
        carlist_id = ""
        brand_model = ""
        ad_link = ""
        link = ""
        created_at = ""
        updated_at = ""
        status = ""

        control = "true"

        #i=0
        lenght_of_chunk = len(chunk[0])
        #print("lenght_of_chunk:",lenght_of_chunk)     # 24  for -> number = np.arange(2,3) # https://www.autoscout24.com/offers/audi-100-coupe-s-restaurationsfahrzeug-motor-laeuft-gasoline-red-f45e40a9-a46c-4b05-8699-9979e2c680f6

        len_for_ad_link = len(links_on_one_page_df.ad_link)
        #print("links_on_one_page_df:",links_on_one_page_df)

        #print("len_for_ad_link:",len_for_ad_link)

        links_on_one_page_df = links_on_one_page_df.replace(np.nan, "")

        for l in range(len_for_ad_link):

            try:
                count = l + 1
            except:
                pass

            if "ad_link" in links_on_one_page_df:

                try:
                    ad_link = links_on_one_page_df.ad_link[l]
                except:
                    ad_link = ""

            if "brand_model" in links_on_one_page_df:
                try:
                    brand_model = links_on_one_page_df.brand_model[l]
                except:
                    brand_model = ""

            if "link" in links_on_one_page_df:
                try:
                    link = links_on_one_page_df.make_model_link[l]
                except:
                    link = ""

            if "download_date_time" in links_on_one_page_df:
                try:
                    created_at = chunk[0][2]
                except:
                    created_at = ""

            if (ad_link == ""):
                control = "false"
            else:
                control = "true"

            if control == "true":
                mySql_insert_query = "INSERT INTO adlinks_de_mileage_asc (count,carlist_id,brand_model,ad_link,link,created_at,updated_at,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                val =                                                    (count,carlist_id,brand_model,ad_link,link,created_at,updated_at,status)

                #cursor = scrap_db.cursor()
                cursor.execute(mySql_insert_query, val) # cursor.executemany(mySql_insert_query, tuple_of_tuples)

                scrap_db.commit()
                print(cursor.rowcount, "Record inserted successfully into *adlinks_de_mileage_asc* table")

                #Disconnect from server
                #scrap_db.close()
        #x +=  1
if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:  # ThreadPoolExecutor
        i = list(range(x,y))    # i = [0,1,2,3...100]
        executor.map(fonksiyon,i)


