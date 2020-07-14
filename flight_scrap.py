import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
import sys
import bs4 as bs
import urllib.request
def dataretriver():
    import requests
    res=requests.get('https://en.wikipedia.org/wiki/List_of_international_airports_by_country')
    from bs4 import BeautifulSoup as bs
    soup = bs(res.content,"html.parser")
    tables = soup.findAll("table",class_='wikitable')
    data=[]
    for table in tables:
        for tag in table.find_all('tr'):
            lis=[]
            for tag2 in tag.find_all('td'):
                lis.append(''.join([i for i in tag2.contents[0]]))
            lis=lis[:3]
            if len(lis)==3:
                lis[-1]=lis[-1][:-1]
            data.append(lis)
    data.pop()
    fp=open('data.csv','w', encoding="utf-8")
    for i in data:
        new=[]
        for j in i:
            s1=j.replace(',',' ')
            new.append(s1)
        if len(new)==3:   
            s=','.join(new)
            s+='\n'
            fp.write(s)
    fp.close()
"""Driver Code"""  
codes=dict()
f=open("datamod.csv",'r',encoding="utf-8")
lis = [line.split(',') for line in f]        
for i,x in enumerate(lis):
    codes[x[0].lower()]=x[-1][:-1]
f.close()
src=input('Enter Source City:').lower()
dest=input('Enter Destination City:').lower()
date1 = input('Enter the Date in DD/MM/YYYY:')
dd,mm,yy = date1.split('/')
from datetime import *
tdy = datetime.strptime(date1, '%d/%m/%Y')
yy1,mm1,dd1 = str(date.today()).split('-')
status = (datetime(int(yy),int(mm),int(dd))>datetime(int(yy1),int(mm1),int(dd1)))
if status:
    print(' '*50+'Loading....')
    main=codes[src]+'-'+codes[dest]
    url="https://www.goibibo.com/flights/air-"+main+"-"+yy+mm+dd+"--1-0-0-E-D/"
    class Client(QWebEnginePage):
        def __init__(self,url):
            global app
            self.app = QApplication(sys.argv)
            QWebEnginePage.__init__(self)
            self.html = ""
            self.loadFinished.connect(self.on_load_finished)
            self.load(QUrl(url))
            self.app.exec_()

        def on_load_finished(self):
            self.html = self.toHtml(self.Callable)

        def Callable(self,data):
            self.html = data
            self.app.quit()

    if __name__ == '__main__':
        client_response = Client(url)
        from collections import defaultdict
        soup = BeautifulSoup(client_response.html,features="html.parser")
        d = defaultdict(str)
        data = []
        for tag in soup.find_all('div'):
            if tag.get('class')==['dF', 'width100', 'alignItemsCenter']:
                if 'Layover' not in d.keys():
                    d['Layover'] = 'Nil'
                data.append(d)
                d = defaultdict()
                d['Name'] = tag.text
            elif tag.get('class')==['col-md-3', 'col-sm-3', 'col-xs-3', 'padL0', 'fGS0']:
                s=''
                for i in str(tag.text)[::-1]:
                    if i!=':' and not i.isdigit():
                        break
                    s+=i
                s=s[::-1]
                d['Departure Time'] = s
            elif tag.get('class')==['ico15', 'fb', 'txtCenter', 'quicks', 'padT5']:
                d['Duration'] = tag.text
            elif tag.get('class')==['col-md-3', 'col-sm-3', 'col-xs-3', 'fGS0', 'width29']:
                s=''
                k = str(tag.text)
                for i in range(len(k)):
                    if not k[i].isdigit():
                        continue
                    s+=k[i:]
                    break
                d['Arrival Time'] = s
            elif tag.get('class')==['col-md-7', 'padL0', 'padR10', 'justifyBetween', 'flexCol']:
                d['Cost'] = str(tag.text)[1:]
            elif tag.get('class')==['dF', 'width100', 'greyLt', 'ico11', 'padT5', 'padB10']:
                d['Layover'] = str(tag.text).replace('Layover - ','')
        data = data[1:]
        import pandas as pd
        data = pd.DataFrame(data)
        print(data.to_string())
else:
    print('Oops!!! Check For Future Flight Schedules...?')
