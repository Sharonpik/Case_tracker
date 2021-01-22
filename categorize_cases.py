import requests
from bs4 import BeautifulSoup
import time
import lxml
import cchardet
import csv
import pandas as pd
from string import digits
import os

# TODO: ADD EXCEPTION WHEN INTERNET CONNECTION IS LOST OR SCRIP IS STOPPED

date_file = input("Enter name of file (E.g. May_01.csv): ")
# Get date_file as input file
df = pd.read_csv(date_file)
# Get date from the Date Column
date = df.Date[0]
print('start')
dic_total = {"approved" : 0, "RFE" : 0, "unchecked" : 0, "rejected": 0}
dic_to_csv = {}
startTime = time.time()
session = requests.Session()

# loop on receipts numbers from Receipts column
for curr_receipt in df.Receipt:
    print(curr_receipt)
    url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
    myobj = {
                'changeLocale': '',
                'appReceiptNum': curr_receipt,
                'initCaseSearch': 'CHECK STATUS'
            }
    x = session.post(url, data = myobj)
    soup = BeautifulSoup(x.text, 'lxml')
    status = str(soup.find_all('h1')[0])
    if status.find("Case Was Received") != -1:
        dic_to_csv[curr_receipt] = "Received"
        dic_total["unchecked"] += 1
    elif status.find("Evidence") != -1:
        dic_to_csv[curr_receipt] = "RFE"
        dic_total["RFE"] += 1
    elif status.find("Case Was Approved") != -1:
        dic_to_csv [curr_receipt] ="Approved"
        dic_total["approved"] += 1
    elif status.find("Rejected") != -1:
        dic_to_csv [curr_receipt] = "Rejected"
        dic_total["rejected"] += 1
    else:
        dic_to_csv[curr_receipt] ="Received"
        dic_total["unchecked"] += 1

print(dic_to_csv)
# Get month without day
remove_digits = str.maketrans('', '', digits)
month = date.translate(remove_digits)

# Path to save output
if not os.path.exists(month):
    os.makedirs(month)
dir_path = month + "\\" + date

with open(dir_path + '_status.csv', 'w', newline="") as file:
    header = ['Date', 'Approved', 'RFE', 'Unchecked' , 'Rejected']
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    writer.writerow({'Date': date,
                     'Approved': dic_total["approved"],
                     'RFE': dic_total["RFE"],
                     'Unchecked': dic_total["unchecked"],
                     'Rejected': dic_total["rejected"]})


with open(dir_path + '_all_receipt_status.csv', 'w', newline="") as file:
    header = ['Date', 'Receipt', 'Status']
    writer = csv.DictWriter(file, fieldnames=header)
    for key in dic_to_csv:
        writer.writerow({'Date': date,
                         'Receipt': key,
                         'Status': dic_to_csv[key]})


executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
print(dic_total)

