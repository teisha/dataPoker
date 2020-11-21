from __future__ import print_function
import pickle
import os.path
import requests
from bs4 import BeautifulSoup
import re

from datetime import datetime, timedelta, date
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
import json
from services import database
from functools import reduce
from data_gatherers import galvestonCounty_config
import pandas as pd
from contextlib import suppress

# from tableaudocumentapi import Workbook



# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

class GalvestonCountyRunner:
    def __init__(self, directory):
        self.tableauData = None
        self.current_date_time = datetime.now().strftime("%m-%d-%Y")
        self.friendswood_stats = dict(dateCollected=self.current_date_time)
        self.history_stats = dict(dateCollected=self.current_date_time)
        self.today_stats = dict(dateCollected=self.current_date_time)
        self.fileName = "{}data/galvestonCounty-{}.json".format(directory, self.current_date_time)
        self.today = datetime.now().strftime("%#d-%B")
        self.full_today = datetime.now().strftime("%B %#d, %Y")
        self.two_days_ago = ( date.today() - timedelta(days=2) )
        print(self.today)
        self.yesterday = date.today() - timedelta(days=1)
        self.history_cutoff = ( date.today() - timedelta(days=5) ).strftime("%m/%d")
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        # creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        # if os.path.exists('token.pickle'):
        #     with open('token.pickle', 'rb') as token:
        #         creds = pickle.load(token)
        #         print(creds)
        # # If there are no (valid) credentials available, let the user log in.
        # if not creds or not creds.valid:
        #     if creds and creds.expired and creds.refresh_token:
        #         creds.refresh(Request())
        #     else:
        #         flow = InstalledAppFlow.from_client_secrets_file(
        #             'config/credentials.json', SCOPES)
        #         creds = flow.run_local_server(port=0)
        #     # Save the credentials for the next run
        #     with open('token.pickle', 'wb') as token:
        #         pickle.dump(creds, token)
        # self.service = build('sheets', 'v4', credentials=creds)
        print ('------------------- INIT GALVESTON COUNTY --------------------')

    def setup_tableau(self):
        print("-------------------- SETUP TABLEAU -----------------")
        url = galvestonCounty_config.tableau_main_url
        r = requests.get(
            url,
            params= {
                ":embed":"y",
                ":showAppBanner":"false",
                ":showShareOptions":"true",
                ":display_count":"no",
                "showVizHome": "no"
            }
        )
        soup = BeautifulSoup(r.text, "html.parser")
        self.tableauData = json.loads(soup.find("textarea",{"id": "tsConfigContainer"}).text)
        self.dataUrl = f'https://public.tableau.com{self.tableauData["vizql_root"]}/bootstrapSession/sessions/{self.tableauData["sessionid"]}'
        print( ' GET FROM ', self.tableauData["sheetId"])
        print( self.dataUrl)
   
    def getTableauTotals(self):
        self.setup_tableau()
        kpi_r = requests.post(self.dataUrl, data= {
            "sheet_id": "KPIs (2)",
        })
        kpis2_data = self.distill_response(kpi_r, 'KPIs2')
        kpis2 = kpis2_data[0]["data"]
        caseDateRecorded = kpis2.at[0, 'DAY(Case Date)-alias-2']
        print("CASE DATE: ", caseDateRecorded)
        self.case_date = caseDateRecorded


        if datetime.strptime(self.case_date, "%B %d, %Y").date() < self.two_days_ago:
            raise ValueError("Galveston data is not new. Last recorded Case Date is ", caseDateRecorded)

        self.history_stats.update({"CaseDateRecorded":caseDateRecorded })
        self.today_stats.update({"CaseDateRecorded":caseDateRecorded })
        self.friendswood_stats.update({"CaseDateRecorded":caseDateRecorded })

        r = requests.post(self.dataUrl, data= {
            "sheet_id": self.tableauData["sheetId"],
        })
        self.allData = self.distill_response(r, 'ALL')

        pbr_r = requests.post(self.dataUrl, data= {
            "sheet_id": "Positives w/ MA (2)",
        })
        positivesPerDay = self.distill_response(pbr_r, 'PosWiMA') 
        self.allData.append( positivesPerDay[0] ) 


        print ("~~~~~~~~~~ ALL DATA ~~~~~~~~~~")
        for data in self.allData:
            print (data["sheetName"])
            with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
                print(data["data"])
              
        # https://public.tableau.com/vizql/w/GCHDCOVID-19Analysis_15970856171690/v/TrendsbyCity/bootstrapSession/sessions/70D84C0C52574EE7960A2AF6245FADDB-0:0
        # print(data["secondaryInfo"]["presModelMap"]["dataDictionary"]["presModelHolder"]["genDataDictionaryPresModel"]["dataSegments"]["0"]["dataColumns"])
        # pagesReg = re.findall('targetSheets\\\\\\\":\[(.*?)\]', r.text, re.MULTILINE)
        # # for sheetList in pagesReg:
        # print(pagesReg[0])
            #  ??????
            # GCHDCOVID-19Analysis_15970856171690
            # GCHDCOVID-19Analysis_15970856171690/sheets/CountyOverview
        # https://public.tableau.com/workbooks/' + [Workbook Repo Url] + '.twb'
        # https://public.tableau.com/workbooks/GCHDCOVID-19Analysis_15970856171690/sheets/CountyOverview
        # https://public.tableau.com/profile/api/galveston.county.health.district#!/workbooks?count=300&index=0
        # https://public.tableau.com/profile/api/galveston.county.health.district#!/workbooks?count=300&index=0
        # https://public.tableau.com/profile/galveston.county.health.district#!/vizhome/GCHDCOVID-19Analysis_15970856171690/CountyOverview
        # https://public.tableau.com/workbooks/BarHoppingThemeandVariationsonaBarChart.twb



        # sourceWB = Workbook('GCHDCOVID-19Analysis_15970856171690')
        # sourceWB.datasources[0].connections[0].server = 'https://public.tableau.com'

        # gotoUrl = f'https://public.tableau.com{tableauData["vizql_root"]}/sessions/{tableauData["sessionid"]}/commands/tabdoc/goto-sheet'
        # goto_r = requests.post(gotoUrl, data={
        #     "windowId": "{B6E1F643-73DC-4B0C-B6FB-295B150DBF79}"
        # })
        # print(goto_r.text)

        # https://public.tableau.com/vizql/w/GCHDCOVID-19Analysis_15970856171690/v/TrendsbyCity/sessions/70D84C0C52574EE7960A2AF6245FADDB-0:0/commands/tabdoc/categorical-filter-by-index
#         visualIdPresModel: {"worksheet":"Positives w/ MA (2)","dashboard":"Trends by City"}
# globalFieldName: [federated.17qcxcc12yamab181nrjd0a4r6ej].[none:Calculation_475411296295043086:nk]
# membershipTarget: filter
# filterIndices: [7]
# filterUpdateType: filter-replace
    def get_friendswood_detail(self):
        
        if self.tableauData == None:
            self.setup_tableau()
        # tableauData = json.loads(soup.find("textarea",{"id": "tsConfigContainer"}).text)
        filterPage = self.tableauData["vizql_root"].replace('CountyOverview', 'TrendsbyCity')
        citydataUrl = f'https://public.tableau.com{filterPage}/bootstrapSession/sessions/{self.tableauData["sessionid"]}'
        print('CITY DATA URL: ' ,citydataUrl)
        print(" =================================================================== ")

        kpi_r = requests.post(citydataUrl, data= {
            "sheet_id": "Trends by City",
            "exclude": "false"
        })
        id = re.search('\"newSessionId\":\"(.*?)-.:.\"', kpi_r.text,)  
        new_session_id = id.group().replace('"newSessionId":"','')
        print(new_session_id)
        kpis2_data = self.distill_response(kpi_r, 'KPIs2')

        dataReg = re.search('\d+;({.*})\d+;({.*})', kpi_r.text, re.MULTILINE)                                  
        # print (dataReg)
        info = json.loads(dataReg.group(1))
        data = json.loads(dataReg.group(2))
        print("MAIN PAGE:")
        print(data["secondaryInfo"]["presModelMap"]["dataDictionary"]["presModelHolder"]["genDataDictionaryPresModel"]["dataSegments"]["0"]["dataColumns"])
        print(" =================================================================== ")

        filterUrl = f'https://public.tableau.com{filterPage}/sessions/{new_session_id[:-1]}/commands/tabdoc/categorical-filter-by-index'
        print(" ******* TRY TO GET FRIENDSWOOD DATA HISTORY ******* ", filterUrl)
        friendswood_r = requests.post(filterUrl, data= {
            "visualIdPresModel": '{"worksheet":"Positives w/ MA (2)","dashboard":"Trends by City"}',
            "globalFieldName": '[federated.17qcxcc12yamab181nrjd0a4r6ej].[none:Calculation_475411296295043086:nk]',
            "membershipTarget": "filter",
            "filterIndices": '[7]',
            "filterUpdateType": "filter-replace"
        })


        # https://public.tableau.com/vizql/w/GCHDCOVID-19Analysis_15970856171690/v/CountyOverview/sessions/63B629AA60804B899FBC4EDD80B358ED-0:0/commands/tabdoc/goto-sheet
        # windowId : {B6E1F643-73DC-4B0C-B6FB-295B150DBF79}
        # another_url = f'https://public.tableau.com{filterPage}/sessions/{new_session_id[:-1]}/commands/tabdoc/goto-sheet'
        # another_friendswood_r = requests.post(another_url , data={
        #      "windowId" : "{B6E1F643-73DC-4B0C-B6FB-295B150DBF79}",
        # })
        # another_friendswood_data = self.distill_response(another_friendswood_r, 'ANOTHER_FRIENDSWOOD')
        # another_friendswoodReg = re.search('\d+;({.*})\d+;({.*})', another_friendswood_r.text, re.MULTILINE)               
        # print (another_friendswoodReg)
        # another_friendswoodinfo = json.loads(another_friendswoodReg.group(1))
        # another_friendswooddata = json.loads(another_friendswoodReg.group(2))
        # print("MAIN PAGE:")
        # print(another_friendswooddata["secondaryInfo"]["presModelMap"]["dataDictionary"]["presModelHolder"]["genDataDictionaryPresModel"]["dataSegments"]["0"]["dataColumns"])




        print(" =================================================================== ")
        data_match = re.search('dataDictionary\":{(.*?)]}}}', friendswood_r.text, re.MULTILINE) 
        friendswood_data = json.loads(data_match.group().replace('dataDictionary":','') )
        print ("FRIENDSWOOD DATA DICTIONARY", friendswood_data)
        print(" =================================================================== ")

        data_match = re.findall('vizData\":({.*?},\"filtersJson)', friendswood_r.text, re.MULTILINE)
        friendswood_vizdata = []
        for line in data_match:
            friendswood_vizdata.append(json.loads(line.replace(',"filtersJson', '') ))
        print(" =================================================================== ")            
        print ("FRIENDSWOOD VIZDATA (column defs) ", friendswood_vizdata)
        print ( " ---- create data structure containing metadata defs ")

        result = []
        for t in friendswood_vizdata:
            rec = t['paneColumnsData']['vizDataColumns']
            recResults = []
            for field in rec:
                if field.get("fieldCaption") != None:
                    print(field.get("fieldCaption", ""))
                    recResults.append({
                        "fieldCaption": field.get("fieldCaption", ""), 
                        "valueIndices": t['paneColumnsData']["paneColumnsList"][field["paneIndices"][0]]["vizPaneColumns"][field["columnIndices"][0]]["valueIndices"],
                        "aliasIndices": t['paneColumnsData']["paneColumnsList"][field["paneIndices"][0]]["vizPaneColumns"][field["columnIndices"][0]]["aliasIndices"],
                        "dataType": field.get("dataType"),
                        "paneIndices": field["paneIndices"][0],
                        "columnIndices": field["columnIndices"][0]
                    })
            print("                            ======================================= ")
            print(recResults)                    
            result.append(recResults)

        print(" =================================================================== ")      
        print ( " ---- #this is the data source - there is only one ")
        # dataFull = data["secondaryInfo"]["presModelMap"]["dataDictionary"]["presModelHolder"]["genDataDictionaryPresModel"]["dataSegments"]["0"]["dataColumns"]
        dataFull = friendswood_data["dataSegments"]["1"]["dataColumns"]  # this is the data source - there is only one
        # print (dataFull)
        cstring = [t for t in dataFull if t["dataType"] == "cstring"]
        if len(cstring) == 0:
            cstring = "No Title"
        else:
            cstring = cstring[0]            
        # for t in dataFull:
        #     if t["dataType"] == "cstring":
        #         cstring.append(t)
        print(" =================================================================== ")
        print ("CSTRING: ", cstring )
        print(" =================================================================== ")        

        for t in dataFull:
            # print (t["dataValues"])
            for index in result:
                frameData = {}
                for report in index:
                # print(index)
                    if t["dataType"] == report["dataType"]:
                        if report.get("valueIndices") != None and len(report["valueIndices"]) > 0:
                            print (f'{report["fieldCaption"]}-value-{report["columnIndices"]}  = {[t["dataValues"][abs(it)] if abs(it) < len(t["dataValues"]) else it for it in report["valueIndices"]]}' )
                            frameData[f'{report["fieldCaption"]}-value-{report["columnIndices"]}'] = [t["dataValues"][abs(it)] if abs(it) < len(t["dataValues"]) else it for it in report["valueIndices"]]
                        if len(report["aliasIndices"]) > 0:
                            print (f'{report["fieldCaption"]}-alias-{report["columnIndices"]} = {onAlias(it, t["dataValues"], cstring) for it in report["aliasIndices"]}')
                            frameData[f'{report["fieldCaption"]}-alias-{report["columnIndices"]}'] = [onAlias(it, t["dataValues"], cstring) for it in report["aliasIndices"]]                        
                df = pd.DataFrame.from_dict(frameData, orient='index').fillna(0).T
                # with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
                #     print(df)        
            print(' ===================================== ')

        print(" =================================================================== ")         
        print(" ******* END FRIENDSWOOD DATA HISTORY  ***********")





        # pbr_r = requests.post(dataUrl, data= {
        #     "sheet_id": "BAN - Cumulative Trends by City",
        # })
        # cumulative_city = self.distill_response(pbr_r, 'BAN_CITY') 
        # for data in cumulative_city:
        #     print (data["sheetName"])
        #     with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
        #         print(data["data"]) 

        # for data in positivesPerDay:
        #     print (data["sheetName"])
        #     with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
        #         print(data["data"])        

        # pbr_r = requests.post(dataUrl, data= {
        #     "sheet_id": "Positives Disparity by Race",
        # })
        # self.distill_response(pbr_r, 'RACE_DISPARITY')

        # pbr_r = requests.post(dataUrl, data= {
        #     "sheet_id": "Race",
        # })
        # self.distill_response(pbr_r, 'RACE')  

        # pbr_r = requests.post(dataUrl, data= {
        #     "sheet_id": "Race Title",
        # })
        # self.distill_response(pbr_r, 'RACE_TITLE')  
             

        # pbr_r = requests.post(dataUrl, data= {
        #     "sheet_id": "Age Band",
        # })
        # self.distill_response(pbr_r, 'AGE')    


        # pbr_r = requests.post(dataUrl, data= {
        #     "sheet_id": "CM City (2)",
        # })
        # self.distill_response(pbr_r, 'CITY_CM')    

        # pbr_r = requests.post(dataUrl, data= {
        #     "sheet_id": "CM Gender2",
        # })
        # gender = self.distill_response(pbr_r, 'GENDER2')      
        # for data in gender:
        #     print (data["sheetName"])
        #     with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
        #         print(data["data"])               



        # pbr_r = requests.post(dataUrl, data= {
        #     "sheet_id": "BAN - Cumulative Trends by Race",
        # })
        # self.distill_response(pbr_r, 'BAN_RACE') 

        # pbr_r = requests.post(dataUrl, data= {
        #     "sheet_id": "Positives BAN",
        # })
        # self.distill_response(pbr_r, 'BAN_POSITIVES')                 

# \"targetSheets\":[\"Positives Disparity by Race\",
# \"Race Title\",\"Race\",\"Positives w/ MA (2)\",
# \"Positives BAN\",\"Max Reported Date\",\"Age Band\",
# \"City\",\"CM Gender2\",\"BAN - Cumulative Trends by Race\",
# \"Cumulative Trends by City (2)\",\"BAN - Cumulative Trends by City \",
# \"Cumulative Trends by Race\",\"KPIs (2)\",\"Positives w/ MA\",\"CM City (2)\"],
# \"type\":\"C\"}]
# Weekly Numbers (3)
# "Weekly Positivity"
# Weekly Trends
# Max Reported Date
# BAN - Cumulative Trends by City
# Cumulative Trends by City (2)

        # Age Band , Cities
        
        # kpi_r = requests.post(dataUrl, data= {
        #     "sheet_id": "KPI Overview",
        # })
        # kpi_data = self.distill_response(kpi_r, 'KPIs')


        # for data in kpis2_data:
        #     print (data["sheetName"])
        #     with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
        #         print(data["data"])          
     

    def distill_response(self, sheetResponse: dict, prefix: str):
        print (f" ================ {prefix} OVERVIIEW: ======================= ")

        # print(sheetResponse.text)
        # with open(f"data/galveston_{prefix}.json", "w") as handle:
        #     handle.writelines( json.dumps(sheetResponse.text )      ) 
        # panelColumnsData = re.findall('presModelHolder\\\":{(\\\"genVizDataPresModel)(.*?)}', sheetResponse.text, re.MULTILINE)
        # for columns in panelColumnsData:
        #     print (columns)
        dataReg = re.search('\d+;({.*})\d+;({.*})', sheetResponse.text, re.MULTILINE)                                  
        # panelsReg = re.findall('vizPaneColumns\\\":\[{(.*?)}\]', sheetResponse.text, re.MULTILINE)
        # for columns in panelsReg:
        #     print( ' ---  ')
        #     print(  len(columns))
        #     print(columns )
        # print (dataReg)
        info = json.loads(dataReg.group(1))
        data = json.loads(dataReg.group(2))
        # dataTuplesCount = len(data["secondaryInfo"]["presModelMap"]["dataDictionary"]["presModelHolder"]["genDataDictionaryPresModel"]["dataSegments"]["0"]["dataColumns"])
        # print (f"data has {dataTuplesCount} values")
        # for i in range(dataTuplesCount):
        #     print (data["secondaryInfo"]["presModelMap"]["dataDictionary"]["presModelHolder"]["genDataDictionaryPresModel"]["dataSegments"]["0"]["dataColumns"][i])
        #     if i == valueIdx:
        #         countValues=data["secondaryInfo"]["presModelMap"]["dataDictionary"]["presModelHolder"]["genDataDictionaryPresModel"]["dataSegments"]["0"]["dataColumns"][valueIdx]
        #     elif i == labelIdx:
        #         countLabels=data["secondaryInfo"]["presModelMap"]["dataDictionary"]["presModelHolder"]["genDataDictionaryPresModel"]["dataSegments"]["0"]["dataColumns"][labelIdx]
        #         for j in range(len(countLabels["dataValues"])):
        #             print (f' {countLabels["dataValues"][j]} : {countValues["dataValues"][j]}')
       
        workSheets = list(data["secondaryInfo"]["presModelMap"]["vizData"]["presModelHolder"]["genPresModelMapPresModel"]["presModelMap"].keys())
        sheetData = []
        for sheet in workSheets:
            # print (sheet)
            sheetdf = self.get_worksheet(data, sheet, prefix)
            sheetData.append(dict(
                sheetName=sheet,
                data=sheetdf) )
        return sheetData

    def get_worksheet(self, data: dict, worksheetName: str, prefix: str):    

        # print(data["secondaryInfo"]["presModelMap"]["vizData"]["presModelHolder"]["genPresModelMapPresModel"]["presModelMap"][workSheets[0]]["presModelHolder"]["genVizDataPresModel"]["paneColumnsData"])
        columnsData = data["secondaryInfo"]["presModelMap"]["vizData"]["presModelHolder"]["genPresModelMapPresModel"]["presModelMap"][worksheetName]["presModelHolder"]["genVizDataPresModel"]["paneColumnsData"]
        # print(columnsData.keys())
        i = 0
        result = [ 
            {
                "fieldCaption": t.get("fieldCaption", ""), 
                "valueIndices": columnsData["paneColumnsList"][t["paneIndices"][0]]["vizPaneColumns"][t["columnIndices"][0]]["valueIndices"],
                "aliasIndices": columnsData["paneColumnsList"][t["paneIndices"][0]]["vizPaneColumns"][t["columnIndices"][0]]["aliasIndices"],
                "dataType": t.get("dataType"),
                "paneIndices": t["paneIndices"][0],
                "columnIndices": t["columnIndices"][0]
            }
            for t in columnsData["vizDataColumns"]
            if t.get("fieldCaption")
        ]        
        # for t in columnsData["vizDataColumns"]:
        #     # print(t)
        #     if t.keys() >= {"fieldCaption"}:
        #         print("PANEINDEX: ", t["paneIndices"])
        #         print("COLUMNINDEX: ",  t["columnIndices"])
        #         paneIndex = t["paneIndices"][0]
        #         columnIndex = t["columnIndices"][0]
        #         if len(t["paneIndices"]) > 1:
        #             paneIndex = t["paneIndices"][1]
        #         if len(t["columnIndices"]) > 1:
        #             columnIndex = t["columnIndices"][1]
        #         result.append( dict(
        #             fieldCaption=t["fieldCaption"],
        #             valueIndicies=columnsData["paneColumnsList"][paneIndex]["vizPaneColumns"][columnIndex]["valueIndices"],
        #             aliasIndices=columnsData["paneColumnsList"][paneIndex]["vizPaneColumns"][columnIndex]["aliasIndices"],
        #             dataType=t["dataType"],
        #             paneIndices=paneIndex,
        #             columnIndices=columnIndex
        #         ) )
        #         i = i + 1
        #     else:
        #         print ("NOPE")

        # for aThing in result:
        #     print(aThing)                

        dataFull = data["secondaryInfo"]["presModelMap"]["dataDictionary"]["presModelHolder"]["genDataDictionaryPresModel"]["dataSegments"]["0"]["dataColumns"]
        cstring = [t for t in dataFull if t["dataType"] == "cstring"]
        if len(cstring) == 0:
            cstring = "No Title"
        else:
            cstring = cstring[0]            
        # for t in dataFull:
        #     if t["dataType"] == "cstring":
        #         cstring.append(t)
        print ( cstring )

        selectWorksheet = data["secondaryInfo"]["presModelMap"]["vizData"]["presModelHolder"]["genPresModelMapPresModel"]["presModelMap"]
        # print(selectWorksheet)
        dataIdx = 1 # 0 if dataTuplesCount == 2 else 1
        nameIdx = 1 # if dataTuplesCount == 2 else 2

        frameData = {}
        for t in dataFull:
            # print (t["dataValues"])
            for index in result:
                # print(index)
                if t["dataType"] == index["dataType"]:
                    if index.get("valueIndices") != None and len(index["valueIndices"]) > 0:
                        frameData[f'{index["fieldCaption"]}-value-{index["columnIndices"]}'] = [t["dataValues"][abs(it)] for it in index["valueIndices"]]
                    if len(index["aliasIndices"]) > 0:
                        print (f'{index["fieldCaption"]}-alias-{index["columnIndices"]}')
                        frameData[f'{index["fieldCaption"]}-alias-{index["columnIndices"]}'] = [onAlias(it, t["dataValues"], cstring) for it in index["aliasIndices"]]                        
            print(' ===================================== ')

        df = pd.DataFrame.from_dict(frameData, orient='index').fillna(0).T
        # with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
        #     print(df)
        return df    

     

    # Call the Sheets API
    def getSpreadsheetData(self, spreadsheetId):
        print(spreadsheetId)
        sheet = self.service.spreadsheets()
        meta = self.service.spreadsheets().get(spreadsheetId=spreadsheetId, fields='sheets(properties(index,sheetId,title))').execute()
        res = self.service.spreadsheets().get(spreadsheetId=spreadsheetId, fields='sheets(data/rowData/values/userEnteredValue,properties(index,sheetId,title))').execute()
        sheetIndex = 0
        sheetName = res['sheets'][sheetIndex]['properties']['title']
        lastRow = len(res['sheets'][sheetIndex]['data'][0]['rowData'])
        lastColumn = max([len(e['values']) for e in res['sheets'][sheetIndex]['data'][0]['rowData'] if e])
        print(meta)
        # print(sheetIndex, sheetName, lastRow, lastColumn)
        result = sheet.values().get(spreadsheetId=spreadsheetId,
                                    range=sheetName,majorDimension='ROWS').execute()
        values = result.get('values', [])

        if not values:
            return dict()
        else:
            returnValue = []
            headers = values[0]
            print(headers)
            sheet_iterator = iter(values)
            next(sheet_iterator)            
            for row in sheet_iterator:
                if len(headers) == len(row):
                    asDict = dict({'date_collected' : self.current_date_time})
                    for i in range(len(headers)):
                        asDict.update({headers[i].strip() : row[i]})
                    # print(asDict)
                    returnValue.append(asDict)
                else:
                    print("SKIPPED:", row)                    
            return returnValue

    def getCityTotals(self):
        print ('City Totals')
        # cityTotals = self.getSpreadsheetData(galvestonCounty_config.totals_by_city)
        totalsByCity = next((data["data"] for data in self.allData if data["sheetName"] == "CM City (2)"), None)
        totals = totalsByCity[['Geographic Level Selected-alias-1','AGG(CM Analysis)-value-3']]
        cases_by_city = dict(totals.values.tolist())
        # for city in cityTotals:
        #     cases_by_city.update({city.get('City').replace('/','') : city.get('Total Cases')})
        friendswood = cases_by_city["FRIENDSWOOD"]
        self.today_stats.update({'cases_by_city': cases_by_city})            
        self.history_stats.update({'cityTotals': totalsByCity.to_json()})
        self.friendswood_stats.update({'Total Cases': friendswood})

    # def getHospitalizedTotals(self):
    #     print('Hospitalizations')
    #     hospitalizedTotals = self.getSpreadsheetData(galvestonCounty_config.hospitalized_quarantined_by_date)
    #     self.history_stats.update({'hospitalized': hospitalizedTotals})
    #     today_hospitalized = next((stat for stat in hospitalizedTotals if stat["Date"] == self.today), None)
    #     if today_hospitalized != None:
    #         self.today_stats.update({'hospitalized': today_hospitalized})

    # def getRollingTotals(self):
    #     print ('Rolling Totals')
    #     rollingTotals = self.getSpreadsheetData(galvestonCounty_config.rolling_totals)
    #     self.history_stats.update({'cumulative_totals': rollingTotals})
    #     cumulative_stats = next((stat for stat in rollingTotals if stat["Date"] == self.today), None)
    #     print(cumulative_stats)
    #     if cumulative_stats != None:
    #         self.today_stats.update({'cumulative_totals': cumulative_stats})        

    def getTotalsPerDay(self):
        print ('Total Per Day')
        kpiTotals = next((data["data"] for data in self.allData if data["sheetName"] == "KPI Overview"), None)
        kpi2Totals = next((data["data"] for data in self.allData if data["sheetName"] == "KPI Overview (2)"), None)
        # dailyTotals = self.getSpreadsheetData(galvestonCounty_config.totals_per_day)
        dailyTotals = dict()
        dailyTotals.update({'Positive': int( kpiTotals.at[0 , "AGG(Total Positive Cases)-alias-1"] )})
        dailyTotals.update({'Active': int( kpiTotals.at[0 ,'AGG(Active Cases)-alias-3'] )})
        dailyTotals.update({'Deceased': int( kpi2Totals.at[ 0, 'AGG(Deceased Count)-alias-1'] )})
        dailyTotals.update({'Recovered': int( kpi2Totals.at[ 0, 'AGG(Recovered Cases)-alias-2'] )})
        dailyTotals.update({'PercentMortality': int( kpi2Totals.at[ 0, 'AGG(Percent Mortality)-alias-5'] )})

        positives = next((data["data"] for data in self.allData if data["sheetName"] == "Positives w/ MA (2)"), None)
        # print( positives )
        # print(self.full_today, self.case_date)
        daily_positives = positives.loc[positives["DAY(Case Date)-alias-2"] == self.case_date]
        # next((stat for stat in positives if stat["DAY(Case Date)-alias-2"] == self.full_today), None)
        if daily_positives.shape[0] > 0:
            print(daily_positives.keys())
            dailyTotals.update({'TotalNew': int( daily_positives.at[0,'AGG(Total Positive Cases)-value-3'])})
            dailyTotals.update({'PercentPositiveNew': int(daily_positives.at[0,'AGG(Total Positive Cases)-alias-5']) })
        else:
            dailyTotals.update({'TotalNew': -1})
            dailyTotals.update({'PercentPositiveNew': -1})

        kpiTotals['tmp'] = 1
        kpi2Totals['tmp'] = 1
        self.history_stats.update({'daily_totals': kpiTotals.merge(kpi2Totals, on=['tmp']).to_json()})
        self.history_stats.update({'positive_history': positives.to_json()})
        self.today_stats.update({'daily_stats': dailyTotals})


    def getTotalsByRace(self):
        print ('Total By RACE/Ethnicity')
        totalsByRace = next((data["data"] for data in self.allData if data["sheetName"] == "Race"), None)
        totals = totalsByRace[['Race-alias-1','AGG(CM Analysis)-value-2']]
        race_stats = dict(totals.values.tolist())
        self.history_stats.update({'totalsByRace': totalsByRace.to_json()})
        self.today_stats.update({'totalsByRace': race_stats})

    def getTotalsByAge(self):
        print ('Total By Age')
        # totalsByAge = self.getSpreadsheetData(galvestonCounty_config.totals_by_age)
        totalsByAge = next((data["data"] for data in self.allData if data["sheetName"] == "Age Band"), None)
        totals = totalsByAge[['Age Band-alias-1','AGG(CM Analysis)-value-2']]
        age_stats = dict(totals.values.tolist())
        # print(age_stats)
        self.history_stats.update({'totalsByAge': totalsByAge.to_json()})
        self.today_stats.update({'totalsByAge': age_stats})

    def getTotalsByGender(self):
        print('Total By Gender')
        # totalsByGender = self.getSpreadsheetData(galvestonCounty_config.totals_by_gender)
        totalsByGender = next((data["data"] for data in self.allData if data["sheetName"] == "CM Gender2"), None)
        totals= totalsByGender[['Gender-alias-1','AGG(CM Analysis)-alias-3']]
        gender_today = dict(totals.values.tolist())
        # for rec in totalsByGender:
        #     genderRec = dict({'Total Cases': rec.get('Total Cases'), 
        #         'Recovered': rec.get('Recovered'),
        #         'Deceased': rec.get('Deceased') })
        #     gender_today.append(dict({f"GENDER {rec.get('')}": genderRec }))                
        self.history_stats.update({'totalsByGender': totalsByGender.to_json()})
        self.today_stats.update({'totalsByGender': gender_today})

    def getNewCases(self):
        print('New Cases')
        newCases = self.getSpreadsheetData(galvestonCounty_config.new_cases_new_tested_by_week)
        self.history_stats.update({'weeklySummary': newCases})
        self.today_stats.update({'lastWeeklySummary': newCases[-1]})

    def getAllData(self):  
        self.getTableauTotals()
        
        self.getTotalsByAge()
        self.getCityTotals()
        self.getTotalsByGender()
        self.getTotalsPerDay()
        self.getTotalsByRace()

        
        print(self.today_stats)
        print(self.friendswood_stats)
        # print(self.history_stats)

        # self.getCityTotals()
        # self.getHospitalizedTotals()
        # self.getRollingTotals()
        # self.getTotalsPerDay()
        # self.getTotalsByAge()
        # self.getTotalsByGender()
        # self.getNewCases()

        # print(self.today_stats)   
        with suppress(FileNotFoundError):
            history_file = open(self.fileName, "w")
            history_file.write('[')
            history_file.writelines(json.dumps(dict(TODAY=self.today_stats))  )
            history_file.write(',')
            history_file.writelines(json.dumps(dict(HISTORY=self.history_stats))  )
            history_file.write(']')
            history_file.close()
        print('-------------------------------------------------------')

    def pickle_off(self):
        print('Saving to file', self.today_stats)
        with open('data/galveston_today.pickle', "wb") as handle:
            pickle.dump(self.today_stats, handle, protocol=pickle.HIGHEST_PROTOCOL)     
        with open('data/galveston_history.pickle', "wb") as handle:
            pickle.dump(self.history_stats, handle, protocol=pickle.HIGHEST_PROTOCOL) 
        with open('data/galveston_friendswood.pickle', "wb") as handle:
            pickle.dump(self.friendswood_stats, handle, protocol=pickle.HIGHEST_PROTOCOL)             

    def pickle_on(self):
        with open('data/galveston_today.pickle', 'rb') as handle:
            self.today_stats = pickle.load(handle)   
        with open('data/galveston_history.pickle', 'rb') as handle:
            self.history_stats = pickle.load(handle)   
        with open('data/galveston_friendswood.pickle', 'rb') as handle:
            self.friendswood_stats = pickle.load(handle)                                                

    def saveToDatabase(self):
        print("TODAY")
        print(self.today_stats)
        database_stats = dict({'date_collected' : self.current_date_time})  
        database_stats.update({"case_date": self.today_stats.get('CaseDateRecorded')})
        print(self.today_stats.get('totalsByAge'))
        database_stats.update({'ALL CASES: City Counts': self.today_stats.get('cases_by_city')})  
        database_stats.update({'AGE GROUPS': self.today_stats.get('totalsByAge')}) 
        formatted_stats = dict()
        race_stats = self.today_stats.get('totalsByRace') 
        for stat in race_stats.keys():
            formatted_stats.update({stat.replace('/','-'): race_stats.get(stat) })
        database_stats.update({'RACE': formatted_stats}) 


        daily_stats = self.today_stats.get('daily_stats')                    
        if daily_stats != None:
            database_stats.update({f"DAILY {self.today} Total Cases" : daily_stats.get('Positive')})
            database_stats.update({f"DAILY {self.today} Recovered" : daily_stats.get('Recovered')})
            database_stats.update({f"DAILY {self.today} Deceased" : daily_stats.get('Deceased')})
            database_stats.update({f"DAILY {self.today} Active" : daily_stats.get('Active')})
            database_stats.update({f"DAILY {self.today} PercentMortality" : daily_stats.get('PercentMortality')})
            database_stats.update({f"DAILY {self.today} TotalNew" : daily_stats.get('TotalNew')})
            database_stats.update({f"DAILY {self.today} PercentPositiveNew" : daily_stats.get('PercentPositiveNew')})
        gender_stats = self.today_stats.get('totalsByGender')
        database_stats.update(gender_stats)


        # for gender_rec in gender_stats:
        #     database_stats.update(gender_rec)
        # database_stats.update(dict(lastWeeklyUpdate=self.today_stats.get('lastWeeklySummary'))   )  
        # summary_stats = self.today_stats.get('cumulative_totals')   
        # if summary_stats != None:
        #     database_stats.update({f"SUMMARY {self.today} Total Cases": summary_stats.get('Total Cases')})
        #     database_stats.update({f"SUMMARY {self.today} Recovered": summary_stats.get('Recovered')})
        #     database_stats.update({f"SUMMARY {self.today} Deaths": summary_stats.get('Deaths')})
        # hospital_stats = self.today_stats.get('hospitalized') 
        # if hospital_stats != None:
        #     database_stats.update({'Hospitalized': hospital_stats.get('Hospitalized')})   
        #     database_stats.update({'Self-Quarantined': hospital_stats.get('Self-Quarantined')}) 
        # 
        #  
        county_totals = reduce(lambda x,y: int(x) + int(y), self.today_stats.get('cases_by_city').values()) 
        database_stats.update(dict(total_county=county_totals) )     
        print("DATABASE")
        print(database_stats)
        database.save_galveston_county(dict(galvestonCounty=database_stats) )  
        database.save_friendswood(dict(galvestonCounty=self.friendswood_stats) )          

def onAlias(it, value, cstring):
    returnplace = abs(it)-1 if abs(it) < len(cstring["dataValues"]) else -1
    # print(value, it, returnplace, cstring)
    # print (value[it] if (it >= 0 and it < len(value)) else cstring["dataValues"][returnplace])
    return value[it] if (it >= 0 and it < len(value)) else cstring["dataValues"][returnplace]

# 'hospitalized': {'date_collected': '07-07-2020', 'Date': '2-July', 'Hospitalized ': '89', 'Self-Quarantined': '2642'}, 
# 'cumulative_totals': {'date_collected': '07-07-2020', 'Date': '2-July', 'Total Cases': '3778', 'Recovered': '1001', 'Deaths': '46'}, 
# 'daily_stats': {'date_collected': '07-07-2020', 'Date': '2-July', 'Total Cases': '213', 'Recovered': '73', '#Deceased': '1'},            

# 'totalsByGender': [{'date_collected': '07-07-2020', '': 'Male', 'Total Cases': '2149', 'Recovered': '554', 'Deceased': '26'}, 
# {'date_collected': '07-07-2020', '': 'Female', 'Total Cases': '2660', 'Recovered': '740', 'Deceased': '24'}]}