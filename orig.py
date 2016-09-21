import urllib2
from bs4 import BeautifulSoup
# import pymysql.cursors
# import datetime
# import os
#
# connection = pymysql.connect(host='127.0.0.1',
#                              user='root',
#                              password='',
#                              db='football',
#                              charset='utf8mb4',
#                              cursorclass='pymysql.cursors.DictCursor')

url = "http://www.transfermarkt.com"
leagues = ["/premier-league/startseite/wettbewerb/GB1",
    "/premier-league/startseite/wettbewerb/GB2",
    "/premier-league/startseite/wettbewerb/GB3",
    "/laliga/startseite/wettbewerb/ES1",
    "/serie-a/startseite/wettbewerb/IT1",
    "/1-bundesliga/startseite/wettbewerb/L1",
    "/ligue-1/startseite/wettbewerb/FR1",
    "/liga-nos/startseite/wettbewerb/PO1",
    "/premier-liga/startseite/wettbewerb/RU1",
    "/eredivisie/startseite/wettbewerb/NL1"]

teams = []

def openpage(page):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    page = opener.open(url+league)
    soup = BeautifulSoup(page, "lxml")
    return soup;

def scrapeleague(link):
    soup = openpage(link);
    table = soup.find('table', {'class':'items'})

    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 2:
            for item in tds:
                print item.text

    # anchors = soup.findAll("a", {"class": "vereinprofil_tooltip"})
    # for tag in anchors:
    #     print tag['href']

for x in range(2000,2016):
    x = str(x);
    for league in leagues:
        leagueurl=url+league+'/plus/?saison_id='+x
        print "scrapping: "+leagueurl
        scrapeleague(leagueurl)
