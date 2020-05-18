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

__author__ = 'Taylor Hutchison'
__email__ = 'aibhleog@tamu.edu'

# reading in the posts
df_dtypes = {'order':int,'id':str,'date':str}
post_df = pd.read_csv('arXiv_posts.txt',sep='\t',dtype=df_dtypes) # main table of data
df_dtypes = {'id':str,'v1':str,'v2':str}
sub_df = pd.read_csv('arXiv_submission_history.txt',sep='\t',dtype=df_dtypes)


# stripping times & formatting to UTC
times = [dt.strptime(t,'%a, %d %b %Y %H:%M:%S %Z') for t in sub_df.v1.values]
times = [t.replace(tzinfo=timezone('UTC')) for t in times]
times_cst = [t.astimezone(timezone('US/Central')) for t in times]

print('Example times in UTC and CST:')
for i in range(4):
	print(times[i].strftime('%d %B %Y %H:%M:%S'),'UTC, ',times_cst[i].strftime('%H:%M:%S'),'CST')


# plotting
plt.figure(figsize=(9,6))
plt.gca().xaxis.set_major_formatter(md.DateFormatter('%m/%d'))

plt.hist(times,bins=40,edgecolor='k',lw=2)
xlims = plt.xlim()
plt.xlim(times[0],xlims[1])

# making dictionary of cutoff times
count = 0
d0 = dt(2020, 5, 5, 18, 00, 00)
colors = plt.cm.Blues(np.linspace(0,1,9))

for d in [7,8,11,12,13,14,15,18]:
	d1 = dt(2020, 5, d, 18, 00, 00)
	plt.axvspan(d0,d1,zorder=0,color=colors[count+1])
	d0 = d1
	count += 1


plt.xlabel('day of the week')
plt.ylabel('number of submissions')

# twin axes to show dates
plt.gca().twiny()
plt.xlim(times[0],xlims[1])
plt.gca().xaxis.set_major_formatter(md.DateFormatter('%a'))

plt.tight_layout()
plt.savefig('submissions_per_day.png')
plt.close('all')		
