import requests
import json
from datetime import datetime
from IPython.lib.pretty import pprint
import pickle
import txarc_config

class Runner:
    def __init__(self):
        self.stat_pickler = []
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



    def write_to_file(self, filename):
        print ('------------------------------------------------------------------')
        print(self.stat_pickler)
        with open(filename, "wb") as handle:
            pickle.dump(self.stat_pickler, handle, protocol=pickle.HIGHEST_PROTOCOL)


