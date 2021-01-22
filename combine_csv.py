import pandas as pd
import csv
import os
import glob

i_129f_receipts = ['May_01_status.csv', 'May_02_status.csv']
#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f,header=0) for f in i_129f_receipts])
#combined_csv.head()
combined_csv.to_csv( "May_Status.csv", quotechar='"',
          quoting=csv.QUOTE_ALL, index=False, encoding='utf-8')