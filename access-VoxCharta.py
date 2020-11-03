'''
Script used to pull voting information from VoxCharta.org.
Accessed via the tamu.voxcharta.org platform.

Have added code accounting for the few posts that aren't
searchable, but DO exist on VoxCharta.  Also added code to 
choose the original post, should replacement posts also exist.
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import threading, time, getpass, sys, subprocess
import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import timedelta

__author__ = 'Taylor Hutchison'
__email__ = 'aibhleog@tamu.edu'

# amount of time to wait
timeit = input('\nTime before closing browser (in seconds):  ') # seconds
timeit = int(timeit)

# ------------------------ #
# -- creating dataframe -- #
# ------------------------ #
df_dtypes = {'order':int,'id':str,'date':str}
main_df = pd.read_csv('arXiv_posts.txt',sep='\t',dtype=df_dtypes) # main table of data
# total votes will be counted and, if possible, will track # of votes per day/week
df = pd.DataFrame({'id':[],'total_votes':[],'vote_rate':[]}) # dataframe to be created in script

# arXiv IDs to run through; note that you can query specific dates or other sorting criteria
#arXiv_ids = main_df.id.values # runs through full list
# unless uncommented above, will be specifying to only look at posts within the last 2 weeks
times = [dt.strptime(t,'%d %b %y') for t in main_df.date.values]
times = np.asarray(times) # useful for the sorting we'll do 

# reference date of 2 weeks ago
ref_date = dt.now() - timedelta(days=14)
print(f"Looking at posts from {dt.strftime(ref_date,'%a, %d %b %y')} and onwards.",end='\n\n')

indexing = np.arange(len(main_df)) 
indexing = indexing[times > ref_date] # only listing entries in the dataframe that are in the last 2 weeks

arXiv_ids = main_df.loc[indexing,'id'].values # IDs of posts within the last 2 weeks!
# ------------------------ #

logmein = False # option to log into VoxCharta account (note: currently broken)

# opening browser & going to VoxCharta
driver = webdriver.Firefox()
if logmein == True:
	# pulling information to access arXiv account
	username = input('\nVoxCharta username:  ')
	assert len(username) > 0, "Need to provide a username"
	password = input('VoxCharta password:  ')
	assert len(password) > 0, "Need to provide account password"

	driver.get("https://tamu.voxcharta.org/wp-login.php")
	assert "Log In" in driver.title

	# finding log in cells
	usern = driver.find_element_by_name("log")
	passw = driver.find_element_by_name("pwd")
	usern.clear()
	passw.clear()

	# adding log in info
	usern.send_keys(username)
	passw.send_keys(password)

	# locating "Log In" button
	login = driver.find_element_by_name("wp-submit")
	login.click()
else:
	driver.get("https://tamu.voxcharta.org/")


# not necessary but keeping anyway
#otherints = driver.find_element_by_name("show_everyone") # so can see all upvotes
#if otherints.is_selected() == False: 
#	otherints.click()
#	print("Now showing votes from all institutions.")


for arXiv_id in arXiv_ids:
	assert len(arXiv_id) == 10, f"Incorrect arXiv ID: {arXiv_id}."
	print(f'\nSearching for {arXiv_id}.')

	# now, finding the search bar and searching for paper title
	try: search = driver.find_element_by_id("searchbox")
	except: time.sleep(7); search = driver.find_element_by_id("searchbox")
	search.clear()
	search.send_keys(arXiv_id)
	submit = driver.find_element_by_class_name("go")
	submit.click()

	time.sleep(5) # have to pause so the code doesn't try to search on previous page 	
	# finding and clicking on result title
	try: results = driver.find_elements_by_tag_name("h3") # looks at all h3 tags (b/c replacement posts)
	except: 
		time.sleep(4) # waiting a little longer for it to load	
		results = driver.find_elements_by_tag_name("h3") # looks at all h3 tags (b/c replacement posts)
	
	if len(results) > 1: # if there's no search result, this will be length == 1
		# choosing the first posted, corrects for [REPLACEMENT] posts that will be top of the search results
		result = results[-2] # This 2nd to last <h3> tag is the first post
		
		# first checking that there isn't just 1 post that is the replacement
		try: replacement_only = result.find_element_by_tag_name("a")
		except: # for some reason this has been failing recently
			try: time.sleep(4); replacement_only = result.find_element_by_tag_name("a")
			except: # if for some reason it decides it can't find it, we'll start over
				driver.get("https://tamu.voxcharta.org/")
				# locating search bar and inputting arXiv_id
				search = driver.find_element_by_id("searchbox")
				search.clear()
				search.send_keys(arXiv_id)
				submit = driver.find_element_by_class_name("go")
				submit.click()
			
				time.sleep(5) # have to pause so the code doesn't try to search on previous page 
				results = driver.find_elements_by_tag_name("h3") # looks at all h3 tags (b/c replacement posts)
				result = results[-2]
				replacement_only = result.find_element_by_tag_name("a")
		
		if replacement_only.text[-13:] == '[Replacement]':
			print('Original post not searchable?')
			no_votes = -99 # so I know which ones don't come up in the search
			# new filler df to log total votes
			filler_df = pd.DataFrame({'id':[arXiv_id],'total_votes':[no_votes],\
				'vote_rate':[f'']})
			df = df.append(filler_df,ignore_index=True)
		
		else:
			result.click()
			time.sleep(5) # have to pause so the code doesn't try to search on previous page 
			# finding total votes
			
			try:
				votes = driver.find_element_by_class_name("votedon")
				total = votes.find_element_by_tag_name("b")
				total = total.text.split(" '")[0]
				print(f'Total votes: {total}')

				votes_df = pd.DataFrame({'cast_date':[],'cast_time':[]})
				vote_times = votes.find_elements_by_tag_name("span")
				for vote in vote_times:
					vote_detail = vote.get_attribute("title")
					print(vote_detail)
					
					cast_time,cast_day = vote_detail.lstrip('Vote cast ').split(', ')
					filler_df = pd.DataFrame({'cast_date':[cast_day],'cast_time':[cast_time]})
					votes_df = votes_df.append(filler_df,ignore_index=True)

				votes_df.to_csv(f'votes_VoxCharta/arXiv_{arXiv_id}_votes.txt',sep='\t',index=False)

				# new filler df to log total votes
				filler_df = pd.DataFrame({'id':[arXiv_id],'total_votes':[total],\
					'vote_rate':[f'votes_VoxCharta/arXiv_{arXiv_id}_votes.txt']})
				df = df.append(filler_df,ignore_index=True)
			except: 
				print('No votes yet.')
				# new filler df to log total votes
				filler_df = pd.DataFrame({'id':[arXiv_id],'total_votes':[0],\
					'vote_rate':[f'']})
				df = df.append(filler_df,ignore_index=True)

	else:
		print('Not searchable?')
		no_votes = -99 # so I know which ones don't come up in the search
		# new filler df to log total votes
		filler_df = pd.DataFrame({'id':[arXiv_id],'total_votes':[no_votes],\
			'vote_rate':[f'']})
		df = df.append(filler_df,ignore_index=True)

# Wait until before closing browser (so we can see the "pycon" search)
time.sleep(timeit)
driver.close()


# saving dataframe
df_dtypes = {'id':str,'total_votes':int,'vote_rate':str}
sub_df = pd.read_csv('VoxCharta_voting.txt',sep='\t',dtype=df_dtypes) # reading in to add
df = df.astype(df_dtypes) # to make sure column dtypes don't change

# appending on data
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
	
# final version with added VoxCharta votes
final_df.to_csv('VoxCharta_voting.txt',sep='\t',index=False)




















