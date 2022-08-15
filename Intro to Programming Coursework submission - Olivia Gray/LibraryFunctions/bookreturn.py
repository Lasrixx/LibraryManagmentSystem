"""
NAME
    bookreturn

DESCRIPTION
    Functions relating to returning a book.

MODULE CONTENTS
    return_book(book_id)

AUTHOR
    Olivia Gray
    24/11/2021

"""

import sys
sys.path.append("DatabaseFuntions")

import DatabaseFunctions.database as db
from datetime import date

def return_book(book_id):
    """
    Checks that a book is currently being loaned then updates the database
    and log to show that it has just been returned.

    Parameters:
    book_id (string): The ID of the book being returned.

    Returns:
    (string): Represents that the book was successfully returned or not.
    
    """
    if str(db.return_availability(book_id)) != "0":
        db.update_log(book_id)
        db.update_availability(book_id,"0")
        return "Return complete"
    else:
        return "Book is already available"

if __name__ == "__main__":
    #Database.txt and logfile.txt must be in LibraryFunctions foler.
    print(return_book("1"))
    print(return_book("14"))
