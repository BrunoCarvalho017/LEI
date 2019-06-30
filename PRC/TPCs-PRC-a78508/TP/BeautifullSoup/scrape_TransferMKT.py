#!/usr/bin/python3

import requests, time, re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

f = open("cenas2.txt", "a")


browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice
site = 'https://www.transfermarkt.pt'
ligas = [
            '/primeira-liga/startseite/wettbewerb/PO1/plus/?saison_id=',
            '/premier-league/startseite/wettbewerb/GB1/plus/?saison_id=',
            '/ligue-1/startseite/wettbewerb/FR1/plus/?saison_id=',
            '/primera-division/startseite/wettbewerb/ES1/plus/?saison_id=',
            '/serie-a/startseite/wettbewerb/IT1/plus/?saison_id='
        ]
classificacoes = [
            '/primeira-liga/tabelle/wettbewerb/PO1/saison_id/',
            '/premier-league/tabelle/wettbewerb/GB1/saison_id/',
            '/ligue-1/tabelle/wettbewerb/FR1/saison_id/',
            '/primera-division/tabelle/wettbewerb/ES1/saison_id/',
            '/serie-a/tabelle/wettbewerb/IT1/saison_id/'
            ]   

def getTeamsLinks(liga,teams,teams_links):
    url = site + liga
    browser.get(url) #navigate to the page

    innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string

    #page = requests.get(site + '/futebol/portugal/primeira-liga/arquivo/')

    # Criar o objeto BeautifulSoup
    soup = BeautifulSoup(innerHTML, 'html.parser')

    table = soup.find("table",{"class":"items"})
    rows = table.find('tbody').find_all('tr')
    
    for row in rows :
        cells = row.find_all('td')
        teams.append(cells[2].find('a').text)
        teams_links.append(cells[2].find('a').get('href'))

def getSquadInfo(team_link,players_links,t,short_name,str_squads):
    season = team_link.split("/")[-1:]
    players = []
    squad = {}

    url = site + team_link

    browser.get(url) #navigate to the page
    innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
    # Criar o objeto BeautifulSoup
    soup = BeautifulSoup(innerHTML, 'html.parser')

    team = soup.find('h1').find('span').text
    # Nome do clube 
    squad['squad_id'] = t
    squad['season'] = season[0]
    squad['name'] = team
    squad['short_name'] = short_name

    elems = soup.find('div',{"class":"responsive-table"}).find_all("a",{"class":"spielprofil_tooltip tooltipstered"})

    j = 0
    i = 0
    p_links =[]
    for elem in elems:
        if not i%2 :
            players.append(elem.text+'#'+str(i))
            players_links.append(elem.get('href'))
            x = str.split(elem.get('href'),'/')[1]
            y = str.split(elem.get('href'),'/')[4]
            p_links.append(x+y)
            j += 1
        i += 1
    players = list(set(players))
    players_links = list(set(players_links))
    squad['players'] = players

    squad_key1 = str.split(team_link,'/')[1]
    squad_key2 = str.split(team_link,'/')[6]
    squad_key = squad_key1+squad_key2

    f.write("### http://prc.di.uminho.pt/football#squad" + squad_key + "\n")
    f.write(":squad" + squad_key + " rdf:type owl:NamedIndividual ,\n")
    f.write("\t\t\t:Squad ;\n")
    f.write("\t\t:id " + str(squad['squad_id']) + " ;\n") 
    f.write("\t\t:season " +"\""+ squad['season'] +"\""+ " ;\n") 
    f.write("\t\t:name " +"\""+ squad['name'] +"\""+ " ;\n") 
    f.write("\t\t:short_name " +"\""+ squad['short_name'] +"\"")  
    
    for p_link in p_links:
        f.write(";\n\t\t:hasPlayer :player" + p_link )
    f.write(".\n\n")

    return squad

def getPlayerInfo(player_link,p,str_players):
    url = site + player_link
    
    player = {}

    browser.get(url) #navigate to the page
    innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
    # Criar o objeto BeautifulSoup
    soup = BeautifulSoup(innerHTML, 'html.parser')

    birthDate = soup.find('span',{"itemprop":"birthDate"})
    birthPlace = soup.find('span',{"itemprop":"birthPlace"})
    nationality = soup.find('span',{"itemprop":"nationality"})
    height = soup.find('span',{"itemprop":"height"})
    name = soup.find('h1',{"itemprop":"name"})
    jersey_number = soup.find('span',{"class":"dataRN"})
    posicao = soup.find_all('div',{"class":"dataDaten"})[1].find_all('span',{"class":"dataValue"})[1]
    
    player['player_id'] = p
    if birthDate is None:
        player['birthDate'] = ""
    else:
        player['birthDate'] = re.sub(r'[\t\n]',"",birthDate.text).split("(")[0]
    
    if birthPlace is None:
        player['birthPlace'] = ""
    else:
        player['birthPlace'] = birthPlace.text
    if nationality is None:
        player['nationality'] = ""
    else:
        player['nationality'] = nationality.text
    if height is None:
        player['height'] = ""
    else:
       player['height'] = re.sub(r'[\D]',"",height.text)
    if name is None:
        player['name'] = ""
    else:
        player['name'] = name.text
    if jersey_number is None:
        player['jersey_number'] = ""
    else:
        player['jersey_number'] = re.sub(r'[\D]',"",jersey_number.text)
    if posicao is None:
        player['posicao'] = ""
    else:
        player['posicao'] = re.sub(r'[\n\t\s]',"",posicao.text)
    

    x = str.split(player_link,'/')[1]
    y = str.split(player_link,'/')[4]
    playerKey = x+y

    f.write("### http://prc.di.uminho.pt/football#player" + playerKey + "\n")
    f.write(":player" + playerKey + " rdf:type owl:NamedIndividual ,\n")
    f.write("\t\t\t:Player ;\n")
    f.write("\t\t:id " + str(p) + " ;\n" )
    f.write("\t\t:birth_date " +"\""+ player['birthDate'] +"\""+ " ;\n" )
    f.write("\t\t:birth_place " +"\""+  player['birthPlace'] +"\""+ " ;\n") 
    f.write("\t\t:nationality " +"\""+  player['nationality'] +"\""+ " ;\n" )
    f.write("\t\t:height " +  player['height'] + " ;\n" )
    f.write("\t\t:name " +"\""+ player['name'] +"\""+ " ;\n") 
    f.write("\t\t:jersey_number " +  player['jersey_number'] + " ;\n") 
    f.write("\t\t:position " +"\""+  player['posicao'] +"\""+ " .\n" )

    return player

def getClassificationInfo(s,c,classification_link,str_classifications):
    url = site + classification_link

    browser.get(url) #navigate to the page
    innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
    # Criar o objeto BeautifulSoup
    soup = BeautifulSoup(innerHTML, 'html.parser')

    tr_elems = soup.find('div',{"class":"responsive-table"}).find('tbody').find_all('tr')
    #find_all("a",{"class":"spielprofil_tooltip tooltipstered"})

    season_key1 = str.split(classification_link,'/')[1]
    season_key2 = str.split(classification_link,'/')[6]
    season_key = season_key1+season_key2

    classification = {}
    classifications = []
    str_seasons = ""
    str_seasons += "### http://prc.di.uminho.pt/football#season" + season_key + "\n"
    str_seasons += ":season" + season_key + " rdf:type owl:NamedIndividual ,\n"
    str_seasons += "\t\t\t:Season ;\n"
    str_seasons += "\t\t:id " + str(s) + " ;\n"
    str_seasons += "\t\t:season " + season_key2 + " ;\n"

    vezes = 0
    for tr_elem in tr_elems:
        squad_key1 = str.split(tr_elem.find_all('td')[1].find('a').get('href'),'/')[1]
        squad_key2 = str.split(tr_elem.find_all('td')[1].find('a').get('href'),'/')[6]
        squad_key = squad_key1+squad_key2
        classification['classification'] = tr_elem.find_all('td')[0].text
        classification['played_games'] = tr_elem.find_all('td')[3].text
        classification['wins'] = tr_elem.find_all('td')[4].text
        classification['draws'] = tr_elem.find_all('td')[5].text
        classification['losses'] = tr_elem.find_all('td')[6].text
        classification['scored_goals'] = str.split(tr_elem.find_all('td')[7].text,':')[0]
        classification['conceded_goals'] = str.split(tr_elem.find_all('td')[7].text,':')[1]
        classification['points'] = tr_elem.find_all('td')[9].text
        classification['squad_name'] = tr_elem.find_all('td')[2].text
        
        classifications.append(classification)

        f.write("### http://prc.di.uminho.pt/football#classification" + squad_key + "\n")
        f.write(":classification" + squad_key + " rdf:type owl:NamedIndividual ,\n")
        f.write("\t\t\t:Classification ;\n")
        f.write("\t\t:id " + str(c) + " ;\n") 
        f.write("\t\t:classification " + re.sub(r'[\W]',"",classification['classification']) + " ;\n" )
        f.write("\t\t:played_games " + classification['played_games'] + " ;\n") 
        f.write("\t\t:wins " + classification['wins'] + " ;\n")
        f.write("\t\t:draws " + classification['draws'] + " ;\n") 
        f.write("\t\t:losses " + classification['losses'] + " ;\n") 
        f.write("\t\t:scored_goals " + classification['scored_goals'] + " ;\n") 
        f.write("\t\t:conceded_goals " + classification['conceded_goals'] + " ;\n")
        f.write("\t\t:points " + classification['points'] + " ;\n") 
        f.write("\t\t:squad_name " +"\""+ re.sub(r'[\n]',"",classification['squad_name']) +"\""+ " ;\n")
        f.write("\t\t:hasSquad :squad" + squad_key + ".\n\n")
        if vezes == 0:
            str_seasons += "\t\t:hasClassification :classification" + squad_key
            vezes += 1
        else:
            str_seasons += ";\n\t\t:hasClassification :classification" + squad_key
            vezes += 1
    str_seasons += ".\n\n"
    f.write(str_seasons)

    return classifications

teams = []
teams_links = []
players_links = []
squads = []
classifications = []
players_info = []
str_squads = ""
str_players = ""
str_classifications = ""

"""
l = 0
for liga in ligas:
    if l == 0:
        for i in range (2018,2016,-1):
            liga = liga + str(i)
            getTeamsLinks(liga,teams,teams_links)
        break 
    l += 1

t = 0
for team_link in teams_links:
    #if t < 1 :
        #tuplo = ()
        squads = getSquadInfo(team_link,players_links,t,teams[t],str_squads) 
        #squads.append(tuplo[0])
        #str_squads += tuplo[1]
        t += 1

p = 0
for player_link in players_links:
    #if p == 0:
        #tuplo = ()
        players_info = getPlayerInfo(player_link,p,str_players)
        #players_info.append(tuplo[0])
        #str_players += tuplo[1]
        p += 1
"""
s = 0
c = 0
for classificacao in classificacoes:
    #if s == 0:
        for i in range (2018,2016,-1):
            classificacao_link = classificacao + str(i)
            #tuplo = ()
            classifications = getClassificationInfo(s,c,classificacao_link,str_classifications)
            #classifications.append(tuplo[0])
            #str_classifications += tuplo[1]
            s += 1
        c += 1
    #s += 1
"""
print(teams)
print('\n')
print(squads)
print('\n')
print(players_info)
print('\n')
"""
"""
print(str_squads)
print('\n')
print(str_players)
print('\n')   
print(str_classifications)
"""
"""
print(players_links)
"""
f.close()