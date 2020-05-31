base_url = "https://services5.arcgis.com/ACaLB9ifngzawspq/ArcGIS/rest/services/DSHS_COVID19_Testing_Service/FeatureServer/"


current_day_report = "2/query?"   # where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&f=pjson&token="
CURRENT_DAY_URL = "" + base_url + current_day_report
current_day_params = {
    'where': '1=1',
    'resultType': 'none',
    'outFields':'*',
    'returnIdsOnly': 'false',
    'returnUniqueIdsOnly': 'false',
    'returnCountOnly': 'false',
    'returnDistinctValues': 'false',
    'cacheHint': 'false',
    'orderByFields': '',
    'groupByFieldsForStatistics': '',
    'outStatistics': '',
    'having': '',
    'resultOffset': '',
    'resultRecordCount': '',
    'sqlFormat': 'none',
    'f': 'pjson',
    'token': ''
}

hospitalizations_by_date_url ="1/query?"  # where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&f=pjson&token="
HOSPITAL_URL = "" + base_url + hospitalizations_by_date_url
hospitalizations_by_date_params = {
    'where': '1=1',
    'objectIds': '',
    'time': '',
    'resultType': 'none',
    'outFields':'*',
    'returnIdsOnly': 'false',
    'returnUniqueIdsOnly': 'false',
    'returnCountOnly': 'false',
    'returnDistinctValues': 'false',
    'cacheHint': 'false',
    'orderByFields': '',
    'groupByFieldsForStatistics': '',
    'outStatistics': '',
    'having': '',
    'resultOffset': '',
    'resultRecordCount': '',
    'sqlFormat': 'none',
    'f': 'pjson',
    'token': ''
}

viral_antibody_breakout_by_day_url ="3/query?"    # where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=standard&f=pjson&token="
VIRAL_ANTIBODY_BREAKOUT_URL= base_url + viral_antibody_breakout_by_day_url
viral_antibody_breakout_by_day_params = {
    'where': '1=1',
    'objectIds': '',
    'time': '',
    'resultType': 'none',
    'outFields':'*',
    'returnIdsOnly': 'false',
    'returnUniqueIdsOnly': 'false',
    'returnCountOnly': 'false',
    'returnDistinctValues': 'false',
    'cacheHint': 'false',
    'orderByFields': '',
    'groupByFieldsForStatistics': '',
    'outStatistics': '',
    'having': '',
    'resultOffset': '',
    'resultRecordCount': '',
    'sqlFormat': 'none',
    'f': 'pjson',
    'token': ''
}

daily_new_cases_by_date_url ="8/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Date%20asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true"
daily_counts_by_county_url ="0/query?f=json&where=Positive%3C%3E0&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Positive%20desc&resultOffset=0&resultRecordCount=254&resultType=standard&cacheHint=true"

total_counties_reporting_url ="0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22count%22%2C%22onStatisticField%22%3A%22OBJECTID%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&resultType=standard&cacheHint=true"
total_counties_with_positives_url ="0/query?f=json&where=Positive%3C%3E0&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22count%22%2C%22onStatisticField%22%3A%22OBJECTID%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&resultType=standard&cacheHint=true"




"""
fields': [
    {'name': 'OBJECTID', 'type': 'esriFieldTypeOID', 'alias': 'OBJECTID', 'sqlType': 'sqlTypeOther', 'domain': None, 'defaultValue': None}, 
    {'name': 'TestType', 'type': 'esriFieldTypeString', 'alias': 'TestType', 'sqlType': 'sqlTypeOther', 'length': 8000, 'domain': None, 'defaultValue': None}, 
    {'name': 'Count_', 'type': 'esriFieldTypeInteger', 'alias': 'Count', 'sqlType': 'sqlTypeOther', 'domain': None, 'defaultValue': None}
], 
'features': [
    {   'attributes': 
        {'OBJECTID': 1, 'TestType': 'TotalTests', 'Count_': 1054793}
    }, 
    {   'attributes': 
        {'OBJECTID': 2, 'TestType': 'AntibodyTests', 'Count_': 98932}
    }, 
    {   'attributes': 
        {'OBJECTID': 3, 'TestType': 'PostiveAntibody', 'Count_': 3882}
    }, 
    {   'attributes': 
        {'OBJECTID': 4, 'TestType': 'ViralTests', 'Count_': 928517}
    }
]
"""


