import requests
import json
from datetime import datetime, timedelta, date
from IPython.lib.pretty import pprint
import pickle

from urllib.parse import unquote, urlencode
from functools import reduce
from data_gatherers import txarc_config
from services import database
from contextlib import suppress

class Runner:
    def __init__(self):
        self.stat_pickler = dict()
        self.today_stats = dict()
        self.current_date_time = datetime.now().strftime("%m-%d-%Y")
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.yesterday = date.today() - timedelta(days=1)
        self.minustwo = date.today() - timedelta(days=2)
        print('-----------------INIT TXDHS------------------------------')

    def load_from_file(self, filename):
        with open(filename, "rb") as handle:
        # with open('filename.pickle', 'rb') as handle:
            self.stat_pickler = pickle.load(handle)
        print("Files loaded", self.stat_pickler)

    def get_daily_stats(self):
        URL = txarc_config.CURRENT_DAY_TEST_URL
        print(URL)
        response = requests.get(url=URL, params=txarc_config.current_day_params)
        print(response)
        stats = response.json()
        # print(type(stats), stats.keys())
        current_day_stats = []
        for feature in stats['features']:
            # print(feature.get('attributes'))
            totals = feature.get('attributes')           
            current_day_stats.append ( dict( test=totals.get('test_type'), total=+totals.get('count_') ) )
            totals.update({'date_collected' : self.current_date_time})

        # print(current_day_stats)
        self.stat_pickler.update( dict(current_day_stats=current_day_stats))
        self.today_stats.update( dict(current_day_stats=current_day_stats))


    def get_hospital_current(self):
        response = requests.get(url=txarc_config.HOSPITALS_CURRENT, params=txarc_config.hospitals_current_params)
        hospital_response = response.json()
        hospitals_current = []
        total_covid = 0
        total_beds_occupied = 0
        total_avail_beds = 0
        total_avail_icu_beds = 0
        total_avail_picu_beds = 0
        total_avail_vents = 0
        patients_ventilated = 0
        total_lab_confirmed = 0
        total_staffed_beds = 0
        total_lab_confirmed_24hrs = 0
        for feature in hospital_response['features']:
            # print(feature.get('attributes'))
            totals = feature.get('attributes')
            totals.update({'date_collected' : self.current_date_time})
            total_covid = total_covid + totals.get("ped_lab_confirmed_inpatient") + totals.get("total_adult_lab_confirmed")
            total_beds_occupied = total_beds_occupied + totals.get('total_beds_occupied')
            total_avail_beds = total_avail_beds +  totals.get("total_beds_available")
            total_avail_icu_beds = total_avail_icu_beds + totals.get("available_staffed_icu") 
            total_avail_picu_beds = total_avail_picu_beds + totals.get("available_staffed_picu")
            total_avail_vents = total_avail_vents + totals.get("total_ventilators_available")
            patients_ventilated = patients_ventilated + totals.get("patients_ventilated")
            total_lab_confirmed = total_lab_confirmed + totals.get("total_lab_confirmed")
            total_staffed_beds = total_staffed_beds + totals.get("total_hospital_capacity")
            total_lab_confirmed_24hrs = total_lab_confirmed_24hrs + totals.get("total_lab_confirmed_24hrs")
            hospitals_current.append(totals)
        harris = next((stat for stat in hospitals_current if stat["tsa"] == "Q"), None)
        galveston = next((stat for stat in hospitals_current if stat["tsa"] == "R"), None)
        # print( harris)
        state_totals = dict(total_covid=total_covid, total_avail_beds=total_avail_beds, total_lab_confirmed=total_lab_confirmed,
            total_avail_icu_beds=total_avail_icu_beds, total_avail_picu_beds=total_avail_picu_beds, total_avail_vents=total_avail_vents,
            total_beds_occupied=total_beds_occupied , patients_ventilated=patients_ventilated,
            total_staffed_beds=total_staffed_beds )
        state_totals.update({'date_collected' : self.current_date_time})
        # print(state_totals)
        self.stat_pickler.update( dict(hospitals_current=hospitals_current))
        self.today_stats.update(dict(harris_hospitals=harris, galveston_hospitals=galveston, 
            hospital_current_totals=state_totals) )
        



    def get_hospital_stats(self):
        response = requests.get(url=txarc_config.HOSPITAL_URL, params=txarc_config.hospitalizations_by_date_params)
        hospital_response = response.json()
        # print(hospital_response)
        new_response = requests.get(url=txarc_config.HOSPITALS_CUMULATIVE, params=txarc_config.hospitals_cum_params)
        new_hospital_response = new_response.json()
        # print(new_hospital_response)
        hospital_stats = []
        todays_stats = dict()
        for feature in hospital_response['features']:
            # print(feature)
            totals = feature.get('attributes')
            totals.update({'date_collected' : self.current_date_time})
            totals.update({'DateString': datetime.fromtimestamp(+totals.get('date')/1000).strftime('%Y-%m-%d') })
            hospital_stats.append ( totals )
        for feature in new_hospital_response['features']:
            totals = feature.get('attributes')  
            todays_stats[totals.get('count_type')] = totals.get('count_');      
            # todays_stats.append(totals)
        todays_stats.update({'date_collected' : self.current_date_time})
        self.stat_pickler.update(dict (hospital_stats=hospital_stats))
        last_stat = next((stat for stat in hospital_stats if stat["DateString"] == self.today), None)
        self.today_stats.update(dict(hospital_stats=todays_stats, hosp_stat=last_stat) )

    def get_viral_antibody_breakout(self):
        print(txarc_config.VIRAL_ANTIBODY_BREAKOUT_URL)
        print(txarc_config.no_date_params)
        response = requests.get(url= txarc_config.VIRAL_ANTIBODY_BREAKOUT_URL, params=txarc_config.no_date_params )
        viral_response = response.json()
        print(viral_response)
        viral_stats = []
        for feature in viral_response['features']:
            # print(feature.get('attributes'))
            totals = feature.get('attributes')
            totals.update({'date_collected' : self.current_date_time})
            # totals.update({'DateString': datetime.fromtimestamp(+totals.get('date')/1000).strftime('%Y-%m-%d') })
            totals.update({'DateString': self.current_date_time })
            # print(totals)
            viral_stats.append(totals)
        self.stat_pickler.update(dict(viral_antibody_stats=viral_stats))   
        last_stat = next((stat for stat in viral_stats if stat["DateString"] == self.yesterday.strftime("%Y-%m-%d")), None)
        self.today_stats.update( dict(viral_antibody_stats=last_stat) )         


    def get_positivity(self):
        print(txarc_config.POSITIVITY_TESTING_URL)
        response = requests.get(url= txarc_config.POSITIVITY_TESTING_URL, params=txarc_config.viral_antibody_breakout_by_day_params )
        positivity_response = response.json()
        positivity_stats = []
        # print(positivity_response)
        for feature in positivity_response['features']:
            # print(feature.get('attributes'))
            totals = feature.get('attributes')
            totals.update({'date_collected' : self.current_date_time})
            totals.update({'DateString': datetime.fromtimestamp(+totals.get('date')/1000).strftime('%Y-%m-%d') })
            # print(totals)
            positivity_stats.append(totals)
        self.stat_pickler.update(dict(positivity_stats=positivity_stats))   
        last_stat = next((stat for stat in positivity_stats if stat["DateString"] == self.yesterday.strftime("%Y-%m-%d")), None)
        if last_stat == None:
            last_stat = next((stat for stat in positivity_stats if stat["DateString"] == self.minustwo.strftime("%Y-%m-%d")), None)
        self.today_stats.update( dict(positivity_stats=last_stat) ) 

    def get_lab_testing_results(self):
        print(txarc_config.LAB_TESTING_URL)
        print(txarc_config.viral_antibody_breakout_by_day_params)
        response = requests.get(url= txarc_config.LAB_TESTING_URL, params=txarc_config.viral_antibody_breakout_by_day_params )
        lab_response = response.json()
        lab_stats = []
        print(lab_response)
        for feature in lab_response['features']:
            # print(feature.get('attributes'))
            totals = feature.get('attributes')
            totals.update({'date_collected' : self.current_date_time})
            totals.update({'DateString': datetime.fromtimestamp(+totals.get('Date')/1000).strftime('%Y-%m-%d') })
            # print(totals)
            lab_stats.append(totals)
        self.stat_pickler.update(dict(lab_stats=lab_stats))   
        last_stat = next((stat for stat in lab_stats if stat["DateString"] == self.yesterday.strftime("%Y-%m-%d")), None)
        if last_stat == None:
            last_stat = next((stat for stat in lab_stats if stat["DateString"] == self.minustwo.strftime("%Y-%m-%d")), None)
        self.today_stats.update( dict(lab_stats=last_stat) ) 


    def get_specimen_results(self):
        print(txarc_config.SPECIMEN_TESTING_URL)
        print(txarc_config.viral_antibody_breakout_by_day_params)
        response = requests.get(url= txarc_config.SPECIMEN_TESTING_URL, params=txarc_config.viral_antibody_breakout_by_day_params )
        specimen_response = response.json()
        specimen_stats = []
        for feature in specimen_response['features']:
            # print(feature.get('attributes'))
            totals = feature.get('attributes')
            totals.update({'date_collected' : self.current_date_time})
            totals.update({'DateString': datetime.fromtimestamp(+totals.get('date')/1000).strftime('%Y-%m-%d') })
            # print(totals)
            specimen_stats.append(totals)
        self.stat_pickler.update(dict(specimen_stats=specimen_stats))   
        last_stat = next((stat for stat in specimen_stats if stat["DateString"] == self.yesterday.strftime("%Y-%m-%d")), None)
        if last_stat == None:
            last_stat = next((stat for stat in specimen_stats if stat["DateString"] == self.minustwo.strftime("%Y-%m-%d")), None)
        self.today_stats.update( dict(specimen_stats=last_stat) ) 

    def get_daily_new_cases_by_date(self):
        response = requests.get(url=txarc_config.DAILY_NEW_CASES_URL, params=txarc_config.daily_new_cases_by_date_params)
        daily_response = response.json()
        # print(daily_response)
        daily_stats = []
        sum_all_fatalities = 0
        total_added_fatalities = 0
        for feature in daily_response['features']:
            totals = feature.get('attributes')
            totals.update({'date_collected' : self.current_date_time})
            totals.update({'DateString': datetime.fromtimestamp(+totals.get('date')/1000).strftime('%Y-%m-%d') })
            # print(totals)
            total_added_fatalities = total_added_fatalities + (int(totals.get('added_fatalities')) if totals.get('added_fatalities') != None else 0) + \
                (int(totals.get('incomplete_added_fatalities')) if totals.get('incomplete_added_fatalities') != None else 0)

            # print((0 if totals.get('DailyNewFatalities') == None or not totals.get('DailyNewFatalities').isnumeric() else totals.get('DailyNewFatalities',0) ))
            sum_all_fatalities = sum_all_fatalities + int(0 if totals.get('fatality_count') == None  else totals.get('fatality_count',0) ) 
            daily_stats.append(totals)
        self.stat_pickler.update(dict(daily_new_cases=daily_stats))      


        last_stat = next((stat for stat in daily_stats if stat["DateString"] >= self.yesterday.strftime("%Y-%m-%d")), None)
        if last_stat != None:
            last_stat.update({'FatalitiesAdded': total_added_fatalities})
            last_stat.update({'ReportedCummulativeFatalities': self.get_daily_cummulative_deaths()})
            last_stat.update({'SumDailyNewFatalities': sum_all_fatalities})
        self.today_stats.update(dict(daily_new_cases=last_stat) )          


    # this is what's displayed on the website as of the 27th
    def get_daily_cummulative_deaths(self):
        response = requests.get(url=txarc_config.DEATHS_CUMMULATIVE, params=txarc_config.death_cummulative_params)
        daily_response = response.json()
        print(daily_response)
        death_stat =  daily_response['features'][0].get('attributes').get("fatalities")
        return death_stat

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

        harris = next((stat for stat in daily_stats if stat["county"] == "Harris"), None)    
        galveston = next((stat for stat in daily_stats if stat["county"] == "Galveston"), None)          
        positive = 0
        fatalities = 0
        recoveries = 0
        active = 0
        for county_no in daily_stats:
            if county_no.get("confirmed"):
                positive = positive + county_no.get("confirmed")
            else:
                print("NO STATS: ", county_no)
            if county_no.get("fatalities"):
                fatalities = fatalities + int( county_no.get("fatalities") )
            if county_no.get("recovered"):
                # print(county_no.get("Recoveries"))
                recoveries = recoveries + int( county_no.get("recovered") )
            if county_no.get("active"):
                active = active + int( county_no.get("active")   )                                                        
        
        # sum_counties = reduce((lambda x,y: dict(sum_positive=x.get("Positive") + y.get("Positive"),
        #     sum_fatalities=x.get("Fatalities") + y.get("Fatalities"),
        #     sum_recoveries=x.get("Recoveries")+y.get("Recoveries"),
        #     sum_active=x.get("Active")+y.get("Active")) ), daily_stats)        
        sum_counties = dict(sum_positive=positive,
            sum_fatalities=fatalities,
            sum_recoveries=recoveries,
            sum_active=recoveries)
        sum_counties.update({'date_collected' : self.current_date_time})            
        self.today_stats.update(dict(sum_counties=sum_counties, harris=harris, galveston=galveston))      

    def get_county_totals(self):
        response_total = requests.get(url=txarc_config.TOTAL_COUNTIES_REPORTING_URL, params=txarc_config.total_counties_reporting_params)
        total_counties = response_total.json()["features"][0]
        # print(total_counties.get("attributes").get("value"))
        response_positives = requests.get(url=txarc_config.TOTAL_POSITIVES_URL, params=txarc_config.total_counties_with_positives_params)
        # print(response_positives.json())
        positive_counties = response_positives.json()["features"][0]
        # print(positive_counties.get("attributes").get("value"))
        totals = dict(total_counties=total_counties.get("attributes").get("value"), 
            positive_counties=positive_counties.get("attributes").get("value"))
        totals.update({'date_collected' : self.current_date_time})
        self.stat_pickler.update(dict(counties=totals))
        self.today_stats.update(dict(counties=totals))

    def run_all(self):
        print (" ===================== TEXAS DSHS BEGIN County Totals ====================")
        self.get_county_totals()
        print (" ===================== TEXAS DSHS BEGIN Daily Stats ====================")
        self.get_daily_stats()
        print (" ===================== TEXAS DSHS BEGIN Hospital Stats ====================")
        self.get_hospital_stats()
        print (" ===================== TEXAS DSHS BEGIN Hospital Current ====================")
        self.get_hospital_current()
        print (" ===================== TEXAS DSHS BEGIN Antibody Breakout ====================")
        # self.get_viral_antibody_breakout()
        print ("No longer available")
        print (" ===================== TEXAS DSHS BEGIN Current Day Positivity ====================")
        self.get_positivity()
        print (" ===================== TEXAS DSHS BEGIN Lab Testing Results ====================")
        self.get_lab_testing_results()
        print (" ===================== TEXAS DSHS BEGIN Specimen Results ====================")
        # self.get_specimen_results()
        print ("No longer available")
        print (" ===================== TEXAS DSHS BEGIN Daily New Cases ====================")
        self.get_daily_new_cases_by_date()
        print (" ===================== TEXAS DSHS BEGIN Counts By County ====================")
        self.get_daily_counts_by_county()
        print (" ===================== TEXAS DSHS DONE ====================")

    def write_to_file(self, filename, archive_dir):
        print ('------------------------------------------------------------------')
        # print(self.stat_pickler)
        # with open(filename, "wb") as handle:
        #     pickle.dump(self.stat_pickler, handle, protocol=pickle.HIGHEST_PROTOCOL)

        json_file = archive_dir + filename.replace('.pickle', '.json')
        with suppress(FileNotFoundError):        
            with open(json_file, "w") as json_handle:
                json_handle.writelines(json.dumps(self.stat_pickler)  )  

        with suppress(FileNotFoundError):
            today_file = filename.replace('.pickle', '-today.json')
            with open(today_file, "w") as json_handle:
                json_handle.writelines(json.dumps(self.today_stats)  )

    def write_to_database(self):
        harris_stats = self.today_stats.get("harris") 
        harris_hospitals = self.today_stats.get("harris_hospitals")
        harris_save_stats = dict()
        harris_save_stats["date_collected"] = harris_stats.get("date_collected")
        harris_save_stats["Positive"] = harris_stats.get("confirmed")
        harris_save_stats["Fatalities"] = harris_stats.get("fatalities")
        harris_save_stats["Recoveries"] = harris_stats.get("recovered")
        harris_save_stats["Active"] = harris_stats.get("active")
        harris_save_stats["TraumaServiceArea"] = harris_hospitals.get("tsa")
        harris_save_stats["RegionalAdvisoryCouncil"] = harris_hospitals.get("rac") 
        harris_save_stats["PopulationEstimate"] = harris_hospitals.get("est_population_2020") 
        harris_save_stats["TotalHospitalCapacity"] = harris_hospitals.get("total_hospital_capacity")
        harris_save_stats["AvailableHospitalBeds"] = harris_hospitals.get("total_beds_available")
        harris_save_stats["AvailableICUBeds"] = harris_hospitals.get("available_staffed_icu")
        harris_save_stats["AvailablePICUBeds"] = harris_hospitals.get("available_staffed_picu")
        harris_save_stats["AvailableVentilators"] = harris_hospitals.get("total_ventilators_available")
        harris_save_stats["COVIDPatients"] = harris_hospitals.get("total_lab_confirmed")
        harris_save_stats["PatientsVentilated"] = harris_hospitals.get("patients_ventilated")
        database.save_harris_county(dict(dhs=harris_save_stats))

        galveston_stats = self.today_stats.get("galveston") 
        galveston_hospitals = self.today_stats.get("galveston_hospitals")
        galveston_save_stats = dict()
        galveston_save_stats["date_collected"] = galveston_stats.get("date_collected")
        galveston_save_stats["Positive"] = galveston_stats.get("confirmed")
        galveston_save_stats["Fatalities"] = galveston_stats.get("fatalities")
        galveston_save_stats["Recoveries"] = galveston_stats.get("recovered")
        galveston_save_stats["Active"] = galveston_stats.get("active")
        galveston_save_stats["TraumaServiceArea"] = galveston_hospitals.get("tsa")
        galveston_save_stats["RegionalAdvisoryCouncil"] = galveston_hospitals.get("rac") 
        galveston_save_stats["PopulationEstimate"] = galveston_hospitals.get("est_population_2020") 
        galveston_save_stats["TotalHospitalCapacity"] = galveston_hospitals.get("total_hospital_capacity")
        galveston_save_stats["AvailableHospitalBeds"] = galveston_hospitals.get("total_beds_available")
        galveston_save_stats["AvailableICUBeds"] = galveston_hospitals.get("available_staffed_icu")
        galveston_save_stats["AvailablePICUBeds"] = galveston_hospitals.get("available_staffed_picu")
        galveston_save_stats["AvailableVentilators"] = galveston_hospitals.get("total_ventilators_available")
        galveston_save_stats["COVIDPatients"] = galveston_hospitals.get("total_lab_confirmed")
        galveston_save_stats["PatientsVentilated"] = galveston_hospitals.get("patients_ventilated")
        database.save_galveston_county(dict(dhs=galveston_save_stats))

        texas_stats = dict()
        texas_stats["date_collected"] = self.today_stats.get("counties").get("date_collected")
        texas_stats["positive_counties"] = self.today_stats.get("counties").get("positive_counties")
        texas_stats["REPORTED_TotalTests"] = next((stat.get("total") for stat in self.today_stats.get("current_day_stats") if stat["test"] == "total_test"), None) 
        texas_stats["AntibodyTests"] = next((stat.get("total") for stat in self.today_stats.get("current_day_stats") if stat["test"] == "antibody_test"), None) 
        texas_stats["PostiveAntibody"] = next((stat.get("total") for stat in self.today_stats.get("current_day_stats") if stat["test"] == "antibody_positive"), None) 
        texas_stats["AntigenTests"] = next((stat.get("total") for stat in self.today_stats.get("current_day_stats") if stat["test"] == "antigen_test"), None) 
        texas_stats["PositiveAntigen"] = next((stat.get("total") for stat in self.today_stats.get("current_day_stats") if stat["test"] == "antigen_positive"), None) 
        texas_stats["ViralTests"] = next((stat.get("total") for stat in self.today_stats.get("current_day_stats") if stat["test"] == "viral_test"), None) 
        hospital_totals = self.today_stats.get("hospital_current_totals")
        texas_stats["HOSP: TotalCovidPatients"] = hospital_totals.get("total_covid")
        texas_stats["HOSP: TotalBedsOccupied"] = hospital_totals.get("total_beds_occupied")
        texas_stats["HOSP: TotalAvailableBeds"] = hospital_totals.get("total_avail_beds")
        texas_stats["HOSP: TotalAvailableICUBeds"] = hospital_totals.get("total_avail_icu_beds")
        texas_stats["HOSP: TotalAvailableVents"] = hospital_totals.get("total_avail_vents")
        texas_stats["HOSP: TotalPatientsVentilated"] = hospital_totals.get('patients_ventilated')
        texas_stats["HOSP: TotalStaffedBeds"] = hospital_totals.get('total_staffed_beds')
        texas_stats["HOSP: NewLast24Hours"] = hospital_totals.get('total_lab_confirmed_24hrs')
        print(" +++++++++++++++++++++++++++++++++++++++++++++++++++++ ")
        print (self.today_stats.get("hospital_stats"))
        if self.today_stats.get("hospital_stats") == None:
            texas_stats["HOSP: StateTotals"] = -1
        else:
            state_hosp_totals=self.today_stats.get("hospital_stats")
            texas_stats["HOSP: C19All-In"] = state_hosp_totals.get("patient_count")
            texas_stats["HOSP: C19Adult"] = state_hosp_totals.get("adult_beds")
            texas_stats["HOSP: C19AdultICU"] = state_hosp_totals.get("adult_icu_beds")
            texas_stats["HOSP: C19Ped"] = state_hosp_totals.get("pediatric_beds")
            texas_stats["StateHospitalReportedTotals"] = state_hosp_totals
        if self.today_stats.get("hosp_stat") == None:
            texas_stats["Hospitalizations"] = -1
        else:    
            texas_stats["Hospitalizations"] = self.today_stats.get("hosp_stat", dict(Hospitalizations=-1)).get("Hospitalizations", -1)
        if self.today_stats.get("viral_antibody_stats") == None:
            texas_stats["SevenDayPositiveTestRate"] = -1
            texas_stats["NewViral"] = -1
            texas_stats["NewAntibody"] = -1
            texas_stats["TotalAntibodyTests"] = -1
            texas_stats["TotalAntigenTests"] = -1
            texas_stats["TotalMolecularTests"] = -1
            texas_stats["NewTotal"] = -1
        else:            
            texas_stats["SevenDayPositiveTestRate"] = self.today_stats.get("viral_antibody_stats", dict()).get("SevenDayPositiveTestRate", -1)
            texas_stats["NewViral"] = self.today_stats.get("viral_antibody_stats", dict()).get("NewViral", -1)
            texas_stats["NewTotal"] = self.today_stats.get("viral_antibody_stats", dict()).get("NewTotal", -1)
            texas_stats["NewAntibody"] = self.today_stats.get("viral_antibody_stats", dict()).get("NewAntibody", -1)
            texas_stats["TotalAntibodyTests"] = self.today_stats.get("viral_antibody_stats", dict()).get("AntibodyTests", -1)
            texas_stats["TotalAntigenTests"] = self.today_stats.get("viral_antibody_stats", dict()).get("AntigenTests", -1)
            texas_stats["TotalMolecularTests"] = self.today_stats.get("viral_antibody_stats", dict()).get("ViralTests", -1)
        if self.today_stats.get("lab_stats") == None:
            texas_stats["LAB_OldTest"] = -1
            texas_stats["LAB_OldPositive"] = -1
            texas_stats["LAB_Tests"] = -1
            texas_stats["LAB_Positives"] = -1
            texas_stats["LAB_Positivity"] = -1
            texas_stats["LAB_Test7Day"] = -1
            texas_stats["LAB_Positive7Day"] = -1
        else:
            texas_stats["LAB_OldTest"] =  self.today_stats.get("lab_stats").get("total_tests")
            texas_stats["LAB_OldPositive"] =  self.today_stats.get("lab_stats").get("positives")            
            texas_stats["LAB_Tests"] = self.today_stats.get("lab_stats").get("new_tests")
            texas_stats["LAB_Positives"] = self.today_stats.get("lab_stats").get("new_positives")
            texas_stats["LAB_Positivity"] = self.today_stats.get("positivity_stats").get("antigen_rate")
            texas_stats["LAB_Test7Day"] = self.today_stats.get("lab_stats").get("test_seven_day")
            texas_stats["LAB_Positive7Day"] = self.today_stats.get("lab_stats").get("positive_seven_day")
        if self.today_stats.get("specimen_stats") == None:
            texas_stats["SEPCIMEN_OldTest"] = -1
            texas_stats["SEPCIMEN_NewTest"] = -1
            texas_stats["SEPCIMEN_OldPositive"] = -1
            texas_stats["SEPCIMEN_NewPositive"] = -1
            texas_stats["SEPCIMEN_Positivity"] = -1
            texas_stats["SPECIMEN_Test7Day"] = -1
            texas_stats["SPECIMEN_TestPositive7Day"] = -1
        else:
            texas_stats["SEPCIMEN_OldTest"] = self.today_stats.get("specimen_stats").get("total_tests")
            texas_stats["SEPCIMEN_NewTest"] = self.today_stats.get("specimen_stats").get("positives")
            texas_stats["SEPCIMEN_OldPositive"] = self.today_stats.get("specimen_stats").get("new_tests")
            texas_stats["SEPCIMEN_NewPositive"] = self.today_stats.get("specimen_stats").get("new_positives")
            texas_stats["SEPCIMEN_Positivity"] = self.today_stats.get("positivity_stats").get("molecular_rate")
            texas_stats["SPECIMEN_Test7Day"] = self.today_stats.get("specimen_stats").get("test_seven_day")
            texas_stats["SPECIMEN_TestPositive7Day"] = self.today_stats.get("specimen_stats").get("positive_seven_day")
        if self.today_stats.get("daily_new_cases") == None:
            texas_stats["CumulativeCases"] = -1
            texas_stats["CumulativeFatalities"] = -1
            texas_stats["DailyNewCases"] = -1
            texas_stats["DailyNewFatalities"] = -1
            texas_stats["SUM-AllDailyNewFatalities"] = -1
        else:
            texas_stats["CumulativeCases"] = self.today_stats.get("daily_new_cases", dict()).get("cumulative_cases", -1)
            texas_stats["CumulativeFatalities"] = self.today_stats.get("daily_new_cases", dict()).get("cumulative_fatalities", -1)
            texas_stats["DailyNewCases"] = self.today_stats.get("daily_new_cases", dict()).get("daily_new_cases", -1)
            texas_stats["DailyNewFatalities"] = self.today_stats.get("daily_new_cases", dict()).get("fatality_count", -1)
            texas_stats["SUM-AllDailyNewFatalities"] = self.today_stats.get("daily_new_cases", dict()).get("SumDailyNewFatalities", -1)
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
    

