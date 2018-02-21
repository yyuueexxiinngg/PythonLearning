import requests
import re
import random
import sys
from bs4 import BeautifulSoup

def singleGacha(dct,overall,times):
    keys = {}
    for i in range(0,times):
        rand_val = random.uniform(0,overall)
        total = 0
        for k, v in dct.items():
            total += v[0]
            if rand_val <= total:
                keys[i+1] = k,v[1],v[2],v[3]
                break
    return keys

def __readGacha(type,region):
    # url = "http://cms.mihoyo.com/mihoyo/hsod2_gacha_rules/index.php/gacha/" + type + "?region=" + str(region) + "_1"
    url = "http://127.0.0.1/gacha/high/18/"
    res = requests.get(url)
    res.encoding = "utf-8"      # encode the res data in order to correctly display Chinese
    soup = BeautifulSoup(res.text,"lxml")
    tables = soup.find_all("table")     # Get all tables

    equimentsList = {}


    upTime = re.findall("\d+-\d+-\d+\d \d+:\d+:\d+",soup.text)
    startTime = upTime[0]
    endTime = upTime[1]

    total = 0       #Calculate the total probability in order to set the random range
    index = 0       #Current index, to skip the first table with overall probability

    for table in tables:
        table = BeautifulSoup(str(table),"lxml")
        if(index == 0):
            index = 1
            continue        #Skip the first table

        innerIndex = 0      #To skip the tr with th
        petPieces = 4        #To add the pieces there 6 types of pieces 4,5,6,7,8,9
        hongShi = 1     #To add the pieces of 源初虹石
        upList = []        #To check whether you reward equiments that currently in up
        godList = []


        for tr in table.find_all("tr",class_='god'):
            upList.append(tr.find_all("td")[0].text)


        index = 0       #To check cunrrent index, in order to get the full list of god equiments. The list should be ended before the first pet pieces

        for tr in table.find_all("tr"):

            if(innerIndex == 0):
                innerIndex = 1
                continue
            td = tr.find_all("td")

            # if(td[1].text == "使魔碎片" and td[0].text != "源初虹石"):      #To add pieces into the keys
            if(td[1].text == "使魔碎片"):
                index = -1
                # if(petPieces > 9):
                #     petPieces = 4
                # petName = td[0].text
                # petName += "*" + str(petPieces)
                # petPieces += 1
                equimentsList[td[0].text] = float(td[2].text[:-1]),td[1].text,False,False
                total = total + float(td[2].text[:-1])
                continue
            # elif(td[0].text == "源初虹石"):
            #     index = -1
            #     petName = td[0].text
            #     petName += "*" + str(hongShi)
            #     hongShi += 1
            #     equimentsList[petName] = float(td[2].text[:-1]),td[1].text,False,False
            #     total = total + float(td[2].text[:-1])
            #     continue

            if(index != -1):
                godList.append(td[0].text)

            total = total + float(td[2].text[:-1])

            if(td[0].text in upList):
                equimentsList[td[0].text] = float(td[2].text[:-1]),td[1].text,True,True
                                                #Probabiilty       Type     Is god  Is in uplist
            elif(td[0].text in godList):
                equimentsList[td[0].text] = float(td[2].text[:-1]),td[1].text,True,False
            else:
                equimentsList[td[0].text] = float(td[2].text[:-1]),td[1].text,False,False

    return equimentsList,total
def gacha(type,region,times):
    if(type == 'high'):
        equimentsList = __readGacha(type,region)
        weponOP = 0
        skillOP = 0
        clothOP = 0
        petOP = 0

        upList ={}
        upOP = 0
        godList = {}
        godOP = 0
        list = equimentsList[0]
        for k, v in list.items():
            if(v[3]):
                # print(k + "up内!")
                upList[k] = float(v[0])
                godList[k] = float(v[0])
                upOP += float(v[0])
                godOP += float(v[0])
            elif(v[2]):
                godList[k] = float(v[0])
                godOP += float(v[0])



            if(v[1] == "武器"):
                weponOP += v[0]
            elif(v[1] == "徽章"):
                skillOP += v[0]
            elif(v[1] == "服装"):
                clothOP += v[0]
            elif(v[1] == "使魔碎片"):
                petOP += v[0]

        print("武器总概率" + str(weponOP) + " 徽章总概率" + str(skillOP) + " 服装总概率" + str(clothOP) + " 使魔碎片总概率" + str(petOP))
        print("神器总概率" + str(godOP) + " UP内总概率" + str(upOP))

        results = singleGacha(equimentsList[0],equimentsList[1],times)

        upNum = 0
        godNum = 0
        godList = {}
        #k is the count of gacha  [0] is the name of item  [1] is the type of item  [2] is whether the equiment is god   [3] is whether it in the uplist
        for k, v in results.items():
            if(v[3]):
                upNum += 1
                godNum += 1
                godList[k] = v[0],True
                print(str(k) + " 金 " + "UP内 " + v[0] + " " + v[1])
            elif(v[2]):
                godNum += 1
                godList[k] = v[0],False
                print(str(k) + " 金 " + v[0] + " " + v[1])
            else:
                print(str(k) + " " + v[0] + " " + v[1])
        print("共无保底单抽"+ str(times) + "发 获得神器" + str(godNum) + "件 UP内" + str(upNum) + "件 UP外" + str(godNum - upNum) + "件 获得神器如下:")
        for k,v in godList.items():
            if(v[1]):
                print(str(k) + " " + v[0])
            else:
                print(str(k) + " " + v[0] +  "       UP外")


if __name__ == "__main__":
    # 0 is ReadGacha  1 is the first arg means the times of singel gacha.  2 is the times of bundle gacha   3 is the type of bundle gacha
    if(len(sys.argv)!=1):
        gacha('high',18,int(sys.argv[1]))
    else:
        gacha('high',18,20)