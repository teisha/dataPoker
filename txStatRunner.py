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
        print('-----------------INIT TXDHS------------------------------')

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


    def get_hospital_current(self):
        response = requests.get(url=txarc_config.HOSPITALS_CURRENT, params=txarc_config.hospitals_current_params)
        hospital_response = response.json()
        hospitals_current = []
        total_covid = 0
        total_staff = 0
        total_avail_beds = 0
        total_avail_icu_beds = 0
        total_avail_vents = 0
        for feature in hospital_response['features']:
            # print(feature.get('attributes'))
            totals = feature.get('attributes')
            totals.update({'date_collected' : self.current_date_time})
            total_covid = total_covid + totals.get("COVIDPatie")
            total_staff = total_staff + totals.get("TotalStaff")
            total_avail_beds = total_avail_beds +  totals.get("AvailHospi")
            total_avail_icu_beds = total_avail_icu_beds + totals.get("AvailICUBe")
            total_avail_vents = total_avail_vents + totals.get("AvailVenti")
            hospitals_current.append(totals)
        harris = next((stat for stat in hospitals_current if stat["TSA"] == "Q"), None)
        # print( harris)
        state_totals = dict(total_covid=total_covid, total_staff=total_staff, total_avail_beds=total_avail_beds,
            total_avail_icu_beds=total_avail_icu_beds, total_avail_vents=total_avail_vents  )
        state_totals.update({'date_collected' : self.current_date_time})
        print(state_totals)
        self.stat_pickler.update( dict(hospitals_current=hospitals_current))
        self.today_stats.update(dict(harris_hospitals=harris, hospital_current_totals=state_totals) )



    def get_hospital_stats(self):
        response = requests.get(url=txarc_config.HOSPITAL_URL, params=txarc_config.hospitalizations_by_date_params)
        hospital_response = response.json()
        new_response = requests.get(url=txarc_config.HOSPITALS_CUMULATIVE, params=txarc_config.hospitals_cum_params)
        new_hospital_response = new_response.json()
        hospital_stats = []
        todays_stats = []
        for feature in hospital_response['features']:
            # print(feature.get('attributes'))
            totals = feature.get('attributes')
            totals.update({'date_collected' : self.current_date_time})
            totals.update({'DateString': datetime.fromtimestamp(+totals.get('Date')/1000).strftime('%Y-%m-%d') })
            hospital_stats.append ( totals )
        for feature in new_hospital_response['features']:
            totals = feature.get('attributes')        
            totals.update({'date_collected' : self.current_date_time})
            todays_stats.append(totals)
        self.stat_pickler.update(dict (hospital_stats=hospital_stats))
        last_stat = next((stat for stat in hospital_stats if stat["DateString"] == self.today), None)
        self.today_stats.update(dict(hospital_stats=todays_stats, hosp_stat=last_stat) )

    def get_viral_antibody_breakout(self):
        print(txarc_config.VIRAL_ANTIBODY_BREAKOUT_URL)
        print(txarc_config.viral_antibody_breakout_by_day_params)
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



    def write_to_file(self, filename, archive_dir):
        print ('------------------------------------------------------------------')
        # print(self.stat_pickler)
        # with open(filename, "wb") as handle:
        #     pickle.dump(self.stat_pickler, handle, protocol=pickle.HIGHEST_PROTOCOL)

        json_file = archive_dir + filename.replace('.pickle', '.json')
        with open(json_file, "w") as json_handle:
            json_handle.writelines(json.dumps(self.stat_pickler)  )  

        today_file = filename.replace('.pickle', '-today.json')
        with open(today_file, "w") as json_handle:
            json_handle.writelines(json.dumps(self.today_stats)  )

    def write_to_database(self):
        harris_stats = self.today_stats.get("harris") 
        harris_hospitals = self.today_stats.get("harris_hospitals")
        harris_save_stats = dict()
        harris_save_stats["date_collected"] = harris_stats.get("date_collected")
        harris_save_stats["Positive"] = harris_stats.get("Positive")
        harris_save_stats["Fatalities"] = harris_stats.get("Fatalities")
        harris_save_stats["Recoveries"] = harris_stats.get("Recoveries")
        harris_save_stats["Active"] = harris_stats.get("Active")
        harris_save_stats["TraumaServiceArea"] = harris_hospitals.get("TSA")
        harris_save_stats["RegionalAdvisoryCouncil"] = harris_hospitals.get("RAC") 
        harris_save_stats["PopulationEstimate"] = harris_hospitals.get("PopEst2020") 
        harris_save_stats["TotalHospitalStaff"] = harris_hospitals.get("TotalStaff")
        harris_save_stats["AvailableHospitalBeds"] = harris_hospitals.get("AvailHospi")
        harris_save_stats["AvailableICUBeds"] = harris_hospitals.get("AvailICUBe")
        harris_save_stats["AvailableVentilators"] = harris_hospitals.get("AvailVenti")
        harris_save_stats["COVIDPatients"] = harris_hospitals.get("COVIDPatie")
        database.save_harris_county(dict(dhs=harris_save_stats))

        texas_stats = dict()
        texas_stats["date_collected"] = self.today_stats.get("counties").get("date_collected")
        texas_stats["positive_counties"] = self.today_stats.get("counties").get("positive_counties")
        texas_stats["REPORTED_TotalTests"] = next((stat.get("total") for stat in self.today_stats.get("current_day_stats") if stat["test"] == "TotalTests"), None) 
        texas_stats["AntibodyTests"] = next((stat.get("total") for stat in self.today_stats.get("current_day_stats") if stat["test"] == "AntibodyTests"), None) 
        texas_stats["PostiveAntibody"] = next((stat.get("total") for stat in self.today_stats.get("current_day_stats") if stat["test"] == "PostiveAntibody"), None) 
        texas_stats["ViralTests"] = next((stat.get("total") for stat in self.today_stats.get("current_day_stats") if stat["test"] == "ViralTests"), None) 
        hospital_totals = self.today_stats.get("hospital_current_totals")
        texas_stats["HOSP: TotalCovidPatients"] = hospital_totals.get("total_covid")
        texas_stats["HOSP: TotalStaffedBeds"] = hospital_totals.get("total_staff")
        texas_stats["HOSP: TotalAvailableBeds"] = hospital_totals.get("total_avail_beds")
        texas_stats["HOSP: TotalAvailableICUBeds"] = hospital_totals.get("total_avail_icu_beds")
        texas_stats["HOSP: TotalAvailableVents"] = hospital_totals.get("total_avail_vents")
        if self.today_stats.get("hosp_stat") == None:
            texas_stats["Hospitalizations"] = -1
        else:    
            texas_stats["Hospitalizations"] = self.today_stats.get("hosp_stat", dict(Hospitalizations=-1)).get("Hospitalizations", -1)
        if self.today_stats.get("viral_antibody_stats") == None:
            texas_stats["SevenDayPositiveTestRate"] = -1
            texas_stats["NewViral"] = -1
            texas_stats["NewAntibody"] = -1
        else:            
            texas_stats["SevenDayPositiveTestRate"] = self.today_stats.get("viral_antibody_stats", dict()).get("SevenDayPositiveTestRate", -1)
            texas_stats["NewViral"] = self.today_stats.get("viral_antibody_stats", dict()).get("NewViral", -1)
            texas_stats["NewAntibody"] = self.today_stats.get("viral_antibody_stats", dict()).get("NewAntibody", -1)
        if self.today_stats.get("daily_new_cases") == None:
            texas_stats["CumulativeCases"] = -1
            texas_stats["CumulativeFatalities"] = -1
            texas_stats["DailyNewCases"] = -1
            texas_stats["DailyNewFatalities"] = -1
        else:
            texas_stats["CumulativeCases"] = self.today_stats.get("daily_new_cases", dict()).get("CumulativeCases", -1)
            texas_stats["CumulativeFatalities"] = self.today_stats.get("daily_new_cases", dict()).get("CumulativeFatalities", -1)
            texas_stats["DailyNewCases"] = self.today_stats.get("daily_new_cases", dict()).get("DailyNewCases", -1)
            texas_stats["DailyNewFatalities"] = self.today_stats.get("daily_new_cases", dict()).get("DailyNewFatalities", -1)
        texas_stats["County_sum_positives"]   = self.today_stats.get("sum_counties", dict()).get("sum_positive", -1)
        texas_stats["County_sum_fatalities"]  = self.today_stats.get("sum_counties", dict()).get("sum_fatalities", -1)
        texas_stats["County_sum_recoveries"]  = self.today_stats.get("sum_counties", dict()).get("sum_recoveries", -1)
        texas_stats["County_sum_active"]  = self.today_stats.get("sum_counties", dict()).get("sum_active", -1)
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
    

