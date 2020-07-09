from __future__ import print_function
import pickle
import os.path
from datetime import datetime, timedelta, date
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import galvestonCounty_config
import json
import database


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

class GalvestonCountyRunner:
    def __init__(self):
        self.friendswood_stats = dict()
        self.history_stats = dict()
        self.today_stats = dict()
        self.current_date_time = datetime.now().strftime("%m-%d-%Y")
        self.fileName = "F:/Dropbox/Coding/covid/data/galvestonCounty-"+ self.current_date_time + ".json"
        self.today = datetime.now().strftime("%#d-%B")
        print(self.today)
        self.yesterday = date.today() - timedelta(days=1)
        self.history_cutoff = ( date.today() - timedelta(days=5) ).strftime("%m/%d")
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                print(creds)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'config/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self.service = build('sheets', 'v4', credentials=creds)
        print ('------------------- INIT GALVESTON COUNTY --------------------')

    # Call the Sheets API
    def getSpreadsheetData(self, spreadsheetId):
        sheet = self.service.spreadsheets()
        meta = self.service.spreadsheets().get(spreadsheetId=spreadsheetId, fields='sheets(properties(index,sheetId,title))').execute()
        res = self.service.spreadsheets().get(spreadsheetId=spreadsheetId, fields='sheets(data/rowData/values/userEnteredValue,properties(index,sheetId,title))').execute()
        sheetIndex = 0
        sheetName = res['sheets'][sheetIndex]['properties']['title']
        lastRow = len(res['sheets'][sheetIndex]['data'][0]['rowData'])
        lastColumn = max([len(e['values']) for e in res['sheets'][sheetIndex]['data'][0]['rowData'] if e])
        print(meta)
        # print(sheetIndex, sheetName, lastRow, lastColumn)
        result = sheet.values().get(spreadsheetId=spreadsheetId,
                                    range=sheetName,majorDimension='ROWS').execute()
        values = result.get('values', [])
        returnValue = []

        if not values:
            return dict()
        else:
            headers = values[0]
            sheet_iterator = iter(values)
            next(sheet_iterator)            
            for row in sheet_iterator:
                asDict = dict({'date_collected' : self.current_date_time})
                for i in range(len(headers)):
                    asDict.update({headers[i]: row[i]})
                print(asDict)
                returnValue.append(asDict)
            return returnValue

    def getCityTotals(self):
        cityTotals = self.getSpreadsheetData(galvestonCounty_config.totals_by_city)
        friendswood = next((stat for stat in cityTotals if stat["City"] == 'Friendswood'), None)
        cases_by_city = dict()
        for city in cityTotals:
            cases_by_city.update({city.get('City').replace('/','') : city.get('Total Cases')})
        self.today_stats.update({'cases_by_city': cases_by_city})            
        self.history_stats.update({'cityTotals': cityTotals})
        self.friendswood_stats.update({'galvestonCounty': friendswood})

    def getHospitalizedTotals(self):
        hospitalizedTotals = self.getSpreadsheetData(galvestonCounty_config.hospitalized_quarantined_by_date)
        self.history_stats.update({'hospitalized': hospitalizedTotals})
        today_hospitalized = next((stat for stat in hospitalizedTotals if stat["Date"] == self.today), None)
        if today_hospitalized != None:
            self.today_stats.update({'hospitalized': today_hospitalized})

    def getRollingTotals(self):
        rollingTotals = self.getSpreadsheetData(galvestonCounty_config.rolling_totals)
        self.history_stats.update({'cumulative_totals': rollingTotals})
        cumulative_stats = next((stat for stat in rollingTotals if stat["Date"] == self.today), None)
        if cumulative_stats != None:
            self.today_stats.update({'cumulative_totals': cumulative_stats})        

    def getTotalsPerDay(self):
        dailyTotals = self.getSpreadsheetData(galvestonCounty_config.totals_per_day)
        self.history_stats.update({'daily_totals': dailyTotals})
        daily_stats = next((stat for stat in dailyTotals if stat["Date"] == self.today), None)
        if daily_stats != None:
            self.today_stats.update({'daily_stats': daily_stats})

    def getTotalsByAge(self):
        totalsByAge = self.getSpreadsheetData(galvestonCounty_config.totals_by_age)
        age_stats = dict()
        for ageGroup in totalsByAge:
            age_stats.update({ageGroup.get('') : ageGroup.get('Total Cases')})
        self.history_stats.update({'totalsByAge': totalsByAge})
        self.today_stats.update({'totalsByAge': age_stats})

    def getTotalsByGender(self):
        totalsByGender = self.getSpreadsheetData(galvestonCounty_config.totals_by_gender)
        self.history_stats.update({'totalsByGender': totalsByGender})
        gender_today = []
        for rec in totalsByGender:
            genderRec = dict({'Total Cases': rec.get('Total Cases'), 
                'Recovered': rec.get('Recovered'),
                'Deceased': rec.get('Deceased') })
            gender_today.append(dict({f"GENDER {rec.get('')}": genderRec }))                
        self.today_stats.update({'totalsByGender': gender_today})

    def getNewCases(self):
        newCases = self.getSpreadsheetData(galvestonCounty_config.new_cases_new_tested_by_week)
        self.history_stats.update({'weeklySummary': newCases})
        self.today_stats.update({'lastWeeklySummary': newCases[-1]})

    def getAllData(self):  
        self.getCityTotals()
        self.getHospitalizedTotals()
        self.getRollingTotals()
        self.getTotalsPerDay()
        self.getTotalsByAge()
        self.getTotalsByGender()
        self.getNewCases()

        print(self.today_stats)   

        history_file = open(self.fileName, "w")
        history_file.write('[')
        history_file.writelines(json.dumps(dict(TODAY=self.today_stats))  )
        history_file.write(',')
        history_file.writelines(json.dumps(dict(HISTORY=self.history_stats))  )
        history_file.write(']')
        history_file.close()

    def pickle_off(self):
        print(self.today_stats)
        with open('data/galveston_today.pickle', "wb") as handle:
            pickle.dump(self.today_stats, handle, protocol=pickle.HIGHEST_PROTOCOL)     
        with open('data/galveston_history.pickle', "wb") as handle:
            pickle.dump(self.history_stats, handle, protocol=pickle.HIGHEST_PROTOCOL) 

    def pickle_on(self):
        with open('data/galveston_today.pickle', 'rb') as handle:
            self.today_stats = pickle.load(handle)   
        with open('data/galveston_history.pickle', 'rb') as handle:
            self.history_stats = pickle.load(handle)                                     

    def saveToDatabase(self):
        print("TODAY")
        print(self.today_stats)
        database_stats = dict({'date_collected' : self.current_date_time})  
        print(self.today_stats.get('totalsByAge'))
        database_stats.update({'ALL CASES: City Counts': self.today_stats.get('cases_by_city')})  
        database_stats.update({'AGE GROUPS': self.today_stats.get('totalsByAge')}) 
        summary_stats = self.today_stats.get('cumulative_totals')   
        if summary_stats != None:
            database_stats.update({f"SUMMARY {self.today} Total Cases": summary_stats.get('Total Cases')})
            database_stats.update({f"SUMMARY {self.today} Recovered": summary_stats.get('Recovered')})
            database_stats.update({f"SUMMARY {self.today} Deaths": summary_stats.get('Deaths')})
        hospital_stats = self.today_stats.get('hospitalized') 
        if hospital_stats != None:
            database_stats.update({'Hospitalized': hospital_stats.get('Hospitalized')})   
            database_stats.update({'Self-Quarantined': hospital_stats.get('Self-Quarantined')})  
        daily_stats = self.today_stats.get('daily_stats')                    
        if daily_stats != None:
            database_stats.update({f"DAILY {self.today} Total Cases" : daily_stats.get('Total Cases')})
            database_stats.update({f"DAILY {self.today} Recovered" : daily_stats.get('Recovered')})
            database_stats.update({f"DAILY {self.today} Deceased" : daily_stats.get('#Deceased')})
        gender_stats = self.today_stats.get('totalsByGender')
        for gender_rec in gender_stats:
            database_stats.update(gender_rec)
        database_stats.update(dict(lastWeeklyUpdate=self.today_stats.get('lastWeeklySummary'))   )         
        print("DATABASE")
        print(database_stats)
        database.save_galveston_county(dict(galvestonCounty=database_stats) )  
        database.save_friendswood(self.friendswood_stats)          



# 'hospitalized': {'date_collected': '07-07-2020', 'Date': '2-July', 'Hospitalized ': '89', 'Self-Quarantined': '2642'}, 
# 'cumulative_totals': {'date_collected': '07-07-2020', 'Date': '2-July', 'Total Cases': '3778', 'Recovered': '1001', 'Deaths': '46'}, 
# 'daily_stats': {'date_collected': '07-07-2020', 'Date': '2-July', 'Total Cases': '213', 'Recovered': '73', '#Deceased': '1'},            

# 'totalsByGender': [{'date_collected': '07-07-2020', '': 'Male', 'Total Cases': '2149', 'Recovered': '554', 'Deceased': '26'}, 
# {'date_collected': '07-07-2020', '': 'Female', 'Total Cases': '2660', 'Recovered': '740', 'Deceased': '24'}]}