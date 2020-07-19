import firebase_admin
from firebase_admin import credentials  
from firebase_admin import db
from _datetime import datetime
import sys

# default_app = firebase_admin.initialize_app()

cred = credentials.Certificate('config/config.json')
firebase_admin.initialize_app(cred,  {
    'databaseURL': 'https://covid-python-tdb2020.firebaseio.com/'
})
ref = db.reference('Texas')
# print(ref.get())

date = datetime.now().strftime("%Y%m%d")
# print(date)


def save_friendswood(stats_dict):
    friendswood_ref = db.reference('Friendswood')
    data = friendswood_ref.child(date).get()
    key = None
    if data:
        key = next(iter(data))
    if key:
        new_stat = friendswood_ref.child(date+ "/" + key).update(stats_dict)
    else:        
        new_stat = friendswood_ref.child(date).push(stats_dict)
    print("Saved Friendswood: ", new_stat.path if new_stat != None else key)    

def save_harris_county(stats_dict):
    harris_ref = db.reference('Harris')
    data = harris_ref.child(date).get()
    key = None
    if data:
        key = next(iter(data))
    if key:
        new_stat = harris_ref.child(date+ "/" + key).update(stats_dict)
    else:        
        new_stat = harris_ref.child(date).push(stats_dict)
    print("Saved Harris County: ", new_stat.path if new_stat != None else key)    

def save_galveston_county(stats_dict):
    galveston_ref = db.reference('Galveston')
    data = galveston_ref.child(date).get()
    key = None
    if data:
        key = next(iter(data))
    if key:
        new_stat = galveston_ref.child(date+ "/" + key).update(stats_dict)
    else:        
        new_stat = galveston_ref.child(date).push(stats_dict)
    print("Saved Galveston County: ", new_stat.path if new_stat != None else key) 


def save_texas(tx_stats_dict):
    texas_ref = db.reference('Texas')
    data = texas_ref.child(date).get()
    key = None
    if data:
        key = next(iter(data))
        print("DATA: ", data)
        print("KEY: ", next(iter(data)) )
    if key:
        new_stat = texas_ref.child(date + "/" + key).update(tx_stats_dict)
    else:        
        new_stat = texas_ref.child(date).push(tx_stats_dict) 
    print("Saved Texas: ", new_stat.path if new_stat != None else key )

def save_us(us_stats_dict):
    us_ref = db.reference('US')
    data = us_ref.child(date).get()
    key = None
    if data:
        key = next(iter(data))
        print("DATA: ", data)
        print("KEY: ", next(iter(data)) )
    if key:
        new_stat = us_ref.child(date + "/" + key ).update(us_stats_dict)
    else:        
        new_stat = us_ref.child(date ).push(us_stats_dict)
    print("Saved US Stats: ", new_stat.path if new_stat != None else key)

def formatDateForKey(date: datetime):
    return date.strftime("%Y%m%d")


def getUs(date: datetime):
    return getDataFor('US', date) 

def getTexas(date: datetime):
    return getDataFor('Texas', date)

def getHarrisCounty(date: datetime):
    return getDataFor('Harris', date)    

def getGalvestonCounty(date: datetime):
    return getDataFor('Galveston', date)   

def getFriendswood(date: datetime):
    return getDataFor('Friendswood', date)   

def getDataFor(region_name: str, date: datetime):    
    data_ref = db.reference(region_name)
    data = data_ref.child(formatDateForKey(date)).get()
    key = None
    if data:
        key = next(iter(data))
        # print("DATA: ", data)
        # print("KEY: ", next(iter(data)) )
        if key != None:
            return data.get(key)
        else:
            return data
    else:
        return None            



# ref = db.reference('/')
# ref.set ({
#     'Employee':
#         {
#             'empl1' : {
#                 'name':'Google',
#                 'lname': 'Forogh',
#                 'age': 24
#             },
#             'empl2': {
#                 'name': 'AWS',
#                 'lname': 'different db',
#                 'age':72
#             }
#         }
# })


# ref = db.reference('Employee')
# # emp_ref = ref.child('empl1')
# # emp_ref.update({
# #     'name':'Python'
# # })

# # multiple update
# ref.update({
#     'empl1/lname': 'updated lname1',
#     'empl2/lname': 'updated lname2'
# })

# ref = db.reference('Employee2')
# emp_ref = ref.push({
#     'name': 'Bob',
#     'lname': 'Bob',
#     'email': 'Bob@Bob.com',
#     'age': 24
# })
# print(emp_ref.key)   #-M9Fqp6hfwpZWGHS7sPA



# try:
# ref.set({
#     'tests': {
#         'date': date,
#         '.sv': 'timestamp',
#         'county': 'Harris',
#         'count': 100
#     }
# })
# except:
#     print('ERROR: ', sys.exc_info()[0])
