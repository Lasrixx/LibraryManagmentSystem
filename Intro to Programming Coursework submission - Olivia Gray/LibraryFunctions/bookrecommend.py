"""
NAME
    bookrecommend

DESCRIPTION
    Contains functions relating to producing a list of recommended
    book titles for the user based on what is most popular and
    what genre they take out most often.

MODULE CONTENTS
    return_popular_books()
    return_member_genre(member_id)
    is_book_new(purchase_date)
    was_book_read(member_id,book_id)
    sum_repeated_titles(popular_books,popular_titles)
    return_recommendations(member_id)
    return_genres()

AUTHOR
    Olivia Gray
    27/11/2021

"""

import sys
sys.path.append("DatabaseFunctions")

from statistics import mode
from datetime import date
import textwrap as tw
import DatabaseFunctions.database as db

def return_popular_books():
    """
    Creates a list containing the amount of times each book has been withdrawn.

    Returns:
    withdrawn_amount (list): List representing the amount of times each book
    has been withdrawn. The index+1 of the list represents the book ID.
    """
    #Order book IDs by popularity
    log = db.return_log()
    database = db.return_database()
    #Book ID are basically indexes (starting at 1)
    #so the index of the list can be used as a tag
    #for which book ID we're looking at
    withdrawn_amount = []
    for record in database:
        #Append 1 so that a book that has never been taken out before
        #will still be affected by the weightings.
        withdrawn_amount.append(1)
    for entry in log:
        withdrawn_amount[int(entry[0])-1] += 1

    return withdrawn_amount

def return_member_genre(member_id):
    """
    Finds which genre of book the user has taken out the most using the
    log text document.

    Parameters:
    member_id (string): The ID of the member that the user wants to
    create a recommendation list for.

    Returns:
    favourite_genre (string): The genre that the user has taken out most often.
    """
    log = db.return_log()
    database = db.return_database()
    withdrawn_books = []
    withdrawn_genre = []

    #Iterate through the log backwards
    #This is so that if there are multiple genres taken out equally
    #as much, it will return the most recent genre they took out as
    #this is likely to be their current favourite genre.
    for i in range(len(log)-1,-1,-1):
        if log[i][1] == member_id:
            withdrawn_books.append(log[i][0])

    for book in withdrawn_books:
        withdrawn_genre.append(database[int(book)-1][1])

    #Find most commonly withdrawn genre
    favourite_genre = mode(withdrawn_genre)

    return favourite_genre

def is_book_new(purchase_date):
    """
    Calculates if a book was purchased by the library in the last year.

    Parameters:
    purchase_date (string): purchase_date of the book ID to check if
    it is new or not.

    Returns:
    (bool): Signifies if a book is newly purchased or not.
    """
    purchase_date = purchase_date.split("/")
    days_since_purchase = (date.today() - date(int(purchase_date[2]),\
                                               int(purchase_date[1]),\
                                               int(purchase_date[0]))).days 
    if days_since_purchase<= 100 :
        return True
    return False

def was_book_read(member_id,book_id):
    """
    Scans the log file to check if a given member has previously
    read a given book.

    Parameters:
    member_id (string): ID of member to check if they have already read
    a book.
    book_id (int): ID of book we are checking if a member has already read.
    """
    log=db.return_log()
    for entry in log:
        if entry[1]==member_id and entry[0]==str(book_id):
            #This means they have already withdrawn the book before.
            return True
    return False

def sum_repeated_titles(popular_books,popular_titles):
    """
    Takes the list of popular titles and removes any repeated titles,
    adding their score to the score in the first occurence of the title
    in the list of popular books.

    Parameters:
    popular_books (list): List of the amount of times a book has been taken out.
    popular_titles (list): List of the titles of each book in popular_books,
    in the same order.

    Returns:
    popular_books (list): List of all books with repeated books added together.
    popular_titles (list): List of all book titles, with repeated occurences
    removed.
    """
    for i in range(len(popular_books)):
        #If the first occurence of the current title is not the current
        #index it has already occured before so we can add the value to the
        #first occurence and remove the current occurence.
        index = popular_titles.index(popular_titles[i])
        if index != i:
            popular_books[index] += popular_books[i]
            #Give the lists an arbitrary null value to remove at the end 
            popular_books[i] = "///"
            popular_titles[i] = "///"

    while "///" in popular_books:
        popular_books.remove("///")
        popular_titles.remove("///")
    return popular_books,popular_titles

def return_recommendations(member_id,num_recommend,new_weight,
                           genre_weight,genre,include_read):
    """
    Collects the information about the most popular books and the member's
    favourite genre and sorts it into a list of 5 recommendations for the
    member.

    Parameters:
    member_id (string): The ID of the member to create a recommendation
    list for.
    num_recommend (int): The number of books should be recommended by the
    function.
    new_weight (int): The priority given to new books in the algorithm
    (higher is better).
    genre_weight (int): The priority given to books belonging to the
    member's favourite genre (higher is better).
    include_read (bool): Whether the algorithm should omit books the
    member has already read.

    Returns:
    recommended_books (list): List of popularity rankings (descending).
    recommended_titles (list): List containing the corresponding book titles
    to the values in recommended_books.
    """
    if db.validate_member_id(member_id) == True:
        database = db.return_database()
        popular_books = return_popular_books()
        
        try:
            if genre != "DEFAULT":
                favourite_genre = genre
            else:
                favourite_genre = return_member_genre(member_id)
        except:
            #If return_member_genre errors, it is because the member has not
            #rented from the library before so the system has no data on them.
            #In this case, recommend them the most popular books.
            popular_titles = []
            for record in database:
                #Fill is used to wrap text to the next line.
                #This stops titles overlapping on the graph.
                popular_titles.append(tw.fill(record[2],width=20)\
                                      +"\n("+record[1]+")")
            #Apply a higher weighting to new books
            for i in range(len(popular_books)):
                if is_book_new(database[i][4]) == True:
                    #Add 1 so that new books will be recommended even if they
                    #have not yet been taken out.
                    popular_books[i] *= new_weight
            #Remove duplicate titles.
            popular_books,popular_titles=sum_repeated_titles\
                                          (popular_books,popular_titles)
            #Sort both popular books and popular titles in descending order
            #according to popular books.   
            popular_books,popular_titles = (list(i) for i in zip\
                    (*sorted(zip(popular_books,popular_titles),reverse=True)))
            #Only return the top 5 recommendations.
            recommended_books = popular_books[:num_recommend]
            recommended_titles = popular_titles[:num_recommend]
            return recommended_books,recommended_titles    

        #Apply a higher weighting to books in popular_books
        #that are the member's preferred genre and new books.
        #Decrease the weighting if the member has already read the book.
        for i in range(len(popular_books)):
            is_new = is_book_new(database[i][4])
            if (was_book_read(member_id,database[i][0]) == True
                and include_read == False):
                popular_books[i] *= 0
            elif (database[i][1].lower() == favourite_genre.lower()
                  and is_new == True):
                popular_books[i] *= (genre_weight+new_weight)
            elif database[i][1].lower() == favourite_genre.lower():
                popular_books[i] *= genre_weight
            elif is_new == True:
                popular_books[i] *= new_weight
            else:
                popular_books[i] *= 1

        #Now need to add together scores of books with same title (different ID)
        popular_titles = []
        for i in range(len(popular_books)):
            popular_titles.append(tw.fill(database[i][2],width=20)\
                                  +"\n("+database[i][1]+")")

        popular_books,popular_titles = sum_repeated_titles\
                                       (popular_books,popular_titles)    
        
        #Sort popular_books now into descending order (most popular at start)
        #This sorts both books and titles into descending order, keeping
        #titles in the order representing books
        popular_books,popular_titles = (list(i) for i in zip\
                (*sorted(zip(popular_books,popular_titles),reverse=True)))

        recommended_books = popular_books[:num_recommend]
        recommended_titles = popular_titles[:num_recommend]

        return recommended_books,recommended_titles

def return_genres():
    """
    Creates a list of every genre the library owns.

    Returns:
    genres (list): Contains each genre that the library owns a book of.
    
    """
    genres=[]
    for record in db.return_database():
        if record[1] not in genres:
            genres.append(record[1])
    return genres

if __name__ == "__main__":
    #Database.txt and logfile.txt must be in LibraryFunctions folder for tests
    #to work correctly
    print(return_popular_books())
    print(return_member_genre("coai"))
    print(return_recommendations("coai",5,2,6))
    print(return_recommendations("qwer",5,7,2))
    print(is_book_new("13/1/2020"))
    print(is_book_new("13/1/2021"))
    print(is_book_new("24/11/2000"))
    print(was_book_read("coai",12))
    print(was_book_read("coai",21))
    print(return_genres())
            




