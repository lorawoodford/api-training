# Additional Resources for the MARAC_API_Workshop
This repo holds additional resources for attendees of the "There's An API for that!" workshops sponsored by the Mid-Atlantic Regional Archives Conference in 2017. These simple scripts and this documentation are meant to encourage users to try Python scripting at their home insitutions. The following details are meant to be understood in order.

We highly encourage you to not make changes against your working, or Production, instance of ArchivesSpace. If you do not have a Developement version of AS, see the take home documentation for details on how to ask for one.

Note that GETs are not that risky, so if you cannot or will not have a Dev instance of AS, you can still try GETs as your familiarize yourself with our scripts.


## Authenticating with secrets.py
Several of these scripts used for interacting with the ArchivesSpace API call a separate secrets.py that should be in the following format:

```
backendurl='YOURBACKENDURL'
user='YOURUSER'
password='YOURPASSWORD'
```
Additional example:
```
backendurl='archivesspace.fakelibrary.edu:8089'
user='archivist21'
password='guest1234'
```
Your first step should be to populate this secrets file with your own information.
