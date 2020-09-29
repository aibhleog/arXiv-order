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
df_dtypes = {'order':int,'id':str,'date':str}
main_df = pd.read_csv('arXiv_posts.txt',sep='\t',dtype=df_dtypes) # main table of data
df = pd.DataFrame({'order':[],'id':[],'date':[]}) # dataframe to be created in script

# ------------------------ #

# opening browser & going to arXiv.org
driver = webdriver.Firefox()
driver.get("https://export.arxiv.org/list/astro-ph/new")

date = driver.find_element_by_tag_name("h3") # expecting "New submissions for ___, DD dd YY"
date = date.text.split(', ')[1] # just pulling out the date part
print(f'Pulling arXiv post IDs for {date}')

# pulling all of the New Submissions
posts = driver.find_element_by_tag_name("dl")


# -- arXiv ID -- #
# -------------- #
items = posts.find_elements_by_tag_name("dt")
# running through the posts to pull out arXiv ID
i = 0
for item in items:
	print(f"{i}) ",end=' ')
	list_id = item.find_element_by_class_name("list-identifier")
	post_order = list_id.find_element_by_tag_name("a")
	arxiv_id = post_order.get_attribute('href')
	arxiv_id = arxiv_id.lstrip('https://export.arxiv.org/abs/')
	print(arxiv_id)
	
	# adding value to dataframe
	filler_df = pd.DataFrame({'order':[int(i)],'id':[arxiv_id],'date':[date]})
	df = df.append(filler_df,ignore_index=True)
	i += 1
# -------------- #

# -- date/time submitted -- #
# ------------------------- #
'''items = posts.find_elements_by_tag_name("dd")
# running through the posts to pull out submission date & time
	[code to be added later]'''

# ------------------------- #

driver.close()


# -- saving dataframe -- #
# ---------------------- #
df = df.astype(df_dtypes) # to make sure column dtypes don't change
main_df = main_df.astype(df_dtypes) # to make sure column dtypes don't change

dates = set(main_df.date.values)
if date in dates:
	print(f'\nLength of main_df: \t\t\t\t\t{len(main_df)}')
	print(f'Length of df: \t\t\t\t\t\t{len(df)}')
	final_df = main_df.append(df,ignore_index=True)
	
	print(f'Length of combined df: \t\t\t\t\t{len(final_df)}')
	final_df.drop_duplicates(inplace=True,subset='id')
	print(f'Length of final_df after dropping id duplicates: \t{len(final_df)}')
else:
	final_df = main_df.append(df,ignore_index=True)
	
final_df.to_csv('arXiv_posts.txt',sep='\t',index=False)
#df.to_csv('arXiv_posts.txt',sep='\t',index=False,float_format='%.5f')











