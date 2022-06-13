from types import NoneType
from bs4 import BeautifulSoup
import requests
import sqlite3
import re

conn = sqlite3.connect('mojposao.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Poslovi;
DROP TABLE IF EXISTS Poslodavci;

CREATE TABLE Poslodavci (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
    naziv TEXT UNIQUE,
    adresa TEXT,
    link TEXT
);

CREATE TABLE Poslovi (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    poslodavci_id INTEGER,
    pozicija TEXT,
    lokacija TEXT,
    link TEXT,
    opis TEXT,
    kategorija INTEGER,
    zadnji_datum INTEGER
);
''')

payload = {'category':7}
r = requests.get('https://mojposao.hr/Pretraga-Poslova/?', params=payload).text


soup = BeautifulSoup(r, 'lxml')
for div in soup.find_all('li', class_= 'featured-job'):
    pozicija = div.find('span', class_="job-position").text
    pozicija = pozicija.strip()
    lokacija = div.find('span', class_='job-location')
    datum_isteka = div.time
    poslodavac = div.a.img['title']
    link_oglas = div.find('div', class_='job-data').a['href']
    

    if re.search('>.*<', str(lokacija)):
        relokacija = re.findall('>(.*)<',  str(lokacija))
        lokacija = "".join(relokacija)
        lokacija = lokacija.strip()
    if re.search('>.*<', str(datum_isteka)):
            redatum_isteka = re.findall('>(.*)<', str(datum_isteka))
            datum_isteka = "".join(redatum_isteka)
            datum_isteka = datum_isteka.rstrip()

    cur.execute('''INSERT OR IGNORE INTO Poslodavci (naziv) VALUES (?) ''', (poslodavac, ))
    cur.execute('SELECT id FROM Poslodavci WHERE naziv = ? ', (poslodavac, ))
    poslodavci_id = cur.fetchone() [0]

    cur.execute('''INSERT OR IGNORE INTO Poslovi (pozicija, lokacija, zadnji_datum, link, poslodavci_id) VALUES (?, ?, ?, ?, ?)''', (pozicija, lokacija, datum_isteka, link_oglas, poslodavci_id ))


    rr = requests.get(link_oglas).text
    ssoup = BeautifulSoup(rr, 'lxml')
    section = ssoup.find('section', id='job-detail')
    try:
        link_poslodavac = section.find('div', id='ad-employer-info').a['href']
    except: link_poslodavac = None
    try: 
        opis = section.article.div.text
    except: opis = None
    try: 
        adresa = section.find('ul', class_='details').text#iz nekog razloga sprema adresu sa razmacima ogromnima koje nebrem maknuti sa .strip(), morti/n ili neki vrag
    except: adresa = None

    cur.execute(''' UPDATE Poslodavci SET link = ? WHERE naziv = ?''', (link_poslodavac, poslodavac))

    cur.execute(''' UPDATE Poslodavci SET adresa = ? WHERE naziv = ?''', (adresa, poslodavac))

    cur.execute(''' UPDATE Poslovi SET opis = ? WHERE pozicija = ?''', (opis,pozicija ))
    conn.commit()








    print(pozicija,lokacija, datum_isteka, poslodavac, link_oglas)







