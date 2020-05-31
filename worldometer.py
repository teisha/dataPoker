import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

def download_texas():
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
    yesterday_out = (dict(texas=yesterday_stats))
    yesterday_file = open(r"data/worldometer-"+ date_time + ".json", "w")
    yesterday_file.write('[')
    yesterday_file.writelines(json.dumps(yesterday_out)  )
    yesterday_file.close()


def download_world():
    API_ENDPOINT = "https://www.worldometers.info/coronavirus/"

    response = requests.get(url = API_ENDPOINT)
    print("RESPONSE STATUS: %s"%response.status_code)
    # print("RESPONSE %s"%response.text)

    worldometer_soup = BeautifulSoup(response.text, 'html5lib')
    yesterday_stats = []
    yesterday_table = worldometer_soup.find(id="nav-yesterday")
    print(yesterday_table.thead)
    for data in yesterday_table.findAll('tr'):
        fields = data.findAll('td')

        if len(fields) >= 7:
            stat = {
                'Country': fields[0].get_text().replace('\n', ''),
                'Total_Cases': fields[1].get_text().replace('\n', ''),
                'New_Cases': fields[2].get_text().replace('\n', ''),
                'Total_Deaths': fields[3].get_text().replace('\n', ''),
                'New_Deaths': fields[4].get_text().replace('\n', ''),
                'Total_Recovered': fields[5].get_text().replace('\n', ''),
                'Active_Cases': fields[6].get_text().replace('\n', ''),
                'Serious': fields[7].get_text().replace('\n', ''),
                'Total_Cases_Per_1M_Pop': fields[8].get_text().replace('\n', ''),
                'Deaths_Per_1M_Pop': fields[9].get_text().replace('\n', ''),
                'Total_Tests': fields[10].get_text().replace('\n', ''),
                'Total_Tests_Per_1M_Pop': fields[11].get_text().replace('\n', ''),
                'Population': fields[12].get_text().replace('\n', '')
            } 
            yesterday_stats.append(stat)
    date_time = datetime.now().strftime("%m-%d-%Y")
    yesterday_file = open(r"data/worldometer-"+ date_time + ".json", "a")
    yesterday_out = (dict(world=yesterday_stats))
    yesterday_file.write(',')
    yesterday_file.writelines(json.dumps(yesterday_out)  )
    yesterday_file.write(']')
    yesterday_file.close()

    # stats_file = open(r"data/worldometer.html", "a")
    # stats_file.writelines(yesterday_table)
    # stats_file.close()
