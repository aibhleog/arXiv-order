'''
Script used to pull voting information from VoxCharta.org.
Accessed via the tamu.voxcharta.org platform.
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import threading, time, getpass, sys, subprocess

__author__ = 'Taylor Hutchison'
__email__ = 'aibhleog@tamu.edu'

# amount of time to wait
timeit = input('\nTime before closing browser (in seconds):  ') # seconds
timeit = int(timeit)

logmein = False

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





# Wait until before closing browser (so we can see the "pycon" search)
time.sleep(timeit)

driver.close()
