# arXiv-order
Some code I'm writing to pursue a theory about arXiv.

Future plans
-----------
* Need to think of a way to automate this process (get it to run daily?)
* In `access_VoxCharta.py`, need to add a `try...except` that flags when there is no search result returned for an arXiv number... because an alarming number of these recent posts don't seem to appear on VoxCharta.
* Get code set up for Benty-Fields, too.

Notes to get things to run:
* Make sure that your `geckodriver` executable and Firefox application are both up to date
* Make sure they they are also matching 64 bit or 32 bit (whatever is necessary for your computer)
* Add the `geckodriver` executable location to your `$PATH` OR place it in `/usr/local/bin`
* If that doesn't work, also place a copy of it in your `/usr/bin/`
