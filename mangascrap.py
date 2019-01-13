import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import os

urlpage = 'https://kissmanga.com/Manga/Saenai-Kanojo-no-Sodatekata-Koisuru-Metronome/Vol-001-Ch-001--v002---How-to-soothe-the-sleepy-her?id=209047' 
splitedString = urlpage.split('/')
seperator = "/"
title = splitedString[-2]
maintileurl = "".join(splitedString[:-1])
mainPath = "./manga"
mangaPath = mainPath+"/"+title
chapterPath = mangaPath+"/"+"chapter" 
#add chapter index line 52

# #create path
if not os.path.exists(mainPath):
    os.makedirs(mainPath)

if not os.path.exists(mangaPath):
    os.makedirs(mangaPath)


# # run firefox and selenium
driver = webdriver.Firefox(executable_path = '/home/nearih/python/webScraping/geckodriver')
driver.get(urlpage)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
time.sleep(9)
results = driver.find_elements_by_xpath("//*[@id='containerRoot']//*[contains(@style,'width: 95%; text-align: center; margin: auto')]//*[@id='divImage']")
chapterhtml = driver.find_elements_by_xpath("//*[@id='containerRoot']//*[contains(@style,'width: 95%; text-align: center; margin: auto')]//*[@class='selectChapter']")
print('Number of results', len(results))
print('Number of chapterhtml', len(chapterhtml))

if len(results) == 0:
    print ("timeout")

# #get chapter list
chapterLinkList = []
chapterClass = chapterhtml[0].text
chapterOption = chapterhtml[0].find_elements_by_tag_name('option')
for chapter in chapterOption:
    chapterNameID = chapter.get_attribute("value")
    chapterLinkList.append(chapterNameID)
driver.close()

# #get each chapter
# #add chapter index here ex [:4]
for j in range(0,len(chapterLinkList)-1):
    driver = webdriver.Firefox(executable_path = '/home/nearih/python/webScraping/geckodriver')
    print (maintileurl+chapterLinkList[j])
    driver.get(maintileurl+"/"+chapterLinkList[j])
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    time.sleep(9)
    results = driver.find_elements_by_xpath("//*[@id='containerRoot']//*[contains(@style,'width: 95%; text-align: center; margin: auto')]//*[@id='divImage']")

# # looking for each chapter
    data = []
    for result in results:
        listTagP = result.find_elements_by_tag_name('p')
        for tagP in listTagP:
            link = tagP.find_element_by_tag_name('img')
            img_link = link.get_attribute("src")
            data.append(img_link)

    # # save to specific path
    # # create folder for each chapter

    for i in range(0,len(data)-1):
        print(i)
        chapterPath = mangaPath+"/"+str(splitedString[-1])
        if not os.path.exists(chapterPath):
            os.makedirs(chapterPath)
        filenamePath = os.path.join(chapterPath,str(i))
        urllib.request.urlretrieve(data[i],filenamePath)
    print ("next")
    driver.close()
print ("done")


