import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime


API_ENDPOINT = "https://www.worldometers.info/coronavirus/usa/texas/"

response = requests.get(url = API_ENDPOINT)
print("RESPONSE STATUS: %s"%response.status_code)
# print("RESPONSE %s"%response.text)

stats_file = open(r"data/worldometer.html", "w")
stats_file.writelines(response.text)
stats_file.close()


worldometer_soup = BeautifulSoup(response.text, 'html5lib')
yesterday_stats = []
yesterday_table = worldometer_soup.find(id="nav-yesterday")
print(yesterday_table.thead)
for data in yesterday_table.findAll('tr'):
    fields = data.findAll('td')

    if len(fields) >= 7:
        stat = {
            'County': fields[0].get_text().replace('\n', ''),
            'Total': fields[1].get_text().replace('\n', ''),
            'New_Cases': fields[2].get_text().replace('\n', ''),
            'Total_Deaths': fields[3].get_text().replace('\n', ''),
            'New_Deaths': fields[4].get_text().replace('\n', ''),
            'Active_Cases': fields[5].get_text().replace('\n', ''),
            'Total_Tests': fields[6].get_text().replace('\n', '')
        } 
        yesterday_stats.append(stat)
date_time = datetime.now().strftime("%m-%d-%Y")
yesterday_file = open(r"data/worldometer-"+ date_time + ".json", "w")
yesterday_file.writelines(json.dumps(yesterday_stats)  )
yesterday_file.close()


