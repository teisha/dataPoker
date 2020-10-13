
from functools import reduce
from data_gatherers import txStatRunner
from data_gatherers import galvestonCounty

test = dict({'cases_by_city': dict({'Alvin': '9', 'Bacliff Bayview San Leon': '225', 'Bayou Vista': '5', 
'Bolivar Peninsula': '14', 'Clear Lake Shores': '16', 'Dickinson': '662', 'Friendswood': '310', 
'Galveston': '1033', 'Hitchcock': '138', 'Jamaica Beach': '4', 'Kemah': '68', 'LaMarque': '377', 
'League City': '1167', 'Santa FeAlgoa': '189', 'Texas City': '843', 'Tiki Island': '3'})})

print (  reduce(lambda x,y: int(x) + int(y), test.get('cases_by_city').values()) )

runThis = galvestonCounty.GalvestonCountyRunner()
runThis.getTableauTotals()
# runThis.getAllData()
# # # runThis.pickle_off()
# # runThis.pickle_on()
# runThis.saveToDatabase()

# runThis = txStatRunner.Runner()
# runThis.get_daily_stats()

print ('---------------------------------------------------')
# print(dir(runThis))


# {'OBJECTID': 1, 'HospitalData': 'COVIDPatientsHospitals', 'Count_': 6533}
# {'OBJECTID': 2, 'HospitalData': 'TotalStaffedBeds', 'Count_': 55266}
# {'OBJECTID': 3, 'HospitalData': 'AvailableBeds', 'Count_': 13711}
# {'OBJECTID': 4, 'HospitalData': 'AvailableICU', 'Count_': 1405}
# {'OBJECTID': 5, 'HospitalData': 'AvailableVentilators', 'Count_': 5561}