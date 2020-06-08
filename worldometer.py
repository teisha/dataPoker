import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import database
from more_itertools.more import strip

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
                'Total': fields[1].get_text().replace('\n', '').replace(',',''),
                'New_Cases': fields[2].get_text().replace('\n', '').replace(',','').replace('+',''),
                'Total_Deaths': fields[3].get_text().replace('\n', '').replace(',',''),
                'New_Deaths': fields[4].get_text().replace('\n', '').replace(',','').replace('+',''),
                'Active_Cases': fields[5].get_text().replace('\n', '').replace(',',''),
                'Total_Tests': fields[6].get_text().replace('\n', '').replace(',','')
            } 
            yesterday_stats.append(stat)
    date_time = datetime.now().strftime("%m-%d-%Y")
    yesterday_out = (dict(texas=yesterday_stats))
    yesterday_file = open(r"data/worldometer-"+ date_time + ".json", "w")
    yesterday_file.write('[')
    yesterday_file.writelines(json.dumps(yesterday_out)  )
    yesterday_file.close()

    texas_stat = next((stat for stat in yesterday_stats if stat["County"] == "Texas Total"), None)
    print("TEXAS: ", texas_stat)
    database.save_texas(dict(worldometer=texas_stat) )

    harris_stat = next((stat for stat in yesterday_stats if stat["County"].strip() == "Harris"), None)
    print("HARRIS: ", harris_stat)

    database.save_harris_county(dict(worldometer=harris_stat) )


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
                'Country': fields[1].get_text().replace('\n', ''),
                'Total_Cases': fields[2].get_text().replace('\n', '').replace(',',''),
                'New_Cases': fields[3].get_text().replace('\n', '').replace(',','').replace('+',''),
                'Total_Deaths': fields[4].get_text().replace('\n', '').replace(',',''),
                'New_Deaths': fields[5].get_text().replace('\n', '').replace(',','').replace('+',''),
                'Total_Recovered': fields[6].get_text().replace('\n', '').replace(',',''),
                'Active_Cases': fields[7].get_text().replace('\n', '').replace(',','').replace('+',''),
                'Serious': fields[8].get_text().replace('\n', '').replace(',',''),
                'Total_Cases_Per_1M_Pop': fields[9].get_text().replace('\n', '').replace(',',''),
                'Deaths_Per_1M_Pop': fields[10].get_text().replace('\n', '').replace(',',''),
                'Total_Tests': fields[11].get_text().replace('\n', '').replace(',',''),
                'Total_Tests_Per_1M_Pop': fields[12].get_text().replace('\n', '').replace(',',''),
                'Population': fields[13].get_text().replace('\n', '').replace(',','')
            } 
            yesterday_stats.append(stat)
    date_time = datetime.now().strftime("%m-%d-%Y")
    yesterday_file = open(r"data/worldometer-"+ date_time + ".json", "a")
    yesterday_out = (dict(world=yesterday_stats))
    yesterday_file.write(',')
    yesterday_file.writelines(json.dumps(yesterday_out)  )
    yesterday_file.write(']')
    yesterday_file.close()

    us_stat = next((stat for stat in yesterday_stats if stat["Country"] == "USA"), None)
    print("US: ", us_stat)
    database.save_us(dict(worldometer=us_stat) )
    # stats_file = open(r"data/worldometer.html", "a")
    # stats_file.writelines(yesterday_table)
    # stats_file.close()

