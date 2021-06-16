# arXiv-order
Some code I'm writing to pursue a theory about arXiv.

TODO list
---------
* figure out the ADS API to pull citation count for all arXiv ids
  * need to get token approved
* there are some VoxCharta vote logs in the `votes_VoxCharta/` folder that are not in the `old_VoxCharta_voting.txt` -- add them!  (could do by hand or could code it)


General Notes
-----------
* Don't use arxiv.org for the data harvesting -- use their copy site, export.arxiv.org (or you'll eventually get denied access to arXiv because you're hogging the resources)
* VoxCharta will freeze (no more daily postings from arXiv) on 31 December 2020
* VoxCharta started *around* 2009?
* when did Benty-Fields start?


Future plans
-----------
* Would it be better to wait a while to let citation count build up on the papers that I have VoxCharta vote counts for (and especially ones where I have both VoxCharta & benty-fields votes for)?
* Need to think of a way to automate this process (get it to run daily?)
* *(site no longer exists)* In `access_VoxCharta.py`, need to add a `try...except` that flags when there is no search result returned for an arXiv number... because an alarming number of these recent posts don't seem to appear on VoxCharta.  
  
**Notes to get things to run:**
* Make sure that your `geckodriver` executable and Firefox application are both up to date
* Make sure they they are also matching 64 bit or 32 bit (whatever is necessary for your computer)
* Add the `geckodriver` executable location to your `$PATH` OR place it in `/usr/local/bin`
* If that doesn't work, also place a copy of it in your `/usr/bin/`

## NOTE: VoxCharta will no longer pull arXiv postings on 31 December 2020
![announcement by James Guillochon](official_VoxCharta_annoucement.png)
