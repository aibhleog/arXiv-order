'''
Reading in submission history data taken via 'access-arXiv' and looking at
submission time versus post order.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from pytz import timezone
import matplotlib.dates as md
from datetime import timedelta
import datetime

__author__ = 'Taylor Hutchison'
__email__ = 'aibhleog@tamu.edu'

# reading in the posts
df_dtypes = {'order':int,'id':str,'date':str}
post_df = pd.read_csv('arXiv_posts.txt',sep='\t',dtype=df_dtypes) # main table of data
df_dtypes = {'id':str,'v1':str,'v2':str}
sub_df = pd.read_csv('arXiv_submission_history.txt',sep='\t',dtype=df_dtypes)

# stripping times & formatting to UTC
times = [dt.strptime(t,'%a, %d %b %Y %H:%M:%S %Z') for t in sub_df.v1.values]
times_utc = [t.replace(tzinfo=timezone('UTC')) for t in times]
times_cst = [t.astimezone(timezone('US/Central')) for t in times]


# plotting
plt.figure(figsize=(11,6))

# submission time
submission_time = datetime.time(18,00,00) # in UTC time

count = 0
coloring, indexing = [],[]
time_since_sub, seconds_since_sub = [],[]
for sub in times:
	sub_date = sub.date() # pulling out the date part
	
	# if the date is Mon and it's before the Mon submission time
	if sub.strftime('%a') == 'Mon' and sub.time() < submission_time:
		friday = dt.combine(sub_date,submission_time) - timedelta(days=3)
		diff = sub - friday
		seconds_since_sub.append(float(diff.seconds))
		time_since_sub.append(str(diff))
		coloring.append(0)
		indexing.append(count)
	
	# if the date is Mon and it's after the Mon submission time
	elif sub.strftime('%a') == 'Mon' and sub.time() >= submission_time:
		diff = sub - dt.combine(sub_date,submission_time)
		seconds_since_sub.append(float(diff.seconds))
		time_since_sub.append(str(diff))
		coloring.append(1)
		indexing.append(count)

	# if the date is Tues and it's before the Tues submission time
	elif sub.strftime('%a') == 'Tue' and sub.time() < submission_time:
		previous_day = dt.combine(sub_date,submission_time) - timedelta(days=1)
		diff = sub - previous_day
		seconds_since_sub.append(float(diff.seconds))
		time_since_sub.append(str(diff))
		coloring.append(1)
		indexing.append(count)
	
	# if the date is Tues and it's after the Tues submission time
	elif sub.strftime('%a') == 'Tue' and sub.time() >= submission_time:
		diff = sub - dt.combine(sub_date,submission_time)
		seconds_since_sub.append(float(diff.seconds))
		time_since_sub.append(str(diff))
		coloring.append(2)
		indexing.append(count)

	# if the date is Wed and it's before the Wed submission time
	elif sub.strftime('%a') == 'Wed' and sub.time() < submission_time:
		previous_day = dt.combine(sub_date,submission_time) - timedelta(days=1)
		diff = sub - previous_day
		seconds_since_sub.append(float(diff.seconds))
		time_since_sub.append(str(diff))
		coloring.append(2)
		indexing.append(count)

	# if the date is Wed and it's after the Wed submission time
	elif sub.strftime('%a') == 'Wed' and sub.time() >= submission_time:
		diff = sub - dt.combine(sub_date,submission_time)
		seconds_since_sub.append(float(diff.seconds))
		time_since_sub.append(str(diff))
		coloring.append(3)
		indexing.append(count)

	# if the date is Thurs and it's before the Thurs submission time
	elif sub.strftime('%a') == 'Thu' and sub.time() < submission_time:
		previous_day = dt.combine(sub_date,submission_time) - timedelta(days=1)
		diff = sub - previous_day
		seconds_since_sub.append(float(diff.seconds))
		time_since_sub.append(str(diff))
		coloring.append(3)
		indexing.append(count)
		
	# if the date is Thurs and it's after the Thurs submission time
	elif sub.strftime('%a') == 'Thu' and sub.time() >= submission_time:
		diff = sub - dt.combine(sub_date,submission_time)
		seconds_since_sub.append(float(diff.seconds))
		time_since_sub.append(str(diff))
		coloring.append(4)
		indexing.append(count)
	
	# if the date is Fri and it's before the Fri submission time
	elif sub.strftime('%a') == 'Fri' and sub.time() < submission_time:
		previous_day = dt.combine(sub_date,submission_time) - timedelta(days=1)
		diff = sub - previous_day
		seconds_since_sub.append(float(diff.seconds))
		time_since_sub.append(str(diff))
		coloring.append(4)
		indexing.append(count)
		
	# if the date is Fri and it's after the Fri submission time
	elif sub.strftime('%a') == 'Fri' and sub.time() >= submission_time:
		diff = sub - dt.combine(sub_date,submission_time)
		seconds_since_sub.append(float(diff.seconds))
		time_since_sub.append(str(diff))
		coloring.append(0)
		indexing.append(count)
		
	# if the date is Saturday
	elif sub.strftime('%a') == 'Sat':
		friday = dt.combine(sub_date,submission_time) - timedelta(days=1)
		diff = sub - friday
		seconds_since_sub.append(float(diff.seconds))
		time_since_sub.append(str(diff))
		coloring.append(0)
		indexing.append(count)
	
	# if the date is Sunday
	elif sub.strftime('%a') == 'Sun':
		friday = dt.combine(sub_date,submission_time) - timedelta(days=2)
		diff = sub - friday
		seconds_since_sub.append(float(diff.seconds))
		time_since_sub.append(str(diff))
		coloring.append(0)
		indexing.append(count)
		
	#else: print(sub.strftime('%a'), sub.time() < submission_time, sub.time() >= submission_time)
	count += 1

print(f'\nFull length: {len(post_df)}, Final length: {len(indexing)}.')

# adding 0.35 seconds to the zero second differences
seconds_since_sub = np.asarray(seconds_since_sub)
seconds_since_sub[seconds_since_sub == 0.0] = 0.5

plt.scatter(seconds_since_sub,post_df.loc[indexing,'order'],s=100,\
	c=coloring,edgecolor='k',cmap=plt.cm.Blues,alpha=0.8)

# -- making legend -- #
colors = plt.cm.Blues(np.linspace(0,1,5))
labels = ['Monday','Tuesday','Wednesday','Thursday','Friday']
for i in range(5):
	plt.scatter(0.5,55+i*4.2,color=colors[i],s=200,edgecolor='k',marker='s')
	plt.text(0.063,0.283-i*0.05,f'{labels[i]} postings',transform=plt.gca().transAxes)
# ------------------- #

ylims = plt.ylim()
plt.ylim(ylims[1],ylims[0])
plt.xscale('log')
plt.xlim(0.3,1e5)
plt.xlabel('time after posting opens [seconds]')
plt.ylabel('submission order')

plt.tight_layout()
plt.savefig('time_after_posting_opens.png')
plt.close('all')		






