
import sys
from data_gatherers.txStatRunner import Runner
from data_gatherers import galvestonCounty, harrisCounty, worldometer
from sys import platform


archive_dir="F:/Dropbox/Coding/covid/"
if platform == "linux" or platform == "linux2":
    archive_dir = "/f/Dropbox/Coding/covid/"

errors = []

try:
    worldometer.download_texas()
    worldometer.download_world()
except:
    errors.append(dict(errorsource='worldometer',error=sys.exc_info()[0]))    

runThis = Runner()
print(dir(runThis))
file_name = "data/txarcgis-"+ runThis.current_date_time + ".pickle"
# runThis.load_from_file(file_name)
try:
    runThis.run_all()
    runThis.write_to_file(file_name, archive_dir)
    runThis.write_to_database()
except:
    errors.append(dict(errorsource='texasDHS',error=sys.exc_info()[0]))


runHarris = harrisCounty.HarrisCountyRunner(archive_dir)
try:
    runHarris.catch_em_all()
    runHarris.get_summarized_data()
    runHarris.save_database()
except:
    errors.append(dict(errorsource='harrisCounty',error=sys.exc_info()[0]))

runGalveston = galvestonCounty.GalvestonCountyRunner(archive_dir)
try:
    runGalveston.getAllData()
    runGalveston.saveToDatabase()       
except:
    errors.append(dict(errorsource='galveston',error=sys.exc_info()[0]))
    print("Galveston data incomplete", sys.exc_info()[0]) 
runGalveston.pickle_off()

print(" ===================ERRORS ==========================")
print(errors)


