'''
This script pulls the post information from "arXiv_posts.txt" and pulls up the
posts to get the submission history.

Future additions: would love to include author count & names (to track multiple submissions/year)
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
df = pd.DataFrame({'id':[],'v1':[],'v2':[]}) # dataframe to be created in script

# arXiv IDs to run through
# note that you can query specific posting dates or other sorting criteria
arXiv_ids = main_df.id.values # list to run through
# ------------------------ #

# opening browser & going to arXiv.org
driver = webdriver.Firefox()
driver.get("https://arxiv.org/")

# running through list of arXiv ID
for arXiv_id in arXiv_ids:
	assert len(arXiv_id) == 10, f"Incorrect arXiv ID: {arXiv_id}."
	
	# locating search bar and inputting arXiv_id
	search = driver.find_element_by_name("query")
	search.send_keys(arXiv_id)
	search.send_keys(Keys.RETURN)

	time.sleep(3) # have to pause so the code doesn't try to search on previous page 
	print(f'\nFinding submission time for {arXiv_id}')
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


# Wait 2 seconds before closing browser 
time.sleep(2)
driver.close()

# saving dataframe
#df.to_csv('arXiv_submission_history.txt',sep='\t',index=False)











