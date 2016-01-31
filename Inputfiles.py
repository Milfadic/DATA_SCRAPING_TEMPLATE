# -*- coding: utf-8 -*-
#Program written by Milenko A. Fadic
#April 2015, Bologna 

#########################Importing Input files###################################################

##THE PURPOSE OF THIS CODE IS TO CREATE THE LIST WHICH CONTAIN ALL INFORMATION NEEDED IN THE SCRAPING. 
      ##FIRST, I DOWNLOAD THE ORDER NAME AND DATE FROM THE FILES.
      ##I THEN CREATE LISTS OF LISTS CONTAINING THE INFORMATION
      ##I REMOVE FROM THE LIST THE ONES THAT 1) ARE NOT AVAILABLE 2) I HAVE ALREADY SCRAPED


import csv

                             
path_milenko="C:/YOUR PATH HERE "                                      
path=path_milenko

#INPUT AND OUTPUT FILE FILES 
rucsinput=    path+"INPUT/RUCS_BALANCE.txt"
rucsscraped=  path+"INPUT/RUCS_SCRAPED.txt"
rucs_noavail=path+"INPUT/RUCS_NOAVAIL.txt"


#THE PURPOSE OF THIS SECTION IS TO GET A LIST OF FILES THAT HAVE NOT BEEN SCRAPPED. IN ORDER TO DO THIS, I TAKE A LIST OF ALL FILES AND SUBTRACT IT
#FROM THE ONES THAT HAVE BEEN ALREADY SCRAPPED AND FROM THOSE THAT WERE NOT FOUND. 

# LIST  OF ALL INPUT 
    with open(rucsinput, 'r') as csvfile:
        rucs=csv.reader(csvfile)
        data = list(list(rec) for rec in csv.reader(csvfile))

        #I transform this to a list of lists. This includes all information which is the universe of POS
    with open(rucsscraped, 'r') as f:
        scrap=csv.reader(f)
        scraped= list(list(scr) for scr in csv.reader(f))
        #This data is the scrapped. It only contains the PO number, I write to this file in the last step.
    with open(rucs_noavail, 'r') as f:
        navail=csv.reader(f)
        navail= list(list(scr) for scr in csv.reader(f))
        #This data is the scrapped. It only contains the PO number, I write to this file in the last step.

allrucs=[]
scraprucs=[]

    for i in data:
        allrucs.append(i[0])
        #This creates a list of the POs that have been scrapped. 


    for i in scraped:
        try:
              scraprucs.append(i[0])
        #This creates a list of the POs that have been scrapped. 
        except:
              pass
    for i in navail:
        scraprucs.append(i[0])
        #This creates a list of the POs that have been scrapped. 
       
    remaining=list(set(allrucs)-set(scraprucs))
        #This is the remaining set. This looks at the universe I need to scrap and looks at what has already been scrap. This information is presented at the
        #begining of the program. The set command makes it so I can substract both things. 



for i in scraprucs:  #This part of the program helps removed the scrapped orders from the dataset
        a=filter(lambda data: str(i)==data[0], data) #This parts filters the element  with order and date fromr the list.
        #In essence what it does, it look at the data LIST, converts the SCRAPPEDORDERS into a STRING and compares it with DATA[0] which is the PO in the
        #DATA LIST. The part below makes the element into a list and REMOVES it from DATA so that I dont scrap it again. THIS IS A VERY IMPORTANT PART
        #The second part of the condition deals with repeated orders. 
        b=sum(a,[]) #This parts makes the element into a list 
        if b==[]:
            pass
        elif len(b)>5:
            pass
        else:
            data.remove(b)
#FINALLY I GET A LIST WITH ALL THE FILES THAT HVAE NOT YET BEEN SCRAPPED. 

print len(allrucs)
print len(scraprucs)
print len(remaining)
