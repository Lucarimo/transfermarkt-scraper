import urllib2
from bs4 import BeautifulSoup

def openpage(page):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    page = opener.open(page)
    soup = BeautifulSoup(page, "lxml")
    return soup;

def scrapeteams(team):
    soup = openpage(team);
    table = soup.find('table', {'class':'items'})

    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) > 2:
            for item in tds:
                print item.text
scrapeteams("http://www.transfermarkt.com/manchester-united/startseite/verein/985/saison_id/2016")






    # anchors = soup.findAll("a", {"class": "vereinprofil_tooltip"})
    # for tag in anchors:
    #     print tag['href']
