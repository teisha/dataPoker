import requests
import json
from datetime import datetime, timedelta, date
import harrisCounty_config
import numpy as np 
import pandas as pd 
import database

class HarrisCountyRunner:
    def __init__(self):
        self.history_stats = dict()
        self.today_stats = dict()
        self.current_date_time = datetime.now().strftime("%m-%d-%Y")
        self.fileName = "F:/Dropbox/Coding/covid/data/harrisCounty-"+ self.current_date_time + ".json"
        self.people_detail_csv = "F:/Dropbox/Coding/covid/data/harrisCountyDetail-"+ self.current_date_time + ".csv"
        self.today = datetime.now().strftime("%m/%d")
        self.yesterday = date.today() - timedelta(days=1)
        self.three_days_ago = ( date.today() - timedelta(days=5) ).strftime("%m/%d")
        print("TODAY: " + self.today + " TWO DAYS AGO: " + self.three_days_ago)
        print('-----------------INIT------------------------------')


    def catch_em_all(self):
        harrisCountyStats=[]
        response = requests.get(url=harrisCounty_config.DAILY_ALL, params=harrisCounty_config.daily_all_params)
        daily_response = response.json()

        # ['OBJECTID', 'Id_str', 'Gender', 'AgeRange', 'Quadrant', 'ExposureType', 'Status', 'CaseType', 'Hospitalized', 'X', 'Y', 'DeceasedCOVID19_str',
        #     'Type', 'DateConvertedtoCase', 'DateConvertedtoCase_str', 'Source', 'confirmed', 'EditDate', 'ZIP', 'Race', 'DateSymptoms', 'DateSymptoms_str', 
        #     'City', 'DeceasedCOVID19Date']
        features = [ sub['attributes'] for sub in daily_response['features'] ]
        df_people = pd.DataFrame(features)
        df_people.to_csv(self.people_detail_csv)

        total_cases = df_people['OBJECTID'].count()    # This is the stat for "Confirmed Cases"
        filterNotCompleted = df_people['Status']!="Completed"
        filterNotDeceased = df_people['Status']!="Deceased"
        active_cases = df_people.where(filterNotCompleted & filterNotDeceased)['OBJECTID'].count()
        recovered_cases = df_people.where(df_people['Status']=="Completed")['OBJECTID'].count()
        deceased_cases =  df_people.where(df_people['Status']=="Deceased")['OBJECTID'].count()
        cases_by_source = df_people.groupby('Source')['OBJECTID'].count()
        cases_by_age = df_people.groupby('AgeRange')['OBJECTID'].count()
        cases_by_gender = df_people.groupby('Gender')['OBJECTID'].count()
        cases_by_city = df_people.groupby('City')['OBJECTID'].count()

        self.today_stats.update({'confirmed_cases': int(total_cases)}) 
        self.today_stats.update({'active_cases': int(active_cases)})
        self.today_stats.update({'recovered_cases': int(recovered_cases)})
        self.today_stats.update({'deceased_cases': int(deceased_cases)})
        self.today_stats.update({'cases_by_source': cases_by_source.to_dict()})
        self.today_stats.update({'cases_by_age': cases_by_age.to_dict()})
        self.today_stats.update({'cases_by_gender': cases_by_gender.to_dict()})
        self.today_stats.update({'cases_by_city': cases_by_city.to_dict()})
        self.today_stats.update({'date_collected' : self.current_date_time})



        series_dateSymptoms = df_people.groupby('DateSymptoms_str')['OBJECTID'].count()
        series_dateConverted = df_people.groupby('DateConvertedtoCase_str')['OBJECTID'].count()
        df_dateSymptoms = pd.DataFrame({'date': series_dateSymptoms.index,
            'count_symptoms': series_dateSymptoms}, columns=['date','count_symptoms'])
        df_dateConverted = pd.DataFrame({'date': series_dateConverted.index,
            'count_converted': series_dateConverted}, columns=['date','count_converted'])            

        dateHistory = pd.merge(df_dateSymptoms, df_dateConverted, how='outer', on="date" )   #.to_csv('data/compare_DateSymptoms_str_updated.csv')
        dateHistory.fillna(0, inplace=True)

        self.history_stats.update({'datedStats' : dateHistory.to_dict('records')})

        # df_dateConverted.drop('DateConvertedtoCase_str', inplace=True)            
        today_counts = dateHistory[dateHistory['date']==self.today].to_dict('records')
        print(today_counts[0])

        self.today_stats.update({'statsByDate': today_counts[0]})

        print (f"TODAY_STATS: {self.today_stats}")   
        print("History")          
        print (dateHistory.tail(10))
        print(self.history_stats)
        # print ( pd.concat([series_dateConverted, series_dateConverted_nonupdate]))   # seems to add them together
        print ( '-------------------------------------------------------------' )
        # print(df_people.groupby('DateSymptoms_str')['DateSymptoms'].count().tail(10))
        # print(df_people.groupby('DateConvertedtoCase_str')['DateConvertedtoCase'].count().tail(10))
        # print(df_people.where(df_people['City'] == 'Friendswood').groupby('DateConvertedtoCase_str')['OBJECTID'].count().tail(10))

        # df_current = df_people[df_people['DateConvertedtoCase_str'] >= self.three_days_ago]
        # print(df_current.columns)
        # print(df_current['OBJECTID'].count())
        # print(df_current['DateConvertedtoCase_str'].value_counts())
        # df_people.to_csv('data/all_harris_county_updated.csv')

        history_file = open(self.fileName, "w")
        history_file.write('[')
        history_file.writelines(json.dumps(dict(DASHUpdated=self.today_stats))  )
        history_file.write(',')
        history_file.writelines(json.dumps(dict(datedTotals=self.history_stats))  )
        history_file.close()
        # for feature in hospital_response['features']:
        #     print(feature)

    def get_summarized_data(self):
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        # This is where worldometer pulls from
        response2 = requests.get(url=harrisCounty_config.SUMMARY_ALL, params=harrisCounty_config.summary_all_params)
        sum_response = response2.json()
        summaries =  [ sub['attributes'] for sub in sum_response['features'] ]
        df_sum = pd.DataFrame(summaries)
        print(df_sum[df_sum['Date_Str'] >= self.three_days_ago])
        history_stats = dict(totals=df_sum[df_sum['Date_Str'] >= self.three_days_ago].to_dict('record'))
        df_rolled = df_sum[df_sum['Date_Str'] >= self.three_days_ago].groupby('Date_Str').agg(
            {
                'Recovered':sum, 
                'Deceased': sum, 
                'Active': sum,
                'NewCases': sum
            })
        # df_rolled.drop('Date_Str', inplace=True)    
        print(df_rolled.loc[self.today:].head(1).to_dict('index'))
        self.today_stats.update(dict(totals=df_rolled.loc[self.today:].head(1).to_dict('index')) )            

        history_file = open(self.fileName, "a")
        history_out = (dict(totals=history_stats))
        history_file.write(',')
        history_file.writelines(json.dumps(history_out)  )
        history_file.write(']')
        history_file.close()

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
        statsbydate = self.today_stats.get('statsByDate') 
        for statname in statsbydate.keys():
            if (statname != "date"):
                database_stats[f"STAT {statsbydate.get('date').replace('/','-')} {statname}"] = statsbydate.get(statname)                
        database_stats['Cities: FRIENDSWOOD'] = self.today_stats.get('cases_by_city').get('Friendswood') 
        # database_stats['Cities: Others'] = 
        summarytotals  = self.today_stats.get('totals')
        for keyname in summarytotals.keys():
            date = keyname
        database_stats[f"SUMMARY {date.replace('/','-')}: Recovered"] = summarytotals.get(date).get('Recovered')
        database_stats[f"SUMMARY {date.replace('/','-')}: Deceased"] = summarytotals.get(date).get('Deceased')
        database_stats[f"SUMMARY {date.replace('/','-')}: Active"] = summarytotals.get(date).get('Active')
        database_stats[f"SUMMARY {date.replace('/','-')}: NewCases"] = summarytotals.get(date).get('NewCases')
        print("DATABASE")
        print(database_stats)        
        database.save_harris_county(dict(harrisCounty=database_stats) )
        


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
