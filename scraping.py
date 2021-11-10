# -*- coding: utf-8 -*-
"""Scraping.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Fz_raq46qAZzK7Y7HMrYyoXcZIUxZjbe

# Projet Scraping ( scraper https://www.lequipe.fr/ )

Nous allons en premier temps scraper les données de l'euro 2021

__Questions: 

Phase de groupe

* Quelles ont-été les équipes les performantes durant la phase de groupe de l'euro 2021 ?

* Quelles ont été les meilleures attaques de la phase de groupe de l'euro 2021 ?

* Quelles ont été les meilleures défenses de la phase de groupe de l'euro 2021 ?

Demi-finales

* Parmis les équipes présentent en demi de finales, retrouve-t-on les équipes qui ont été les plus performantes durant la phase groupe ? 


La finale

* être parmis les meilleurs défenses et meilleures attaques de la phase de groupe contribue-t-il à gagner l'euro ?

Meilleurs buteurs de l'euro  
* Quels sont les meilleurs buteurs de l'euro 2021 ?

### **Pré-requis**
"""

!pip install requests
!pip install bs4
!pip install pprint

import requests
from bs4 import BeautifulSoup
from pprint import pprint

"""### **Phase de groupe**"""

url = "https://www.lequipe.fr/Football/euro/page-calendrier-resultats/tous-les-groupes"
html = requests.get(url)
bsObj = BeautifulSoup(html.content, "lxml")

list_equipe = bsObj.find_all({"tr"}, {"class":"table__row"})
equipe_points = []
equipe_attaquants = []
equipe_defenseur = []

for item in list_equipe :
    nom = item.find({"td"}, {"class": "table__col--name"})
    points = item.find({"td"}, {"class": "table__col--points"})
    buts = item.find_all({"td"}, {"class": "min--tablet"})
    if nom is not None and points is not None: equipe_points.append([nom.getText(strip=True), int(points.getText(strip=True))])
    if nom is not None and buts is not None: equipe_attaquants.append([nom.getText(strip=True), int(buts[0].getText(strip=True))])
    if nom is not None and buts is not None: equipe_defenseur.append([nom.getText(strip=True), int(buts[1].getText(strip=True))])

"""##### **Equipes les plus performantes**"""

classements_points = sorted(equipe_points, key=lambda x:x[1], reverse=True)
pprint(classement_points[:10])

"""##### **Meilleures équipes en attaque**"""

classements_attaquants = sorted(equipe_attaquants, key=lambda x:x[1], reverse=True)
pprint(classements_attaquants[:5])

"""##### **Meilleures équipes en défense**"""

classements_defenseurs = sorted(equipe_defenseur, key=lambda x:x[1])
pprint(classements_defenseurs[:5])

"""### **Demi finale**"""

url = "https://www.lequipe.fr/Football/euro/page-calendrier-resultats/demi-finales"
html = requests.get(url)
bsObj = BeautifulSoup(html.content, "lxml")

list_equipe_df = bsObj.find_all({"span"}, {"class":"TeamScore__nameshort"})
list_equipe_df_text = []

for item in list_equipe_df :
    list_equipe_df_text.append(item.getText(strip=True))

pprint(list_equipe_df_text)

print("Equipes en demi-finale qui faisaient parties des équipes les plus performantes durant la phase de groupe:")
for equipe_groupes in classement_points[:10]:
  for equipe_df in list_equipe_df_text:
    if equipe_groupes[0] == equipe_df:
      print(f"- {equipe_df}")

"""### **Finale**"""

url = "https://www.lequipe.fr/Football/euro/page-calendrier-resultats/demi-finales"
html = requests.get(url)
bsObj = BeautifulSoup(html.content, "lxml")

gagnant_euro = bsObj.find({"div"}, {"class":"TeamScore__team--winner"}).getText(strip=True)

for attaquant in equipe_attaquants:
  for defenseur in equipe_defenseur:
    if attaquant[0] == gagnant_euro and defenseur[0] == gagnant_euro:
      print(f"{gagnant_euro} fait parti des meilleures équipes en attaque et en défense et à gagner l'Euro 2021")

"""**Etant donné les résultats ci-dessus, nous pouvons dire qu'être parmi les meilleurs en attaque et en défense contribue à remporter l'Euro 2021**

### **Meilleurs buteurs**
"""

url = "https://www.lequipe.fr/Football/euro/page-classement-individuel/buteurs"
html = requests.get(url)
bsObj = BeautifulSoup(html.content, "lxml")

buteurs = bsObj.find_all({"tr"}, {"class":"table__row"})

for buteur in buteurs:
  nom_buteur = buteur.find({"a"}, {"class":"table__playerName"})
  nom_equipe = buteur.find({"div"}, {"class":"table__teamName"})
  nombre_but = buteur.find({"span"}, {"class":"table__col--sorted"})
  
  if nom_buteur is not None and nombre_but is not None and nom_equipe is not None:
    nom_buteur = nom_buteur.getText(strip=True).replace(nom_equipe.getText(strip=True), "")
    print(f"{nom_buteur} avec {nombre_but.getText(strip=True)} buts")