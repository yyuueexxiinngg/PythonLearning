import requests
import re
import random
from bs4 import BeautifulSoup

def __readGacha(type,region):
    url = "http://cms.mihoyo.com/mihoyo/hsod2_gacha_rules/index.php/gacha/" + type + "?region=" + str(region) + "_1"

    res = requests.get(url)
    res.encoding = "utf-8"      # encode the res data in order to correctly display Chinese
    soup = BeautifulSoup(res.text,"lxml")
    tables = soup.find_all("table")     # Get all tables
    overallProbability = []

    upTime = re.findall("\d+-\d+-\d+\d \d+:\d+:\d+",soup.text)
    startTime = upTime[0]
    endTime = upTime[1]

    for table in tables:
        table = BeautifulSoup(str(table),"lxml")
        for tr in table.find_all("tr",class_='gradeX'):     # Get overall probabilities (God,5 star,4 star,3 star,pet)
            overallProbability.append(float(tr.find_all("td")[1].text[:-1]))        # Store into the list   [:-1]means remove the % at the last index. Using float to prase the str to float

    godOP = overallProbability[0]
    fiveStarOP = overallProbability[1] - overallProbability[0]
    fourStarOP = overallProbability[2]
    threeStarOP = overallProbability[3]
    petOP = overallProbability[4]

    sum = godOP + fiveStarOP + fourStarOP + threeStarOP + petOP

    if(sum>100):
        difference = (sum - 100)/5
        godOP -= difference
        fiveStarOP -= difference
        fourStarOP -= difference
        threeStarOP -= difference
        petOP -= difference
    elif(sum<100):
        difference = (100 - sum)/5
        godOP += difference
        fiveStarOP += difference
        fourStarOP += difference
        threeStarOP += difference
        petOP += difference

    data = {'upTime':upTime,'overall':{'god':godOP,'fiveStar':fiveStarOP,'fourStar':fourStarOP,'threeStar':threeStarOP,'pet':petOP}}        #Store the data into dict

    return data

def gacha(type,region,times):
    data = []
    if(type == 'high'):
        data = __readGacha(type,region)
        print(data['overall'])

    #{'upTime': ['2018-02-04 00:00:00', '2018-02-06 23:59:59'], 'overall': {'god': 13.918, 'fiveStar': 24.008, 'fourStar': 28.13, 'threeStar': 36.225, 'pet': 11.223}}
    for i in range(0,times):
        _random = random.random() * 100
        if(_random < data['overall']['god']):
            print(str(i+1) + "获得一件神器!" + "  种子: " + str(_random))
        elif(_random < data['overall']['god'] + data['overall']['fiveStar']):
            print(str(i+1) +"获得一件五星装备" + "  种子: " + str(_random))
        elif(_random < data['overall']['god'] + data['overall']['fiveStar']+ data['overall']['fourStar']):
            print(str(i+1) +"获得一件四星装备" + "  种子: " + str(_random))
        elif(_random < data['overall']['god'] + data['overall']['fiveStar']+ data['overall']['fourStar'] + data['overall']['threeStar']):
            print(str(i+1) +"获得一件三星装备" + "  种子: " + str(_random))
        elif(_random < data['overall']['god'] + data['overall']['fiveStar']+ data['overall']['fourStar'] + data['overall']['threeStar']+ data['overall']['pet']):
            print(str(i+1) +"获得一个使魔碎片" + "  种子: " + str(_random))


if __name__ == "__main__":
    gacha('high',18,10)
