"""
NAME
    booksearch

DESCRIPTION
    Contains functions relating to searching through the database
    to return books with a given title.

MODULE CONTENTS
    search_books_by_title(title)
    search_books_by_id(book_id)
    return_overdue_books_by_title(title)
    return_overdue_books_by_id(book_id)
    calculate_overdue_by(checkout_date)
    is_book_in_database(title)

AUTHOR
    Olivia Gray
    20/11/2021
"""

import sys
sys.path.append("DatabaseFuntions")

import DatabaseFunctions.database as db
from datetime import date

def search_books_by_title(title):
    """
    Returns a list of books with a given title.

    Parameters:
    title (string): The book title that the user wants
    to search for in the database.

    Returns:
    books (list): List containing all books with the specified title.

    """
    books = []
    for record in db.return_database():
        #Converts to both the given title and title in the database
        #to lowercase as we should not care if there is a
        #capitalisation error in the input.
        if record[2].lower().find(title.lower()) != -1:
            books.append(record)
    return books

def search_books_by_id(book_id):
    """
    Returns the book with the given ID number.

    Parameters:
    book_id (string): The ID of the book to get all associated information of.

    Returns:
    record (list): List containing relevant information of the book, e.g.
    title, author, availability, etc....
    """
    for record in db.return_database():
        #Record[0] refers to the book ID field
        if record[0] == book_id:
            return record

def return_overdue_books_by_title(title):
    """
    Returns a list of overdue books with a given title.

    Parameters:
    title (string): The book title that the user wants to sesarch for.

    Returns:
    overdue_books (list): List containing the book ID, book title, and
    overdue amount of every overdue book with the specified title.
    """
    overdue_books = []
    for entry in db.return_overdue():
        log_book_id = int(entry[0])
        book_title = db.return_database()[log_book_id-1][2]
        #Filters the list of all overdue books to
        #just those with the given title.
        if book_title.lower().find(title.lower()) != -1:
            checkout_date = entry[2].split("/")
            overdue_by = calculate_overdue_by(checkout_date)
            overdue_books.append([log_book_id,book_title,overdue_by])
    return overdue_books

def return_overdue_books_by_id(book_id):
    """
    Returns how much a given book ID is overdue by

    Parameters:
    book_id (string): The ID of the book to check if it is overdue.

    Returns:
    (list): List containing the given book ID and how much it is overdue by.
    The list will empty if the book ID is not overdue.
    """
    for entry in db.return_overdue():
        if entry[0] == book_id:
            overdue_by = calculate_overdue_by(entry[2].split("/"))
            return [entry[0],overdue_by]
    return []
                                              

def calculate_overdue_by(checkout_date):
    """
    Calculates how much a book is overdue by. The book is not
    specified for this function.

    Parameters:
    checkout_date (list): Contains date in format ["dd","mm","yyyy"].

    Returns:
    overdue_by (int): How many days above 60 that the book has been
    on loan for.
    """
    #Uses datetime module to calculate the difference between
    #the date the book was checked out and today's date
    #Subtract 60 from the result as it takes 60 days of
    #being on loan to become overdue.
    overdue_by = (date.today() - date(int(checkout_date[2]),
                                      int(checkout_date[1]),
                                      int(checkout_date[0]))).days-60
    return overdue_by

def is_book_in_database(title):
    """
    Checks whether a book exists in the database text file
    as a form of validation.

    Parameters:
    title (string): The book title that needs to be validated.

    Returns:
    (bool): Signifying whether the book does exist in the database.
    """
    for record in db.return_database():
        if title.lower() == record[2].lower():
            return True
    return False

if __name__ == "__main__":
    #These tests will only work when database.txt and logfile.txt
    #Are in the LibraryFunctions folder.
    print(search_books_by_title("Dune"))
    print(search_books_by_title("the"))
    print(search_books_by_title(""))
    print(search_books_by_title("234"))
    print(search_books_by_id("1"))
    print(search_books_by_id("24"))
    print(return_overdue_books_by_title("the lord of the rings"))
    print(return_overdue_books_by_title("The"))
    print(return_overdue_books_by_id("1"))
    print(return_overdue_books_by_id("25"))
    print(calculate_overdue_by(["13","3","2020"]))
    print(is_book_in_database("the lord of the rings"))
    print(is_book_in_database("horrid henry"))
        
                               

