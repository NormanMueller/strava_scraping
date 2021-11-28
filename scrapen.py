from selenium import webdriver
import pandas as pd
import os
import time
from selenium.webdriver.common.keys import Keys

class get_strava_data():
    """ """
    def __init__(self, path , website , user ,pw) -> None:
        
        self.path = path
        self.website = website
        self.user = user
        self.pw= pw
        self.driver = ''
        self.cols = ['td.view-col.col-type','td.view-col.col-dist','td.view-col.col-date','td.view-col.col-time']
        self.css_id = "search-results"


    def login_to_website (self):
        
        def fill_email (self):

            self.driver = webdriver.Chrome(self.path) 
            self.driver.get(self.website)
            time.sleep(2)
            search = self.driver.find_element_by_id("email")
            search.clear()
            search.send_keys(self.user)
        
        def fill_password (self): 

            search2= self.driver.find_element_by_id("password")
            search2.clear()
            search2.send_keys(self.pw)

       
        def login(self):

            time.sleep(1)
            fill_email(self)
            fill_password(self)
            login= self.driver.find_element_by_id("login-button")
            login.click()
            time.sleep(2)

        login(self)


    def get_aktivitie_data (self ):


        def find_aktivities(self):

            self.login_to_website()
            table = self.driver.find_element_by_id(self.css_id)
            time.sleep(2)
            return  table 
        

        def get_aktivities (self):
            table = find_aktivities(self)
            return table

        def append_value ( tag, liste): 
            x = tag.text
            liste.append(x)


        def get_data (self):
            
            table = get_aktivities(self)
            dist=[]
            date=[]
            time2=[]
            typex=[]

            for durchlauf in  range(6):
               
                for col in self.cols:
                    
                    tags = table.find_elements_by_css_selector(str(col))
                    
                
                    for tag in tags:

                        if str(col) == 'td.view-col.col-dist':
                            append_value(tag, dist)
                
                        elif str(col) == 'td.view-col.col-date':
                            append_value(tag, date)
        
                        elif str(col) == 'td.view-col.col-time':
                            append_value(tag, time2) 
                
                        elif str(col) == 'td.view-col.col-type':
                            append_value(tag, typex) 


                next_page = self.driver.find_element_by_css_selector("button.btn.btn-default.btn-sm.next_page")
                next_page.click()
                time.sleep(2)
    
            data ={'Type':typex ,'Distance' :dist, 'Date' : date, 'Time' : time}
            data = pd.DataFrame(data)
            time.sleep(2)
            
            return data
        
        return get_data(self)


    def transform_data (self):

        data = self.get_aktivitie_data()
        data["Date"] =pd.to_datetime(data["Date"].str.slice(4, 15))
        data["Distance"] = data["Distance"].str.split(' ',1).str[0]
        data["Distance"] =data["Distance"].str.replace(',','.').astype('float')
        self.driver.close()
        
        return data


x = get_strava_data(path = r"C:\Users\norma\chromedriver.exe",
                website= 'https://www.strava.com/athlete/training',
                user = 'nomueller@uni-osnabrueck.de',
                pw = 'Kroos92m.'
                 )

print(x.transform_data())