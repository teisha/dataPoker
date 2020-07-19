
import sys
sys.path.insert(0, 'services')

import importlib
loader = importlib.machinery.SourceFileLoader('database', 'services/database.py')
database = loader.load_module('database')
from _datetime import date, timedelta, datetime
import pandas as pd
from collections import ChainMap


class TexasReporter:

    def __init__(self):
        self.todaysdate = datetime.now()


    def getTexasStats(self, numdays: int):
        dates = []
        datelist = pd.date_range(start=self.todaysdate -timedelta(days=numdays), end=self.todaysdate).tolist()
        # print(datelist)
        for date_item in datelist:
            dhs_stats = database.getTexas(date)
            if dhs_stats != None:
                dates.append(dict({date_item.to_pydatetime().date() :  dhs_stats.get('dhs') }))
        # print(dates)
        dframe_dhs = pd.DataFrame.from_dict(ChainMap(*dates), orient='index')
        print(dframe_dhs.columns)

        cutoff = datetime(2020,7,6).date()
        print(dframe_dhs.filter(regex='HOSP').sort_index(axis = 0).loc[cutoff:])            
        print(dframe_dhs[['DailyNewCases','DailyNewFatalities','CumulativeCases','CumulativeFatalities','SevenDayPositiveTestRate',
          'NewViral','ViralTests','REPORTED_TotalTests']].sort_index(axis = 0))

    def talk_to_me(self, numdays: int):
        dates = []
        datelist = pd.date_range(start=self.todaysdate -timedelta(days=numdays), end=self.todaysdate).tolist()
        for date_item in datelist:
            friendswood_stats = database.getFriendswood(date_item)
            # print(friendswood_stats)
            if friendswood_stats != None:
                fwood = dict()
                harris = friendswood_stats.get('harrisCounty')
                harrisCountyTotal = int(harris.get('Friendswood TotalConfirmedCases') if harris.get('Friendswood TotalConfirmedCases') != None else harris.get('Harris County:') )
                fwood.update({'HarrisCo TOTAL': harrisCountyTotal})
                fwood.update({'HarrisCo Deceased': harris.get('Friendswood Deceased') })
                fwood.update({'HarrisCo Recovered': harris.get('Friendswood Recovered') })
                fwood.update({'HarrisCo ActiveCases': harris.get('Friendswood ActiveCases') })

                galveston = friendswood_stats.get('galvestonCounty')
                if galveston != None:
                    galvestonTotal = int(galveston.get('Total Cases'))
                    fwood.update({'GalvestonCo TOTAL': galveston.get('Total Cases')})
                    fwood.update({'GalvestonCo Recovered': galveston.get('Recovered') })
                    fwood.update({'Friendswood TOTAL': harrisCountyTotal + galvestonTotal})
                    fwood.update({'Friendswood Recovered': int(harris.get('Friendswood Recovered')  if harris.get('Friendswood Recovered') != None else '0' ) + 
                        int(galveston.get('Recovered') if galveston.get('Recovered') != None else '0' )  })
                else:
                    fwood.update({'Friendswood TOTAL': harrisCountyTotal}) 
                    fwood.update({'Friendswood Recovered': harris.get('Friendswood Recovered')})                   

                dates.append(dict({date_item.to_pydatetime().date() : fwood}))
                # print(dates)

        dframe_fwood = pd.DataFrame.from_dict(ChainMap(*dates), orient='index')
        print(dframe_fwood[['Friendswood TOTAL', 'HarrisCo TOTAL','GalvestonCo TOTAL', 'HarrisCo Deceased', 'Friendswood Recovered' ]].sort_index(axis = 0))


    
if __name__ == "__main__":
    reporter = TexasReporter()
    reporter.talk_to_me(45)
    # reporter.getStats(date.today() - timedelta(days=5) )    