import pytest
from data_gatherers import worldometer

#  uvenv/bin/python -m pytest -s tests/test_worldometer.py >> printout.txt
#  uvenv/bin/python -m pytest -s tests/test_worldometer.py -k "get_data"
class TestClass:
    fileName = 'data/test_worldometer.json'

    def test_get_data(self):
        worldometer.download_texas()

    def test_get_world(self):        
        worldometer.download_world()