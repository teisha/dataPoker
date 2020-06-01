from txStatRunner import Runner
import worldometer


worldometer.download_texas()
worldometer.download_world()

runThis = Runner()
print(dir(runThis))
file_name = "data/txarcgis-"+ runThis.current_date_time + ".pickle"
# runThis.load_from_file(file_name)
runThis.get_county_totals()
runThis.get_daily_stats()
runThis.get_hospital_stats()
runThis.get_viral_antibody_breakout()
runThis.get_daily_new_cases_by_date()
runThis.get_daily_counts_by_county()

runThis.write_to_file(file_name)