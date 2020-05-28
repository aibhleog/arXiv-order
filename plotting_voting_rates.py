'''
Plotting the voting history for a particular post on VoxCharta.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from datetime import datetime as dt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.dates as md

__author__ = 'Taylor Hutchison'
__email__ = 'aibhleog@tamu.edu'

# reading in the main table about VoxCharta voting
# currently going to find the post with max votes and look at that
df_dtypes = {'id':str,'total_votes':int,'vote_rate':str}
main_df = pd.read_csv('VoxCharta_voting.txt',sep='\t',dtype=df_dtypes)

max_votes = main_df.query(f'total_votes == {main_df["total_votes"].max()}').copy()
max_id = max_votes.id.values[0]
max_vote_rate = max_votes.vote_rate.values[0]
max_votes = max_votes.total_votes.values[0] # it's okay to overwrite this variable

df_dtypes = {'cast_date':str,'cast_time':str}
df = pd.read_csv(max_vote_rate,sep='\t',dtype=df_dtypes)
df['cast'] = df['cast_date'] + ' ' + df['cast_time']

# looking at the vote rates!
times = [dt.strptime(t,'%m/%d/%Y %I:%M%p') for t in df.cast.values]

plt.figure(figsize=(10,5))
plt.gca().xaxis.set_major_formatter(md.DateFormatter('%m/%d'))
plt.title(f'Voting history for {max_id} // Total votes: {max_votes}')

plt.scatter(times,range(len(times)))
plt.xlim(times[0] - timedelta(days=1), times[-1] + timedelta(days=1))
plt.xlabel('vote cast')
plt.ylabel('vote order')

plt.tight_layout()
plt.savefig(max_vote_rate[:-4]+'.pdf')
plt.close()
