# Additional Resources for the MARAC_API_Workshop
This repo holds additional resources for attendees of the "There's An API for that!" workshops sponsored by the Mid-Atlantic Regional Archives Conference in 2017. These simple scripts and this documentation are meant to encourage users to try Python scripting at their home insitutions. The following details are meant to be understood in order.

We highly encourage you to not make changes against your working, or Production, instance of ArchivesSpace. If you do not have a Developement version of AS, see the take home documentation for details on how to ask for one.

Note that GETs are not that risky, so if you cannot or will not have a Dev instance of AS, you can still try GETs as your familiarize yourself with our scripts.

How do I use these?
1. Read below to get a general understanding of what scripts are offered here.
2. Once you pick a script to use (we suggest starting with getSingleRecord.py), open it using the list of files towards the top of the page and then download -- or copy and paste -- the entire script to a directory on your computer. You'll always need at least two things in that directory: the script itself, and the secrets.py file. If you have to copy and paste, do this: Open Atom > create a new file > go back to GitHub > copy the script > save > name it *exactly* what it's called in GitHub.

## Authenticating with secrets.py
Several of these scripts used for interacting with the ArchivesSpace API call a separate secrets.py that should be in the following format:

```
backendurl='YOURBACKENDURL'
user='YOURUSER'
password='YOURPASSWORD'
```
Or, more explicitly:
```
backendurl='archivesspace.fakelibrary.edu:8089'
user='archivist21'
password='guest1234'
```
Your first step should be to populate this secrets file with your own information.

## Get a single Resource record with getSingleRecord.py
getSingleRecord will authenticate to your instance of AS using
