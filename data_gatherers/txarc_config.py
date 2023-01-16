
base_url = "https://services3.arcgis.com/vljlarU2635mITsl/arcgis/rest/services/covid19_case_data_hosted/FeatureServer/"

Old_base_url = "https://services5.arcgis.com/ACaLB9ifngzawspq/ArcGIS/rest/services/DSHS_COVID19_Testing_Service/FeatureServer/"
base_url_v3 = "https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/DSHS_COVID19_TestData_Service/FeatureServer/"
base_url_v4 = "https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/TX_DSHS_COVID19_TestData_Service/FeatureServer/"
base_url_v5 = "https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/DSHS_COVID19_Testing_Data_Service/FeatureServer/"


# https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/TX_DSHS_COVID19_Cases_Service/FeatureServer/0/query?f=pbf&cacheHint=true&resultOffset=0&resultRecordCount=254&where=CatOrder%3D2&orderByFields=Count_%20DESC&outFields=*&resultType=standard&returnGeometry=false&spatialRel=esriSpatialRelIntersects
# https://services3.arcgis.com/vljlarU2635mITsl/arcgis/rest/services/covid19_case_data_hosted/FeatureServer/1/query?f=pbf&geometry={"spatialReference":{"latestWkid":3857,"wkid":102100},"xmin":-10018754.171394993,"ymin":0.000002983957529067993,"xmax":-0.000002983957529067993,"ymax":10018754.171394993}&maxRecordCountFactor=4&resultOffset=0&resultRecordCount=8000&where=1=1&orderByFields=OBJECTID&outFields=OBJECTID,category_order,probable&outSR=102100&quantizationParameters={"extent":{"spatialReference":{"latestWkid":3857,"wkid":102100},"xmin":-10018754.171394993,"ymin":0.000002983957529067993,"xmax":-0.000002983957529067993,"ymax":10018754.171394993},"mode":"view","originPosition":"upperLeft","tolerance":19567.879241000017}&resultType=tile&spatialRel=esriSpatialRelIntersects&geometryType=esriGeometryEnvelope&inSR=102100
# https://services3.arcgis.com/vljlarU2635mITsl/arcgis/rest/services/covid19_test_data_hosted/FeatureServer/1/query?f=pbf&geometry={"spatialReference":{"latestWkid":3857,"wkid":102100},"xmin":-12523442.714242995,"ymin":0.000002983957529067993,"xmax":-10018754.171394993,"ymax":2504688.542850986}&maxRecordCountFactor=4&resultOffset=0&resultRecordCount=8000&where=1=1&orderByFields=OBJECTID&outFields=OBJECTID,category&outSR=102100&quantizationParameters={"extent":{"spatialReference":{"latestWkid":3857,"wkid":102100},"xmin":-12523442.714242995,"ymin":0.000002983957529067993,"xmax":-10018754.171394993,"ymax":2504688.542850986},"mode":"view","originPosition":"upperLeft","tolerance":4891.969810250004}&resultType=tile&returnGeometry=false&spatialRel=esriSpatialRelIntersects&geometryType=esriGeometryEnvelope&inSR=102100
test_cases_url = "https://services3.arcgis.com/vljlarU2635mITsl/arcgis/rest/services/covid19_test_data_hosted/FeatureServer/"
base_cases_url = "https://services3.arcgis.com/vljlarU2635mITsl/arcgis/rest/services/covid19_case_data_hosted/FeatureServer/"
base_cases_url_1 = "https://services5.arcgis.com/ACaLB9ifngzawspq/ArcGIS/rest/services/TX_DSHS_COVID19_Cases_Service/FeatureServer/"
base_cases_url_0 = "https://services5.arcgis.com/ACaLB9ifngzawspq/ArcGIS/rest/services/DSHS_COVID19_Cases_Service/FeatureServer/"

# https://services3.arcgis.com/vljlarU2635mITsl/arcgis/rest/services/covid19_test_data_hosted/FeatureServer/1/query?f=pbf&geometry={"spatialReference":{"latestWkid":3857,"wkid":102100},"xmin":-12523442.714242995,"ymin":5009377.085698988,"xmax":-10018754.171394993,"ymax":7514065.62854699}&maxRecordCountFactor=4&resultOffset=0&resultRecordCount=8000&where=1=1&orderByFields=OBJECTID&outFields=OBJECTID,category&outSR=102100&quantizationParameters={"extent":{"spatialReference":{"latestWkid":3857,"wkid":102100},"xmin":-12523442.714242995,"ymin":5009377.085698988,"xmax":-10018754.171394993,"ymax":7514065.62854699},"mode":"view","originPosition":"upperLeft","tolerance":4891.969810250004}&resultType=tile&returnGeometry=false&spatialRel=esriSpatialRelIntersects&geometryType=esriGeometryEnvelope&inSR=102100
# https://services3.arcgis.com/vljlarU2635mITsl/arcgis/rest/services/covid19_test_data_hosted/FeatureServer/1/query?f=pbf&geometry={"spatialReference":{"latestWkid":3857,"wkid":102100},"xmin":-12523442.714242995,"ymin":0.000002983957529067993,"xmax":-10018754.171394993,"ymax":2504688.542850986}&maxRecordCountFactor=4&resultOffset=0&resultRecordCount=8000&where=1=1&orderByFields=OBJECTID&outFields=OBJECTID,category&outSR=102100&quantizationParameters={"extent":{"spatialReference":{"latestWkid":3857,"wkid":102100},"xmin":-12523442.714242995,"ymin":0.000002983957529067993,"xmax":-10018754.171394993,"ymax":2504688.542850986},"mode":"view","originPosition":"upperLeft","tolerance":4891.969810250004}&resultType=tile&returnGeometry=false&spatialRel=esriSpatialRelIntersects&geometryType=esriGeometryEnvelope&inSR=102100
# https://services3.arcgis.com/vljlarU2635mITsl/arcgis/rest/services/covid19_tsa_data_hosted/FeatureServer/0/query?f=pbf&geometry={"spatialReference":{"latestWkid":3857,"wkid":102100},"xmin":-10018754.171394993,"ymin":0.000002983957529067993,"xmax":-7514065.62854699,"ymax":2504688.542850986}&maxRecordCountFactor=4&resultOffset=0&resultRecordCount=8000&where=1=1&orderByFields=OBJECTID&outFields=OBJECTID,tsa&outSR=102100&quantizationParameters={"extent":{"spatialReference":{"latestWkid":3857,"wkid":102100},"xmin":-10018754.171394993,"ymin":0.000002983957529067993,"xmax":-7514065.62854699,"ymax":2504688.542850986},"mode":"view","originPosition":"upperLeft","tolerance":4891.969810250004}&resultType=tile&spatialRel=esriSpatialRelIntersects&geometryType=esriGeometryEnvelope&inSR=102100

hospital_base_url = "https://services3.arcgis.com/vljlarU2635mITsl/arcgis/rest/services/covid19_tsa_data_hosted/FeatureServer/"
          # "https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/DSHS_COVID_Hospital_Data/FeatureServer/"
          # https://services5.arcgis.com/ACaLB9ifngzawspq/ArcGIS/rest/services/DSHS_COVID19_Testing_Service/FeatureServer/8/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=%2A&orderByFields=Date+asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true  
          # https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/DSHS_COVID19_Cases_Service/FeatureServer/8/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Date%20asc&resultOffset=0&resultRecordCount=32000&resultType=standard&cacheHint=true



DEATHS_CUMMULATIVE = "" + base_cases_url + "4/query?" 
# DEATHS_CUMMULATIVE = "" + base_cases_url + "5/query?" 
death_cummulative_params = {
    'f': 'json',
    'where': 'category=\'Fatalities\'',
    'returnGeometry': 'false',
    'spatialRel': 'esriSpatialRelIntersects',
    'outFields':'*',
    'outStatistics':'[{"statisticType":"sum","onStatisticField":"count_","outStatisticFieldName":"reportedCumulativeFatalities"}]',
    'resultType': 'standard',
    'cacheHint': 'true'
}

# 23565


# current_day_report = "2/query?"   # where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&f=pjson&token="
current_day_report = "8/query?" 
CURRENT_DAY_TEST_URL = "" + test_cases_url + current_day_report  
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

hospitalizations_by_date_url = "7/query?"
# hospitalizations_by_date_url ="2/query?"
# hospitalizations_by_date_url ="1/query?"  # where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&f=pjson&token="
HOSPITAL_URL = "" + test_cases_url + hospitalizations_by_date_url
hospitalizations_by_date_params = {
    'f':'json',
    'where': '1=1',
    'returnGeometry':'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'orderByFields': 'date asc',
    'resultOffset': '0',
    'resultRecordCount': '32000',
    'resultType': 'standard',
    'cacheHint': 'true'
}

viral_antibody_breakout_by_day_url ="4/query?"
# viral_antibody_breakout_by_day_url ="3/query?"    # where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=standard&f=pjson&token="
VIRAL_ANTIBODY_BREAKOUT_URL= test_cases_url + viral_antibody_breakout_by_day_url
LAB_TESTING_URL = f"{test_cases_url}5/query?"     # Antigen
SPECIMEN_TESTING_URL = f"{test_cases_url}4/query?"      # PCR (molecular)
POSITIVITY_TESTING_URL = f"{test_cases_url}6/query?"
no_date_params = {
    'f': 'json',
    'where': '1=1',
    'returnGeometry':'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'resultOffset': '0',
    'resultRecordCount': '50',
    'resultType': 'standard',
    'cacheHint': 'true'
}

viral_antibody_breakout_by_day_params = {
    'f': 'json',
    'where': '1=1',
    'returnGeometry':'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'orderByFields': 'date desc',
    'resultOffset': '0',
    'resultRecordCount': '50',
    'resultType': 'standard',
    'cacheHint': 'true'
}

'''

test_count (ID:2)
OBJECTID (type: esriFieldTypeOID, alias: OBJECTID, SQL Type: sqlTypeOther, length: 0, nullable: false, editable: false)
test_category (type: esriFieldTypeString, alias: test_category, SQL Type: sqlTypeOther, length: 30, nullable: true, editable: true)
unknown_county (type: esriFieldTypeInteger, alias: unknown_county, SQL Type: sqlTypeOther, nullable: true, editable: true)
total_test (type: esriFieldTypeInteger, alias: total_test, SQL Type: sqlTypeOther, nullable: true, editable: true)
category_order (type: esriFieldTypeInteger, alias: category_order, SQL Type: sqlTypeOther, nullable: true, editable: true)

antigen_test (ID:3)
molecular_test (ID:4)
OBJECTID (type: esriFieldTypeOID, alias: OBJECTID, SQL Type: sqlTypeOther, length: 0, nullable: false, editable: false)
date (type: esriFieldTypeDate, alias: date, SQL Type: sqlTypeOther, length: 8, nullable: true, editable: true)
total_tests (type: esriFieldTypeInteger, alias: total_tests, SQL Type: sqlTypeOther, nullable: true, editable: true)
new_tests (type: esriFieldTypeDouble, alias: new_tests, SQL Type: sqlTypeOther, nullable: true, editable: true)
positives (type: esriFieldTypeInteger, alias: positives, SQL Type: sqlTypeOther, nullable: true, editable: true)
new_positives (type: esriFieldTypeDouble, alias: new_positives, SQL Type: sqlTypeOther, nullable: true, editable: true)
test_seven_day (type: esriFieldTypeDouble, alias: test_seven_day, SQL Type: sqlTypeOther, nullable: true, editable: true)
positive_seven_day (type: esriFieldTypeDouble, alias: positive_seven_day, SQL Type: sqlTypeOther, nullable: true, editable: true)

test_by_date (ID:5)
OBJECTID (type: esriFieldTypeOID, alias: OBJECTID, SQL Type: sqlTypeOther, length: 0, nullable: false, editable: false)
Date (type: esriFieldTypeDate, alias: Date, SQL Type: sqlTypeOther, length: 8, nullable: true, editable: true)
viral_average (type: esriFieldTypeDouble, alias: viral_average, SQL Type: sqlTypeOther, nullable: true, editable: true)
antibody_average (type: esriFieldTypeDouble, alias: antibody_average, SQL Type: sqlTypeOther, nullable: true, editable: true)
antigen_average (type: esriFieldTypeDouble, alias: antigen_average, SQL Type: sqlTypeOther, nullable: true, editable: true)

testing (ID:8)
OBJECTID (type: esriFieldTypeOID, alias: OBJECTID, SQL Type: sqlTypeOther, length: 0, nullable: false, editable: false)
test_type (type: esriFieldTypeString, alias: test_type, SQL Type: sqlTypeOther, length: 255, nullable: true, editable: true)
count_ (type: esriFieldTypeInteger, alias: count, SQL Type: sqlTypeOther, nullable: true, editable: true)

'''



'''
case_by_county (ID:0)
OBJECTID (type: esriFieldTypeOID, alias: OBJECTID, SQL Type: sqlTypeOther, length: 0, nullable: false, editable: false)
county (type: esriFieldTypeString, alias: county, SQL Type: sqlTypeOther, length: 26, nullable: true, editable: true)
confirmed (type: esriFieldTypeInteger, alias: confirmed, SQL Type: sqlTypeOther, nullable: true, editable: true)
active (type: esriFieldTypeInteger, alias: active, SQL Type: sqlTypeOther, nullable: true, editable: true)
probable (type: esriFieldTypeInteger, alias: probable, SQL Type: sqlTypeOther, nullable: true, editable: true)
recovered (type: esriFieldTypeInteger, alias: recovered, SQL Type: sqlTypeOther, nullable: true, editable: true)
fatalities (type: esriFieldTypeInteger, alias: fatalities, SQL Type: sqlTypeOther, nullable: true, editable: true)
Shape__Area (type: esriFieldTypeDouble, alias: Shape__Area, SQL Type: sqlTypeDouble, nullable: true, editable: false)
Shape__Length (type: esriFieldTypeDouble, alias: Shape__Length, SQL Type: sqlTypeDouble, nullable: true, editable: false)

case_count (ID:2) - this is cumulative (Fatalities, Recovered, Active, Confirmed, Probably)
OBJECTID (type: esriFieldTypeOID, alias: OBJECTID, SQL Type: sqlTypeOther, length: 0, nullable: false, editable: false)
case_category (type: esriFieldTypeString, alias: case_category, SQL Type: sqlTypeOther, length: 48, nullable: true, editable: true)
category_order (type: esriFieldTypeInteger, alias: category_order, SQL Type: sqlTypeOther, nullable: true, editable: true)
total_case (type: esriFieldTypeInteger, alias: total_case, SQL Type: sqlTypeOther, nullable: true, editable: true)


demographic_category (ID:4)
Fields:
OBJECTID (type: esriFieldTypeOID, alias: OBJECTID, SQL Type: sqlTypeOther, length: 0, nullable: false, editable: false)
case_category (type: esriFieldTypeString, alias: case_category, SQL Type: sqlTypeOther, length: 255, nullable: true, editable: true)
age (type: esriFieldTypeString, alias: age, SQL Type: sqlTypeOther, length: 255, nullable: true, editable: true)
age_count (type: esriFieldTypeInteger, alias: age_count, SQL Type: sqlTypeOther, nullable: true, editable: true)
gender (type: esriFieldTypeString, alias: gender, SQL Type: sqlTypeOther, length: 255, nullable: true, editable: true)
gender_count (type: esriFieldTypeDouble, alias: gender_count, SQL Type: sqlTypeOther, nullable: true, editable: true)
race_ethnicity (type: esriFieldTypeString, alias: race_ethnicity, SQL Type: sqlTypeOther, length: 255, nullable: true, editable: true)
race_ethnicity_count (type: esriFieldTypeDouble, alias: race_ethnicity_count, SQL Type: sqlTypeOther, nullable: true, editable: true)


trend (ID:3)
OBJECTID (type: esriFieldTypeOID, alias: OBJECTID, SQL Type: sqlTypeOther, length: 0, nullable: false, editable: false)
date (type: esriFieldTypeDate, alias: date, SQL Type: sqlTypeOther, length: 8, nullable: true, editable: true)
cumulative_cases (type: esriFieldTypeInteger, alias: cumulative_cases, SQL Type: sqlTypeOther, nullable: true, editable: true)
daily_new_cases (type: esriFieldTypeInteger, alias: daily_new_cases, SQL Type: sqlTypeOther, nullable: true, editable: true)
cumulative_probable (type: esriFieldTypeInteger, alias: cumulative_probable, SQL Type: sqlTypeOther, nullable: true, editable: true)
daily_new_probable (type: esriFieldTypeInteger, alias: daily_new_probable, SQL Type: sqlTypeOther, nullable: true, editable: true)
cumulative_fatalities (type: esriFieldTypeInteger, alias: cumulative_fatalities, SQL Type: sqlTypeOther, nullable: true, editable: true)
daily_new_fatalities (type: esriFieldTypeInteger, alias: daily_new_fatalities, SQL Type: sqlTypeOther, nullable: true, editable: true)
added_fatalities (type: esriFieldTypeInteger, alias: added_fatalities, SQL Type: sqlTypeOther, nullable: true, editable: true)
incomplete_new_fatalities (type: esriFieldTypeDouble, alias: incomplete_new_fatalities, SQL Type: sqlTypeOther, nullable: true, editable: true)
incomplete_added_fatalities (type: esriFieldTypeDouble, alias: incomplete_added_fatalities, SQL Type: sqlTypeOther, nullable: true, editable: true)
case_average (type: esriFieldTypeDouble, alias: case_average, SQL Type: sqlTypeOther, nullable: true, editable: true)
fatality_average (type: esriFieldTypeDouble, alias: fatality_average, SQL Type: sqlTypeOther, nullable: true, editable: true)
probable_average (type: esriFieldTypeDouble, alias: probable_average, SQL Type: sqlTypeOther, nullable: true, editable: true)
fatality_count (type: esriFieldTypeDouble, alias: fatality_count, SQL Type: sqlTypeOther, nullable: true, editable: true)

'''


daily_new_cases_by_date_url = "3/query?"
# daily_new_cases_by_date_url ="2/query?"
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



# https://services5.arcgis.com/ACaLB9ifngzawspq/arcgis/rest/services/TX_DSHS_COVID19_Cases_Service/FeatureServer/3/query?f=json&where=(GenderCount%20IS%20NOT%20NULL)%20AND%20(CaseCat%3D%27Confirmed%20Cases%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=20&resultType=standard&cacheHint=true
# This was on page 1
daily_counts_by_county_url ="0/query?"   # f=json&where=Positive%3C%3E0&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Positive%20desc&resultOffset=0&resultRecordCount=254&resultType=standard&cacheHint=true"
DAILY_COUNTY_COUNTS_URL = base_cases_url + daily_counts_by_county_url
daily_counts_by_county_params = {
    'f': 'json',
    'where': 'confirmed>0',
    'returnGeometry': 'false',
    'spatialRel': 'esriSpatialRelIntersects',
    'outFields':'*',
    'orderByFields': 'confirmed desc',
    'resultOffset': '0',
    'resultRecordCount':'500',
    'resultType': 'standard',
    'cacheHint': 'true'
}

total_counties_reporting_url ="0/query?" # f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22count%22%2C%22onStatisticField%22%3A%22OBJECTID%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&resultType=standard&cacheHint=true"
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

total_counties_with_positives_url ="0/query?" # f=json&where=Positive%3C%3E0&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22count%22%2C%22onStatisticField%22%3A%22OBJECTID%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&resultType=standard&cacheHint=true"
TOTAL_POSITIVES_URL = base_cases_url + total_counties_with_positives_url
total_counties_with_positives_params = {
    'f': 'json',
    'where': 'confirmed>0',
    'returnGeometry': 'false',
    'spatialRel': 'esriSpatialRelIntersects',
    'outFields':'*',
    'outStatistics':'[{"statisticType":"count","onStatisticField":"OBJECTID","outStatisticFieldName":"value"}]',
    'resultType': 'standard',
    'cacheHint': 'true'
}





