'''
This script pulls the post information from "old_arXiv_posts.txt" and pulls up the
posts to get the submission history.

Future additions: would love to include author count & names (to track multiple submissions/year)
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime as dt
import threading, time, getpass, sys, subprocess
import pandas as pd
import numpy as np

__author__ = 'Taylor Hutchison'
__email__ = 'aibhleog@tamu.edu'


# ------------------------ #
# -- creating dataframe -- #
# ------------------------ #
df_dtypes = {'order':int,'id':str,'date':str}
main_df = pd.read_csv('old_arXiv_posts.txt',sep='\t',dtype=df_dtypes) # main table of data
df = pd.DataFrame({'id':[],'v1':[],'v2':[]}) # dataframe to be created in script

#date = main_df.loc[len(main_df)-1,'date'] # latest date, assumes "access_arXiv.py" run first
# arXiv IDs to run through
# note that you can query specific posting dates or other sorting criteria
#arXiv_ids = main_df.query(f'date == "{date}"').id.values
arXiv_ids = main_df.id.values[30000:35000]

# ------------------------ #

# opening browser & going to arXiv.org
driver = webdriver.Firefox()
driver.get("https://export.arxiv.org/")


# starting ID & ending ID (so I can gauge when it should end)
print(f'Starting ID: \t{arXiv_ids[0]}\nEnding ID: \t{arXiv_ids[-1]}.',end='\n\n')

# adding a timer to this to see how long it takes
start_it = dt.now()
print('Starting timer', start_it,end='\n\n')

# running through list of arXiv ID
for arXiv_id in arXiv_ids:
	assert len(arXiv_id) == 10, f"Incorrect arXiv ID: {arXiv_id}."
	
	# locating search bar and inputting arXiv_id
	search = driver.find_element_by_name("query")
	search.clear()
	search.send_keys(arXiv_id)
	search.send_keys(Keys.RETURN)

	time.sleep(7) # have to pause so the code doesn't try to search on previous page 
	print(f'\nFinding submission time for {arXiv_id}')
	try: submission_history = driver.find_element_by_class_name("submission-history")
	except: 
		try: # this is annoying
			time.sleep(5)
			submission_history = driver.find_element_by_class_name("submission-history")
		except: # if for some reason it decides it can't load the page, we'll start over
			driver.get("https://export.arxiv.org/")
			# locating search bar and inputting arXiv_id
			search = driver.find_element_by_name("query")
			search.clear()
			search.send_keys(arXiv_id)
			search.send_keys(Keys.RETURN)
			time.sleep(7) # have to pause so the code doesn't try to search on previous page 
			submission_history = driver.find_element_by_class_name("submission-history")
	
	submission_history = submission_history.text # full submission history
	#print(submission_history)

	submission = []
	# the following two lines are really ugly, but essentially it clips out the text focused on 
	# the first submission; to check this, print the "submission" variable to see the full text
	submission.append(submission_history.split('[v1] ')[1].split(' (')[0])
	try: submission.append(submission_history.split('[v1] ')[1].split(' (')[1].split('[v2] ')[1])
	except IndexError: pass # only going to focus on first two versions

	print(submission)
	# adding info to dataframe
	if len(submission) < 2: submission.append('') # in case only one submission
	filler_df = pd.DataFrame({'id':[arXiv_id],'v1':[submission[0]],'v2':[submission[1]]})
	df = df.append(filler_df,ignore_index=True)

print('\nThat took:',dt.now()-start_it,f'for {len(arXiv_ids)} IDs')


# Wait 2 seconds before closing browser 
time.sleep(2)
driver.close()


# saving dataframe
df_dtypes = {'id':str,'v1':str,'v2':str}
sub_df = pd.read_csv('old_arXiv_submission_history.txt',sep='\t',dtype=df_dtypes) # reading in to add
df = df.astype(df_dtypes) # to make sure column dtypes don't change

# appending on data
final_df = sub_df.append(df,ignore_index=True)

# checking for duplicates
ids = set(final_df.id.values) # creates 'set' of unique values 
if len(ids) != len(final_df): # SO checking for duplicates added in to table
	print(f'\nLength of sub_df: \t\t\t\t\t{len(sub_df)}')
	print(f'Length of df: \t\t\t\t\t\t{len(df)}')
	print(f'Length of combined df: \t\t\t\t\t{len(final_df)}')
	final_df.drop_duplicates(inplace=True,subset='id',keep='last') # want most up-to-date sub. history
	print(f'Length of final_df after dropping id duplicates: \t{len(final_df)}')
else:
	print(f'\nNo duplicates, check passed.')

# saving table again
final_df.to_csv('old_arXiv_submission_history.txt',sep='\t',index=False)

















