import requests
import json
from datetime import datetime, timedelta, date
from IPython.lib.pretty import pprint
import pickle
import txarc_config
from urllib.parse import unquote, urlencode
from functools import reduce
import database

class Runner:
    def __init__(self):
        self.stat_pickler = dict()
        self.today_stats = dict()
        self.current_date_time = datetime.now().strftime("%m-%d-%Y")
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.yesterday = date.today() - timedelta(days=1)

    def load_from_file(self, filename):
        with open(filename, "rb") as handle:
        # with open('filename.pickle', 'rb') as handle:
            self.stat_pickler = pickle.load(handle)
        print("Files loaded", self.stat_pickler)

    def get_daily_stats(self):
        # print(URL)
        URL = txarc_config.CURRENT_DAY_URL
        response = requests.get(url=URL, params=txarc_config.current_day_params)
        # print(type(stats), stats.keys())
        stats = response.json()
        current_day_stats = []
        for feature in stats['features']:
            # print(feature.get('attributes'))
            totals = feature.get('attributes')
            current_day_stats.append ( dict( test=totals.get('TestType'), total=+totals.get('Count_') ) )
            totals.update({'date_collected' : self.current_date_time})
        self.stat_pickler.update( dict(current_day_stats=current_day_stats))
        self.today_stats.update( dict(current_day_stats=current_day_stats))


    def get_hospital_stats(self):
        response = requests.get(url=txarc_config.HOSPITAL_URL, params=txarc_config.hospitalizations_by_date_params)
        hospital_response = response.json()
        hospital_stats = []
        for feature in hospital_response['features']:
            # print(feature.get('attributes'))
            totals = feature.get('attributes')
            totals.update({'date_collected' : self.current_date_time})
            totals.update({'DateString': datetime.fromtimestamp(+totals.get('Date')/1000).strftime('%Y-%m-%d') })
            hospital_stats.append ( totals )
        self.stat_pickler.update(dict (hospital_stats=hospital_stats))
        last_stat = next((stat for stat in hospital_stats if stat["DateString"] == self.today), None)
        self.today_stats.update(dict(hospital_stats=last_stat) )

    def get_viral_antibody_breakout(self):
        response = requests.get(url= txarc_config.VIRAL_ANTIBODY_BREAKOUT_URL, params=txarc_config.viral_antibody_breakout_by_day_params )
        viral_response = response.json()
        viral_stats = []
        for feature in viral_response['features']:
            # print(feature.get('attributes'))
            totals = feature.get('attributes')
            totals.update({'date_collected' : self.current_date_time})
            totals.update({'DateString': datetime.fromtimestamp(+totals.get('Date')/1000).strftime('%Y-%m-%d') })
            viral_stats.append(totals)
        self.stat_pickler.update(dict(viral_antibody_stats=viral_stats))   
        last_stat = next((stat for stat in viral_stats if stat["DateString"] == self.yesterday.strftime("%Y-%m-%d")), None)
        self.today_stats.update( dict(viral_antibody_stats=last_stat) )         

    def get_daily_new_cases_by_date(self):
        response = requests.get(url=txarc_config.DAILY_NEW_CASES_URL, params=txarc_config.daily_new_cases_by_date_params)
        daily_response = response.json()
        # print(daily_response)
        daily_stats = []
        for feature in daily_response['features']:
            # print(feature.get('attributes'))
            totals = feature.get('attributes')
            totals.update({'date_collected' : self.current_date_time})
            totals.update({'DateString': datetime.fromtimestamp(+totals.get('Date')/1000).strftime('%Y-%m-%d') })
            daily_stats.append(totals)
        self.stat_pickler.update(dict(daily_new_cases=daily_stats))      
        last_stat = next((stat for stat in daily_stats if stat["DateString"] == self.today), None)
        self.today_stats.update(dict(daily_new_cases=last_stat) )          


    def get_daily_counts_by_county(self):
        response = requests.get(url=txarc_config.DAILY_COUNTY_COUNTS_URL, params=txarc_config.daily_counts_by_county_params)
        # print(response.url)
        daily_response = response.json()
        daily_stats = []
        for feature in daily_response['features']:
            # print(feature.get('attributes'))
            totals = feature.get('attributes')
            totals.update({'date_collected' : self.current_date_time})
            daily_stats.append(totals)
        self.stat_pickler.update(dict(daily_counts_by_county=daily_stats))  
        # print(daily_stats)
        # sum_counties = reduce((lambda x,y: dict(cumulative_cases=x["CumulativeCases"] + y["CumulativeCases"],
        #     cumulative_fatalities=x["CumulativeFatalities"] + y["CumulativeFatalities"],
        #     daily_new_cases=x["DailyNewCases"]+y["DailyNewCases"],
        #     daily_new_fatalities=x["DailyNewFatalities"]+y["DailyNewFatalities"]) ), daily_stats)

        harris = next((stat for stat in daily_stats if stat["County"] == "Harris"), None)            
        positive = 0
        fatalities = 0
        recoveries = 0
        active = 0
        for county_no in daily_stats:
            if county_no.get("Positive"):
                positive = positive + county_no.get("Positive")
            else:
                print("NO STATS: ", county_no)
            if county_no.get("Fatalities"):
                fatalities = fatalities + county_no.get("Fatalities")
            if county_no.get("Recoveries"):
                recoveries = recoveries + county_no.get("Recoveries")
            if county_no.get("Active"):
                active = active + county_no.get("Active")                                                           
        
        # sum_counties = reduce((lambda x,y: dict(sum_positive=x.get("Positive") + y.get("Positive"),
        #     sum_fatalities=x.get("Fatalities") + y.get("Fatalities"),
        #     sum_recoveries=x.get("Recoveries")+y.get("Recoveries"),
        #     sum_active=x.get("Active")+y.get("Active")) ), daily_stats)        
        sum_counties = dict(sum_positive=positive,
            sum_fatalities=fatalities,
            sum_recoveries=recoveries,
            sum_active=recoveries)
        sum_counties.update({'date_collected' : self.current_date_time})            
        self.today_stats.update(dict(sum_counties=sum_counties, harris=harris))      

    def get_county_totals(self):
        response_total = requests.get(url=txarc_config.TOTAL_COUNTIES_REPORTING_URL, params=txarc_config.total_counties_reporting_params)
        total_counties = response_total.json()["features"][0]
        # print(total_counties.get("attributes").get("value"))
        response_positives = requests.get(url=txarc_config.TOTAL_POSITIVES_URL, params=txarc_config.total_counties_with_positives_params)
        positive_counties = response_positives.json()["features"][0]
        # print(positive_counties.get("attributes").get("value"))
        totals = dict(total_counties=total_counties.get("attributes").get("value"), 
            positive_counties=positive_counties.get("attributes").get("value"))
        totals.update({'date_collected' : self.current_date_time})
        self.stat_pickler.update(dict(counties=totals))
        self.today_stats.update(dict(counties=totals))



    def write_to_file(self, filename):
        print ('------------------------------------------------------------------')
        # print(self.stat_pickler)
        # with open(filename, "wb") as handle:
        #     pickle.dump(self.stat_pickler, handle, protocol=pickle.HIGHEST_PROTOCOL)

        json_file = filename.replace('.pickle', '.json')
        with open(json_file, "w") as json_handle:
            json_handle.writelines(json.dumps(self.stat_pickler)  )  

        today_file = filename.replace('.pickle', '-today.json')
        with open(today_file, "w") as json_handle:
            json_handle.writelines(json.dumps(self.today_stats)  )

    def write_to_database(self):
        harris_stats = self.today_stats.get("harris") 
        database.save_harris_county(dict(dhs=dict(date_collected=harris_stats.get("date_collected"),
            Positive=harris_stats.get("Positive"), 
            Fatalities=harris_stats.get("Fatalities"),
            Recoveries=harris_stats.get("Recoveries"),
            Active=harris_stats.get("Active")))       )


        texas_stats = dict()
        texas_stats["date_collected"] = self.today_stats.get("counties").get("date_collected")
        texas_stats["positive_counties"] = self.today_stats.get("counties").get("positive_counties")
        texas_stats["REPORTED_TotalTests"] = next((stat.get("total") for stat in self.today_stats.get("current_day_stats") if stat["test"] == "TotalTests"), None) 
        texas_stats["AntibodyTests"] = next((stat.get("total") for stat in self.today_stats.get("current_day_stats") if stat["test"] == "AntibodyTests"), None) 
        texas_stats["PostiveAntibody"] = next((stat.get("total") for stat in self.today_stats.get("current_day_stats") if stat["test"] == "PostiveAntibody"), None) 
        texas_stats["ViralTests"] = next((stat.get("total") for stat in self.today_stats.get("current_day_stats") if stat["test"] == "ViralTests"), None) 
        texas_stats["Hospitalizations"] = self.today_stats.get("hospital_stats").get("Hospitalizations")
        texas_stats["SevenDayPositiveTestRate"] = self.today_stats.get("viral_antibody_stats").get("SevenDayPositiveTestRate")
        texas_stats["NewViral"] = self.today_stats.get("viral_antibody_stats").get("NewViral")
        texas_stats["NewAntibody"] = self.today_stats.get("viral_antibody_stats").get("NewAntibody")
        texas_stats["CumulativeCases"] = self.today_stats.get("daily_new_cases").get("CumulativeCases")
        texas_stats["CumulativeFatalities"] = self.today_stats.get("daily_new_cases").get("CumulativeFatalities")
        texas_stats["DailyNewCases"] = self.today_stats.get("daily_new_cases").get("DailyNewCases")
        texas_stats["DailyNewFatalities"] = self.today_stats.get("daily_new_cases").get("DailyNewFatalities")
        texas_stats["County_sum_positives"]   = self.today_stats.get("sum_counties").get("sum_positive")
        texas_stats["County_sum_fatalities"]  = self.today_stats.get("sum_counties").get("sum_fatalities")
        texas_stats["County_sum_recoveries"]  = self.today_stats.get("sum_counties").get("sum_recoveries")
        texas_stats["County_sum_active"]  = self.today_stats.get("sum_counties").get("sum_active")

        database.save_texas( dict(dhs=texas_stats))


#         {"counties": {"total_counties": 254, "positive_counties": 235, "date_collected": "06-07-2020"}, 
# "current_day_stats": [{"test": "TotalTests", "total": 1255899}, 
#     {"test": "AntibodyTests", "total": 118509}, 
#     {"test": "PostiveAntibody", "total": 4767}, 
#     {"test": "ViralTests", "total": 1100446}], 
# "hospital_stats": {"OBJECTID": 65, "Date": 1591509600000, "Hospitalizations": 1878, "date_collected": "06-07-2020", "DateString": "2020-06-07"}, 
# "viral_antibody_stats": {"OBJECTID": 64, "Date": 1591423200000, "SevenDayPositiveTestRate": 0.0755, "TotalTests": null, "ViralTests": 1100446, "AntibodyTests": 118509, "NewViral": 21226, "NewAntibody": 2226, "NewTotal": 23452, "date_collected": "06-07-2020", "DateString": "2020-06-06"}, 
# "daily_new_cases": {"OBJECTID": 96, "Date": 1591509600000, "CumulativeCases": 74978, "CumulativeFatalities": 1830, "DailyNewCases": 1425, "DailyNewFatalities": 11, "date_collected": "06-07-2020", "DateString": "2020-06-07"}, 
# "sum_counties": {"sum_positive": 74978, "sum_fatalities": 1830, "sum_recoveries": 39926, "sum_active": 39926, "date_collected": "06-07-2020"}, 
    

