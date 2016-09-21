import urllib2
from bs4 import BeautifulSoup
import pymysql.cursors
import datetime
import os

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

connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='',
                             db='football',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def openpage(page):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    page = opener.open(page)
    soup = BeautifulSoup(page, "lxml")
    return soup

def scrapeleague(link):
    try:
        with connection.cursor() as cursor:
            soup = openpage(link);
            table = soup.find('table', {'class':'items'})

            for tr in table.find_all('tr'):
                tds = tr.find_all('td')
                if len(tds) > 2:
                    sql = '''
                            INSERT INTO teams(
                                fullname,
                                shortname,
                                squad,
                                age,
                                foreignplayers,
                                totmarketval,
                                marketval)
                            VALUES(%s, %s, %s, %s, %s, %s, %s)
                        '''

                    fullname = tds[1].text
                    shortname = tds[2].text
                    squad = tds[3].text
                    age = tds[4].text
                    foreignplayers= tds[5].text
                    totmarketval = tds[6].text
                    marketval = tds[7].text

                    try:
                        cursor.execute(sql, (fullname, shortname, squad, age, foreignplayers, totmarketval, marketval))
                        connection.commit()
                    except (pymysql.err.InternalError, pymysql.err.DataError) as e:
                        print e
                        continue

            print 'Done'

    finally:
        "Finished"

for x in range(2000,2016):
    for league in leagues:
        leagueurl=url+league+"/plus/?saison_id="+str(x)
        print "scrapping: "+leagueurl
        scrapeleague(leagueurl)
