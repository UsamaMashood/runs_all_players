import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from openpyxl import Workbook


wb = Workbook()
sheet = wb.active
sheet.title = 'Players Details'

sheet.append(['Name', 'Year', 'Matches', 'Runs', 'Team' ])
main_link = 'https://en.wikipedia.org'
fake_user = UserAgent()
responce = requests.get('https://en.wikipedia.org/wiki/List_of_One_Day_International_cricketers', headers = {'fake-user' : fake_user.chrome})

soup = BeautifulSoup(responce.text, 'lxml')
data_links = soup.find_all('dl')
teams = [team.text for team in soup.find_all('span', class_="mw-headline")]
temp_list = ['Australia', 'West Indies', 'Bangladesh', 'Zimbabwe', 'Sri Lanka', 'South Africa', 'Pakistan', 'New Zealand']

for index,links in enumerate(data_links):
    if 'XI' not in teams[index]:
        link = (main_link + links.dd.i.a['href'])
        responce = requests.get(link, headers = {'fake-user' : fake_user.chrome})

        soup= BeautifulSoup(responce.text, 'lxml')
        try:
            table = soup.find_all('table',class_='wikitable')[0].tbody
        except:
            table = soup.find_all('table')[1].tbody

        if teams[index] in temp_list:
            for temp in table.find_all('tr')[1:]:
                a = []
                for i in temp.find_all('td')[1:5]:
                    if '\n' in  i.text:
                        c=i.text.replace('\n','')
                        if '\xa0' in c:
                            a.append(c.replace('\xa0',''))
                        else:
                            a.append(c)
                    else:
                        if '\xa0' in i.text:
                            a.append(i.text.replace('\xa0',''))
                        else:
                            a.append(i.text)
                a.append(teams[index])
                sheet.append(a)


        else:
            for temp in table.find_all('tr')[2:]:
                a=[]
                try:
                    if '\n' in temp.th.text:
                        c=temp.th.text.replace('\n','')
                        if '\xa0' in c:
                            a.append(c.replace('\xa0',''))
                        else:
                            a.append(c)
                    else:
                        if '\xa0' in temp.th.text:
                            a.append(temp.th.text.replace('\xa0', ''))
                        else:
                            a.append(temp.th.text)
                    matchdata = temp.find_all('td')
                    years = matchdata[1].text + '-' + matchdata[2].text
                    matches = matchdata[3].text
                    runs = matchdata[4].text
                except:

                    matchdata = temp.find_all('td')
                    if '\n' in matchdata[1].text:
                        c=matchdata[1].text.replace('\n','')
                        if '\xa0' in c:
                            a.append(c.replace('\xa0', ''))
                        else:
                            a.append(c)
                    else:
                        if '\xa0' in matchdata[1].text:
                            a.append(matchdata[1].text.replace('\xa0', ''))
                        else:
                            a.append(matchdata[1].text)
                    years = matchdata[2].text + '-' + matchdata[3].text
                    matches = matchdata[4].text
                    runs = matchdata[5].text
                if '\n' in years:

                    a.append(years.replace('\n',''))
                else:
                    a.append(years)
                if '\n' in matches:
                    a.append(matches.replace('\n',''))
                else:
                    a.append(matches)
                if '\n' in runs:
                    a.append(runs.replace('\n',''))
                else:
                    a.append(runs)
                a.append(teams[index])
                sheet.append(a)


wb.save('player_runs_detail.xlsx')
