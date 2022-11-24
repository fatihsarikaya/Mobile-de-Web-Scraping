from tkinter import E
from xml.etree.ElementTree import QName
import bs4
import urllib.request
import pandas as pd
import pymysql
import mysql.connector
import configparser
import re
import numpy as np
import time
import concurrent.futures
#import erequests
import lxml
from multiprocessing import Pool
#from multiprocessing import Process, Lock
from multiprocessing import Process
from datetime import datetime
from tqdm import tqdm #progress bar
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy import create_engine
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="mobile_de"
)
mycursor = mydb.cursor()

sql = "SELECT ad_link FROM adlinks_de_mileage_asc"

mycursor.execute(sql)

# Fetching 1st row from the table
# result = mycursor.fetchmany(size =2)

myresult = mycursor.fetchall()

all_links = myresult[0:]

len_all_links = len(all_links)

# print("firstlink:",myresult[0])

# print("len_all_links:",len_all_links)

# print("all_links:",all_links)

dataframe = pd.DataFrame(all_links, columns=['links'])

# print("dataframe:",dataframe)

# print("ilklink:",dataframe.links[0])

x = 5
y = 6

def fonksiyon (i):

#global x
#global y

#number = np.arange(x,y) 

#for i in tqdm(number):
    ad_link = dataframe.links[i]  # ad_link = dataframe["links"][i]
    print(ad_link)

    fireFoxOptions = Options()
    fireFoxOptions.binary_location = r'C:\Program Files\Firefox Developer Edition\firefox.exe'  # PC"ye Firefox Developer yüklenmelidir. 
    fireFoxOptions.add_argument("--headless") 
    #fireFoxOptions.add_argument("--window-size=1920,1080")
    #fireFoxOptions.add_argument('--start-maximized')
    fireFoxOptions.add_argument('--disable-gpu')
    fireFoxOptions.add_argument('--no-sandbox')
    
    driver = webdriver.Firefox(options=fireFoxOptions)

    sleep_time = 5

    #options = webdriver.ChromeOptions()
    #prefs = {"profile.managed_default_content_settings.images": 2}
    #options.add_experimental_option("prefs", prefs)
    #service = Service(executable_path = r'C:\Users\Fatih\Desktop\mobile-de\chromedriver.exe')
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
    # Go to webpage and scrape data

    # Test for Audi 100
    # html = 'https://www.autoscout24.com/offers/audi-100-avant-2-6-e-quattro-tuev07-2024-2-hand-ahk-klimaau-gasoline-red-5c71ae6d-2317-49de-b45b-cd3eef70cb8a?sort=standard&desc=D&lastSeenGuidPresent=true&cldtidx=1&position=1&search_id=19ctily0e8&source_otp=t40&source=listpage_search-results'
    # driver.get(html)

    driver.get(ad_link)
    time.sleep(sleep_time)
    ad_source = driver.page_source
    ad_soup = BeautifulSoup(ad_source, 'lxml') # html.parser

    mainresults = ad_soup.find_all('div', {'class': 'cBox cBox--content u-overflow-inherit '})

    try:
        brand_and_model = ad_soup.find("h1", {"class": ('h2 u-text-break-word')}).get_text()
    except:
        brand_and_model = ' '

    try:
        model_version = ad_soup.find("div", {"class": ('listing-subtitle')}).get_text()
    except:
        model_version = ' '

    try:
        location = ad_soup.find("p", {"class": ('seller-address')}).get_text()
    except:
        location = ' '

    try:
        price = ad_soup.find("span", {"class": ('h3')}).get_text()
    except:
        price = ' '

    try:
        dealer = ad_soup.find("a", {"id": ('dealer-details-link-top')}).get_text()
    except:
        dealer = ' '

    ########## # ACCEPT COOKIES E TIKLAMAK İÇİN ; 2 İŞLEM DE ÇALIŞIYOR
    # driver.find_element(By.XPATH,"//button[@class='sc-bczRLJ iBneUr mde-consent-accept-btn']").click()
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='sc-bczRLJ iBneUr mde-consent-accept-btn']"))).click()
    # time.sleep(3)
    ########## #

    # script = ad_soup.findAll('script')[1].string
    # data = script.split("bootstrapData['menuMonthWeeks'] = ", 1)[-1]#.rsplit(';', 1)[0]
    # data = json.loads(data)

    #driver.find_element(By.XPATH, "//span[@id='sellerPhoneNumberClickableArea']").click()
    # driver.find_element(By.XPATH,"//span[@id='seller-phone']").click()
    # driver.find_element(By.XPATH,"//a[@id='sellerPhoneRevealButton']").click()
    time.sleep(3)

    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='sellerPhoneRevealButton']"))).click()
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='seller-phone']"))).click()
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='sellerPhoneRevealButton']"))).click()
    # time.sleep(3)

    # driver.find_element(By.CLASS_NAME,"hidden-phonereveal-icon").click()

    # driver.find_element(By.ID,"seller-phone").click()
    # driver.execute_script("arguments[0].click();", element)
    # print("clicked tel number")
    # time.sleep(2)
    try:
        WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(By.XPATH, "//button[@class='sc-bczRLJ iBneUr mde-consent-accept-btn']")).click()
        WebDriverWait(driver, timeout=10).until(
            lambda d: d.find_element(By.XPATH, "//p[@class='phone-number-container']")).click()
        tel_number = driver.find_element(By.XPATH, "//p[@class='phone-number-container']").text
        #print(tel_number)
    except:
        tel_number = ' '
        #print("NOT found tel number")
    try:
        contact_name = ad_soup.find("div", {"class": ('g-col-10 u-no-pad-left')}).get_text()
    except:
        contact_name = ' '

    cars_data = pd.DataFrame({
        'brand_and_model': brand_and_model,
        'model_version': model_version,
        'location': location,
        'price': price,
        'dealer': dealer,
        'tel_number': tel_number,
        'contact_name': contact_name,
    },
        index=[0])

    #print("cars_data: ", cars_data)

    ######################################################################################################

    try:
        table_pre = ad_soup.find("div", {"class": "cBox cBox--content cBox-body"})  # 1 (6 in one)
        all_div = table_pre.findAll("div", {"class": ('key-feature__content')})  # 6 (2 in one)
        all_title = table_pre.findAll("div", {"class": ('key-feature__label')})  # 6
        all_results = table_pre.findAll("div", {"class": ('key-feature__value')})  # 6

    except:
        pass

    description_list = []
    value_list = []
    try:

        div_length = len(all_div)
    except:
        div_length = 6

    
    for i in range(div_length):
        try:
            description_list.append(all_title[i].text)
            description_list = list(map(lambda x: x.replace(" ", "_"), description_list))
            value_list.append(all_results[i].text)
            
        except:
            description_list.append('')  # no_description
            value_list.append('')  # no_value

    #print("description_list:", description_list)
    #print("value_list:", value_list)

    ############################################################################################################################
    try:
        technical_data_div = ad_soup.find_all("div", {"class": ('cBox-body cBox-body--technical-data')})
        len_technical_data_div = technical_data_div[0].find_all('div', {'class': ('g-row u-margin-bottom-9')})  # .get_text() # for len
        #print("len_technical_data_div:",len(len_technical_data_div))
    except:
        len_technical_data_div = [1]

    try:
        all_keys = technical_data_div[0].find_all('div', {'class': ('g-col-6')})[::2]

        all_values = technical_data_div[0].find_all("div", {"class": ('g-col-6')})[1::2]  # .get_text()

    except:
        pass

    all_key = []
    all_value = []

    try:
        div_lengths = len(len_technical_data_div)
    except:
        div_lengths = 1

    #print("len_technical_data_div:", len(len_technical_data_div))

    for j in range(div_lengths):
        try:
            # all_key=list(filter(lambda x: (x != filter_words),all_key))

            all_key = list(map(lambda x: x.replace("CO₂_Emissionen_", "CO2_Emissionen_"), all_key))
            all_key = list(map(lambda x: x.replace("CO₂_Effizienz_", "CO2_Effizienz_"), all_key))
            # all_keys=list(filter(lambda x: (x = ''),equipment_value))

            all_key.append(all_keys[j].get_text())
            all_key = list(map(lambda x: x.replace(" ", "_"), all_key))
            all_key = list(map(lambda x: x.replace("-", "_"), all_key))

            all_value.append(all_values[j].get_text())
            # all_value=list(map(lambda x: x.replace(" ", "_"),all_value))
            # all_value=list(map(lambda x: x.replace("-", "_"),all_value))
        except:
            pass
            # all_key.append('') # no_key
            # all_value.append('') # no_value

    #print("all_key:", all_key)
    #print("all_value:", all_value)

    ##################################################################################################################

    try:
        pdiv = ad_soup.find_all('div', {'class': 'bullet-list'})
        # equipment_keys = ad_soup.find_all('h4',{'class' : 'h3'})
    except:
        pass

    equipment_keys = "Features"

    equipment_key = []

    try:
        equipment_key_length = len(pdiv)
    except:
        equipment_key_length = 1

    for k in range(equipment_key_length):
        try:
            equipment_key.append(equipment_keys)
            # equipment_key=list(map(lambda x: x.replace(" & ", "_"),equipment_key))
            # equipment_key=list(map(lambda x: x.replace("", "features"),equipment_key))

        except:
            equipment_key.append('')  # no_equipment_key

    #print("equipment_key:", equipment_key)

    ##################################################################################################################
    try:

        pdiv = ad_soup.find_all('div', {'class': 'bullet-list'})  # [0] # ABS
        equipment_values = pdiv  # .findAll('p')

    except:
        pass

    equipment_value = []

    try:
        dd_ul_li_length = len(pdiv)
    except:
        dd_ul_li_length = 1

    for l in range(dd_ul_li_length):
        try:
            equipment_value.append(equipment_values[l].get_text())
            # equipment_key=list(map(lambda x: x.replace(" & ", "_"),equipment_key))
            # equipment_value=list(filter(lambda x: (x == equipment_lis),equipment_value))

        except:
            equipment_value.append('')  # no_equipment_value

    #print("equipment_value:", equipment_value)

    ##################################################################################################################
    #print("len_pdiv:", dd_ul_li_length)
    ##################################################################################################################
    df3 = pd.DataFrame(list(zip(equipment_key, equipment_value)), columns=['all_key', 'all_value'])

    df2 = pd.DataFrame(list(zip(all_key, all_value)), columns=['all_key', 'all_value'])

    # create a dataframe
    df1 = pd.DataFrame(list(zip(description_list, value_list)), columns=['description_list', 'value_list'])

    # Sütun adları olarak -description_list- den gelen verileri transpose et
    # df = df.T
    df1 = df1.set_index('description_list').T.reset_index(drop=True)
    df1 = df1.rename_axis(None, axis=1)
    # df1['link'] = ad_link
    #######
    df1.insert(0, "brand_and_model", brand_and_model)
    df1.insert(1, "model_version", model_version)
    df1.insert(2, "location", location)
    df1.insert(3, "price", price)
    df1.insert(4, "dealer", dealer)
    df1.insert(5, "tel_number", tel_number)
    df1.insert(6, "contact_name", contact_name)

    ##################################################
    df2_3 = pd.concat([df2, df3])  # concat
    df2_3 = df2_3.set_index('all_key').T.reset_index(drop=True)
    df2_3 = df2_3.rename_axis(None, axis=1)

    df_last = pd.concat([df1, df2_3], axis=1)  # join_axes=[df1.index])

    df_last = df_last.astype(str).groupby(df_last.columns, sort=False, axis=1).agg(
        lambda x: x.apply(','.join, 1))  #####BAK

    # datetime string

    now = datetime.now()
    datetime_string = str(now.strftime("%Y%m%d_%H%M%S"))

    try:
        Vehicle_Description = ad_soup.find("div", {"class": ('g-col-12 description')}).get_text()  # DUZELT
    except:
        Vehicle_Description = ' '

    ###############################################################
    try:
        Picture_count = ad_soup.find_all("div", {"class": ('gallery-img-wrapper u-flex-centerer slick-slide slick-cloned')})[0]
        Car_Picture_Link = Picture_count.find('img').attrs['src']
    except:
        Car_Picture_Link = ' '

    # images = ad_soup.findAll('img')
    # images = Picture_count.findAll('img')
    

    df_last['vehicle_description'] = Vehicle_Description
    df_last['car_picture_link'] = Car_Picture_Link
    df_last['ad_link'] = ad_link
    df_last['download_date_time'] = datetime_string

    ##################################################################################################################

    # Store credantials in file my.propertiesans use Config parser to read from it

    config = configparser.RawConfigParser()
    config.read(filenames='my.properties')
    # print(config.sections())

    scrap_db = pymysql.connect(host='localhost', user='root', password='1234', database='mobile_de', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

    cursor = scrap_db.cursor()

    # Drop table as per requirement

    # cursor.execute('DROP TABLE IF EXISTS CARS')

    # Create table as per requirement

    sql = """CREATE TABLE CARS(
        brand_and_model VARCHAR(32),
        model_version VARCHAR(64),
        location VARCHAR(64),
        price VARCHAR(32),
        dealer VARCHAR(32),
        contact_name VARCHAR(32),
        tel_number VARCHAR(32),
        mileage VARCHAR(32),
        gearbox VARCHAR(32),
        first_registration VARCHAR(7),
        hu VARCHAR(7),
        fuel VARCHAR(64),
        power VARCHAR(16),
        seller VARCHAR(16),
        vehicle_condition VARCHAR(32),
        category VARCHAR(32),
        seats VARCHAR(8),
        doors VARCHAR(8),
        country_version VARCHAR(32),
        sliding_door VARCHAR(32),
        vehicle_number VARCHAR(16),
        previous_owners VARCHAR(8),
        cubic_capacity VARCHAR(16),
        fuel_consumption VARCHAR(64),
        CO2_emissions VARCHAR(32),
        energy_efficiency_class VARCHAR(8),
        CO2_efficiency VARCHAR(80),
        emission_class VARCHAR(16),
        emissions_sticker VARCHAR(16),
        number_of_vehicle_owners VARCHAR(16),
        climatisation VARCHAR(16),
        airbags VARCHAR(32),
        colour VARCHAR(16),
        manufacturer_colour VARCHAR(16),
        interior_design VARCHAR(16),

        features VARCHAR(2048),
        vehicle_description VARCHAR(4096),
        car_picture_link VARCHAR(256),
        ad_link VARCHAR(256),
        download_date_time VARCHAR(32)
        )"""

    #cursor.execute(sql)   #Save data to the table

    for row_count in range(0, df_last.shape[0]):
        chunk = df_last.iloc[row_count:row_count + 1, :].values.tolist()

        # print("-------------------------------------------------------")
        # print(chunk[0])
        # print("-------------------------------------------------------")

        brand_and_model = ""
        model_version = ""
        location = ""
        price = ""
        dealer = ""
        tel_number = ""
        contact_name = ""
        mileage = ""
        first_registration = ""
        hu = ""
        power = ""
        gearbox = ""
        previous_owners = ""
        fuel = ""
        seller = ""
        vehicle_condition = ""
        category = ""
        seats = ""
        doors = ""
        country_version = ""
        sliding_door = ""
        vehicle_number = ""
        cubic_capacity = ""
        fuel_consumption = ""
        CO2_emissions = ""
        energy_efficiency_class = ""
        CO2_efficiency = ""
        emission_class = ""
        emissions_sticker = ""
        number_of_vehicle_owners = ""
        climatisation = ""
        parking_sensors = ""
        airbags = ""
        colour = ""
        manufacturer_colour = ""
        interior_design = ""
        features = ""
        vehicle_description = ""
        car_picture_link = ""
        ad_link = ""
        download_date_time = ""

        # control = "true"

        
        lenght_of_chunk = len(chunk[0])
        # print("lenght_of_chunk:",lenght_of_chunk)    

        if "brand_and_model" in cars_data:
            try:
                brand_and_model = chunk[0][0]
            except:
                brand_and_model = ""

        if "model_version" in cars_data:
            try:
                model_version = chunk[0][1]
            except:
                model_version = ""

        if "location" in cars_data:
            try:
                location = chunk[0][2]
            except:
                location = ""

        if "price" in cars_data:
            try:
                price = chunk[0][3]
            except:
                price = ""

        if "dealer" in cars_data:
            try:
                dealer = chunk[0][4]
            except:
                dealer = ""

        if "tel_number" in cars_data:
            try:
                tel_number = chunk[0][5]
            except:
                tel_number = ""

        if "contact_name" in cars_data:
            try:
                contact_name = chunk[0][6]
            except:
                contact_name = ""

        ##########################################################

        if "Kilometerstand" in description_list:
            index_no = description_list.index("Kilometerstand")
            try:
                mileage = value_list[index_no]
            except:
                mileage = ""

        if "Erstzulassung" in description_list:
            index_no = description_list.index("Erstzulassung")
            try:
                first_registration = value_list[index_no]
            except:
                first_registration = ""

        if "HU_" in all_key:
            index_no = all_key.index("HU_")
            try:
                hu = all_value[index_no]
            except:
                hu = ""

        if "Leistung" in description_list:
            index_no = description_list.index("Leistung")
            try:
                power = value_list[index_no]
            except:
                power = ""

        if "Getriebe" in description_list:
            index_no = description_list.index("Getriebe")
            try:
                gearbox = value_list[index_no]
            except:
                gearbox = ""

        if "Fahrzeughalter" in description_list:
            index_no = description_list.index("Fahrzeughalter")
            try:
                previous_owners = value_list[index_no]
            except:
                previous_owners = ""

        if "Kraftstoffart" in description_list:
            index_no = description_list.index("Kraftstoffart")
            try:
                fuel = value_list[index_no]
            except:
                fuel = ""

        ##############################################################       #BAK

        if "Fahrzeugzustand_" in all_key:
            index_no = all_key.index("Fahrzeugzustand_")
            try:
                vehicle_condition = all_value[index_no]  # index_no=0 olmali (burasi icin)
            except:
                vehicle_condition = ""

        if "Kategorie_" in all_key:
            index_no = all_key.index("Kategorie_")
            try:
                category = all_value[index_no]
            except:
                category = ""

        if "Hubraum_" in all_key:
            index_no = all_key.index("Hubraum_")
            try:
                cubic_capacity = all_value[index_no]
            except:
                cubic_capacity = ""

        if "Anzahl_Sitzplätze_" in all_key:
            index_no = all_key.index("Anzahl_Sitzplätze_")
            try:
                seats = all_value[index_no]
            except:
                seats = ""

        if "Anzahl_der_Türen_" in all_key:
            index_no = all_key.index("Anzahl_der_Türen_")
            try:
                doors = all_value[index_no]
            except:
                doors = ""

        if "Herkunft_" in all_key:
            index_no = all_key.index("Herkunft_")
            try:
                country_version = all_value[index_no]
            except:
                country_version = ""

        if "Schiebetür_" in all_key:
            index_no = all_key.index("Schiebetür_")
            try:
                sliding_door = all_value[index_no]
            except:
                sliding_door = ""

        if "Fahrzeugnummer_" in all_key:
            index_no = all_key.index("Fahrzeugnummer_")
            try:
                vehicle_number = all_value[index_no]
            except:
                vehicle_number = ""

        if "Seller" in all_key:
            index_no = all_key.index("Seller")
            try:
                seller = all_value[index_no]
            except:
                seller = ""

        if "Verbrauch_" in all_key:
            index_no = all_key.index("Verbrauch_")
            try:
                fuel_consumption = all_value[index_no]
            except:
                fuel_consumption = ""

        if "CO2_Emissionen_" in all_key:
            index_no = all_key.index("CO2_Emissionen_")
            try:
                CO2_emissions = all_value[index_no]
            except:
                CO2_emissions = ""

        if "Energieeffizienzklasse_" in all_key:
            index_no = all_key.index("Energieeffizienzklasse_")
            try:
                energy_efficiency_class = all_value[index_no]
            except:
                energy_efficiency_class = ""

        if "CO2_Effizienz_" in all_key:
            index_no = all_key.index("CO2_Effizienz_")
            try:
                CO2_efficiency = all_value[index_no]
            except:
                CO2_efficiency = ""

        if "Schadstoffklasse_" in all_key:
            index_no = all_key.index("Schadstoffklasse_")
            try:
                emission_class = all_value[index_no]
            except:
                emission_class = ""

        if "Umweltplakette_" in all_key:
            index_no = all_key.index("Umweltplakette_")
            try:
                emissions_sticker = all_value[index_no]
            except:
                emissions_sticker = ""

        if "Anzahl_der_Fahrzeughalter_" in all_key:
            index_no = all_key.index("Anzahl_der_Fahrzeughalter_")
            try:
                number_of_vehicle_owners = all_value[index_no]
            except:
                number_of_vehicle_owners = ""

        if "Klimatisierung_" in all_key:
            index_no = all_key.index("Klimatisierung_")
            try:
                climatisation = all_value[index_no]
            except:
                climatisation = ""

        if "Einparkhilfe_" in all_key:
            index_no = all_key.index("Einparkhilfe_")
            try:
                parking_sensors = all_value[index_no]
            except:
                parking_sensors = ""

        if "Airbags_" in all_key:
            index_no = all_key.index("Airbags_")
            try:
                airbags = all_value[index_no]
            except:
                airbags = ""

        if "Farbe_" in all_key:
            index_no = all_key.index("Farbe_")
            try:
                colour = all_value[index_no]
            except:
                colour = ""

        if "Farbe_(Hersteller)_" in all_key:
            index_no = all_key.index("Farbe_(Hersteller)_")
            try:
                manufacturer_colour = all_value[index_no]
            except:
                manufacturer_colour = ""

        if "Innenausstattung_" in all_key:
            index_no = all_key.index("Innenausstattung_")
            try:
                interior_design = all_value[index_no]
            except:
                interior_design = ""

                ######################################################
        if chunk[0][lenght_of_chunk - 5] != "":
            features = chunk[0][lenght_of_chunk - 5]  # features

        #####################################################

        if chunk[0][lenght_of_chunk - 4] != "":
            vehicle_description = chunk[0][lenght_of_chunk - 4]  # vehicle_description

        if chunk[0][lenght_of_chunk - 3] != "":
            car_picture_link = chunk[0][lenght_of_chunk - 3]  # car_picture_link

        if chunk[0][lenght_of_chunk - 2] != "":
            ad_link = chunk[0][lenght_of_chunk - 2]  # ad_link

        if chunk[0][lenght_of_chunk - 1] != "":
            download_date_time = chunk[0][lenght_of_chunk - 1]  # datetime_string

    # print("-------------------------------------------------------")
    # print(brand_and_model)
    # print("-------------------------------------------------------")

    if (brand_and_model == ' '):
        control = "false"
    else:
        control = "true"

    if control == "true":
        mySql_insert_query = "INSERT INTO CARS (brand_and_model,model_version,location,price,dealer,tel_number,contact_name,mileage,first_registration,hu,power,gearbox,previous_owners,fuel,seller,vehicle_condition,category,seats,doors,country_version,sliding_door,vehicle_number,cubic_capacity,fuel_consumption,CO2_emissions,energy_efficiency_class,CO2_efficiency,emission_class,emissions_sticker,number_of_vehicle_owners,climatisation,parking_sensors,airbags,colour,manufacturer_colour,interior_design,features,vehicle_description,car_picture_link,ad_link,download_date_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val =                                  (brand_and_model,model_version,location,price,dealer,tel_number,contact_name,mileage,first_registration,hu,power,gearbox,previous_owners,fuel,seller,vehicle_condition,category,seats,doors,country_version,sliding_door,vehicle_number,cubic_capacity,fuel_consumption,CO2_emissions,energy_efficiency_class,CO2_efficiency,emission_class,emissions_sticker,number_of_vehicle_owners,climatisation,parking_sensors,airbags,colour,manufacturer_colour,interior_design,features,vehicle_description,car_picture_link,ad_link,download_date_time)

        # cursor = scrap_db.cursor()
        cursor.execute(mySql_insert_query, val)  # cursor.executemany(mySql_insert_query, tuple_of_tuples)

        scrap_db.commit()
        print(cursor.rowcount, "Record inserted successfully into *CARS* table")

        # Disconnect from server
        # scrap_db.close()

    driver.close()
    # driver.quit()

  
if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:  # ThreadPoolExecutor
        i = list(range(x,y))    # i = [0,1,2,3...100]
        executor.map(fonksiyon,i)

#fonksiyon (0,4)

