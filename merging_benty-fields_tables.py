'''
Script used to create table of recently posted papers -- sorted by posting order.
NOTE: ignoring papers that are cross-listed.

Reads in the table that already exists with data from previous dates, adds on the
new data compiled in this script.  In case this script is run more than one per
day, it also searches for duplicates and drops them.
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import threading, time, getpass, sys, subprocess
import pandas as pd
import numpy as np

__author__ = 'Taylor Hutchison'
__email__ = 'aibhleog@tamu.edu'


# ------------------------ #
# -- creating dataframe -- #
# ------------------------ #
df_dtypes = {'id':str,'last-week':bool,'last-month':bool,'last-6-months':bool}
sub_df = pd.read_csv('benty-fields_voting-crossover.txt',sep='\t',dtype=df_dtypes)

freq = ['last-week','last-month','last-6-months']
df_dtypes = {'id':str,'total_votes':int}

df_week = pd.read_csv(f'benty-fields_voting-{freq[0]}.txt',sep='\t',dtype=df_dtypes)
df_month = pd.read_csv(f'benty-fields_voting-{freq[1]}.txt',sep='\t',dtype=df_dtypes)
df_6months = pd.read_csv(f'benty-fields_voting-{freq[2]}.txt',sep='\t',dtype=df_dtypes)

i = 0
for table in [df_week,df_month,df_6months]:
	print(f'Length of {freq[i]}:  {len(table)}')
	i += 1
	

# adding all to one dataframe
df = pd.DataFrame({'id':[],'total_votes':[]}) # dataframe to be created in script
df = df.append(df_week,ignore_index=True)
df = df.append(df_month,ignore_index=True)
df = df.append(df_6months,ignore_index=True)

# reformatting
df.drop_duplicates(inplace=True,subset='id',keep='first')
df.reset_index(inplace=True,drop=True)
df = df.astype(df_dtypes)


# ----------------------- #
# -- checking if in df -- #
# ----------------------- #
df['last-week'] = df['id'].isin(df_week['id'])
df['last-month'] = df['id'].isin(df_month['id'])
df['last-6-months'] = df['id'].isin(df_6months['id'])

df = df[['id','last-week','last-month','last-6-months']]

# appending on data to original table
final_df = sub_df.append(df,ignore_index=True)
	
# checking for duplicates
ids = set(final_df.id.values) # creates 'set' of unique values 
if len(ids) != len(final_df): # SO checking for duplicates added in to table
	print(f'\nLength of sub_df: \t\t\t\t\t{len(sub_df)}')
	print(f'Length of df: \t\t\t\t\t\t{len(df)}')
	print(f'Length of combined df: \t\t\t\t\t{len(final_df)}')
	final_df.drop_duplicates(inplace=True,subset='id',keep='last') # want most up-to-date #'s
	print(f'Length of final_df after dropping id duplicates: \t{len(final_df)}')
else:
	print(f'\nNo duplicates, check passed.')


df.to_csv('benty-fields_voting-crossover.txt',sep='\t',index=False)
print('\nFinal table saved')

