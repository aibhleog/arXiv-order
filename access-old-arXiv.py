'''
Script used to go through past postings and pull out the same information as 'access-arXiv.py'
NOTE: ignoring papers that are cross-listed.  The date pulled from this search process can be off
by about half a day (because it's the submission date; announcement date doesn't share the day).

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
import math

__author__ = 'Taylor Hutchison'
__email__ = 'aibhleog@tamu.edu'


# amount of time to wait
start_date = input('\nStarting search date (in YYYY-MM):  ') # from date
print(f'Date chosen is: {start_date}') 
#end_date = input('\nEnd search date (in YYYY-MM):  ') # from date
end_date = '2020-05-06' # when I started pull from astro-ph/new
print(f'Date chosen is: {end_date}') 


# ------------------------ #
# -- creating dataframe -- #
# ------------------------ #
df_dtypes = {'order':int,'id':str,'sub_date':str}
#main_df = pd.read_csv('arXiv_posts.txt',sep='\t',dtype=df_dtypes) # main table of data
df = pd.DataFrame({'order':[],'id':[],'sub_date':[]}) # dataframe to be created in script

# ------------------------ #

# opening browser & going to arXiv.org
driver = webdriver.Firefox()
driver.get('https://arxiv.org/')

# Advanced Search
print('\nOpening Advanced Search.',end='\n\n')
advanced = driver.find_element_by_link_text('Advanced Search') # opening Advanced Search
advanced.click() # opening Advanced Search
time.sleep(1) # wait to load

# -- Advanced Searching -- #
# physics
physics = driver.find_element_by_name('classification-physics') # choosing physics
physics.click()
print('Physics chosen.')
# astro-ph
astroph = driver.find_element_by_name('classification-physics_archives') # choosing physics
astroph = astroph.find_element_by_xpath('//option[@value="astro-ph"]')
astroph.click()
print('Astro-ph chosen.')
# excluding cross-listed papers
nocrosslists = driver.find_element_by_xpath('//input[@value="exclude"]') # no cross-listed papers
nocrosslists.click()
print('Excluding cross-lists.')
# inserting "start" date
fromdate = driver.find_element_by_name('date-from_date') # choosing starting date
fromdate.clear()
fromdate.send_keys(f'{start_date}')
print(f'Setting starting search date as {start_date}')
# inserting "end" date
todate = driver.find_element_by_name('date-to_date') # choosing ending date
todate.clear()
todate.send_keys(f'{end_date}')
print(f'Setting starting search date as {end_date}')
# searching by original submission date
announcements = driver.find_element_by_id('date-date_type-1') # searching by org. submission date
announcements.click()
print('Searching by original submission date.')
# hide abstracts (because I'm not going to read them)
noabstracts = driver.find_element_by_id('abstracts-1')
noabstracts.click()
print("Hiding abstracts (because I won't be reading them).")
# number of search results per page
results = driver.find_element_by_id('size')
results = results.find_element_by_xpath('//option[@value=200]')
results.click()
print('Search results chosen: 200 per page.')
# click "Search" button
submit = driver.find_element_by_class_name('button.is-link.is-medium')
submit.click()
print('Searching...',end='\n\n')


# resorting results to oldest first
order = driver.find_element_by_xpath('//option[@value="announced_date_first"]')
order.click()
# click "Go" button
submit = driver.find_element_by_class_name('button.is-small.is-link')
submit.click()


# ------------------------------------- #
# pulling all of the submission results #
# ------------------------------------- #

# -- arXiv ID -- #
# -------------- #
total_results = driver.find_element_by_tag_name('h1')
total_results = total_results.text
total_results = total_results.split('of ')[1].split(' results')[0]
total_results = ''.join(total_results.split(',')) # removing commas
pages = int(math.ceil(int(total_results)/200))
print(f'Total number of results: {total_results}.',end='\n\n')


i = 0
for j in range(pages):
	print(f'\nPage {j+1} of {pages}...',end='\n\n')

	posts = driver.find_element_by_tag_name('ol')	
	items = posts.find_elements_by_tag_name('li')
	# running through the posts to pull out arXiv ID
	for item in items:
		print(f'{i}) ',end=' ')
		
		# arXiv number
		list_id = item.find_element_by_class_name('list-title.is-inline-block')
		post_order = list_id.find_element_by_tag_name('a')
		arxiv_id = post_order.get_attribute('href')
		arxiv_id = arxiv_id.lstrip('https://arxiv.org/abs/')
		print(arxiv_id, end=', ')
		
		notes = item.find_element_by_xpath('//p[@class="is-size-7"]')
		posts = notes.text

		submission = []
		# the following two lines are really ugly, but essentially it clips out the text focused on 
		# the first submission; to check this, print the "submission" variable to see the full text
		submission.append(posts.split('Submitted ')[1].split('; v1 submitted ')[0])
		try: submission.append(posts.split('Submitted ')[1].split('; v1 submitted ')[1].split('; ')[0])
		except IndexError: pass # only going to focus on first two versions
		
		# stripping the comma to match the syntax of 'access-arXiv'
		date = submission[-1] # the last one is the first submission date
		date_split = date.split('; ')[0].split(',')
		date = date_split[0] + date_split[1] # proper syntax
		print(f'{date}')
		
		# adding value to dataframe
		filler_df = pd.DataFrame({'order':[int(-99)],'id':[arxiv_id],'date':[date]})
		df = df.append(filler_df,ignore_index=True)
		i += 1
		# -------------- #

	# double checking that 
	try:
		next = driver.find_element_by_xpath('//a[@class="pagination-next"]')
		next.click()
	except: pass


time.sleep(3)
driver.close()


# -- saving dataframe -- #
# ---------------------- #
# saving dataframe
df_dtypes = {'order':int,'id':str,'sub_date':str}
sub_df = pd.read_csv('old_arXiv_posts.txt',sep='\t',dtype=df_dtypes) # reading in to add
df = df.astype(df_dtypes) # to make sure column dtypes don't change

# appending on data
final_df = sub_df.append(df,ignore_index=True)

# checking for duplicates
ids = set(final_df.id.values) # creates 'set' of unique values 
if len(ids) != len(final_df): # SO checking for duplicates added in to table
	print(f'\nLength of sub_df: \t\t\t\t\t{len(sub_df)}')
	print(f'Length of df: \t\t\t\t\t\t{len(df)}')
	print(f'Length of combined df: \t\t\t\t\t{len(final_df)}')
	final_df.drop_duplicates(inplace=True,subset='id')
	print(f'Length of final_df after dropping id duplicates: \t{len(final_df)}')
else:
	print(f'\nNo duplicates, check passed.')
	
final_df.to_csv('old_arXiv_posts.txt',sep='\t',index=False)
#df.to_csv('old_arXiv_posts.txt',sep='\t',index=False,float_format='%.5f')










