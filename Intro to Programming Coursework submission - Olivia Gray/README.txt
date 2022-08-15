To test individual modules database.txt and logfile.txt must be moved into the corresponding packages: 
e.g. to test booksearch.py, put the text files into the LibraryFunctions package; 
to test database.py, put the text files into the DatabaseFunctions package.

It is recommended to create a copy of the text files provided as these have been designed to test 
all functionalities given in the project specification. Use the copies to restore the original 
versions of the files. Ensure saved file is named 'database.txt' and 'logfile.txt'.

For the recommendation algorithm, here are some examples of member ID's that will generate 
different results: coai (for fantasy) and trln (for travel). This is because the recommendation algorithm works best
with members that are used a lot in the log file, as it generates a more accurate result.
If the member is new it will recommend the newest or most popular books in the library by default.
You can override the recommendation algorithm by specifying the genre from the recommendation
configuration panel.

For best experience, use the GUI in fullscreen windowed mode. This works on my own Windows laptop, however,
I tested my program on the Haslegrave computers by remote connection, and the GUI looked zoomed-in
with the Quit button being cut off the bottom of the screen. If this occurs, please test my coursework
on a 1920x1080 (laptop) screen. 

In the future, I would like to add:
	Searching through books by author,
	Responsively resizing widgets as the window size is altered,
	Add various filters to search, e.g. by overdue books
	Functionality to add a new book to the library database from within the program.

Submitted by Olivia Gray (F128451)