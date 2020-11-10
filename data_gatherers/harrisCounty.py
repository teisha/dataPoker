import requests
import json
from datetime import datetime, timedelta, date
from data_gatherers import harrisCounty_config
import numpy as np 
import pandas as pd 
from services import database
from contextlib import suppress

class HarrisCountyRunner:
    def __init__(self, directory: str):
        self.history_stats = dict()
        self.today_stats = dict()
        self.current_date_time = datetime.now().strftime("%m-%d-%Y")
        self.fileName = "{}data/harrisCounty-{}.json".format(directory, self.current_date_time )
        self.people_detail_csv = "{}data/harrisCountyDetail-{}.csv".format(directory, self.current_date_time )
        self.today = datetime.now().strftime("%m/%d")
        self.yesterday = date.today() - timedelta(days=1)
        self.history_cutoff = ( date.today() - timedelta(days=5) ).strftime("%m/%d")
        print("TODAY: " + self.today + " HISTORY CUTOFF: " + self.history_cutoff)
        print('-----------------INIT HARRIS COUNTY RUNNER ------------------------------')


    def catch_em_all(self):
        print(' ----------- CATCH EM ALL ----------------- ')
        harrisCountyRecords=[]
        total_recs = requests.get(url=harrisCounty_config.DAILY_ALL, params=harrisCounty_config.total_rec_params)
        total_response = total_recs.json()
        print(total_response)

        total = 0
        if 'features' in total_response:
            total = total_response['features'][0].get('attributes').get('value')
        else:
            raise Exception('Cannot determine total records: ', total_response)            
        print(f"Analyzing {total} records")
        city_totals= requests.get(url=harrisCounty_config.CITY_SUMMARY_URL, params=harrisCounty_config.city_summary_params)
        city_response = city_totals.json()
        cases_by_city = []
        for citydata in city_response['features']:
            city_stats = dict({'TotalConfirmedCases': citydata.get('attributes').get('TotalConfirmedCases'),
                'ActiveCases': citydata.get('attributes').get('ActiveCases'),
                'Recovered': citydata.get('attributes').get('Recovered'),
                'Deceased': citydata.get('attributes').get('Deceased'),})
            cases_by_city.append(dict({citydata.get('attributes').get('CityName2'): city_stats }) )

        age_totals= requests.get(url=harrisCounty_config.DAILY_ALL, params=harrisCounty_config.agerange_summary_params)
        age_response = age_totals.json()

# A second method that we have been using at CartONG is to take advantage of the resultOffset query parameter (available since 10.3), 
# which allows to “skip the specified number of records and [to return response] starting from the next record” (Esri). 
# If we iterate queries, while each time adding the number of returned records
        chunk_params = harrisCounty_config.daily_all_params 
        while len(harrisCountyRecords) < int(total):
            
        # for feature in age_response['features']:
        #     # whereClause = f"City='{feature.get('attributes').get('City')}'"
        #     whereClause = f"AgeRange='{feature.get('attributes').get('AgeRange')}'"
        #     chunk_params=harrisCounty_config.daily_all_params
        #     chunk_params.update({'where': whereClause})
        #     print(chunk_params)
            currentOffset = int(chunk_params.get('resultOffset') )
            print('Current Offset is: ', currentOffset)
            response = requests.get(url=harrisCounty_config.DAILY_ALL, params=chunk_params)
            daily_response = response.json() 
            chunk_count = len(daily_response['features'])
            print(f"Count of chunk received: {chunk_count}")
            for rec in daily_response['features']:
                harrisCountyRecords.append(rec['attributes'])

            # features = [ sub['attributes'] for sub in  daily_response['features']]
            print(len(harrisCountyRecords))
            chunk_params.update({'resultOffset': f'{currentOffset + chunk_count}'})

        # ['OBJECTID', 'Id_str', 'Gender', 'AgeRange', 'Quadrant', 'ExposureType', 'Status', 'CaseType', 'Hospitalized', 'X', 'Y', 'DeceasedCOVID19_str',
        #     'Type', 'DateConvertedtoCase', 'DateConvertedtoCase_str', 'Source', 'confirmed', 'EditDate', 'ZIP', 'Race', 'DateSymptoms', 'DateSymptoms_str', 
        #     'City', 'DeceasedCOVID19Date']

        df_people = pd.DataFrame(harrisCountyRecords)
        try:
            df_people.to_csv(self.people_detail_csv)
        except:
            pass    
        
        total_cases = df_people['OBJECTID'].count()    # This is the stat for "Confirmed Cases"
        if int(total_cases) != int(total):
            print(age_response)
            raise Exception(f"STOP PROCESSING: Processed {total_cases} records, but expected {total}.  Make sure the API is still pulling back all the records ") 

        filterNotCompleted = df_people['Status']!="Completed"
        filterNotDeceased = df_people['Status']!="Deceased"
        active_cases = df_people.where(filterNotCompleted & filterNotDeceased)['OBJECTID'].count()
        recovered_cases = df_people.where(df_people['Status']=="Completed")['OBJECTID'].count()
        deceased_cases =  df_people.where(df_people['Status']=="Deceased")['OBJECTID'].count()
        cases_by_source = df_people.groupby('Source')['OBJECTID'].count()
        cases_by_age = df_people.groupby('AgeRange')['OBJECTID'].count()
        cases_by_gender = df_people.groupby('Gender')['OBJECTID'].count()
        # cases_by_city = df_people.groupby(df_people['City'].apply(lambda x: x if x != '' else 'Undefned'))['OBJECTID'].count()

        self.today_stats.update({'confirmed_cases': int(total_cases)}) 
        self.today_stats.update({'active_cases': int(active_cases)})
        self.today_stats.update({'recovered_cases': int(recovered_cases)})
        self.today_stats.update({'deceased_cases': int(deceased_cases)})
        self.today_stats.update({'cases_by_source': cases_by_source.to_dict()})
        self.today_stats.update({'cases_by_age': cases_by_age.to_dict()})
        self.today_stats.update({'cases_by_gender': cases_by_gender.to_dict()})
        self.today_stats.update({'cases_by_city': cases_by_city})
        self.today_stats.update({'date_collected' : self.current_date_time})

        series_dateSymptoms = df_people.groupby('DateSymptoms_str')['OBJECTID'].count()
        df_dateSymptoms = pd.DataFrame({'date': series_dateSymptoms.index,
            'count_symptoms': series_dateSymptoms}, columns=['date','count_symptoms'])
        # series_dateConverted = df_people.groupby('DateConvertedtoCase_str')['OBJECTID'].count()
        # df_dateConverted = pd.DataFrame({'date': series_dateConverted.index,
        #     'count_converted': series_dateConverted}, columns=['date','count_converted'])            
        # dateHistory = pd.merge(df_dateSymptoms, df_dateConverted, how='outer', on="date" )   #.to_csv('data/compare_DateSymptoms_str_updated.csv')

        dateHistory = df_dateSymptoms
        dateHistory.fillna(0, inplace=True)

        self.history_stats.update({'datedStats' : dateHistory.to_dict('records')})

        # df_dateConverted.drop('DateConvertedtoCase_str', inplace=True)            
        today_counts = dateHistory[dateHistory['date']==self.today].to_dict('records')
        self.today_stats.update({'statsByDate': today_counts[0] if len(today_counts) > 0 else dict()  })

        print (f"TODAY_STATS: {self.today_stats}")   
        # print ( pd.concat([series_dateConverted, series_dateConverted_nonupdate]))   # seems to add them together
        print ( '-------------------------------------------------------------' )
        # print(df_people.groupby('DateSymptoms_str')['DateSymptoms'].count().tail(10))
        # print(df_people.groupby('DateConvertedtoCase_str')['DateConvertedtoCase'].count().tail(10))
        # print(df_people.where(df_people['City'] == 'Friendswood').groupby('DateConvertedtoCase_str')['OBJECTID'].count().tail(10))

        # df_current = df_people[df_people['DateConvertedtoCase_str'] >= self.history_cutoff]
        # print(df_current.columns)
        # print(df_current['OBJECTID'].count())
        # print(df_current['DateConvertedtoCase_str'].value_counts())
        # df_people.to_csv('data/all_harris_county_updated.csv')
    
        try:
            history_file = open(self.fileName, "w")
            history_file.write('[')
            history_file.writelines(json.dumps(dict(DASHUpdated=self.today_stats))  )
            history_file.write(',')
            history_file.writelines(json.dumps(dict(datedTotals=self.history_stats))  )
            history_file.close()
        except:
            pass            
        # for feature in hospital_response['features']:
        #     print(feature)
        

    def get_summarized_data(self):
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        # This is where worldometer pulls from
        response2 = requests.get(url=harrisCounty_config.SUMMARY_ALL, params=harrisCounty_config.summary_all_params)
        sum_response = response2.json()
        summaries =  [ sub['attributes'] for sub in sum_response['features'] ]
        df_sum = pd.DataFrame(summaries)
        print (f'History Cutoff => {self.history_cutoff}')
        print(df_sum[df_sum['Date_Str'] >= self.history_cutoff])
        history_stats = dict(totals=df_sum[df_sum['Date_Str'] >= self.history_cutoff].to_dict('record'))
        df_rolled = df_sum[df_sum['Date_Str'] >= self.history_cutoff].groupby('Date_Str').agg(
            {
                'Recovered':sum, 
                'Deceased': sum, 
                'Active': sum,
                'NewCases': sum
            })
        # df_rolled.drop('Date_Str', inplace=True) 
        # print(df_rolled.loc[self.today:].head(1).to_dict('index'))
        self.today_stats.update(dict(totals=df_rolled.loc[self.today:].head(1).to_dict('index')) )            
        print(self.today_stats.get('totals'))

        with suppress(FileNotFoundError):        
            with open(self.fileName, "a") as history_file:
                history_out = (dict(totals=history_stats))
                history_file.write(',')
                history_file.writelines(json.dumps(history_out)  )
                history_file.write(']')

    def save_database(self):
        database_stats = dict({'date_collected' : self.current_date_time})
        database_stats['ConfirmedCases'] = self.today_stats.get('confirmed_cases')
        database_stats['ActiveCases'] =  self.today_stats.get('active_cases')
        database_stats['RecoveredCases'] =  self.today_stats.get('recovered_cases')
        database_stats['DeceasedCases'] =  self.today_stats.get('deceased_cases')
        source = self.today_stats.get('cases_by_source')
        for sourcename in source.keys():
            database_stats[f"SOURCE: {sourcename}"] = source.get(sourcename)
        ages = self.today_stats.get('cases_by_age')
        for agerange in ages.keys():
            database_stats[f"AGE_RANGE: {agerange}"] = ages.get(agerange) 
        genders = self.today_stats.get('cases_by_gender')
        for genderoptions in genders.keys():
            database_stats[f"GENDER: {genderoptions}"] = genders.get(genderoptions)             
        statsbydate = self.today_stats.get('statsByDate') 
        for statname in statsbydate.keys():
            if (statname != "date"):
                database_stats[f"STAT {statsbydate.get('date').replace('/','-')} {statname}"] = statsbydate.get(statname)                

        database_stats['ALL CASES: City Counts'] = self.today_stats.get('cases_by_city')
        summarytotals  = self.today_stats.get('totals')
        date = None
        for keyname in summarytotals.keys():
            date = keyname
        if date != None:
            database_stats[f"SUMMARY {date.replace('/','-')}: Recovered"] = summarytotals.get(date).get('Recovered')
            database_stats[f"SUMMARY {date.replace('/','-')}: Deceased"] = summarytotals.get(date).get('Deceased')
            database_stats[f"SUMMARY {date.replace('/','-')}: Active"] = summarytotals.get(date).get('Active')
            database_stats[f"SUMMARY {date.replace('/','-')}: NewCases"] = summarytotals.get(date).get('NewCases')
        print("DATABASE")
        print(database_stats)        
        database.save_harris_county(dict(harrisCounty=database_stats) )

        friendswood_stats = dict({'date_collected' : self.current_date_time})
        get_friendswood = next((stat for stat in self.today_stats.get('cases_by_city') if "Friendswood" in stat.keys()), None)
        print(get_friendswood)
        friendswood_stats['Friendswood TotalConfirmedCases'] = get_friendswood.get('Friendswood').get('TotalConfirmedCases')
        friendswood_stats['Friendswood ActiveCases'] = get_friendswood.get('Friendswood').get('ActiveCases')
        friendswood_stats['Friendswood Recovered'] = get_friendswood.get('Friendswood').get('Recovered')
        friendswood_stats['Friendswood Deceased'] = get_friendswood.get('Friendswood').get('Deceased')
        database.save_friendswood(dict(harrisCounty=friendswood_stats))
        


"""
pd.read_json expects a string. However, r.json() returns a dict object.

In your case, you should explore the structure of the returned JSON object by looking at x.keys(). This will yield ['count', '_links', 'teams']. You are probably interested in the 'teams' field.

As such, you should do the following:

r = requests.get('http://api.football-data.org/v1/competitions/398/teams')
x = r.json()
df = pd.DataFrame(x['teams'])
print df
"""


        # response_nonupdate = requests.get(url=harrisCounty_config.DAILY_ALL_NOUPDATE, params=harrisCounty_config.daily_all_params)
        # daily_nonupdate_respone = response_nonupdate.json()
        # features_nonupdate = [ sub['attributes'] for sub in daily_nonupdate_respone['features'] ]
        # df_people_nonupdate = pd.DataFrame(features_nonupdate)
        # print (f"TOTAL_RECS: {df_people['OBJECTID'].count()}, compare to nonupdate: {df_people_nonupdate['OBJECTID'].count()}")   

        # series_dateConverted_nonupdate = df_people_nonupdate.groupby('DateSymptoms_str')['OBJECTID'].count()
        # df_dateConverted_nonupdate = pd.DataFrame({'date': series_dateConverted_nonupdate.index,
        #     'count_nonupdated': series_dateConverted_nonupdate}, columns=['date','count_nonupdated'])            
        # pd.merge(df_dateConverted, df_dateConverted_nonupdate, how='outer', on="date" ).to_csv('data/compare_DateSymptoms_str_updated.csv')
        # print(pd.merge(df_dateConverted, df_dateConverted_nonupdate, how='outer', on="date" ) )   # They're both series, not dataframe
