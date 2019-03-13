import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import datetime
import csv
import urllib

url = "https://www.518.com.tw/job-index.html"
resp = requests.get(url)
resp.encoding = 'utf-8' # encoded with format utf-8 for chinese character
soup = BeautifulSoup(resp.text, 'lxml')

# parse colname 
rows = soup.find_all('ul', class_='all_job_hover')
# get strings and convert into list
colname = list(rows.pop(0).stripped_strings) 

#parse rest content info
contents=[]
u=1

for row in rows:
    for i in range(3):
        bigtitle=row.find_next('li',attrs={'class':'title'})#標題外層
        title=bigtitle.find_next('span')#標題內層的標題
        url=title.find_next('span')#徵才連結

        bbarea=url.find_next('li',attrs={'class':'area'})#職位地區最外層
        barea=bbarea.find_next('span')#職位地區外層
        area=barea.find_next('span')#職位地區外層
        area1=area.find_next('span')#縣市?
        area2=area1.find_next('span')#地區?

        exp=area2.find_next('li',attrs={'class':'exp'})#經歷
        edu=exp.find_next('li',attrs={'class':'edu'})#學歷
        bdate=edu.find_next('li',attrs={'class':'date'})#刊登時間?
        date=bdate.find_next('span')#刊登時間
        bcompany=date.find_next('li',attrs={'class':'company'})#公司?
        company=bcompany.find_next('a')
        sumbox=company.find_next('li',attrs={'class':'sumbox'})#薪資&工作內容 外層
        salary=sumbox.find_next('p')#薪資
        content=salary.find_next('p')#工作內容

        c=[title.string, url.string, area1.string, area2.string, exp.string,edu.string,date.string,company.string,salary.string,content.string]
        print(c)
        contents.append(c)
        df=pd.DataFrame(contents,columns = ["徵才職位", "徵才連結", "縣市", "地區", "經歷", "學歷", "刊登時間", "公司", "薪資", "工作內容"])
        df.head()
        url=f"https://www.518.com.tw/job-index-P-{u}.html?i=1&am=1"

cwd=os.getcwd()
timestamp=datetime.datetime.now()
timestamp=timestamp.strftime('%Y%m%d')
filename=os.path.join(cwd,'518{}.csv'.format(timestamp))
df.to_csv(filename,index=False, encoding='utf_8_sig')
print('Save csv to {}'.format(filename))

