

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
total_rec_params = {
    'f':'json',
    'where': '1=1',
    'returnGeometry':'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'outStatistics': '[{"statisticType":"count","onStatisticField":"OBJECTID","outStatisticFieldName":"value"}]',
    'resultType': 'standard',
    'cacheHint': 'true'
}
CITY_SUMMARY_URL = 'https://services.arcgis.com/su8ic9KbA7PYVxPS/ArcGIS/rest/services/HCPHCovidCityZip/FeatureServer/1/query?'
# CITY_SUMMARY_URL = 'https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/CITY_LIMITS_COVID/FeatureServer/1/query?'
# CITY_SUMMARY_URL = 'https://services.arcgis.com/su8ic9KbA7PYVxPS/ArcGIS/rest/services/HCPHCovidDashboard/FeatureServer/1/query?'
city_summary_params = {
    'f':'json',
    'where': '1=1',
    'returnGeometry':'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'groupByFieldsForStatistics': 'CityName2',
    'orderByFields': 'CityName2',
    'outStatistics': '[{"statisticType":"sum","onStatisticField":"TotalConfirmedCases","outStatisticFieldName":"TotalConfirmedCases"},{"statisticType":"sum","onStatisticField":"ActiveCases","outStatisticFieldName":"ActiveCases"},{"statisticType":"sum","onStatisticField":"Recovered","outStatisticFieldName":"Recovered"},{"statisticType":"sum","onStatisticField":"Death","outStatisticFieldName":"Deceased"}]',
    'resultType': 'standard',
    'cacheHint': 'true'
}
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