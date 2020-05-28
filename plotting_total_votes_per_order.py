'''
Plotting the total votes for a given arXiv post versus the post order.

Future plans:	color points by submission window (Mon-Fri)
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from datetime import datetime as dt

__author__ = 'Taylor Hutchison'
__email__ = 'aibhleog@tamu.edu'

# reading in the posts
df_dtypes = {'order':int,'id':str,'date':str}
post_df = pd.read_csv('arXiv_posts.txt',sep='\t',dtype=df_dtypes) # main table of data
df_dtypes = {'id':str,'total_votes':int,'vote_rate':str}
votes_df = pd.read_csv('VoxCharta_voting.txt',sep='\t',dtype=df_dtypes)

# -- only looking at posts over 1 week old -- #
# ------------------------------------------- #
times = [dt.strptime(t,'%d %b %y') for t in post_df.date.values]
times = np.asarray(times) # useful for the sorting we'll do 

# reference date of 1 week ago
ref_date = dt.now() - timedelta(days=7)
print(f"Looking at posts from {dt.strftime(ref_date,'%a, %d %b %y')} and before.",end='\n\n')

indexing = np.arange(len(post_df)) 
indexing = indexing[times < ref_date] # only listing entries in the dataframe that are over 1 week old

old_posts = post_df.loc[indexing.tolist()].copy()
old_votes = votes_df.loc[indexing.tolist()].copy()
# ------------------------------------------- #

indexing = old_votes.query('total_votes > 0').index.values

plt.figure()
plt.scatter(old_votes.loc[indexing,'total_votes'],old_posts.loc[indexing,'order'],\
		edgecolor='k',alpha=0.8)

ylims = plt.ylim()
plt.ylim(ylims[1],ylims[0])
plt.xlabel('total number of votes on VoxCharta')
plt.ylabel('posting order')

plt.tight_layout()
plt.savefig('total_votes_per_order.png')
plt.close()
