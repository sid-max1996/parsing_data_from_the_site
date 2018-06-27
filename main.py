import time
import re
import io
import os
from selenium import webdriver

from module import *

driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://rus-motor.ru/")

mainElem = driver.find_element_by_id("m_grid");
liArr = mainElem.find_elements_by_tag_name("li")

#settings
id = 1000000*11;
itemId = 10000000*11;
appId = 2
tablePref = 'auto'
itemType = 'model'
#--------------------#

firstIter = 1
secondIter = 1
thirdIter = 1

#start index for searching info
startInd = 12+14+8+2+2+6+1+3+8+1
#lastInd = len(liArr)
lastInd = 13+14+8+2+2+6+1+3+8+1

firstDriver = webdriver.Chrome("chromedriver.exe")
secondDriver = webdriver.Chrome("chromedriver.exe")
thirdDriver = webdriver.Chrome("chromedriver.exe")

#first page main models
for mainInd in range(startInd, lastInd):
    subcat = set()
    li = liArr[mainInd]
    print('<--------------------------------->')
    print('mainCat '+str(firstIter))
    a = li.find_element_by_tag_name("a")
    content = a.get_attribute('innerHTML')
    img = a.find_element_by_tag_name("img")
    src = img.get_attribute('src')

    div = a.find_element_by_tag_name("div")
    imgName = div.get_attribute('innerHTML')
    print('mainName: ' + imgName)
    imgPath = "images/models/" + imgName + ".jpg"
    SaveImg(src, imgPath)

    liInnerHtml = li.get_attribute('innerHTML')
    content = re.sub(r'src=.*jpg',  'src="'+imgPath, content)

    #go to the next page
    href = a.get_attribute('href')
    #firstDriver = webdriver.Chrome("chromedriver.exe")
    firstDriver.get(href)

    name = imgName
    alias = re.sub(r'\s', '', name).lower()
    content = ''

    file = open(name+'.sql', 'w', encoding='utf-8')

    try:
        divContent = firstDriver.find_element_by_class_name("text_desc");
        content = divContent.get_attribute('innerHTML')
    except Exception as e:
        divContent = firstDriver.find_element_by_class_name("p_descr_t");
        pArray = divContent.find_elements_by_tag_name("p");
        for p in pArray:
            content += "<p>{innerHtml}</p>\n".format(innerHtml=p.get_attribute('innerHTML'))
        print(format(e))
    
    tupleRes = GetTitleAndDesc(firstDriver, True)
    title = tupleRes[0]
    description = tupleRes[1]

    params = CategoryParams(id, appId, name, alias, content, imgPath, title, description, 0)
    idParent = id
    insertSql = GetCategoryTemplate(tablePref, params)
    file.write(insertSql+'\n')
    id+=1

    #make children category
    directory = "images/models/"+alias

    if not os.path.exists(directory):
        os.mkdir(directory)

    #second page subcategories
    childrenTable = firstDriver.find_element_by_id("models");
    trArr = childrenTable.find_elements_by_tag_name("tr")
    trTitle = trArr[0]
    titles = GetTableTitles(trTitle)
    for i in range(1, len(trArr)):
        itemsSet = set()
        print('subCat: '+str(secondIter))
        chId = id;
        tr = trArr[i]
        tdArr = tr.find_elements_by_tag_name("td");
        tdName = tdArr[1]
        a = tdName.find_element_by_tag_name("a")
        href = a.get_attribute('href')
        chAlias = re.search(r'/[^/]*/$', href)[0].replace('/', '')
        chName = a.get_attribute('innerHTML')
        if(chName not in subcat):
            subcat.add(chName)
            tdImg = tdArr[0]    
            tdImgPath = directory+'/'+chAlias+'.jpg';
            try:
                img = tdImg.find_element_by_tag_name("img")
                src = img.get_attribute('src')
                SaveImg(src, tdImgPath)
            except Exception as e:
                print('No Img')
                tdImgPath = None

            #all subcategory td in table get content
            textDataCh = '';
            try:
                for tdInd in range(len(tdArr)):
                    text = tdArr[tdInd].get_attribute('innerHTML')
                    text = text.strip()
                    text = re.sub(r'href=.*"',  'href="/'+alias+'/'+chAlias+'"', text)
                    if tdImgPath is not None:
                        text = re.sub(r'src=.*jpg',  'src="'+tdImgPath, text)
                    text = '<div>{title}: {innerHtml}</div>'.format(title=titles[tdInd], innerHtml=text)
                    textDataCh += text
            except Exception as e: 
                print(format(e))
            #-----------------------------------------------#
        
            #secondDriver = webdriver.Chrome("chromedriver.exe")
            secondDriver.get(href)
            tupleRes = GetTitleAndDesc(secondDriver, True)
            chTitle = tupleRes[0]
            chDesc = tupleRes[1]

            params = CategoryParams(chId, appId, chName, chAlias, textDataCh, tdImgPath, chTitle, chDesc, idParent)
            insertSql = GetCategoryTemplate(tablePref, params)
            file.write(insertSql+'\n')

            #third page items
            try:
                itemTable = secondDriver.find_element_by_class_name("dv_list");
                itemTrArr = itemTable.find_elements_by_tag_name("tr")
                trTitle = itemTrArr[0]
                titles = GetTableTitles(trTitle)
                #thirdDriver = webdriver.Chrome("chromedriver.exe")
                for i in range(1, len(itemTrArr)):
                    print('item: ' + str(thirdIter) + ' sub: ' + str(secondIter) + ' main: ' + str(firstIter))
                    itemTr = itemTrArr[i]
                    itemTdArr = itemTr.find_elements_by_tag_name("td");
                    itemTdName = itemTdArr[0]
                    a = itemTdName.find_element_by_tag_name("a")
                    href = a.get_attribute('href')
                    itemAlias = re.search(r'/[^/]*/$', href)[0].replace('/', '')
                    itemName = a.get_attribute('innerHTML')

                    if itemName not in itemsSet:
                        itemsSet.add(itemName)
                        #all item td in table get content
                        textDataItem = ''
                        for tdInd in range(len(itemTdArr)):
                            text = itemTdArr[tdInd].get_attribute('innerHTML')
                            text = text.strip()
                            text = re.sub(r'href=.*"',  'href="/'+alias+'/'+chAlias+'/'+itemAlias+'"', text)
                            text = '<div>{title}: {innerHtml}</div>'.format(title=titles[tdInd], innerHtml=text)
                            textDataItem += text
                         #-----------------------------------------------#
        
                        thirdDriver.get(href)
                        tupleRes = GetTitleAndDesc(thirdDriver, True)
                        itemTitle = tupleRes[0]
                        itemDesc = tupleRes[1]

                        #items write
                        params = ItemParams(itemId, appId, itemType, itemName, itemAlias, textDataItem, itemTitle, itemDesc, chId)
                        insertSql = GetItemTemplate(tablePref, params)
                        file.write(insertSql+'\n')

                        #link item cat
                        insertSql = GetItemCatLinkTemplate(tablePref, chId, itemId)
                        file.write(insertSql+'\n')

                        itemId+=1
                    thirdIter+=1
                #thirdDriver.quit()
                    #------------#
            except Exception as e: 
                thirdIter+=1
                print(format(e))
            #----------third page items end-------------#
            thirdIter = 1
        

            #secondDriver.quit()
            secondIter+=1
            id+=1
            #----------second page subcategories end-------------#
        else:
            thirdIter = 1
            secondIter+=1
    secondIter = 1
    #firstDriver.quit()
    firstIter+=1
    file.close()
    print('-------------------------------')
    print(name+'.sql complite!!!')
#----------first page main models end-------------#

driver.quit();
firstDriver.quit()
secondDriver.quit()
thirdDriver.quit()

print('Complite!!!')