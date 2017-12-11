import webbrowser

import requests
import time
from bs4 import BeautifulSoup
import random_org
import random

ssid="PHPSESSID="
header={
"Host":"islands.smp.uq.edu.au",
"Connection":"keep-alive",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
"Accept":"*/*",
"DNT":"1",
"Referer":"https://islands.smp.uq.edu.au/village.php?Mahuti",#"https://islands.smp.uq.edu.au/telephone.php",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"en-US,en;q=0.8",
"Cookie":ssid#ssid
    }
def phoneAsk(text):
    # https://islands.smp.uq.edu.au/village.php?Mahuti
    return requests.get("https://islands.smp.uq.edu.au/php/talk.php?call=268768896&chat=hi",headers=header)


def getany(addr):
    # https://islands.smp.uq.edu.au/village.php?Mahuti
    return requests.get(addr,headers=header).content

def getVillagerList(villageNum):
    vlist=[]
    nullct=0
    for i in range(0,1550):
        print(i)
        ppl=getHouseMembers(i,villageNum)
        if len(ppl)==0:
            nullct+=1
            if nullct>100:
                return vlist
        else:
            for p in ppl:
                vlist.append(p)
    return ppl

#villageList=["Vardo","Bjurholm","",,,,,,,,,,,,,,,,,,]
maxVillageNum=26
def getHouse(h,v=18):
    # https://islands.smp.uq.edu.au/village.php?Mahuti
    # https://islands.smp.uq.edu.au/house.php?v=18&h=681
    """curl "https://islands.smp.uq.edu.au/house.php?v=18^&h=681" -H "DNT: 1" -H "Accept-Encoding: gzip, deflate, br" -H "Accept-Language: en-US,en;q=0.8" -H
     "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36" -H
     "Accept: */*" -H "Referer: https://islands.smp.uq.edu.au/village.php?Mahuti" -H "Cookie: PHPSESSID=gb6vgn5gisu4brfo9anl9iviu1" -H "Connection: keep-alive" --compressed"""
    header["Referer"] = "https://islands.smp.uq.edu.au/village.php?Mahuti"
    return requests.get("https://islands.smp.uq.edu.au/house.php?v={}&h={}".format(v,h),headers=header).content

def getHouseMembers(h,v=18):
    soup = BeautifulSoup(getHouse(h,v), "html.parser")
    rows = soup.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        #print(cols,cols[0].text.strip(),cols[0].text.strip()=="This house is empty")
        if len(cols)==0 or cols[0].text.strip()=="This house is empty":
            return []
        cols2 = [ele.text.strip() for ele in cols]
        cols2.append(cols[0].find("a",href=True)['href'].split("id=")[1])
        data.append([ele for ele in cols2 if ele]) # Get rid of empty values
    return data


# Note: this only runs the survey, does not collect data
def runSurvey(personid):
    # it looks like the api is /task.php?id=<ID>&code=<CODE>
    # codes so far: reportcard,survey

    #just in case, not sure if needed
    header["Referer"] = "https://islands.smp.uq.edu.au/islander.php?id={}".format(personid)
    return requests.get("https://islands.smp.uq.edu.au/task.php?id={}&code=survey".format(personid), headers=header).content

def runTask(personid,task):
    # it looks like the api is /task.php?id=<ID>&code=<CODE>
    # codes so far: reportcard,survey

    #just in case, not sure if needed
    header["Referer"] = "https://islands.smp.uq.edu.au/islander.php?id={}".format(personid)
    return requests.get("https://islands.smp.uq.edu.au/task.php?id={}&code={}".format(personid,task), headers=header).content

def getSurveyResults(personid):
    # the reply
    # nvm we just have to soup it from the websource. Just grab the divs with the class taskresultquestion and taskresultresponse
    # we'll just take the most recent answer per unique question
    source=requests.get("https://islands.smp.uq.edu.au/islander.php?id={}".format(personid),headers=header).content
    soup = BeautifulSoup(source, "html.parser")

    # Note: these should be in chronological order
    questions = soup.find_all("div", {"class": "taskresultquestion"})
    answers = soup.find_all("div", {"class": "taskresultresponse"})
    questions = [q.text.strip() for q in questions]
    answers = [a.text.strip() for a in answers]
    output={}
    for q,a in zip(questions,answers):
        if not q in output:
            output[q]=a
    return output


def inPersonChat(text):
    # https://islands.smp.uq.edu.au/alice.php?2k9yb82yaurdsvl2up5t&
    # that first value is a hardcoded constant, not sure what it does?
    # oh wait, may be served hardcoded but be specific to the person
    # particularly since no id
    pass


#returns true if person has consented
def getConsent(personid):
    # referer must be set for this to work
    # reply is either b'decline;<NAME> has declined to participate in your study.'
    # or
    header["Referer"] = "https://islands.smp.uq.edu.au/islander.php?id={}".format(personid)
    return requests.get("https://islands.smp.uq.edu.au/php/consent.php?id={}".format(personid), headers=header).content[:6]==b"accept"

# Returns
# TODO automate house count
def surveyRandoms(count, houseCount, village=18):
    idsSurveyed = []
    numberSurveyed = 0
    seed = random_org.org_randint(-(1 << 16), 1 << 16, 1)[0]
    print("SEEDED:", seed)
    random.seed(seed)
    while numberSurveyed < count:
        housenum = random.randint(0, houseCount - 1)
        #print("Next house (",housenum+1,")")
        #time.sleep(10)
        members = getHouseMembers(housenum, village)
        random.shuffle(members)
        for member in members:
            consent=getConsent(member[3])
            #print("Next person ",member[0],member[3],consent)

            if consent:
                runSurvey(member[3])
                numberSurveyed += 1
                member.append(housenum+1)
                idsSurveyed.append(member)
                print("Surveyed #{}:".format(numberSurveyed),member[0])
                break

    return idsSurveyed

def collectData(idsSurveyed):
    # print(idsSurveyed)
    for person in idsSurveyed:
        print("Collected from",  person[0])
        #print("Type:",type(person)," len:",len(person))
        sr=getSurveyResults(person[3])
        # print(sr)
        person.append(sr)
        #print("Type:",type(person)," len:",len(person))
    # print(idsSurveyed)
    return idsSurveyed

"""
Method:
use surveyRandoms to survey random people from each town.
use this list to count friends
then collect survey data
"""
surveyData2=[[35, 14, 677], [22, 7, 490], [39, 11, 806], [14, 10, 323], [57, 6, 1182], [35, 13, 711], [63, 8, 1250], [27, 12, 567], [42, 9, 926], [35, 3, 705], [57, 5, 1161], [47, 0, 1021], [40, 4, 810], [34, 1, 708], [30, 2, 652], [32, 25, 656], [25, 20, 506], [67, 18, 1464], [72, 21, 1514], [37, 23, 782], [9, 17, 222], [38, 24, 778], [34, 15, 722], [22, 16, 433], [20, 22, 437], [28, 26, 564], [39, 19, 800]]
surveyData=[[3, 14, 677], [2, 7, 490], [4, 11, 806], [1, 10, 323], [6, 6, 1182], [4, 13, 711], [6, 8, 1250], [3, 12, 567], [4, 9, 926], [4, 3, 705], [6, 5, 1161], [5, 0, 1021], [4, 4, 810], [3, 1, 708], [3, 2, 652], [3, 25, 656], [2, 20, 506], [7, 18, 1464], [7, 21, 1514], [4, 23, 782], [1, 17, 222], [4, 24, 778], [3, 15, 722], [2, 16, 433], [2, 22, 437], [3, 26, 564], [4, 19, 800]]

# Generated from project 1
RAND_IDS=['h5wwsdnvfm', 'lj8rs7xxha', 'd6t6bpejmj', 'fcnf546bbj', 'ghtsy734qh', '5yhkvmqp5q', 'gwkcjm9u2v', 'v37kbqjfyx', 'zn9f8aay3r', 'crmdsbxb96', 'eqygq27cw3', '5uvdrdmccs', 'hrslx6p23j', '6derjnyjkv', 'abbgteb329', 'jlzcx6495f', 'xwcplfz6eg', '9ajdhavctq', 'xs6d6e5ray', '5kj82pt5wj', 'vnbkh8vnxs', 'en3rvzyx5v', 'xpcw2kekcx', '2xm5p6pfz4', 'kzlf6e5rj5', 'x6ubrxvnxd', 'kdbllggrlk', 'mel5nah8dg', 'hntdfzyab2', 'th7ad29rj4', 'enunhcguc9', 'zhh2fvsbyg', '4paypqby3x', 'xfsb3j333y', 'p5kja2br8j', 'j9t7dfyk92', '2yvpdsajjf', 'mgsyw4wx56', 'xkg2pfvmzg', 'bdg9dbfxsm', 'rua6gbfg3a', 'p543rm6ds7', 'rtla3u94hm', 'kgq4thqsdd', 'g3v9sml4qs', 'ck2n9953nl', 'dtuyvzkr3y', 'rafu96nsbe', '4v7fdva3cc', '75bn42seq8', 'rv4nydnxqq', 'p47e2ma7br', '7m6h5y3e5a', 'lflxp6z4se', 's4xt3a5uag', 'k8llzzrvx9', 'nlllqrkx3b', 'wadsjzpp6q', 'nq8afgnaxg', 'zmzuhnnvje', 'fyvr7c434h', 'e9d8eqgf2d', 'vtzc96zf74', 'gbprcxkvl8', 'bpzdr6hdw8', 'pdcwklc3fb', 'bu8a4y4egt', 'wv3qjymbap', '9mapdtr4zp', 'f289lrjvxy', 'q4sz46hnsm', 'e8lwq6u2sw', '7kkgfz2uzw', 'abu9c6zyfq', 'sp28khhlmw', 'd42zzfmm9s', '3xdzkkvg88', 'stjrk6kub2', 'etlkv7xgjr', 'pfdaj8ljac', 'kcxfc3g7ps', '9yvzcphl7s', 'we5ta72u8w', 'khgsrseqze', '34sc9knrpf', 'vd2x97spn6', 't6j7e6mbzy', 'jkuhkrrg6q', 'yg97n5dxjc', 'fkzulfnhj5', 't6tzrtzc5n', 'm384kefj5g', 'ync4znwnxy', 'tjhdkbk392', 'vrf9clqnlx', '4lmgcms2za', 'f66ddeyqk8', 'ez5swl2jyp', 'bgm3he8e6f']

def runStudy():
    villdat={}
    for vill in surveyData:
        print("Surveying ",vill[1])
        villdat[vill[1]]=surveyRandoms(vill[0],vill[2],vill[1])
    repr(villdat)
    for i in range(27):
        print("Friending ",i)
        dat=villdat[i]
        for person in dat:
            person.append(len(getFriends(person[3])))
    repr(villdat)
    for i in range(27):
        print("Collecting ",i)
        dat=villdat[i]
        collectData(dat)
    return villdat

def runStudy2(villdat,samples=surveyData):
    # print("villdat:",villdat)
    for vill in samples:
        print("Surveying ",vill[1])
        villdat[vill[1]]=surveyRandoms(vill[0],vill[2],vill[1])
    # print("villdat:",villdat)
    for vill in samples:
        print("Collecting ", vill[1])
        dat = villdat[vill[1]]
        villdat[vill[1]]=collectData(dat)
    print("villdat 1",villdat[1])
    for vill in samples:
        print("Experimenting ",vill[1])
        dat=villdat[vill[1]]
        for person in dat:
            runTask(person,"energydrink")
    # print("villdat:",villdat)
    for vill in samples:
        print("Surveying ",vill[1])
        surveyRandoms(vill[0],vill[2],vill[1])
    # print("villdat:",villdat)
    for vill in samples:
        print("Collecting ", vill[1])
        dat = villdat[vill[1]]
        villdat[vill[1]] =collectData(dat)
    return villdat

def getPersonStory(personid):
    source = requests.get("https://islands.smp.uq.edu.au/islander.php?id={}".format(personid), headers=header).content
    soup = BeautifulSoup(source, "html.parser")
    eventsraw = soup.find_all("div", {"class": "timelineevent"})
    #print("LEN:",len(eventsraw))
    events = []
    for q in eventsraw:
        for n in q.text.strip().split("\n"):
            events.append(n)
    return events

def getFriends(personid):
    events=getPersonStory(personid)
    friends=[]
    for event in events:
        if "Friends with" in event:
            #print("Friend event:",event)
            friends.append(event[event.find("Friends with")+13:])
            #print(friends)
        elif "No longer friends with " in event:
            #print("Nofriend event:",event)
            try:
                friends.remove(event[event.find("No longer friends with ")+23:])
            except ValueError:
                pass
            #print(friends)
    return friends

def openPeopleLinks(a):
    for i in a:
        webbrowser.open("https://islands.smp.uq.edu.au/islander.php?id=" + i[3])

def toTSV(compstring,sv):
     for p in sv:
         print(compstring.format(*p,**p[5]))
if __name__ == "__main__":
    r = getHouse(1466)
    print(r)
    testid="cke7y4tecv"
    compstring = "Benjamin Welsh\tSouth\tMahuti\t{0}\t{"
"""
compstring="Benjamin Welsh\tSouth\tMahuti\t{4}\t{0}\tAccept\t{Are you a vegetarian?}\t{How many serves of fruit do you usually eat each day?}"
NOTES:
Non-existant houses are treated as empty.
from bs4 import BeautifulSoup
soup=BeautifulSoup(a,"html.parser")
tag=soup.find("p",{"id":"detail"})
tag.decode_contents()


>>> clm=getany("https://islands.smp.uq.edu.au/climate.php?1")
>>> len(clm)
353820
>>> soup=BeautifulSoup(clm,"html.parser")
>>> table=soup.find('table')
>>> body=table.find('tbody')
>>> len(str(body))
4
>>> body
>>> table=soup.find('table')
>>> len(table)
14159
>>> len(str(table))
353037
>>> rows = table_body.find_all('tr')
Traceback (most recent call last):
  File "<input>", line 1, in <module>
NameError: name 'table_body' is not defined
>>> rows = table.find_all('tr')
>>> len(rows)
7079
>>> data=[]
>>> for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele]) # Get rid of empty values
>>> data[1]
['01/013', '18.2', '0.0']
>>> data[0]
[]
>>> data[2]
['02/013', '18.3', '2.2']
>>> data[3]
['03/013', '20.6', '0.0']

"""
