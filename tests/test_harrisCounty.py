import pytest
from data_gatherers import harrisCounty

#  python -m pytest -s tests/test_harrisCounty.py >> printout.txt
class TestClass:
    def test_get_data(self):
        runThis = harrisCounty.HarrisCountyRunner()
        runThis.fileName = 'data/test_harris.json'
        runThis.get_summarized_data()

        assert runThis.fileName == 'data/test_harris.json'
        assert runThis.today_stats.get('totals') != dict()
        print (runThis.today_stats.get('totals').values())
        todayStats = next( stat for stat in runThis.today_stats.get('totals').values())
        assert todayStats != None
        assert todayStats.get('Recovered') > 0
        assert todayStats.get('Deceased') > 0
        assert todayStats.get('Active') > 0
        assert todayStats.get('NewCases') > 0