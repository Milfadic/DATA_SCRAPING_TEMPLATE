# -*- coding: utf-8 -*-
#Program written by Milenko A. Fadic
#May 2015, Bologna 

#IMPORT MODULES 

import webbrowser
import cookielib
import urllib, urllib2
from urllib2 import urlopen
from bs4 import BeautifulSoup,NavigableString
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import html5lib
import csv
import time
from datetime import datetime
from datetime import date
from time import gmtime, strftime

#########################Functions###################################################
#This part of the program is done so I can set a download rate. If it is a weekday, I put a delay of 20 after each loop in order not to overload the server.
#The delay can be adjusted below.


# It opens driver. It refresh it so the icon in the calendar work. If it does not open, i do a time out
def opendriver(driver, sitescrap):
                try:
                    driver.get(sitescrap)
                except TimeoutException:
                    #driver.close
                    driver.get(sitescrap)
                else:             
                    print "BROWSER SHOULD BE OPEN, 3O SECONDS IS THE TIMEOUT RATE"
                    driver.set_page_load_timeout(45)
                    
#DOES A CHECK ON THE DATE AND THEN DOES A PAUSE BASED ON THE HIGH DOWNLOAD OR LOW DOWNLOAD 

def hourpeak(time_sleep_low_rate, time_sleep_high_rate ):
            c_time=strftime("%H", gmtime())  #This sets the time and integer time to see the rate of download. They are the args that go in hourpeak
            c_time2=int(c_time)
            c_time3=strftime("%H:%M:%S", gmtime())  
            c_date=strftime("%Y-%m-%d",gmtime())
            c_day=date.isoweekday(date.today())

            if ((c_day < 6) and (c_time2 >10 or c_time2 <2)) :
                peak="lowdownload"
            else:
                peak= "highdownload"
            if peak== "lowdownload":   #Function that defines rate of download. I can change the numbers accordinigly 
                time.sleep(time_sleep_low_rate)
            else:
                time.sleep(time_sleep_high_rate)
            print "This is the rate of download", peak


#SCRAPS FIRST TAB 

def scrap_2(soup, sys, driver, company_ruc, ActionChains, admin_a):
      table_num=0
      for tables in soup.find_all('div', {'class':'z-listbox'}): #This looks at the number of boxes
            max_page=[]
            try:         #This looks to see if there are multiple pages per record, if so I have to scrap each of them...
              next_button=tables.find_all('button', {'class':'z-paging-next'})
              next_button_c=tables.find('button', {'class':'z-paging-next'})
              number_pages= tables.find_all('span', {'class':'z-paging-text'}) #This is the text that has the number of pages in there.....
              for i in number_pages:
                    pg=i.text.strip().replace("/","")   #REPLACE NUMBERS
                    pg=pg.strip()
                    max_page.append(pg) #FIND THE NUMBERS OF PAGES
              mpg=max(max_page)
              mpg=int(mpg)
              print "This is the number of pages", mpg
               #IF THERE IS ONLY ONE PAGE, THEN FOR EACH LINE  ENCODE IT, THEN APPEND IT TO A LIST A. AFTER IT IS FINISH FOR EVERY LINE THEN APPEND LIST A TO LIST B AND WRITE IT TO PROGRAM. 
              if mpg < 2:
                  print "Div only has one page"
                  resultk=[] 
                  for tr in tables.find_all('tr', {'class':'z-listitem'}):
                        result=[]
                        result.append((company_ruc,'|'))
                        for elem in tr:
                              tabresult =[elem.text.strip().encode('utf-8')]
                              result.append(([tabresult],"|"))
                        resultk.append([result])
                        with open(admin_a, 'a') as f:
                            csv.writer(f).writerows(resultk)
            #IF THERE ARE MORE THAN  ONE PAGE, THEN FOR EACH PAGE AND EACH LINE  ENCODE IT,
            #THEN APPEND IT TO A LIST A. AFTER IT IS FINISH FOR EVERY LINE THEN APPEND LIST A TO LIST B AND WRITE IT TO PROGRAM.             
              else:           
                  j=1
                  print "Admin has more than two pages"
                  while j< mpg+1:  #NOTE THAT THE CONTENT CHANGES, SO I HAVE TO DEFINE A SOUP EACH TIME
                        content = driver.page_source
                        soup = BeautifulSoup(''.join(content))
                        for tr in soup.find_all('tr', {'class':'z-listitem'}):
                              result=[]
                              result.append((company_ruc,'|'))
                              for elem in tr:
                                    tabresult =[elem.text.strip().encode('utf-8')]
                                    result.append(([tabresult],"|"))
                              with open(admin_a, 'a') as f:
                                    csv.writer(f).writerow(result)
                             
                        j=j+1
                        button_driver=driver.find_elements_by_class_name('z-paging-next')
                        ActionChains(driver).move_to_element(button_driver[table_num]).click().perform()
                        time.sleep(3)
            #IN CASE OF AN EXCEPTION THEN PRINT ERRORS         
            except:
                  print sys.exc_info()
            finally:
                  table_num=table_num+1




#FOR SCRAP 3,4,AND 1. THEN PROCEUDRE IS SIMILAR TO SCRAP 2. THERE ARE SUBTLE DIFFERENCES SUCH AS WHERE TO PLACE THE IDENTIFIER, BUT THE LOGIC IS THE SAME. THEY ARE NOT ANNOTATED
#BUT SERVE FOR ADDITIONAL DETAILS. 
def scrap_3(soup, sys, driver, company_ruc, ActionChains, kardex):
            table_num=0
            for tables in soup.find_all('div', {'class':'z-listbox'}):
                  print "tables found"
                  max_page=[]
                  next_button=tables.find_all('button', {'class':'z-paging-next'})
                  next_button_c=tables.find('button', {'class':'z-paging-next'})
                  number_pages= tables.find_all('span', {'class':'z-paging-text'})
                  mpg=[]
                  for i in number_pages:
                    pg=i.text.strip().replace("/","")
                    pg=pg.strip()
                    max_page.append(pg)
                  mpg=max(max_page)
                  mpg=int(mpg)
                  if mpg < 2:
                        print "Has only 1 table"
                        for mytable in tables.find_all('div',{'class':'z-listbox-body'}):  #FIND THE TABLE
                             resulte=[]
                             print "FOUND ALL DIVS"
                             for tr in mytable.find_all('tr',{'class':'z-listitem'}):
                                   result=[]
                                   result.append((company_ruc,'@|'))
                                   for elem in tr: #FOR EACH ELEMENT IN EACH ROW I STRIP, ENCODE, AND ENTER THE TEXT INTO A LIST
                                          tabresult =[elem.text.strip().encode('utf-8')]
                                          result.append(([tabresult],"@|"))
                                   resulte.append([result])
                             with open(kardex, 'a') as f:
                                    csv.writer(f).writerows(resulte)
            
                  else:           
                    j=1
                    resultj=[]
                    while j< mpg+1:
                       print "Has Multiple Tables"
                       content = driver.page_source
                       soup = BeautifulSoup(''.join(content))
                       for tr in soup.find_all('tr',{'class':'z-listitem'}):
                             result=[]
                             result.append((company_ruc,'@'))
                             for elem in tr: #FOR EACH ELEMENT IN EACH ROW I STRIP, ENCODE, AND ENTER THE TEXT INTO A LIST
                                    tabresult =[elem.text.strip().encode('utf-8')]
                                    result.append(([tabresult],"@|"))
                             resultj.append([result])
                             with open(kardex, 'a') as f:
                                    csv.writer(f).writerow(result)
                       j=j+1
                       button_driver=driver.find_elements_by_class_name('z-paging-next')
                       ActionChains(driver).move_to_element(button_driver[table_num]).click().perform()
                       time.sleep(3)

def scrap_4(soup, sys, driver, company_ruc, ActionChains, documents):
            tab_pop_up=soup.find_all('div', {'class':'z-tabpanel'})
            for tables in tab_pop_up[2] :
                  print "Found Pop up"
                  max_page=[]
                  next_button=tables.find_all('button', {'class':'z-paging-next'})
                  next_button_c=tables.find('button', {'class':'z-paging-next'})
                  number_pages= tables.find_all('span', {'class':'z-paging-text'})
                  mpg=[]
                  for i in number_pages:
                        max_page=[]
                        pg=i.text.strip().replace("/","")
                        pg=pg.strip()
                        max_page.append(pg)
                  print "found number of pages"
                  mpg=max(max_page)
                  mpg=int(mpg)
                  if mpg < 2:
                             print "only 1 page"
                             resultj=[]
                             content = driver.page_source
                             soup = BeautifulSoup(''.join(content))
                             for tr in soup.find_all('tr',{'class':'z-listitem'}):
                                   result=[]
                                   result.append((company_ruc,'@'))
                                   for elem in tr: #FOR EACH ELEMENT IN EACH ROW I STRIP, ENCODE, AND ENTER THE TEXT INTO A LIST
                                          tabresult =[elem.text.strip().encode('utf-8')]
                                          result.append(([tabresult],"@|"))
                                   resultj.append([result])
                             with open(documents, 'a') as f:
                                    csv.writer(f).writerows(resultj)
                             print "finished one page"
                  else:           
                    j=0
                    resultk=[]
                    while j< mpg:
                       print "many pages"
                       content = driver.page_source
                       soup = BeautifulSoup(''.join(content))
                       for tr in soup.find_all('tr',{'class':'z-listitem'}): #FOR EACH LINE
                             result=[]
                             result.append((company_ruc,'@'))
                             for elem in tr: #FOR EACH ELEMENT IN EACH ROW I STRIP, ENCODE, AND ENTER THE TEXT INTO A LIST
                                    tabresult =[elem.text.strip().encode('utf-8')]
                                    result.append(([tabresult],"@|"))
                             resultk.append(result)
                       with open(documents, 'a') as f:
                              csv.writer(f).writerows(resultk)
                       resultk=[]
                       j=j+1
                       button_driver=driver.find_elements_by_class_name('z-paging-next')
                       ActionChains(driver).move_to_element(button_driver[2]).click().perform()
                       time.sleep(3)


def scrap_1(soup,sys,driver, company_ruc, ActionCHains, info_general_a, info_general_b):
      z=1
      for mytable in soup.find_all('div',{'class':'z-groupbox-3d'}):  #FIND THE TABLE
           resultc=[]
           resultd=[]
           for tr in mytable.find_all('tr',{'class':'z-row'}):
                 k=1
                 resulta=[]
                 resultb=[]
                 for td in tr.find_all('td', {'class':'z-row-inner'}):
                        for br in td.find_all('br'):
                              br.replaceWith("@")
                        if (k % 2==0):  #These are the response, meaning the text
                               values= td.contents
                               resulta.append((company_ruc, "|Total",z, "|Fila", k, "|", [values],"|"))
                        else:  #This is the description
                               desciption= td.text
                               resultb.append((company_ruc, "|Total",z, "|", k, "|", [desciption],"|"))
                        z=z+1
                        k=k+1
                 resultc.append([resulta])
                 resultd.append([resultb])
           with open(info_general_a, 'a') as f:
                  csv.writer(f).writerows(resultc)
           with open(info_general_b, 'a') as f:
                  csv.writer(f).writerows(resultd)
##
