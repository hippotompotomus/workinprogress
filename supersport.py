import os
import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

conn = sqlite3.connect('supersport.sqlite')
cur = conn.cursor()

cur.executescript('''

DROP TABLE IF EXISTS Drzave;
DROP TABLE IF EXISTS Oklade;

CREATE TABLE Drzave (

	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	drzava TEXT UNIQUE

);

CREATE TABLE Oklade (

	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	drzava_id INTEGER,
	oklada TEXT,
	jedan INTEGER,
	X INTEGER,
	dva INTEGER

);
''')



os.environ['PATH'] += 'C:\\Users\\PC\\Desktop\\python'
driver = webdriver.Chrome()
driver.get('https://supersport.hr')
driver.implicitly_wait(2)

main_count = 1
secondary_count = 1
tertiary_count = 1	

wait = WebDriverWait(driver, 10)

driver.find_element(By.XPATH, value='//*[@id="mount-naslovnica"]/div/div[1]/div[1]/div/div[2]/a[2]').click() #supersport/sports
driver.find_element(By.XPATH, value='//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div[3]/span').click()#/sports/nogomet
time.sleep(3)
nogomet = driver.find_elements(By.XPATH, value='//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/div[1]/child::div')

print(len(nogomet))#iz nekog razloga nije sve zemlje uhvatil
for i in range(len(nogomet)):

	drzava_button = driver.find_element(By.XPATH, value=f'//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/div[1]/div[{main_count}]/div')
	cur.execute('''INSERT INTO Drzave (drzava) VALUES (?) ''', (drzava_button.text, ))
	cur.execute('''SELECT id FROM Drzave WHERE drzava = ? ''', (drzava_button.text, ))
	drzava_id = cur.fetchone()[0]

	wait.until(
		EC.element_to_be_clickable(drzava_button)
		)	#ovaj EC je realno beskoristan tu jer tu i tam baca bug da  element click intercepted: Element is not clickable at point (98, 760). Other element would receive the click:
	time.sleep(2)						
	drzava_button.click()
	time.sleep(2)#nekad ne loada duljinu tablice kak spada
	država_tablice = driver.find_elements(By.XPATH, value='//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/descendant::table')
	print('država tablice', len(država_tablice))
	if len(država_tablice) > 0: 
		for i in range(len(država_tablice)):
			broj_redova = driver.find_elements(By.XPATH, value =f'//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[{secondary_count}]/div/table/tbody/child::tr')
			print('broj redova',len(broj_redova))
			try:#nki weird bug de broj tablice krivo očita (vjerojatno nisu formatirali tablice jednako sve)
				x_check = driver.find_element(By.XPATH, value=f'//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[{secondary_count}]/div/table/thead/tr/td[4]').text
															
				if x_check == 'x' or x_check == 'X':			

					for i in range(len(broj_redova)):
						if range(len(broj_redova)) == 0:#rješva bug de registrira više tablica nego kaj ima
							continue
						else:
							try:
								try:

									first_team = driver.find_element(By.XPATH, value=f'//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[{secondary_count}]/div/table/tbody/tr[{tertiary_count}]/td[2]/div/div[1]/span/span[1]').text
									second_team = driver.find_element(By.XPATH, value=f'//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[{secondary_count}]/div/table/tbody/tr[{tertiary_count}]/td[2]/div/div[1]/span/span[3]').text
									matchup = str(first_team) + '-' + str(second_team)

								except:#bedaki su negde stavili sve u jedan span

									first_team = driver.find_element(By.XPATH, value=f'//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[{secondary_count}]/div/table/tbody/tr[{tertiary_count}]/td[2]/div/div[1]/span').text
									matchup = first_team



								kvota1 = driver.find_element(By.XPATH, value = f'//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[{secondary_count}]/div/table/tbody/tr[{tertiary_count}]/td[3]/div').text
								kvotax = driver.find_element(By.XPATH, value = f'//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[{secondary_count}]/div/table/tbody/tr[{tertiary_count}]/td[4]/div').text
								kvota2 = driver.find_element(By.XPATH, value = f'//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[{secondary_count}]/div/table/tbody/tr[{tertiary_count}]/td[5]/div').text
								
								
							except: #ako je live onda se pomiču elementi
								live_check = driver.find_element(By.XPATH, value=f'//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[{secondary_count}]/div/table/tbody/tr[{tertiary_count}]/td[2]/table/tbody/tr').text
								#live check je trenutno beskoristan realno, bacal je traceback na if
								first_team = driver.find_element(By.XPATH, value=f'//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[{secondary_count}]/div/table/tbody/tr[{tertiary_count}]/td[3]/table/tbody/tr[1]/td/div').text																
								second_team = driver.find_element(By.XPATH, value=f'//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[{secondary_count}]/div/table/tbody/tr[{tertiary_count}]/td[3]/table/tbody/tr[2]/td/div').text
								matchup = str(first_team) + '-' + str(second_team)

								kvota1 = driver.find_element(By.XPATH, value = f'//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[{secondary_count}]/div/table/tbody/tr[{tertiary_count}]/td[8]/div').text
								kvotax = driver.find_element(By.XPATH, value = f'//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[{secondary_count}]/div/table/tbody/tr[{tertiary_count}]/td[9]/div').text
								kvota2 = driver.find_element(By.XPATH, value = f'//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[{secondary_count}]/div/table/tbody/tr[{tertiary_count}]/td[10]/div').text

						tertiary_count = tertiary_count + 1
						header = driver.find_element(By.XPATH, value=f'//*[@id="scroller-relative"]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[{secondary_count}]/div/table/thead/tr/td[2]').text
						oklada = matchup + '-' + header
						cur.execute('INSERT OR IGNORE INTO Oklade (drzava_id, oklada, jedan, X, dva) VALUES (?, ?, ?, ?, ?)', (drzava_id, oklada, kvota1, kvotax, kvota2))
						print(matchup, kvota1, kvotax, kvota2)
				else: 
					secondary_count = secondary_count + 1
					tertiary_count = 1
					continue
			except:
				continue


					
				
			secondary_count = secondary_count + 1
			tertiary_count = 1

	main_count = main_count + 1
	secondary_count = 1


conn.commit()

