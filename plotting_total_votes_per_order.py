'''
Plotting the total votes for a given arXiv post versus the post order.

Future plans:	color points by submission window (Mon-Fri)
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'Taylor Hutchison'
__email__ = 'aibhleog@tamu.edu'

# reading in the posts
df_dtypes = {'order':int,'id':str,'date':str}
post_df = pd.read_csv('arXiv_posts.txt',sep='\t',dtype=df_dtypes) # main table of data
df_dtypes = {'id':str,'total_votes':int,'vote_rate':str}
votes_df = pd.read_csv('VoxCharta_voting.txt',sep='\t',dtype=df_dtypes)

indexing = votes_df.query('total_votes > 0').index.values

plt.figure()
plt.scatter(votes_df.loc[indexing,'total_votes'],post_df.loc[indexing,'order'],\
		edgecolor='k',alpha=0.8)

ylims = plt.ylim()
plt.ylim(ylims[1],ylims[0])
plt.xlabel('total number of votes on VoxCharta')
plt.ylabel('posting order')

plt.tight_layout()
plt.savefig('total_votes_per_order.png')
plt.close()
