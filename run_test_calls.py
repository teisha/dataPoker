import harrisCounty

runThis = harrisCounty.HarrisCountyRunner()
runThis.catch_em_all()
runThis.get_summarized_data()
runThis.save_database()

print ('---------------------------------------------------')
# print(dir(runThis))


# {'OBJECTID': 1, 'HospitalData': 'COVIDPatientsHospitals', 'Count_': 6533}
# {'OBJECTID': 2, 'HospitalData': 'TotalStaffedBeds', 'Count_': 55266}
# {'OBJECTID': 3, 'HospitalData': 'AvailableBeds', 'Count_': 13711}
# {'OBJECTID': 4, 'HospitalData': 'AvailableICU', 'Count_': 1405}
# {'OBJECTID': 5, 'HospitalData': 'AvailableVentilators', 'Count_': 5561}