'''
Script used to pull voting information from benty-fields.com.
Must be logged in to access the benty-fields.

NOTES:  
		1) benty-fields mostly organizes paper suggestions based upon voting
		history and chosen preferences (machine learning involved), so these
		voting totals can be considered as a control sample (in a way?).
		2) Additionally, can only see the total votes for the "most popular"; the
		total votes per paper is not information available through the search.
		--> (so smaller sample than VoxCharta votes)
		3) "last year" not an option
		
THOUGHT: how new is benty-fields?
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
timeit = 2 # seconds

# ------------------------ #
# -- creating dataframe -- #
# ------------------------ #
df_dtypes = {'id':str,'total_votes':int}
# will be creating them inside the outermost for loop
# ------------------------ #

logmein = True # option to log into benty-fields account

# opening browser & going to benty-fields
if logmein == True:
	# pulling information to access arXiv account
	username = 'aibhleog@tamu.edu'
	password = 'al3xand3r!'
	#username = input('\nBenty-Fields username:  ')
	assert len(username) > 0, "Need to provide a username"
	#password = input('Benty-Fields password:  ')
	assert len(password) > 0, "Need to provide account password"

	driver = webdriver.Firefox()
	driver.get("https://www.benty-fields.com/login")
	assert "Login" in driver.title

	# finding log in cells
	usern = driver.find_element_by_id("email")
	passw = driver.find_element_by_id("password")
	usern.clear()
	passw.clear()

	# adding log in info
	usern.send_keys(username)
	passw.send_keys(password)

	# locating "Log In" button
	buttons = driver.find_element_by_class_name("modal-footer")
	login = buttons.find_element_by_xpath("//button[@type='submit' and contains(.,'Login')]")
	login.click()
else:
	driver = webdriver.Firefox()
	driver.get("https://www.benty-fields.com/most_popular")


# going to Most Popular page
driver.get("https://www.benty-fields.com/most_popular")

frequencies = ['last week','last month','last 6 months']
freq_days = [7,30,180]

for freq in frequencies: # running through frequencies
	print(f'''\n---------------------------------------
Looking at Most Popular: {freq}
---------------------------------------\n''')

	df = pd.DataFrame({'id':[],'total_votes':[]}) # dataframe for the frequency
	idx = frequencies.index(freq)

	if freq != 'last week': # have to change frequency
		period = driver.find_element_by_xpath("//button[@data-toggle='dropdown']")
		period.click() # this works

		# THIS WORKS!!! Can I tell you how long this took me to figure out.......
		loc = f"//ul[@class='dropdown-menu inner']/li[contains(.,'{freq}')]"
		last_month = driver.find_element_by_xpath(loc)
		last_month.click() # this works
		time.sleep(5) # let it load
		# ... just realized I could have just used the URL 
		#     most_popular/1?period=180 # where period == number of days


	# -- most popular votes -- #
	# ------------------------ #
	i = 0
	for page in range(1,50): # start with page 1, go to page 50
		# going page by page for at least 20 pages
		items = driver.find_elements_by_class_name("paper")
		
		# running through the posts to pull out arXiv ID
		for item in items:
			print(f"{i}) ",end=' ')
			arxiv_id = item.get_attribute('id') # "paper####.#####v#"
			arxiv_id = arxiv_id.lstrip('paper') 
			arxiv_id = arxiv_id.rsplit('v')[0]
			print(arxiv_id,end='\t')
			
			# total votes
			votes = item.find_element_by_tag_name("h3").text
			votes = votes.rsplit('Votes ')[1].rsplit(') ')[0] # pulling out just vote count
			votes = int(votes) # just because
			print(f"{votes} votes")

			# adding value to dataframe
			filler_df = pd.DataFrame({'id':[arxiv_id],'total_votes':[votes]})
			df = df.append(filler_df,ignore_index=True)
			i += 1

		# going to the next page using the link (instead of clicking the buttons)

		next_page = f"https://www.benty-fields.com/most_popular/{page+1}?period={freq_days[idx]}"
		driver.get(next_page)

	# saving dataframe
	freq_dash = freq.replace(' ','-')
	df_dtypes = {'id':str,'total_votes':int}
	sub_df = pd.read_csv(f'benty-fields_voting-{freq_dash}.txt',sep='\t',dtype=df_dtypes) # reading in to add
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
	
	final_df.to_csv(f'benty-fields_voting-{freq_dash}.txt',sep='\t',index=False)
	print(f"\nData saved to 'benty-fields_voting-{freq_dash}.txt'",end='\n\n')
	
# Wait until before closing browser (so we can see the "pycon" search)
time.sleep(timeit)
driver.close()
















