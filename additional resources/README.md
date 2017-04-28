# Additional Resources for the MARAC_API_Workshop
This repo holds additional resources for attendees of the "There's An API for that!" workshops sponsored by the Mid-Atlantic Regional Archives Conference in 2017.

## Get a single Resource record with [getSingleRecord.py](../master/additional%20resources/getSingleRecord.py)
This GET script retrieves a single ArchivesSpace record based on the record's 'uri,' which is specified in the 'endpoint' variable on line 13. The resulting output is named _ASrecord.json_, and will appear in the same directoy as where you saved the script.

How to use:
1. Download to a local directory and open in Atom
2. Investigate line 13. Change the URI to reflect which AS resource you want to download. If you do not know, go to the AS interface, navigate to the record, and look at the address bar. Then return to Atom and change line 13.
3. Open the terminal/cygwin window and run this scipt using `python getSingleRecord.py`

This script looks for a CSV named _people.csv_ and then uses VIAF's "personalNames" index and retrieves VIAF, Library of Congress, and International Standard Name Identifier (ISNI) URIs for each potential match. These results are written to a new file named _viafPeopleResults.csv_. Credit to our friend and colleague [Eric Hanson](https://github.com/ehanson8 "Eric's GitHub").



## [viafReconciliationPeople.py](../master//additional%20resources/viafReconciliationPeople.py)
Similar to the script we ran in the workshop (viafReconciliationCorporate.py) This script looks for a CSV named _people.csv_ and then uses VIAF's "personalNames" index and retrieves VIAF, Library of Congress, and International Standard Name Identifier (ISNI) URIs for each potential match. These results are written to a new file named _viafPeopleResults.csv_. Credit to our friend and colleague [Eric Hanson](https://github.com/ehanson8 "Eric's GitHub").

The format of the  _people.csv_ should look like this:

| name          |
| ------------- |
| JK Rowling    |
| Mark Twain    |
| Adams, Douglas|


You can run this script by typing `python viafReconciliationPeople.py` in cygwin/the Mac terminal. Remember that you need to be running cygwin/the Mac terminal from the directory where the script and your _people.csv_ is saved. An output file named _viafPeopleResults.csv_ will appear in the same directory.

# Slides
You will note some additional slides in this subfolder:

## ArchivesSpace_Phila2016_Celia-ODBC.pdf
This is a pdf of a presentation given by Celia Caust-Ellenbogen (Swarthmore) crediting and explaining Nancy Enneking's (Getty) approach to connecting ArchivesSpace to Access through an ODBC connection. For those attendees that wish the API could assist in reporting and analysis, this is our recommended approach. Thanks to Celia for her permission to post these slides, and much credit and thanks to Nancy by proxy!

## Did you vagrant destroy? (both .pdf and .pptx)
These are slides meant specifically to review how to interact with the vagrant box after the workshop is over, and especially for those users who may have left it running by accident, or, needed to download the new version.

## [Automating Web Archives Records in ASpace](http://www.gregwiedeman.com/presentations/slides/wasapi.html#/)
This presentation by Gregory Wiedeman (University Archivist at SUNY Albany) was Lora's inspiration for her Archive-It script. We do not offer it for download, just follow the link immediately above.
