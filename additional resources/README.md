# Additional Resources for the MARAC_API_Workshop
This repo holds additional resources for attendees of the "There's An API for that!" workshops sponsored by the Mid-Atlantic Regional Archives Conference in 2017. These simple scripts and this documentation are meant to encourage users to try Python scripting at their home insitutions. The following details are meant to be understood in order.

**We highly recommend AGAINST making any changes or using any of these scripts against your working, or Production, instance of ArchivesSpace.** If you do not have a Development version of AS, see the take home documentation for details on how to ask for one.

Note that GET scripts are not that risky, so if you cannot or will not have a Dev instance of AS, you can still try GETs as your familiarize yourself with our scripts. If fear of making mistakes is holding you back, and rightly so, you should investigate options for running a Dev or Virtual Machine (VM) of AS. If your insutition decides to ramp up its use of APIs, a testing environment is a necessity.

#### How do I use these?
1. What you see above is a list of scripts available for download. Anything that ends in .py is a Python script. Read below to get an general understanding of what scripts are offered here and what they do.
2. Once you pick a script to use (we suggest starting with getSingleRecord.py), open it using the list of files towards the top of the page and then download -- or copy and paste -- the entire script to a directory on your computer. If you have to copy and paste, do this: Open Atom > create a new file > go back to GitHub > copy the script > save > name it *exactly* what it's called in GitHub.
3. You'll always need at least two things in that directory: the script itself, and the secrets.py file. So your next step is to download and then edit secrets.py with your info. See below.

#### How do I _run_ these?
This is a subtly different question from the above. This section gives practical advice for how to run these scripts, though it still raises more questions than answers. The first thing you need to know is what operating system (OS) you are using, and what OS architecture underlies the system you want to communicate to. So for example, ArchivesSpace is Linux-based, and Windows cannot communicate directly with a Linux-based app, but OS X (Macs) can.

*Windows users*
Windows users who attended the workshop will recall that we took steps to install _cygwin_, which is a "Linux-like environment for Windows making it possible to port software running on POSIX systems (such as Linux, BSD, and Unix systems) to Windows." Cygwin allows WIndows to communicate with Linux-like applications. Please see our presentation slides to walk yourself through installing cygwin and the packages required to run our scripts. Keep the cygwin installer around, it comes in handy (see immediately below).

Pro-tip: If you ever run a script and cygwin says something along the lines of "pip: command not found" it means you're missing a package (in that example, the missing package is called pip). Try Googling the error message and you will almost certainly find other people with the same problem; use their answers to determine what package you need to install, and then re-run the cgywin installer. When you get to the Install Packages screen, there is where to look for packages. This isn't a easy pro-tip, just an insight on how these programs work.

*Mac users*
There is a reason why devlopers love Macs: they're easy! You should be able to run these scripts directly from the terminal with no problem. However, you may encounter other scripts that don't run: you're probably are missing packages. Our best advice is to Google the exact error message that pops up (if one does), and chances are you'll find the solution online.

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
Once you download this, populate this secrets file with your own information.

## Get a single Resource record with _getSingleRecord.py_
This GET script retrieves a single ArchivesSpace record based on the record's 'uri,' which is specified in the 'endpoint' variable on line 13. The resulting output is named ASrecord.json, and will appear in the same directoy as where you saved the script.

How to use:
1. Download to a local directory and open in Atom
2. Investigate line 13. Change the URI to reflect which AS resource you want to download. If you do not know, go to the AS interface, navigate to the record, and look at the address bar. Then return to Atom and change line 13.
3. Be sure your



## ArchivesSpace_Phila2016_Celia-ODBC.pdf
This is a pdf of a presentation given by Celia Caust-Ellenbogen (Swarthmore) crediting and explaining Nancy Enneking's (Getty) approach to connecting ArchivesSpace to Access through an ODBC connection. For those attendees that wish the API could assist in reporting and analysis, this is our recommended approach. Thanks to Celia for her permission to post these slides, and much credit and thanks to Nancy by proxy!
