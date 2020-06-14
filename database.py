import firebase_admin
from firebase_admin import credentials  
from firebase_admin import db
from _datetime import datetime
import sys

# default_app = firebase_admin.initialize_app()

cred = credentials.Certificate('config.json')
firebase_admin.initialize_app(cred,  {
    'databaseURL': 'https://covid-python-tdb2020.firebaseio.com/'
})
ref = db.reference('Texas')
print(ref.get())

date = datetime.now().strftime("%Y%m%d")
print(date)


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
    print("Saved: ", new_stat)    


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
    print("Saved: ", new_stat)

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
    print("Saved: ", new_stat)






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