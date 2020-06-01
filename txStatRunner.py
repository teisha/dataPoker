import requests
import json
from datetime import datetime
from IPython.lib.pretty import pprint
import pickle
import txarc_config
from urllib.parse import unquote, urlencode

class Runner:
    def __init__(self):
        self.stat_pickler = dict()
        self.current_date_time = datetime.now().strftime("%m-%d-%Y")

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
        self.stat_pickler.update( dict(current_day_stats=current_day_stats))


    def get_hospital_stats(self):
        response = requests.get(url=txarc_config.HOSPITAL_URL, params=txarc_config.hospitalizations_by_date_params)
        hospital_response = response.json()
        hospital_stats = []
        for feature in hospital_response['features']:
            # print(feature.get('attributes'))
            totals = feature.get('attributes')
            totals.update({'DateString': datetime.fromtimestamp(+totals.get('Date')/1000).strftime('%Y-%m-%d') })
            hospital_stats.append ( totals )
        self.stat_pickler.update(dict (hospital_stats=hospital_stats))

    def get_viral_antibody_breakout(self):
        response = requests.get(url= txarc_config.VIRAL_ANTIBODY_BREAKOUT_URL, params=txarc_config.viral_antibody_breakout_by_day_params )
        viral_response = response.json()
        viral_stats = []
        for feature in viral_response['features']:
            print(feature.get('attributes'))
            totals = feature.get('attributes')
            totals.update({'DateString': datetime.fromtimestamp(+totals.get('Date')/1000).strftime('%Y-%m-%d') })
            viral_stats.append(totals)
        self.stat_pickler.update(dict(viral_antibody_stats=viral_stats))            

    def get_daily_new_cases_by_date(self):
        response = requests.get(url=txarc_config.DAILY_NEW_CASES_URL, params=txarc_config.daily_new_cases_by_date_params)
        daily_response = response.json()
        # print(daily_response)
        daily_stats = []
        for feature in daily_response['features']:
            # print(feature.get('attributes'))
            totals = feature.get('attributes')
            totals.update({'DateString': datetime.fromtimestamp(+totals.get('Date')/1000).strftime('%Y-%m-%d') })
            daily_stats.append(totals)
        self.stat_pickler.update(dict(daily_new_cases=daily_stats))                


    def get_daily_counts_by_county(self):
        response = requests.get(url=txarc_config.DAILY_COUNTY_COUNTS_URL, params=txarc_config.daily_counts_by_county_params)
        print(response.url)
        daily_response = response.json()
        daily_stats = []
        for feature in daily_response['features']:
            print(feature.get('attributes'))
            totals = feature.get('attributes')
            totals.update({'DateString': datetime.now().strftime('%Y-%m-%d') })
            daily_stats.append(totals)
        self.stat_pickler.update(dict(daily_counts_by_county=daily_stats))         

    def get_county_totals(self):
        response_total = requests.get(url=txarc_config.TOTAL_COUNTIES_REPORTING_URL, params=txarc_config.total_counties_reporting_params)
        total_counties = response_total.json()["features"][0]
        # print(total_counties.get("attributes").get("value"))
        response_positives = requests.get(url=txarc_config.TOTAL_POSITIVES_URL, params=txarc_config.total_counties_with_positives_params)
        positive_counties = response_positives.json()["features"][0]
        # print(positive_counties.get("attributes").get("value"))
        totals = dict(total_counties=total_counties.get("attributes").get("value"), 
            positive_counties=positive_counties.get("attributes").get("value"))
        self.stat_pickler.update(dict(counties=totals))
        # return (dict(total_counties=total_counties.get("attributes").get("value"), 
        #     total_positive_counties=positive_counties.get("attributes").get("value"))) 

    def write_to_file(self, filename):
        print ('------------------------------------------------------------------')
        print(self.stat_pickler)
        with open(filename, "wb") as handle:
            pickle.dump(self.stat_pickler, handle, protocol=pickle.HIGHEST_PROTOCOL)

        json_file = filename.replace('.pickle', '.json')
        with open(json_file, "w") as json_handle:
            json_handle.writelines(json.dumps(self.stat_pickler)  )          
