import pytest
from data_gatherers import txStatRunner

#  uvenv/bin/python -m pytest -s tests/test_texasdhs.py >> printout.txt
#  uvenv/bin/python -m pytest -s tests/test_texasdhs.py -k "get_lab"
class TestClass:
    runThis = txStatRunner.Runner()
    runThis.fileName = 'data/test_harris.json'

    def test_get_data(self):
        self.runThis.get_daily_new_cases_by_date()

        print(self.runThis.today_stats) 
        assert self.runThis.stat_pickler.get('daily_new_cases',None) != None
        assert self.runThis.fileName == 'data/test_harris.json'
        # assert runThis.today_stats.get('totals') != dict()
        # print (runThis.today_stats.get('totals').values())
        # todayStats = next( stat for stat in runThis.today_stats.get('totals').values())
        # assert todayStats != None
        # assert todayStats.get('Recovered') > 0
        # assert todayStats.get('Deceased') > 0
        # assert todayStats.get('Active') > 0
        # assert todayStats.get('NewCases') > 0
    def test_all(self):
        self.runThis.run_all()
        assert self.runThis.today_stats.get('counties', None) != None        

    def test_get_county_totals_data(self):
        self.runThis.get_county_totals()
        # print(self.runThis.today_stats) 
        assert self.runThis.stat_pickler.get('counties', None) != None
        assert self.runThis.today_stats.get('counties', None) != None


    def test_get_lab_testing_results(self):
        self.runThis.get_lab_testing_results()
        print(self.runThis.today_stats)
        assert self.runThis.stat_pickler.get("lab_stats") != None

# "features":[{"attributes":{"OBJECTID":1,"TestType":"TotalTests","Count_":10862674}},
# {"attributes":{"OBJECTID":2,"TestType":"AntibodyTests","Count_":539765}},
# {"attributes":{"OBJECTID":3,"TestType":"PostiveAntibody","Count_":55555}},
# {"attributes":{"OBJECTID":4,"TestType":"ViralTests","Count_":9787236}},
# {"attributes":{"OBJECTID":5,"TestType":"AntigenTests","Count_":535673}},
# {"attributes":{"OBJECTID":6,"TestType":"AntigenPositive","Count_":45348}}]}

# {'OBJECTID': 229, 'Date': 1605765600000, 'SevenDayPositiveTestRate': 0.0992, 'TotalTests': None, 'ViralTests': 9787236, 'AntibodyTests': 539765, 'NewViral': 90552, 'NewAntibody': 2861, 'NewTotal': 103732, 'AntigenTests': 535673, 'date_collected': '11-21-2020', 'DateString': '2020-11-19'}

# Add to data pull - seems to match the current daily number :
# https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/DSHS_COVID19_TestData_Service/FeatureServer/4/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Date%20asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true
# {OBJECTID":244,"Date":1605333600000,"Tests":136062,"Positives":15751,"Positivity":0.1274,"Test7Day":88882,"Positive7Day":11320}   
# current positivity rate?

    def test_get_specimen_testing_results(self):
        self.runThis.get_specimen_results()
        print(self.runThis.today_stats)
        assert self.runThis.stat_pickler.get("specimen_stats") != None
        assert self.runThis.today_stats.get("specimen_stats", dict(idontexist=None)) != dict(idontexist=None)
# Reported as new "Positivity Rate"
# https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/DSHS_COVID19_TestData_Service/FeatureServer/5/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Date%20asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true
# {"OBJECTID":258,"Date":1605333600000,"OldTest":null,"NewTest":310,"OldPositive":null,"NewPositive":41,"PositivityRate":0.1169,"TestSevenDay":48424.86,"PositiveSevenDay":5660.29}  


    # def test_get_seven_day_positive_summaries(self):

        # {"attributes":{"OBJECTID":258,"Date":1605744000000,"Specimen":0.121376726,"Lab_report":0.128,"Traditional":"0.0992"}}]}
# Feature Server 6:
#     {
#       "attributes" : {
#         "OBJECTID" : 252, 
#         "Date" : 1605225600000, 
#         "Specimen" : 0.121, 
#         "Lab_report" : 0.129, 
#         "Traditional" : "0.0906"
#       }
#     }, 
#     {
#       "attributes" : {
#         "OBJECTID" : 253, 
#         "Date" : 1605312000000, 
#         "Specimen" : 0.1169, 
#         "Lab_report" : 0.1274, 
#         "Traditional" : "0.0988"
#       }
#     }