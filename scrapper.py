import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import csv


links = []
for i in range(27):
    site = "https://www.hltv.org/stats/matches?offset={}&startDate=2019-07-30&endDate=2019-10-30&rankingFilter=Top50".format(i * 50)
    req = requests.get(site)

    soup = bs(req.content, "html.parser")

    for match in soup.find_all("td", class_="date-col"):
        links.append(match.find("a")['href'])

full_links = ["https://www.hltv.org" + link for link in links]

with open('data.csv', 'w', newline='') as csvfile:
    wr = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    header = ['Left_score', 'Right_score', 'Total_score', 'Map', 'Outcome']

    for p in range(1, 11):
        p = str(p)
        header += ["p" + p + "_link", "p" + p + "_id", "p" + p + "_kills", "p" + p + "_deaths", "p" + p + "_kast", "p" + p + "_adr", "p" + p + "_rating"]


    wr.writerow(header)

    i = 0

    for link in full_links:
        print(i)
        i+=1
        req = requests.get(link)
        soup = bs(req.content, "html.parser")

        rowdata = []

        left_score = int(soup.find("div", class_="team-left").find("div", class_="bold").text)
        right_score = int(soup.find("div", class_="team-right").find("div", class_="bold").text)
        total_score = left_score + right_score
        mapcs = soup.find("div", class_="match-info-box").contents[3].strip()
        outcome = 1 if left_score > right_score else 0

        rowdata.append(left_score)
        rowdata.append(right_score)
        rowdata.append(total_score)
        rowdata.append(mapcs)
        rowdata.append(outcome)


        left_players = soup.find_all("table", class_="stats-table")[0].find("tbody")
        for row in left_players.find_all("tr"):

            p1_link = str(row.find('td', class_="st-player").find('a')['href'])
            qindex = p1_link.find("?")
            p1_link = p1_link[:qindex]
            rowdata.append(p1_link)

            p1_id = row.find('td', class_="st-player").text
            rowdata.append(p1_id)

            p1_kills = str(row.find('td', class_="st-kills").text)
            kindex = p1_kills.find(" ")
            p1_kills = p1_kills[:kindex]
            rowdata.append(p1_kills)

            p1_deaths = row.find('td', class_="st-deaths").text
            rowdata.append(p1_deaths)
            p1_kast = row.find('td', class_="st-kdratio").text
            rowdata.append(p1_kast)
            p1_adr = row.find('td', class_="st-adr").text
            rowdata.append(p1_adr)
            p1_rating = row.find('td', class_="st-rating").text
            rowdata.append(p1_rating)

        right_players = soup.find_all("table", class_="stats-table")[1].find('tbody')
        for row in right_players.find_all("tr"):
            p2_link = str(row.find('td', class_="st-player").find('a')['href'])
            qindex = p2_link.find("?")
            p2_link = p2_link[:qindex]
            rowdata.append(p2_link)

            p2_id = row.find('td', class_="st-player").text
            rowdata.append(p2_id)

            p2_kills = str(row.find('td', class_="st-kills").text)
            kindex = p2_kills.find(" ")
            p2_kills = p2_kills[:kindex]
            rowdata.append(p2_kills)

            p2_deaths = row.find('td', class_="st-deaths").text
            rowdata.append(p2_deaths)
            p2_kast = row.find('td', class_="st-kdratio").text
            rowdata.append(p2_kast)
            p2_adr = row.find('td', class_="st-adr").text
            rowdata.append(p2_adr)
            p2_rating = row.find('td', class_="st-rating").text
            rowdata.append(p2_rating)

        wr.writerow(rowdata)

        sleep(0.5)
