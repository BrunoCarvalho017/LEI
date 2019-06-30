#!/usr/bin/python3

import requests, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice

site = 'https://www.zerozero.pt'

#url = site + "/futebol/portugal/primeira-liga/arquivo/"
browser.get(site) #navigate to the page

innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string

#page = requests.get(site + '/futebol/portugal/primeira-liga/arquivo/')

# Criar o objeto BeautifulSoup
soup = BeautifulSoup(innerHTML, 'html.parser')
#print(soup.prettify())



"""
season_archive = soup.find(class_='fs-table tournament-page-archiv')
season_archive_items = season_archive.find_all('a')

season_archive_links = []
# Usar .contents para pegar as tags <a> filhas
for season_name in season_archive_items:
    #names = season_name.contents[0]
    season_archive_links.append(season_name.get('href'))

#eliminar os links do vencedor
for x in season_archive_links:
    if (str.split(x,sep='/')[1] == 'equipa'):
        season_archive_links.remove(x)
    

def getClassificatioInfo(season_link):
    season_classification_items = []
    str = ""

    url = site + season_link + 'classificacoes/'
    browser.get(url) #navigate to the page

    innerHTML = browser.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup(innerHTML, 'html.parser')
    
    table = soup.find('table', id="table-type-1")
    j = 0
    keys = []
    rows = table.find_all("tr")
    kv_pair = {}
    for row in rows:
        if(j == 0):
            cells = row.find_all("th")
            for cell in cells:
                str += cell.get('title') + " "
                keys.append(cell.get('title'))
        else:
            k = 0
            cells = row.find_all("td")
            for cell in cells:
                if(k == 1):
                    str += cell.find('a').text + " "
                    kv_pair[keys[k]] = cell.find('a').text
                else:
                    str += cell.text + " "
                    kv_pair[keys[k]] = cell.text
                k += 1
            season_classification_items.append(kv_pair)
            kv_pair = {}
        j += 1
        str += "\n"

    print(str) 
    print(season_classification_items)
    print(len(season_classification_items))

def getRoundsInfo(season_link):
    str = ""
    url = site + season_link + 'resultados/'

    browser.set_script_timeout(10)
    #browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice
    #element = WebDriverWait(browser, 10).until(EC.invisibility_of_element_located((By.ID, "tournament-page-results-more")))
    #browser.implicitly_wait(30)
    browser.get(url) #navigate to the page


    i = 0
    element = browser.find_element_by_link_text('Mostrar mais jogos')
    while i < 3:
        browser.execute_script("arguments[0].click();", element)
        time.sleep(5)
        i += 1
    
    #innerHTML = browser.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    
    table = soup.find('table')

    rounds = []
    games = []
    rows = table.find('tbody').find_all("tr")
    kv_pair_round = {}
    kv_pair_game = {}
    i = 0
    for row in rows:        
        if(row.get('class')[0] == 'event_round'):
            if(i != 0):
                print(len(games))
                kv_pair_round['games'] = games
                rounds.append(kv_pair_round)
                kv_pair_round = {}
                games = []
            kv_pair_round['round'] = row.find('td').text
        else:
            cells = row.find_all("td")
            kv_pair_game['time'] = cells[1].text
            kv_pair_game['team_home'] = cells[2].find('span').text
            kv_pair_game['team_away'] = cells[3].find('span').text
            kv_pair_game['score'] = cells[4].text
            games.append(kv_pair_game)
            kv_pair_game = {}
        i += 1
    #Inserção da última ronda (pq não volta a entrar no ciclo)
    kv_pair_round['games'] = games
    rounds.append(kv_pair_round)
    kv_pair_round = {}
    games = []
    print(len(rounds))
    print(rounds)
"""
#getRoundsInfo(season_archive_links[0])