#!/usr/bin/env python
# coding: utf-8

# In[39]:


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
import datetime


# In[2]:


# driver = webdriver.Chrome(executable_path = "H:\\MSIT 2nd Year\\DADV\\Selenium\\chromedriver.exe")
# driver.maximize_window()

# driver.get("https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?flag=0")
# driver.get("https://www.bseindia.com/corporates/List_Scrips.aspx")
# #selecting the segment as Equity
# segment = Select(driver.find_element_by_id("ContentPlaceHolder1_ddSegment"))
# segment.select_by_visible_text("Equity")

# #selecting the status as Active
# segment = Select(driver.find_element_by_id("ContentPlaceHolder1_ddlStatus"))
# segment.select_by_visible_text("Active")

# driver.find_element_by_id("ContentPlaceHolder1_btnSubmit").click()
# time.sleep(2)


# driver.find_element_by_id("ContentPlaceHolder1_lnkDownload").click()


# In[40]:


import pandas as pd
import numpy as np
import random


# In[108]:

while True:
    try:
        lisData = pd.read_csv("C:\\Users\\Someshwar Thumma\\Downloads\\ListOfScrips.csv")
        # print("downloding.. List_Scrips,,")
        break
    except Exception as e:
        time.sleep(1)
        pass
    


# In[114]:


lis = lisData.sample(10)
finalList = list(lis["Security Code"])
securityId = list(lis["Security Id"])
securityName = list(lis["Security Name"])
print(finalList)
lis

# print("readed scripts and opening the new page.")
# perfect values: [523796, 539288, 531930, 532240, 530555, 532924, 512169, 511714, 508306, 526235]

# In[115]:


# #Directing the webpage
# driver = webdriver.Chrome(executable_path = "H:\\MSIT 2nd Year\\DADV\\Selenium\\chromedriver.exe")
driver.get("https://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?flag=0")

#SecurityCode

driver.find_element_by_id("ContentPlaceHolder1_txtToDate").click()
time.sleep(1)
x = datetime.datetime.now()
date = x.strftime("%d")
year = x.strftime("%Y")
driver.find_element_by_link_text(date).click()
time.sleep(1)
#ContentPlaceHolder1_txtToDate
driver.find_element_by_id("ContentPlaceHolder1_txtFromDate").click()
time.sleep(1)
year = str(int(year)-1)
yearOptions = Select(driver.find_element_by_class_name("ui-datepicker-year"))
yearOptions.select_by_visible_text(year)
driver.find_element_by_link_text(date).click()
time.sleep(5)

for securityCode in finalList:  
    search = driver.find_element_by_id('ContentPlaceHolder1_smartSearch').clear()
    search = driver.find_element_by_id('ContentPlaceHolder1_smartSearch')
    search.send_keys(int(securityCode))
    driver.find_element_by_class_name("quotemenu").click()

    driver.find_element_by_id('ContentPlaceHolder1_btnSubmit').click()
    #ContentPlaceHolder1_btnDownload > i
    driver.find_element_by_id('ContentPlaceHolder1_btnDownload1').click()


# In[125]:
# print("reading files.")

df = pd.DataFrame()
for i in range(len(finalList)):
    try:
        link = "C:\\Users\\Someshwar Thumma\\Downloads\\"+str(finalList[i])+".csv"
    except Exception as e:
        print("File not found with security code: "+str(finalList[i]))
        pass
    data = pd.read_csv(link)["Close Price"]
    gain = (data[len(data)-1]/data[0])-1
    newRow = {'Code':finalList[i], 'ID':securityId[i], 'Name':securityName[i], 'Gain':gain}
    df = df.append(newRow, ignore_index=True)


# In[126]:


df.sort_values("Gain", axis = 0, ascending = False, inplace = True, na_position ='last')
print(str(df['Name'][0])+ " has the highest gain of " +str(df['Gain'][0]))

