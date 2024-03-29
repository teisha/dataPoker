import pytest
from data_gatherers import harrisCounty
from sys import platform

archive_dir="F:/Dropbox/Coding/covid/"
if platform == "linux" or platform == "linux2":
    archive_dir = "/f/Dropbox/Coding/covid/"




#  venv/bin/python -m pytest -s tests/test_harrisCounty.py >> printout.txt
#  venv/bin/python -m pytest -s tests/test_harrisCounty.py -k 'test_get_data'
class TestClass:
    def test_get_data(self):
        runThis = harrisCounty.HarrisCountyRunner(archive_dir)
        runThis.fileName = 'data/test_harris.json'
        runThis.catch_em_all()

        assert runThis.fileName == 'data/test_harris.json'
        assert runThis.today_stats.get('totals') != dict()
        print (runThis.today_stats.get('totals'))
        print ("VALUES::")
        print (runThis.today_stats.get('totals').values())
        # todayStats = next( stat for stat in runThis.today_stats.get('totals').values())
        todayStats = runThis.today_stats.get('totals')
        assert todayStats != None
        assert todayStats.get('Recovered') > 0
        assert todayStats.get('Deceased') > 0
        assert todayStats.get('Active') > 0
        # assert todayStats.get('NewCases') > 0

    def test_catch_them_all(self):
        runThis = harrisCounty.HarrisCountyRunner(archive_dir)
        runThis.catch_em_all()
        runThis.get_summarized_data()
        runThis.save_database()