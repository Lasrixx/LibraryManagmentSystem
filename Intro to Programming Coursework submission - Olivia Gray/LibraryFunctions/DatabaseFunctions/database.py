"""
NAME
    database
    
DESCRIPTION
    Contains all functions that directly access or alter the
    database.txt and logfile.txt files.
    This is designed to prevent other modules from needing to
    access the database or loogfile directly.
    Also contains input validation functions.

MODULE CONTENTS
    return_database()
    return_availability(book_id)
    update_availability(book_id, member_id)
    return_log()
    return_overdue()
    add_log_entry(book_id,member_id)
    update_log(book_id)
    validate_member_id(member_id)
    validate_book_id(book_id)

AUTHOR
    Olivia Gray
    20/11/2021
"""

from datetime import date

database_file = "database.txt"
log_file = "logfile.txt"

def return_database():
    """
    Returns a list of all records from database.txt.

    Returns:
    records (list): The list of all records of books.
    
    """

    records = []
    try:
        database = open(database_file,"r")
        for line in database:
            record = line.strip().split(", ")
            records.append(record)
        database.close()
        return records
    except:
        return []

def return_availability(book_id):
    """
    Returns the value in the member_id field of
    the record with the given book_id.

    Parameters:
    book_id (string): The book ID to check the availability of. 

    Returns:
    availability (string): String representing the book is
    available or who currently has it.
    
    """
    
    #book_id corresponds to the index of the records list
    #book_id is 1-indexed, whereas records is 0-indexed
    #index 5 within each record refers to the member_id field
    return return_database()[int(book_id)-1][5]

def update_availability(book_id, member_id):
    """
    Modifies the database text document with up-to-date details of
    whether a book is on loan or not. It works both ways: updating when
    a book is taken out and when it is returned (in this case, 0 is given
    as the member ID).

    Parameters:
    book_id (string): the ID of the book whose availability needs updating.
    member_id (string): the ID of the member who currently has the book;
    this value will be given as '0' if the book is being returned and will
    be made available again.

    Returns:
    void

    """
    books = return_database()
    books[int(book_id)-1][5] = member_id

    #Change list into one correctly formatted string for file
    updated_books = []
    for record in books:
        line = ", ".join(record)
        updated_books.append(line)
    updated_books = "\n".join(updated_books)

    try:
        database = open(database_file,"w")
        database.write(updated_books)
        database.close()
    except:
        return "Writing to file failed - file not found"

def return_log():
    """
    Returns a list of all entries in the log.
    The log contains information relating to books being withdrawn and returned
    and which member did this.

    Returns:
    records (list): List of all records in the log.
    
    """
    records = []
    try:
        log = open(log_file,"r")
        for line in log:
            record = line.strip().split(", ")
            records.append(record)
        log.close()
        return records
    except:
        return []

def return_overdue():
    """
    Returns a list of books that have been on loan for more than 60 days.
    This function will use Python's standard datetime library to
    calculate the difference between 2 dates.

    Returns:
    overdue_books (list): List containing all books that have been borrowed
    for more than 60 days.

    """

    #Read through logfile, but only need to check for overdue books when they
    #have not yet been returned (represented by '-' in the return date field
    #index 3 within each record refers to the return date field
    overdue_books = []
    current_date = date.today()
    for record in return_log():
        if record[3] == "-":
            #Convert checkout_date to year, month, day format and
            #check if loaned for longer than 60 days
            checkout_field = record[2].split("/")
            checkout_date = date(int(checkout_field[2]),\
                                 int(checkout_field[1]),int(checkout_field[0]))
            if (current_date-checkout_date).days > 60:
                overdue_books.append(record)
    return overdue_books

def add_log_entry(book_id,member_id):
    """
    Appends a new line to the log file when the librarian checks out a book.

    Parameters:
    book_id (string): The ID of the book being withdrawn.
    member_id (string): The ID of the member withdrawing the book.

    Returns:
    void

    """
    #Convert datetime format (yyyy-mm-dd) to dd/mm/yyyy.
    current_date = str(date.today()).split("-")
    checkout_date = current_date[2]+"/"\
            +current_date[1]+"/"+current_date[0]
    #Create the new line for the log,
    #with book ID, member ID, checkout date format.
    entry = "\n" + str(book_id) + ", " + member_id + ", "\
            + checkout_date + ", -"
    try:
        log = open(log_file,"a")
        log.write(entry)
        log.close()
    except:
        return "file not found"

def update_log(book_id):
    """
    Modifies the log text file when a book is returned so the correct
    entry will now include its return date.

    Parameters:
    book_id (string): The ID of the book being returned.

    Returns:
    void

    """
    
    updated_log = []
    for entry in return_log():
        #Checks that the given book ID has been taken out
        #Entry[0] is book ID and Entry[3]is return date,
        #which will be "-" if the book has not yet been returned.
        if entry[0] == str(book_id) and entry[3]=="-":
            current_date = str(date.today()).split("-")
            entry[3] = current_date[2]+"/"+current_date[1]+"/"+current_date[0]
        updated_log.append(", ".join(entry))

    updated_log = "\n".join(updated_log)
    
    try:
        log = open(log_file,"w")
        log.write(updated_log)
        log.close()
    except:
        return "file not found"

def validate_member_id(member_id):
    """
    Returns a boolean value representing whether a given member_id
    has passed the validation checks.

    Parameters:
    member_id (string): The member ID to be validated.

    Returns:
    (bool): Boolean representing that the
    member ID has passed validation checks or not.
    """

    #To pass validity checks:
        #ID must be length 4
        #ID must be lowercase
        #ID must only contain alphabetical characters
        #(i.e. no numbers or symbols)

    if len(member_id) != 4:
        return False
    elif member_id.lower() != member_id:
        return False
    else:
        for i in member_id:
            #Ord() converts a character to its ASCII value
            #ASCII values 98-121 are the lowercase alphabet.
            if ord(i) < 97 or ord(i) > 122:
                return False
    return True
    
def validate_book_id(book_id):
    """
    Checks that the book ID the user inputs is valid according to the rules
    of the database text file.

    Parameters:
    book_id (string): the ID of the book to validate.

    Returns:
    (bool): Boolean value representing whether the given book ID passes
    the validation checks.
    
    """
    
    #To pass validity check:
        #ID must be between 1 and number of records in database
        #ID must only contain numbers
    for i in str(book_id):
        #ASCII values 49-56 are numbers 0-9
        if ord(i) < 48 or ord(i) > 57:
            return False
    if int(book_id) < 1 or int(book_id) > len(return_database()):
        return False            
    return True

if __name__=="__main__":
    #To test this code, the database.txt and logfile.txt
    #need to moved into the DatabaseFunctions sub-package
    #This module must be accessed through modules in
    #LibraryFunctions which apply input validation
    #Therefore, erroneous data should not be used in these tests.
    print(return_database())
    print(return_availability(1))
    print(return_availability(24))
    print(return_log())
    print(return_overdue())
    print(validate_member_id("coai"))
    print(validate_member_id("12mn"))
    print(validate_member_id("lmnpq"))
    print(validate_member_id("12345"))
    print(validate_book_id("12"))
    print(validate_book_id("24"))
    print(validate_book_id("100"))
    print(validate_book_id("1o"))
          
          
    

