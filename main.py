
import sys
from data_gatherers.txStatRunner import Runner
from data_gatherers import galvestonCounty, harrisCounty, worldometer

errors = []

worldometer.download_texas()
worldometer.download_world()

runThis = Runner()
print(dir(runThis))
file_name = "data/txarcgis-"+ runThis.current_date_time + ".pickle"
archive_dir="F:/Dropbox/Coding/covid/"
# runThis.load_from_file(file_name)
runThis.get_county_totals()
runThis.get_daily_stats()
runThis.get_hospital_stats()
runThis.get_hospital_current()
runThis.get_viral_antibody_breakout()
runThis.get_daily_new_cases_by_date()
runThis.get_daily_counts_by_county()

runThis.write_to_file(file_name, archive_dir)
runThis.write_to_database()


runHarris = harrisCounty.HarrisCountyRunner()
try:
    runHarris.catch_em_all()
    runHarris.get_summarized_data()
    runHarris.save_database()
except:
    errors.append(dict(errorsource='harrisCounty',error=sys.exc_info()[0]))

runGalveston = galvestonCounty.GalvestonCountyRunner()
try:
    runGalveston.getAllData()
    runGalveston.saveToDatabase()       
except:
    errors.append(dict(errorsource='galveston',error=sys.exc_info()[0]))
    print("Galveston data incomplete", sys.exc_info()[0]) 
runGalveston.pickle_off()

print(" ===================ERRORS ==========================")
print(errors)


