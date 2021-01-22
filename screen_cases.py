import csv
import pandas as pd
from string import digits
import os
import screener

date_file = input("Enter name of file (E.g. May_01.csv): ")
# Get date_file as input file
df = pd.read_csv(date_file)

print(df)

#for date in df.Date:
#    print(date)