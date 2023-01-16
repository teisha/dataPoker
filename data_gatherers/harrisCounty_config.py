





# 12/27/2021
# https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/Download_Positivity_Rate/FeatureServer/0/query?f=pbf&cacheHint=true&resultOffset=0&resultRecordCount=1&where=1=1&orderByFields=&outFields=*&resultType=standard&returnGeometry=false&spatialRel=esriSpatialRelIntersects

# DAILY_ALL="https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/InvestigationForPublicDashboard_DASHUpdate/FeatureServer/0/query?"
DAILY_ALL="https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/HCPHCovidDashboard/FeatureServer/0/query?"
# DAILY_ALL_NOUPDATE="https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/InvestigationForPublicDashboard_DASH/FeatureServer/0/query?"
daily_all_params = {
    'f':'json',
    'where': '1=1',
    'returnGeometry':'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'resultOffset': '0',
    'orderByFields': 'OBJECTID',
    'resultType': 'standard',
    'cacheHint': 'true'
}
# total_rec_params = {
#     'f':'json',
#     'where': '1=1',
#     'returnGeometry':'false',
#     'spatialRel':'esriSpatialRelIntersects',
#     'outFields':'*',
#     'outStatistics': '[{"statisticType":"count","onStatisticField":"OBJECTID","outStatisticFieldName":"value"}]',
#     'resultType': 'standard',
#     'cacheHint': 'true'
# }
'''
OBJECTID_1 (type: esriFieldTypeOID, alias: OBJECTID_1, SQL Type: sqlTypeOther, length: 0, nullable: false, editable: false)
OBJECTID (type: esriFieldTypeInteger, alias: OBJECTID, SQL Type: sqlTypeOther, nullable: false, editable: true)
NAME (type: esriFieldTypeString, alias: NAME, SQL Type: sqlTypeOther, length: 50, nullable: true, editable: true)
GDB_GEOMATTR_DATA (type: esriFieldTypeBlob, alias: GDB_GEOMATTR_DATA, SQL Type: sqlTypeOther, nullable: true, editable: true)
City (type: esriFieldTypeString, alias: City, SQL Type: sqlTypeOther, length: 100, nullable: true, editable: true)
Total (type: esriFieldTypeInteger, alias: Total, SQL Type: sqlTypeOther, nullable: true, editable: true)
Active (type: esriFieldTypeString, alias: Active, SQL Type: sqlTypeOther, length: 10, nullable: true, editable: true)
Deceased (type: esriFieldTypeString, alias: Deceased, SQL Type: sqlTypeOther, length: 10, nullable: true, editable: true)
Recovered (type: esriFieldTypeInteger, alias: Recovered, SQL Type: sqlTypeOther, nullable: true, editable: true)
Date (type: esriFieldTypeDate, alias: Date, SQL Type: sqlTypeOther, length: 8, nullable: false, editable: true)
Date_Label (type: esriFieldTypeString, alias: Date_Label, SQL Type: sqlTypeOther, length: 4000, nullable: true, editable: true)
Today (type: esriFieldTypeString, alias: Today, SQL Type: sqlTypeOther, length: 4000, nullable: true, editable: true)


%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Total%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%2C%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Active%22%2C%22outStatisticFieldName%22%3A%22ActiveCases%22%7D%5D
%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Total%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D
%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Total%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D


'''
# https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/COH_City_Limit_hatched/FeatureServer/0/query?f=json&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outStatistics=%5B%7B%22statisticType%22%3A%22exceedslimit%22%2C%22outStatisticFieldName%22%3A%22exceedslimit%22%2C%22maxPointCount%22%3A4000%2C%22maxRecordCount%22%3A2000%2C%22maxVertexCount%22%3A250000%7D%5D
# https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/Download_Reported_COVID_Cases_Timeline/FeatureServer/0/query?f=pbf&cacheHint=true&resultOffset=0&resultRecordCount=32000&where=Source%3D%27HCTX%27&orderByFields=Date_Str%20ASC&outFields=*&resultType=standard&returnGeometry=false&spatialRel=esriSpatialRelIntersects
# https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/Download_New_Cases_Trend/FeatureServer/0/query?f=pbf&cacheHint=true&resultOffset=0&resultRecordCount=32000&where=1%3D1&orderByFields=Date%20ASC&outFields=*&resultType=standard&returnGeometry=false&spatialRel=esriSpatialRelIntersects
# https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/Download_Hospital_Usage_14_Day_Average/FeatureServer/0/query?f=pbf&cacheHint=true&resultOffset=0&resultRecordCount=1&where=1%3D1&orderByFields=Date%20DESC&outFields=*&resultType=standard&returnGeometry=false&spatialRel=esriSpatialRelIntersects
# https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/Download_Positivity_Rate/FeatureServer/0/query?f=pbf&cacheHint=true&resultOffset=0&resultRecordCount=1&where=1%3D1&orderByFields=Date%20DESC&outFields=*&resultType=standard&returnGeometry=false&spatialRel=esriSpatialRelIntersects
# https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/Download_Hospital_Population_Trend/FeatureServer/0/query?f=pbf&cacheHint=true&resultOffset=0&resultRecordCount=1&where=1%3D1&outFields=*&resultType=standard&returnGeometry=false&spatialRel=esriSpatialRelIntersects
# https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/Download_New_Cases_Trend/FeatureServer/0/query?f=json&where=1%3D1&outFields=*&returnCountOnly=true
CITY_SUMMARY_URL = 'https://services.arcgis.com/su8ic9KbA7PYVxPS/ArcGIS/rest/services/Download_COVID_Cases_By_City/FeatureServer/0/query?'
# CITY_SUMMARY_URL = 'https://services.arcgis.com/su8ic9KbA7PYVxPS/ArcGIS/rest/services/HCPH_COVID19_City_list_/FeatureServer/1/query?'
# CITY_SUMMARY_URL = 'https://services.arcgis.com/su8ic9KbA7PYVxPS/ArcGIS/rest/services/HCPHCovidCityZip/FeatureServer/1/query?'
# CITY_SUMMARY_URL = 'https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/CITY_LIMITS_COVID/FeatureServer/1/query?'
# CITY_SUMMARY_URL = 'https://services.arcgis.com/su8ic9KbA7PYVxPS/ArcGIS/rest/services/HCPHCovidDashboard/FeatureServer/1/query?'
#     'outStatistics': '[{"statisticType":"sum","onStatisticField":"Total","outStatisticFieldName":"TotalConfirmedCases"},{"statisticType":"sum","onStatisticField":"Active","outStatisticFieldName":"ActiveCases"},{"statisticType":"sum","onStatisticField":"Recovered","outStatisticFieldName":"Recovered"},{"statisticType":"sum","onStatisticField":"Deceased","outStatisticFieldName":"Deceased"}]',
# city_summary_params = {
#     'f':'json',
#     'where': '1=1',
#     'returnGeometry':'false',
#     'spatialRel':'esriSpatialRelIntersects',
#     'outFields':'*',
#     'groupByFieldsForStatistics': 'NAME',
#     'orderByFields': 'NAME',
#     'outStatistics': '[{"statisticType":"sum","onStatisticField":"Total","outStatisticFieldName":"TotalConfirmedCases"},{"statisticType":"sum","onStatisticField":"Active","outStatisticFieldName":"ActiveCases"},{"statisticType":"sum","onStatisticField":"Recovered","outStatisticFieldName":"Recovered"},{"statisticType":"sum","onStatisticField":"Deceased","outStatisticFieldName":"Deceased"}]',
#     'resultType': 'standard',
#     'cacheHint': 'true'
# }
city_summary_params = {
    'f':'json',
    'where': '1=1',
    'returnGeometry':'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'resultType': 'standard',
    'cacheHint': 'true'
}


# TOTAL_REC_URL = 'https://services.arcgis.com/su8ic9KbA7PYVxPS/ArcGIS/rest/services/HCPH_COVID19_Zip_Codes_map_prod/FeatureServer/0/query?'
TOTAL_REC_URL = 'https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/Download_Current_COVID_Case_Counts/FeatureServer/0/query?'
total_rec_params = {
    'f':'json',
    # 'where': '1=1',
    'where':'Source<>\'ALL\'', 
    'returnGeometry':'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'groupByFieldsForStatistics':'Today',
    # 'outStatistics': '[{"statisticType":"sum","onStatisticField":"TotalConfirmedCases","outStatisticFieldName":"TotalConfirmedCases"},{"statisticType":"sum","onStatisticField":"ActiveCases","outStatisticFieldName":"ActiveCases"},{"statisticType":"sum","onStatisticField":"Recovered","outStatisticFieldName":"Recovered"},{"statisticType":"sum","onStatisticField":"Death","outStatisticFieldName":"Deceased"}]',
    'outStatistics': '[{"statisticType":"sum","onStatisticField":"Confirmed_Cases","outStatisticFieldName":"TotalConfirmedCases"},{"statisticType":"sum","onStatisticField":"Active","outStatisticFieldName":"ActiveCases"},{"statisticType":"sum","onStatisticField":"Recovered","outStatisticFieldName":"Recovered"},{"statisticType":"sum","onStatisticField":"Deaths","outStatisticFieldName":"Deceased"}]',
    'resultType': 'standard',
    'cacheHint': 'true'
}

# Today
'''
%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Total%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%2C%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22Active%22%2C%22outStatisticFieldName%22%3A%22ActiveCases%22%7D%5D
'''


agerange_summary_params = {
    'f':'json',
    'where': '1=1',
    'returnGeometry':'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'groupByFieldsForStatistics': 'AgeRange',
    'orderByFields': 'AgeRange',
    'outStatistics': '[{"statisticType":"count","onStatisticField":"OBJECTID","outStatisticFieldName":"value"}]',
    'resultType': 'standard',
    'cacheHint': 'true'
}

# SUMMARY_ALL="https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/InvestigationForPublicDashboard_DASHUpdate/FeatureServer/1/query?"
SUMMARY_ALL="https://services.arcgis.com/su8ic9KbA7PYVxPS/ArcGIS/rest/services/HCPHCovidDashboard/FeatureServer/1/query?"
summary_all_params = {
    'f':'json',
    'where': '1=1',
    'returnGeometry':'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'resultType': 'standard',
    'cacheHint': 'true'
}