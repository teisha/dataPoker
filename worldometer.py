import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import database


def download_texas():
    API_ENDPOINT = "https://www.worldometers.info/coronavirus/usa/texas/"

    response = requests.get(url = API_ENDPOINT)
    print("RESPONSE STATUS: %s"%response.status_code)
    # print("RESPONSE %s"%response.text)
    stats_file = open(r"F:/Dropbox/Coding/covid/data/worldometer.html", "w")
    stats_file.writelines(response.text)
    stats_file.close()

    worldometer_soup = BeautifulSoup(response.text, 'html5lib')
    yesterday_stats = []
    yesterday_table = worldometer_soup.find(id="nav-yesterday")
    # print(yesterday_table.thead)
    headers = yesterday_table.findAll('th')
    for data in yesterday_table.findAll('tr'):
        fields = data.findAll('td')

        if len(fields) >= 7:
            stat = {
                headers[0].get_text().replace('<br/>', '_'): fields[0].get_text().replace('\n', ''),
                headers[1].get_text().replace('<br/>', '_'): fields[1].get_text().replace('\n', '').replace(',',''),
                headers[2].get_text().replace('<br/>', '_'): fields[2].get_text().replace('\n', '').replace(',','').replace('+',''),
                headers[3].get_text().replace('<br/>', '_'): fields[3].get_text().replace('\n', '').replace(',',''),
                headers[4].get_text().replace('<br/>', '_'): fields[4].get_text().replace('\n', '').replace(',','').replace('+',''),
                headers[5].get_text().replace('<br/>', '_'): fields[5].get_text().replace('\n', '').replace(',',''),
                headers[6].get_text().replace('<br/>', '_'): fields[6].get_text().replace('\n', '').replace(',','')

                # 'County': fields[0].get_text().replace('\n', ''),
                # 'Total': fields[1].get_text().replace('\n', '').replace(',',''),
                # 'New_Cases': fields[2].get_text().replace('\n', '').replace(',','').replace('+',''),
                # 'Total_Deaths': fields[3].get_text().replace('\n', '').replace(',',''),
                # 'New_Deaths': fields[4].get_text().replace('\n', '').replace(',','').replace('+',''),
                # 'Active_Cases': fields[5].get_text().replace('\n', '').replace(',',''),
                # 'Total_Tests': fields[6].get_text().replace('\n', '').replace(',','')
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

    galveston_stat = next((stat for stat in yesterday_stats if stat["County"].strip() == "Galveston"), None)
    print('GALVESTON:' , galveston_stat)             
    database.save_galveston_county(dict(worldometer=galveston_stat))


def download_world():
    API_ENDPOINT = "https://www.worldometers.info/coronavirus/"

    response = requests.get(url = API_ENDPOINT)
    print("RESPONSE STATUS: %s"%response.status_code)
    # print("RESPONSE %s"%response.text)

    worldometer_soup = BeautifulSoup(response.text, 'html5lib')
    yesterday_stats = []
    yesterday_table = worldometer_soup.find(id="nav-yesterday")
    headers = yesterday_table.findAll('th')
    # print(yesterday_table.thead, headers)

    for data in yesterday_table.findAll('tr'):
        fields = data.findAll('td')

        if len(fields) >= 7:
            stat = {
                headers[1].get_text().replace('\n', '').replace(',', '_'): fields[1].get_text().replace('\n', ''),
                headers[2].get_text().replace('\n', ''): fields[2].get_text().replace('\n', '').replace(',',''),
                headers[3].get_text().replace('\n', ''): fields[3].get_text().replace('\n', '').replace(',','').replace('+',''),
                headers[4].get_text().replace('\n', ''): fields[4].get_text().replace('\n', '').replace(',',''),
                headers[5].get_text().replace('\n', ''): fields[5].get_text().replace('\n', '').replace(',','').replace('+',''),
                headers[6].get_text().replace('\n', ''): fields[6].get_text().replace('\n', '').replace(',',''),
                headers[7].get_text().replace('\n', ''): fields[7].get_text().replace('\n', '').replace(',','').replace('+',''),
                headers[8].get_text().replace('\n', ''): fields[8].get_text().replace('\n', '').replace(',',''),
                headers[9].get_text().replace('\n', '').replace(',', '_').replace(' ', '_'): fields[9].get_text().replace('\n', '').replace(',',''),
                headers[10].get_text().replace('\n', '').replace(' ', '_').replace('/', '_'): fields[10].get_text().replace('\n', '').replace(',',''),
                headers[11].get_text().replace('\n', '').replace(' ', '_').replace('/', '_'): fields[11].get_text().replace('\n', '').replace(',',''),
                headers[12].get_text().replace('\n', '').replace(' ', '_').replace('/', '_'): fields[12].get_text().replace('\n', '').replace(',',''),
                headers[13].get_text().replace('\n', '').replace(' ', '_').replace('/', '_'): fields[13].get_text().replace('\n', '').replace(',',''),
                headers[14].get_text().replace('\n', '').replace(' ', '_').replace('/', '_'): fields[13].get_text().replace('\n', '').replace(',','')

# 'Country': fields[1].get_text().replace('\n', ''),
                # 'Total_Cases': fields[2].get_text().replace('\n', '').replace(',',''),
                # 'New_Cases': fields[3].get_text().replace('\n', '').replace(',','').replace('+',''),
                # 'Total_Deaths': fields[4].get_text().replace('\n', '').replace(',',''),
                # 'New_Deaths': fields[5].get_text().replace('\n', '').replace(',','').replace('+',''),
                # 'Total_Recovered': fields[6].get_text().replace('\n', '').replace(',',''),
               # field added here - these numbers aren't correct
                # 'Active_Cases': fields[7].get_text().replace('\n', '').replace(',','').replace('+',''),
                # 'Serious': fields[8].get_text().replace('\n', '').replace(',',''),
                # 'Total_Cases_Per_1M_Pop': fields[9].get_text().replace('\n', '').replace(',',''),
                # 'Deaths_Per_1M_Pop': fields[10].get_text().replace('\n', '').replace(',',''),
                # 'Total_Tests': fields[11].get_text().replace('\n', '').replace(',',''),
                # 'Total_Tests_Per_1M_Pop': fields[12].get_text().replace('\n', '').replace(',',''),
                # 'Population': fields[13].get_text().replace('\n', '').replace(',','')
            } 
            yesterday_stats.append(stat)
    date_time = datetime.now().strftime("%m-%d-%Y")
    yesterday_file = open(r"F:/Dropbox/Coding/covid/data/worldometer-"+ date_time + ".json", "a")
    yesterday_out = (dict(world=yesterday_stats))
    yesterday_file.write(',')
    yesterday_file.writelines(json.dumps(yesterday_out)  )
    yesterday_file.write(']')
    yesterday_file.close()

    country_stat_name = headers[1].get_text().replace('<br/>', '_').replace(',', '_')
    us_stat = next((stat for stat in yesterday_stats if stat[country_stat_name] == "USA"), None)
    print("US: ", us_stat)
    database.save_us(dict(worldometer=us_stat) )
    # stats_file = open(r"data/worldometer.html", "a")
    # stats_file.writelines(yesterday_table)
    # stats_file.close()

