

DAILY_ALL="https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/InvestigationForPublicDashboard_DASHUpdate/FeatureServer/0/query?"
DAILY_ALL_NOUPDATE="https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/InvestigationForPublicDashboard_DASH/FeatureServer/0/query?"
daily_all_params = {
    'f':'json',
    'where': '1=1',
    'returnGeometry':'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
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
city_summary_params = {
    'f':'json',
    'where': '1=1',
    'returnGeometry':'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'groupByFieldsForStatistics': 'City',
    'orderByFields': 'City',
    'outStatistics': '[{"statisticType":"count","onStatisticField":"OBJECTID","outStatisticFieldName":"value"}]',
    'resultType': 'standard',
    'cacheHint': 'true'
}

SUMMARY_ALL="https://services.arcgis.com/su8ic9KbA7PYVxPS/arcgis/rest/services/InvestigationForPublicDashboard_DASHUpdate/FeatureServer/1/query?"
summary_all_params = {
    'f':'json',
    'where': '1=1',
    'returnGeometry':'false',
    'spatialRel':'esriSpatialRelIntersects',
    'outFields':'*',
    'resultType': 'standard',
    'cacheHint': 'true'
}