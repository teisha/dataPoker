
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

    def get_texas_stats(self, numdays: int):
        dates = []
        tx_dates = []
        tx_test_dates = []
        datelist = pd.date_range(start=self.todaysdate -timedelta(days=numdays), end=self.todaysdate).tolist()
        # print(datelist)
        for date_item in datelist:
            texas_stats = dict()
            texas_test_stats = dict()
            alltx_stats = database.getTexas(date_item)
            if alltx_stats != None:
                dhs_stats = alltx_stats.get('dhs')
                if dhs_stats != None:
                    dhs_stats.update({'day': date_item.to_pydatetime().strftime('%a')})
                    dates.append(dict({date_item.to_pydatetime().date() :  alltx_stats.get('dhs') }))

                    texas_stats.update({'day': date_item.to_pydatetime().strftime('%a')})
                    texas_test_stats.update({'day': date_item.to_pydatetime().strftime('%a')})
                    texas_stats.update({'DailyNew': dhs_stats.get('DailyNewCases')})
                    texas_stats.update({'DailyFatal': dhs_stats.get('DailyNewFatalities')})
                    texas_stats.update({'CumCases': dhs_stats.get('CumulativeCases')})
                    texas_stats.update({'CumFatal': dhs_stats.get('CumulativeFatalities')})
                    texas_test_stats.update({'SevenDayPositive': dhs_stats.get('SevenDayPositiveTestRate')})
                    texas_test_stats.update({'NewAntigen': dhs_stats.get('AntigenTests')})
                    texas_test_stats.update({'NewViral': dhs_stats.get('NewViral')})
                    texas_test_stats.update({'CumViral': dhs_stats.get('ViralTests')})
                    texas_test_stats.update({'TotalTests': dhs_stats.get('REPORTED_TotalTests')})
                worldo_stats = alltx_stats.get('worldometer')
                if worldo_stats != None:
                    # {'ActiveCases': '139903', 'County': 'Texas Total', 'NewCases': '11060', 'NewDeaths': '131', 'TotalCases': '285772', 'TotalDeaths': '3471', 'TotalTests': '2864541'}
                    texas_stats.update({'WO DailyNew' : worldo_stats.get('NewCases')})
                    texas_stats.update({'WO DailyDeaths' : worldo_stats.get('NewDeaths')})
                    texas_stats.update({'WO TotalCases' : worldo_stats.get('TotalCases')})
                    texas_stats.update({'WO TotalDeaths' : worldo_stats.get('TotalDeaths')})

            tx_dates.append(dict({date_item.to_pydatetime().date() :  texas_stats }))
            tx_test_dates.append(dict({date_item.to_pydatetime().date() :  texas_test_stats }))
        # print(dates)
        print("- ---  ----  ----- TEXAS STATE NUMBERS ----- ---- --- -")
        dframe_dhs = pd.DataFrame.from_dict(ChainMap(*dates), orient='index')
        print(dframe_dhs.columns)
        dframe_dhs_tests = pd.DataFrame.from_dict(ChainMap(*tx_test_dates), orient='index')
        print(dframe_dhs_tests.columns) 
        dframe_texas = pd.DataFrame.from_dict(ChainMap(*tx_dates), orient='index')
        # dframe_texas = 

        cutoff = datetime(2020,7,6).date()
        print("               -- Hospitals --")
        print(dframe_dhs.filter(regex='HOSP').sort_index(axis = 0).loc[cutoff:])            
        # print(dframe_dhs[['day','DailyNewCases','DailyNewFatalities','CumulativeCases','CumulativeFatalities','SevenDayPositiveTestRate',
        #   'NewViral','ViralTests','REPORTED_TotalTests']].sort_index(axis = 0))
        print("               -- Tests --")
        print(dframe_dhs_tests.sort_index(axis=0)) 
        print("               -- Daily Stats --")       
        print(dframe_texas.sort_index(axis=0))          

    def get_friendswood_stats(self, numdays: int):
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

        print("- ---  ----  ----- FRIENDSWOOD ----- ---- --- -")
        dframe_fwood = pd.DataFrame.from_dict(ChainMap(*dates), orient='index')
        print(dframe_fwood[['Friendswood TOTAL', 'HarrisCo TOTAL','GalvestonCo TOTAL', 'Friendswood Recovered' , 'HarrisCo Deceased']].sort_index(axis = 0))


    def get_county_stats(self, numdays: int):
        harris_dates = []
        gal_dates = []
        datelist = pd.date_range(start=self.todaysdate -timedelta(days=numdays), end=self.todaysdate).tolist()
        for date_item in datelist:
            stats = dict()
            stats.update({'day': date_item.to_pydatetime().strftime('%a')})
            harris_stats = database.getHarrisCounty(date_item)
            if harris_stats != None:
                har_dhs = harris_stats.get('dhs')
                if har_dhs != None:
                    stats.update({'Beds': har_dhs.get('AvailableHospitalBeds')})
                    stats.update({'ICU': har_dhs.get('AvailableICUBeds')})
                    stats.update({'Vents': har_dhs.get('AvailableVentilators')})
                    stats.update({'COVID hosp': har_dhs.get('COVIDPatients')})
                    stats.update({'DHS Active': har_dhs.get('Active')})
                    stats.update({'DHS Deaths': har_dhs.get('Fatalities')})
                    stats.update({'DHS Positive': har_dhs.get('Positive')})
                    stats.update({'DHS Recover': har_dhs.get('Recoveries')})
                har_co = harris_stats.get('harrisCounty')
                if har_co != None:
                    stats.update({'Active': har_co.get('ActiveCases')})
                    stats.update({'Fatalities': har_co.get('DeceasedCases')})
                    stats.update({'Positive': har_co.get('ConfirmedCases')})
                    stats.update({'Recoveries': har_co.get('RecoveredCases')})                
                    stats.update({'New Cases': har_co.get(f"SUMMARY {date_item.strftime('%m-%d')}: NewCases")})

                har_world = harris_stats.get('worldometer')
                if har_world != None:
                    stats.update({'WO Case': har_world.get('NewCases')})
                    stats.update({'WO Death': har_world.get('NewDeaths')})                
# 'SUMMARY 07-21: Active': 38791, 'SUMMARY 07-21: Deceased': 560, 'SUMMARY 07-21: NewCases': 1385, 'SUMMARY 07-21: Recovered': 19129                
                harris_dates.append(dict({date_item.to_pydatetime().date() : stats}))                
                
            gal_stats = dict()    
            gal_stats.update({'day': date_item.to_pydatetime().strftime('%a')})
            galveston_stats = database.getGalvestonCounty(date_item)
            if galveston_stats:
                gal_dhs = galveston_stats.get('dhs')
                if gal_dhs != None:
                    gal_stats.update({'Beds': gal_dhs.get('AvailableHospitalBeds')})
                    gal_stats.update({'ICU': gal_dhs.get('AvailableICUBeds')})
                    gal_stats.update({'Vents': gal_dhs.get('AvailableVentilators')})
                    gal_stats.update({'COVID hosp': gal_dhs.get('COVIDPatients')})
                    gal_stats.update({'DHS Active': gal_dhs.get('Active')})
                    gal_stats.update({'DHS Deaths': gal_dhs.get('Fatalities')})
                    gal_stats.update({'DHS Positive': gal_dhs.get('Positive')})
                    gal_stats.update({'DHS Recoveries': gal_dhs.get('Recoveries')})
                gal_co = galveston_stats.get('galvestonCounty')
                if gal_co != None:
                    # calc_fatal = int(gal_co.get('GENDER Female').get('Deceased')) + int(gal_co.get('GENDER Male').get('Deceased'))
                    # gal_stats.update({'GAL-CalcdFatal': calc_fatal})
                    gal_stats.update({'GAL-Fatalities': gal_co.get(f"DAILY {date_item.strftime('%#d-%B')} Deceased")})
                    gal_stats.update({'GAL-Positive': gal_co.get(f"DAILY {date_item.strftime('%#d-%B')} Total Cases")})
                    gal_stats.update({'GAL-New': gal_co.get(f"DAILY {date_item.strftime('%#d-%B')} TotalNew")})
                    gal_stats.update({'GAL-Recoveries': gal_co.get(f"DAILY {date_item.strftime('%#d-%B')} Recovered")})    
                    gal_stats.update({'GAL-Pct Positive': gal_co.get(f"DAILY {date_item.strftime('%#d-%B')} PercentPositiveNew")})
                gal_world = galveston_stats.get('worldometer')
                if gal_world != None:
                    gal_stats.update({'WO NewCase': gal_world.get('NewCases')})
                    gal_stats.update({'WO Death': gal_world.get('NewDeaths')})                           
                gal_dates.append(dict({date_item.to_pydatetime().date() : gal_stats}))  

        print("- ---  ----  ----- HARRIS COUNTY ----- ---- --- -")
        dframe_harris = pd.DataFrame.from_dict(ChainMap(*harris_dates), orient='index')
        print(dframe_harris.sort_index(axis = 0))
        print(dframe_harris.columns)
        print("- ---  ----  ----- GALVESTON COUNTY ----- ---- --- -")
        dframe_gal = pd.DataFrame.from_dict(ChainMap(*gal_dates), orient='index')
        print(dframe_gal.sort_index(axis = 0))  
        print(dframe_gal.columns) 
               

        
        # print(galveston_stats.get('dhs'))
        # print(galveston_stats.get('galvestonCounty'))
        # print(galveston_stats.get('worldometer'))


    def talk_to_me(self, numdays: int):
        self.get_county_stats(numdays)
        self.get_texas_stats(numdays)
        self.get_friendswood_stats(numdays)
    
if __name__ == "__main__":
    reporter = TexasReporter()
    reporter.talk_to_me(21)
    # reporter.getStats(date.today() - timedelta(days=5) )    