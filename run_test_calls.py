import galvestonCounty

runThis = galvestonCounty.GalvestonCountyRunner()
# runThis.getAllData()
# runThis.pickle_off()
runThis.pickle_on()
runThis.saveToDatabase()

print ('---------------------------------------------------')
# print(dir(runThis))


# {'OBJECTID': 1, 'HospitalData': 'COVIDPatientsHospitals', 'Count_': 6533}
# {'OBJECTID': 2, 'HospitalData': 'TotalStaffedBeds', 'Count_': 55266}
# {'OBJECTID': 3, 'HospitalData': 'AvailableBeds', 'Count_': 13711}
# {'OBJECTID': 4, 'HospitalData': 'AvailableICU', 'Count_': 1405}
# {'OBJECTID': 5, 'HospitalData': 'AvailableVentilators', 'Count_': 5561}