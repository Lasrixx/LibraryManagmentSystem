"""
NAME
    bookcheckout

DESCRIPTION
    Contains all functions that deal with checking out a book.

MODULE CONTENTS
    checkout_book(book_id, member_id)
    return_overdue_books_by_member(member_id)

AUTHOR
    Olivia Gray
    22/11/2021
    
"""

import sys
sys.path.append("DatabaseFunctions")

import DatabaseFunctions.database as db

def checkout_book(book_id,member_id):
    """
    Checks that the book the user wants to check out is available
    then updates the log file and database with the appropriate information.

    Parameters:
    book_id (string): The ID of the book to be withdrawn.
    member_id (string): The ID of the person withdrawing the book.

    Returns:
    (string): Confirms that the checkout was successful or
    that the book is not available to check out from the library.

    """
    #First checks that a valid member and book IDs are given,
    #if they are, then update the availability 
    if db.validate_member_id(member_id) == True:
        if db.validate_book_id(book_id) == True:
            #If the book is available, represented by 0, then
            #it is possible to check it out of the library.
            if str(db.return_availability(book_id)) == "0":
                db.add_log_entry(book_id,member_id)
                db.update_availability(book_id,member_id)
                return "Checkout complete"
            else:
                return "Book is not available for loan"
        else:
            return "Invalid book ID given"
    else:
        return "Invalid member ID given"


def return_overdue_books_by_member(member_id):
    """
    From the list of all overdue books, narrow down the list to only
    overdue books for a specified member.

    Parameters:
    member_id (string): The member to check if they owe any books.

    Returns:
    overdue_books (list): The list of all overdue books a single member owes.
    
    """
    overdue_books = []
    if db.validate_member_id(member_id) == True:
        for entry in db.return_overdue():
            #Out of all overdue books, filter to only include overdue books
            #Owed by the given member.
            if entry[1] == member_id:
                log_book_id = int(entry[0])
                overdue_books.append(db.return_database()[log_book_id-1])
    return overdue_books

if __name__=="__main__":
    #Database.txt and logfile.txt files must be in LibraryFunctions
    #folder for tests to work.
    print(checkout_book("1","12gh"))
    print(checkout_book("100","mglk"))
    print(checkout_book("20","test"))
    print(return_overdue_books_by_member("dfgh"))
    print(return_overdue_books_by_member("plae"))
          
        

        
        
        

