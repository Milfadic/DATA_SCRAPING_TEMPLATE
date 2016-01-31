# -*- coding: utf-8 -*-
#Program written by Milenko A. Fadic
#May, Bologna 
#Data Scraping of sample website
#Note, this is for illustrative purposes only. The code does not include the website to be scrapped. 


#Importing libraries needed
     
      #IMPORTING THE FUNCTIONS AND THE FILES FROM OTHER PYTHON SCRIPTS IN SAME LOCAL DIRECTORY 
      import Inputfiles_BALANCE as J
      import Functions_BALANCE_Working_version as G
      #See note above 

      import sys
      sys.path.append("YOUR LOCAL PATH")
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
      from selenium.webdriver.common.action_chains import ActionChains
      import html5lib
      import csv
      import time
      from datetime import datetime
      from datetime import date
      from time import gmtime, strftime

#Defining Key variables
      #Sleep time for delays
      time_sleep_low_rate=15
      time_sleep_high_rate=10
      time_sleep_date_finder=2
      time_sleep_internet_failure=0  #When I can't 5 five consecutive orders, I make the program sleep this much to wait for better interent
      wait = WebDriverWait(driver,15)  #This is how long I am willing to wait for SERCOP server

      #This is the site to be scrapped. 
      sitescrap='http://YOUR SITE HERE'

      #Choose your browser. Note selenium has to be updated to match the latest browser
      #driver = webdriver.Chrome()
      driver = webdriver.Firefox()

      #Define my driver
      action = webdriver.ActionChains(driver)

      #Fail is used for error handling 
      fail=0


#Opening the driver. See function script
G.opendriver(driver, sitescrap)

#Setting path. If you work in multiple systems, you can have multiple paths and just define them 

path_milenko="YOUR LOCAL PATH"       
path=path_milenko


#OUTPUT PATH FILES. This defined where is the output going to go. 
info_general_a=     path+"OUTPUT/info_a.txt"
info_general_b=     path+"OUTPUT/info_b.txt"
admin_a=              path+"OUTPUT/admin_a.txt"
kardex=             path+"OUTPUT/kardex.txt"
documents=          path+"OUTPUT/docs.txt"


for i in  J.remaining: #Starts the loop for all RUCS: See J. to see how the loops are calculated. 
      success_a=0; success_b=0; success_c=0; success_d=0
      success_buscar=0
      try:       
##########1-----------
            G.hourpeak(time_sleep_low_rate, time_sleep_high_rate ) #Function to determine wait
            failure=0
            company_ruc=str(i) #Convert RUC to string 
            print company_ruc
            j=0  
            try:  #Wait for the element to appear
                  wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@type='radio']")))  #Clicking first on the Radio Button
            except:
                  print "UNABLE TO CLICK LINK, WRITING INTO NOT FOUND, REFRESHING DRIVER"
                  print sys.exc_info() #Print any errors 
                  driver.set_page_load_timeout(30)
                  while failure<10: #If it does not work, then try 10 times. After every fail wait 1 minute. 
                      try:
                              print "REFRESHING FOR THE TIME NUMBER" ,failure
                              driver.refresh()
                              time.sleep(60)
                              driver.find_elements_by_xpath("//*[@type='radio']")
                              break
                      except: #If not, then try to refresh the browser. 
                              print "TIME OUT"
                              time.sleep(9)
                              failure=failure+1
                              if failure==9:
                                    driver.set_page_load_timeout(60)
                                    try:
                                          driver.refresh()
                                    except:
                                          failure=1              
            finally: #Find the all radio bottoms and click the second one 
                  pass
            for i in driver.find_elements_by_xpath("//*[@type='radio']"):
                 j=j+1
                 if (j==2):
                       i.click()
                 else:
                       pass
            time.sleep(4) 
            input_ruc=driver.find_element_by_class_name('z-combobox')
            ActionChains(driver).move_to_element(input_ruc).send_keys(company_ruc).send_keys(webdriver.common.keys.Keys.ESCAPE).perform()
            #I have a unique ID, I search for that unique ID. Becuase of autofill, I have to first escape and then hit search 
            time.sleep(3)
            #Need to escape because of the search recommendation which dont allow me to clcik 
            buscar= driver.find_element_by_class_name('z-button-cm') #Look for search bottom. 
            buscar.click() #click on search 

            success_buscar=1 #Program knows part 1 is succesful 
            #IF THE ESEARCH IS SUCCESSFUL, I WILL GO TO ANOTHER SCREEN. THEN I WAIT FOR THE TABS TO APPEAR. I CLICK ON THEM AND THEN SCRAP THEIR CONTENT. 
            wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,'Información General')))    #This wait for the order to appear 
            success_buscar=2
            #LOOK FOR TAB 
            docs_online= driver.find_element_by_partial_link_text('Información General')
            print "Información General Found, Entering"
            #CLICK ON THEM 
            ActionChains(driver).move_to_element(docs_online).click().perform()
            time.sleep(10)
            content = driver.page_source
            #DEFINE SCRAPPING AREA
            soup = BeautifulSoup(''.join(content))
            #SCRAP ALL INFO 
            G.scrap_1(soup,sys,driver, company_ruc, ActionChains, info_general_a, info_general_b)
            print "Scrapped Inf. Done , Now exiting"
            success_a=1
            time.sleep(10)
            #FIND EXIT 
            exit_button= driver.find_element_by_class_name ('z-window-modal-close')
            #CLICK ON EXIT 
            exit_button.click()

#A SIMILAR PROCEDURE IS DONE FOR 2 MORE TABS. THEY ARE THE SAME PROCEDURE AS THE FIRST TAB WHICH IS WHY THEY ARE NOT ANNOTATED. 
                          
                        ########TAB 2-----------
                        ##            time.sleep(6)
                        ##            admin= driver.find_element_by_partial_link_text('NAME OF TAB')
                        ##            ActionChains(driver).move_to_element(admin).click().perform()
                        ##            print "Found, Entering"
                        ##            time.sleep(7)
                        ##            content = driver.page_source
                        ##            soup = BeautifulSoup(''.join(content))
                        ##            G.scrap_2(soup, sys, driver, company_ruc, ActionChains, admin_a)
                        ##            print "Done , Now exiting"
                        ##            success_b=1
                        ##            exit_button= driver.find_element_by_class_name ('z-window-modal-close')
                        ##            exit_button.click()
                        ##            time.sleep(3)
                        ######TAB 3-----------
                        ##            wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,'Kardex')))    #This wait for the order to appear
                        ##            Kardex= driver.find_element_by_partial_link_text('Kardex')
                        ##            ActionChains(driver).move_to_element(Kardex).click().perform()
                        ##            print "Kardex found, Entering"
                        ##            time.sleep(5)
                        ##            content = driver.page_source
                        ##            soup = BeautifulSoup(''.join(content))
                        ##            G.scrap_3(soup, sys, driver, company_ruc, ActionChains, kardex)
                        ##            exit_button= driver.find_element_by_class_name ('z-window-modal-close')
                        ##            exit_button.click()
                        ##            print "Scrapped Kardex , Now exiting"

############TAB 4-----------
            #THIS LAST TAB IS INTERESTING BECAUSE IT OPENS A NEW WINDOW. AS A RESULT, YOU HAVE TO SWITCH TO THE OPENED WINDOW IN ORDER TO EXECUTE. 
            
            print "Finding LAST TAB"
            time.sleep(5)
            wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,'TAB NAME HERE')))    #CLICK ON LAST TAB. A NEW WINDOW WILL OPEN 

            parent= driver.current_window_handle #HERE IS WHERE YOU DEFINE THE PARENT WINDOW
            docs= driver.find_element_by_partial_link_text('TAB NAME HERE')
            ActionChains(driver).move_to_element(docs).click().perform() #CLICK ON THE LINK THAT WILL OPEN THE WINDOW
      
            success_c=1 #THIS SHOWS THAT THE WINSOW WAS OPENED

            time.sleep(7)  
            pop_up=driver.window_handles #YOU DEFINE THE WINDOWS THAT ARE OPENED
            pop_upa=pop_up[1] #[1] SHOWS THAT THIS IS THE POP-POP AS 0 WAS THE PARENT 
            driver.switch_to_window(pop_upa) #SWITCH TO THE POP-UP WINDOW 

            success_c=2
            
            time.sleep(6)
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME ,'z-tab-text'))) #WAT FOR ELEMENT
            tab=driver.find_elements_by_class_name('z-tab') 
            ActionChains(driver).move_to_element(tab[2]).click().perform() #GO TO THIRD TAB 
            content = driver.page_source
            soup = BeautifulSoup(''.join(content)) #DEFINE SCRAPING AREA
            print "going into scrap"
            G.scrap_4(soup, sys, driver, company_ruc, ActionChains, documents) #SCRAP 
            print "scrapped"
            success_d=2

            driver.close() #CLOSE POP 

            success_d=1

#THIS PART HANDLES THE EXCEPTIONS 
      except:  #IF I OPENED THE POP UP THEN....SWITCH TO MAIN, AND GO BACK
            print "ON EXCEPTIONS, THERE WAS A PROBLEM FOUND"
            fail=fail+1
            print sys.exc_info()
            if fail==10: #IF THERE WERE 10 EXEPCIONS THEN WRITE IT IN TH LOG AND  OPEN A NEW BROWSER AND START PROCESS AGAIN. 
                  print "FAIL WAS 5, #A"
                  try:
                        sitescrap=''
                        driver = webdriver.Chrome()
                        with open(J.rucs_noavail, 'a') as f:
                              csv.writer(f).writerow([company_ruc])
                        wait = WebDriverWait(driver,20)  #This is how long I am willing to wait for SERCOP server
                        action = webdriver.ActionChains(driver)
                        G.opendriver(driver, sitescrap)
                  except:
                        G.opendriver(driver, sitescrap)
                  finally:
                        print "New Driver should be open"
                        fail=0
                        pass
            elif success_d==1 or (success_b==1 and success_c==1)or success_a==1 or (success_buscar==2 and success_buscar==0): #B #IN CASE I FIND A PROBLEM AT THE 4TH STAGE, I PRINT MISTAKE, WRITE INTO FILE AND GO BACK TO INITIAL SCREEN
                  print "#B PROBLEM AFTER SCRAPING DOCUMENT, WRITTEN ORDER IN SCRAPED, GOING BACK "
                  print sys.exc_info()
                  with open(J.rucsscraped, 'a') as f:
                              csv.writer(f).writerow([company_ruc])
                  try:
                        driver.back()
                  except:
                        fail=fail+1

#THE FOLLOWING ARE THE SAME PROCEDURE BUT CAPTURE ERRORS AT DIFFERENT STAGES. THE ONLY DIFFERENCE IS FOR THE POP-UP WINDOW FOR WHICH I HAVE TO FIRST GO BACK. 

            elif (success_c==2 and success_d==2):#C
            #SUCCESS_C=2 CAPTURES IF THE POPO UP WAS OPEN. IF SO, CLOSE THE POP UP, SWITCH TO DRIVER AND GO 
                  print "#C CLOSING POP UP WINDOW"
                  driver.close()
                  print "Switched to Main"
                  try:
                        driver.switch_to_window(pop_up[0])
                        print sys.exc_info()
                        print "GOING BACK TO MAIN PAGE"
                        driver.back()
                  except:
                        with open(J.rucs_noavail, 'a') as f:
                              csv.writer(f).writerow([company_ruc])
                        fail=fail+1
           
            elif success_buscar==1:#F
                  try:
                        print "#F RUC NOT FOUND IN SEARCH"
                        with open(J.rucs_noavail, 'a') as f:
                                    csv.writer(f).writerow([company_ruc])
                        driver.refresh()
                        time.sleep(5)
                  except:
                        fail=fail+1
            else:
                  with open(J.rucs_noavail, 'a') as f:
                              csv.writer(f).writerow([company_ruc])
                  try:
                        driver.refresh()
                  except:
                        pass
 
      else:
            
            try:
                        with open(J.rucsscraped, 'a') as f:
                              csv.writer(f).writerow([company_ruc])
                        print "ALL PAGE HAVE BEEN SCRAPPED, POP UP WINDOW CLOSED, WRITING INTO LOG"
   
            except:
                        print "ALL PAGES SCRAPED, BUT THERE WAS A PROBLEM "
                        print sys.exc_info()
                        try:
                              driver.quit()
                              print "DRIVER CLSOED"
                              time.sleep(30)
                              G.opendriver(driver, sitescrap)
                        except:
                              pass

            finally:
                  try:
                        driver.switch_to_window(pop_up[0])
                        driver.back()
                  except:
                        pass

