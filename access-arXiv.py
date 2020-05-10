'''
Script used to create table of recently posted papers -- sorted by posting order.
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
df = pd.DataFrame({'id':[]})

# ------------------------ #

# opening browser & going to arXiv.org
driver = webdriver.Firefox()
driver.get("https://arxiv.org/list/astro-ph/new")

# pulling all of the New Submissions
posts = driver.find_element_by_tag_name("dl")
items = posts.find_elements_by_tag_name("dt")

# running through the posts to pull out information
i = 0
for item in items:
	print(f"{i}) ",end=' ')
	list_id = item.find_element_by_class_name("list-identifier")
	post_order = list_id.find_element_by_tag_name("a")
	arxiv_id = post_order.get_attribute('href')
	arxiv_id = arxiv_id.lstrip('https://arxiv.org/abs/')
	print(arxiv_id)
	
	# adding value to dataframe
	filler_df = pd.DataFrame({'id':[arxiv_id]})
	df = df.append(filler_df,ignore_index=True)
	i += 1

driver.close()
