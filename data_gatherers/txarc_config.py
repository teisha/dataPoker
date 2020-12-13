Old_base_url = "https://services5.arcgis.com/ACaLB9ifngzawspq/ArcGIS/rest/services/DSHS_COVID19_Testing_Service/FeatureServer/"

base_url = "https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/DSHS_COVID19_Testing_Data_Service/FeatureServer/"
base_url_v3 = "https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/DSHS_COVID19_TestData_Service/FeatureServer/"
base_url_v4 = "https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/TX_DSHS_COVID19_TestData_Service/FeatureServer/"

base_cases_url_0 = "https://services5.arcgis.com/ACaLB9ifngzawspq/ArcGIS/rest/services/DSHS_COVID19_Cases_Service/FeatureServer/"
base_cases_url = "https://services5.arcgis.com/ACaLB9ifngzawspq/ArcGIS/rest/services/TX_DSHS_COVID19_Cases_Service/FeatureServer/"
hospital_base_url = "https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/DSHS_COVID_Hospital_Data/FeatureServer/"
          # https://services5.arcgis.com/ACaLB9ifngzawspq/ArcGIS/rest/services/DSHS_COVID19_Testing_Service/FeatureServer/8/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=%2A&orderByFields=Date+asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true  
          # https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/DSHS_COVID19_Cases_Service/FeatureServer/8/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Date%20asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true
# current_day_report = "2/query?"   # where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&f=pjson&token="
current_day_report = "3/query?" 


DEATHS_CUMMULATIVE = "" + base_cases_url + "5/query?" 
death_cummulative_params = {
    'f': 'json',
    'where': '1=1',
    'returnGeometry': 'false',
    'spatialRel': 'esriSpatialRelIntersects',
    'outFields':'*',
    'outStatistics':'[{"statisticType":"sum","onStatisticField":"Count_","outStatisticFieldName":"reportedCumulativeFatalities"}]',
    'resultType': 'standard',
    'cacheHint': 'true'
}



CURRENT_DAY_URL = "" + base_url_v4 + current_day_report
current_day_params = {
    'f':'json',
    'where': '1=1',
    'returnGeometry':'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'resultOffset': '0',
    'resultRecordCount': '50',
    'resultType': 'standard',
    'cacheHint': 'true'
}


# https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/DSHS_COVID_Hospital_Data/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22count%22%2C%22onStatisticField%22%3A%22OBJECTID%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&outSR=102100&resultType=standard&cacheHint=true
# https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/DSHS_COVID_Hospital_Data/FeatureServer/1/query?f=json&where=HospitalData%3D%27AvailableVentilators%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=50&resultType=standard&cacheHint=true


# where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outSR=102100&resultType=standard&cacheHint=true
HOSPITALS_CURRENT = hospital_base_url + "0/query?"
HOSPITALS_CUMULATIVE = hospital_base_url + "1/query?"
hospitals_current_params = {
    'where': '1=1',
    'returnGeometry': 'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'outSR':'102100',
    'resultType':'standard',
    'cacheHint':'true',
    'f': 'json',
}
hospitals_cum_params = {
    'where': '1=1',
    'returnGeometry': 'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'resultType':'standard',
    'cacheHint':'true',
    'f': 'json',
}

hospitalizations_by_date_url ="2/query?"
# hospitalizations_by_date_url ="1/query?"  # where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&f=pjson&token="
HOSPITAL_URL = "" + base_url_v4 + hospitalizations_by_date_url
hospitalizations_by_date_params = {
    'f':'json',
    'where': '1=1',
    'returnGeometry':'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'orderByFields': 'Date asc',
    'resultOffset': '0',
    'resultRecordCount': '32000',
    'resultType': 'standard',
    'cacheHint': 'true'
}

viral_antibody_breakout_by_day_url ="4/query?"
# viral_antibody_breakout_by_day_url ="3/query?"    # where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=standard&f=pjson&token="
VIRAL_ANTIBODY_BREAKOUT_URL= base_url_v4 + viral_antibody_breakout_by_day_url
LAB_TESTING_URL = f"{base_url_v4}5/query?"
SPECIMEN_TESTING_URL = f"{base_url_v4}6/query?"
viral_antibody_breakout_by_day_params = {
    'f': 'json',
    'where': '1=1',
    'returnGeometry':'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'orderByFields': 'Date desc',
    'resultOffset': '0',
    'resultRecordCount': '50',
    'resultType': 'standard',
    'cacheHint': 'true'
}


daily_new_cases_by_date_url ="2/query?"
# daily_new_cases_by_date_url ="8/query?"   # f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Date%20asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true"
DAILY_NEW_CASES_URL = base_cases_url + daily_new_cases_by_date_url
daily_new_cases_by_date_params = {
    'f': 'json',
    'where': '1=1',
    'returnGeometry': 'false',
    'spatialRel': 'esriSpatialRelIntersects',
    'outFields':'*',
    'orderByFields': 'Date asc',
    'resultOffset': '0',
    'resultRecordCount':'32000',
    'resultType': 'standard',
    'cacheHint': 'true'
}


# This was on page 1
daily_counts_by_county_url ="1/query?"   # f=json&where=Positive%3C%3E0&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Positive%20desc&resultOffset=0&resultRecordCount=254&resultType=standard&cacheHint=true"
DAILY_COUNTY_COUNTS_URL = base_cases_url + daily_counts_by_county_url
daily_counts_by_county_params = {
    'f': 'json',
    'where': 'Positive>0',
    'returnGeometry': 'false',
    'spatialRel': 'esriSpatialRelIntersects',
    'outFields':'*',
    'orderByFields': 'Positive desc',
    'resultOffset': '0',
    'resultRecordCount':'500',
    'resultType': 'standard',
    'cacheHint': 'true'
}

total_counties_reporting_url ="1/query?" # f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22count%22%2C%22onStatisticField%22%3A%22OBJECTID%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&resultType=standard&cacheHint=true"
TOTAL_COUNTIES_REPORTING_URL = base_cases_url + total_counties_reporting_url
total_counties_reporting_params = {
    'f': 'json',
    'where': '1=1',
    'returnGeometry': 'false',
    'spatialRel': 'esriSpatialRelIntersects',
    'outFields':'*',
    'outStatistics':'[{"statisticType":"count","onStatisticField":"OBJECTID","outStatisticFieldName":"value"}]',
    'resultType': 'standard',
    'cacheHint': 'true'
}

total_counties_with_positives_url ="1/query?" # f=json&where=Positive%3C%3E0&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22count%22%2C%22onStatisticField%22%3A%22OBJECTID%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&resultType=standard&cacheHint=true"
TOTAL_POSITIVES_URL = base_cases_url + total_counties_with_positives_url
total_counties_with_positives_params = {
    'f': 'json',
    'where': 'Positive>0',
    'returnGeometry': 'false',
    'spatialRel': 'esriSpatialRelIntersects',
    'outFields':'*',
    'outStatistics':'[{"statisticType":"count","onStatisticField":"OBJECTID","outStatisticFieldName":"value"}]',
    'resultType': 'standard',
    'cacheHint': 'true'
}



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


