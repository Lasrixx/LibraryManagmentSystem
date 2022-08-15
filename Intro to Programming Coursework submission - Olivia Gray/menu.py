"""
NAME
    menu

DESCRIPTION
    Contains functions necessary to build the GUI for the application.

MODULE CONTENTS
    quit_program()
    submit_search()
    clear_search()
    list_all()
    get_search_input(search_input)
    submit_check()
    submit_return()
    submit_checkout()
    expand_checkout()
    collapse_checkout()
    submit_recommend()

AUTHOR
    Olivia Gray
    25/11/2021
"""

import sys
sys.path.append("LibraryFunctions")

from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import \
     (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import LibraryFunctions.booksearch as booksearch
import LibraryFunctions.bookreturn as bookreturn
import LibraryFunctions.bookcheckout as bookcheckout
import LibraryFunctions.bookrecommend as bookrecommend

def quit_program():
    """
    Closes the application when the user presses the 'Quit' button.
    """
    window.quit()
    window.destroy()

def submit_search(book_title,button_pressed):
    """
    Calls the searching functions from booksearch and outputs them to the
    interface.
    """
    books = booksearch.search_books_by_title(book_title)
    #Empty out the results of the last search
    clear_search()
    if books != [] or button_pressed == True:
        booksearch_invalid_book_label.configure(text="")
        overdue_books = booksearch.return_overdue_books_by_title(book_title)
        for i in range(len(books)):
            #Filling in the data in the table 
            search_output_id.insert(i,books[i][0])
            search_output_genre.insert(i,books[i][1])
            search_output_title.insert(i,books[i][2])
            search_output_author.insert(i,books[i][3])
            search_output_purchase_date.insert(i,books[i][4])
            if books[i][5] == "0":
                #If book is available, we know it is not overdue
                search_output_available.insert(i,"Yes")
                search_output_overdue.insert(i,"No")
                search_output_member.insert(i,"-")
            else:
                #If book is not available, decide whether it is overdue
                search_output_available.insert(i,"No")
                search_output_member.insert(i,books[i][5])
                #Initialise overdue as false and if we find a book is
                #actually overdue we can change it
                overdue=False
                for overdue_book in overdue_books:
                    if int(overdue_book[0])==int(books[i][0]):
                        search_output_overdue.insert(i,"Yes - " +\
                                    str(overdue_book[2]) + " days")
                        search_output_overdue.itemconfig(i,bg=pale_red)
                        overdue = True
                if overdue == False:
                    search_output_overdue.insert(i,"No")                
    elif books == []:
        booksearch_invalid_book_label.configure(text=\
        "Library does not own book", font="none 12 bold", fg="red")

def clear_search():
    """
    Empties the contents in the book search table.
    """
    search_output_id.delete(0,END)
    search_output_genre.delete(0,END)
    search_output_title.delete(0,END)
    search_output_author.delete(0,END)
    search_output_purchase_date.delete(0,END)
    search_output_available.delete(0,END)
    search_output_member.delete(0,END)
    search_output_overdue.delete(0,END)

def list_all():
    """
    Calls search with an empty string so the while library database is
    ouptutted in the table.
    """
    submit_search("",True)

def get_search_input(search_input):
    """
    Calls a search with a given sequence of characters so the table
    only contains books with the sequence of characters in its title.
    If the text field is empty, the table should be cleared.
    """
    book_title = search_input.get()
    if search_input.get():
        submit_search(book_title,False)
    else:
        clear_search()

def submit_check(check_input,button_pressed):
    """
    Calls the search function and outputs it in the return/checkout table.
    """
    collapse_checkout()
    book_ids = check_input.get()
    book_ids = book_ids.split(",")
    stripped_book_ids = []
    #Strip whitespace from the IDs to stop errors appearing in the GUI
    #when user types ',' not followed by an ID or ',,'.
    for book_id in book_ids:
        if book_id.strip() != "":
            stripped_book_ids.append(book_id.strip())
    #Remove previous results
    return_checkout_invalid_book_label.configure(text="")
    return_checkout_id.delete(0,END)
    return_checkout_genre.delete(0,END)
    return_checkout_title.delete(0,END)
    return_checkout_author.delete(0,END)
    return_checkout_available.delete(0,END)
    return_checkout_member.delete(0,END)
    return_checkout_overdue.delete(0,END)
    if button_pressed == False:
        return_checkout_complete.delete(0,END)
    output=""
    if check_input.get() != "":
        for i in range(len(stripped_book_ids)):
            #Get all data about a given book ID
            book_data = booksearch.search_books_by_id(stripped_book_ids[i])
            if book_data != None:
                #Fill out table with the information
                return_checkout_id.insert(i,book_data[0])
                return_checkout_genre.insert(i,book_data[1])
                return_checkout_title.insert(i,book_data[2])
                return_checkout_author.insert(i,book_data[3])
                if book_data[5] == "0":
                    return_checkout_available.insert(i,"Yes")
                    return_checkout_member.insert(i,"-")
                    return_checkout_overdue.insert(i,"No")
                else:
                    return_checkout_available.insert(i,"No")
                    return_checkout_member.insert(i,book_data[5])
                    overdue=booksearch.return_overdue_books_by_id(book_data[0])
                    if overdue != []:
                        return_checkout_overdue.insert(i,"Yes - "\
                                                       +str(overdue[1])+" days")
                        return_checkout_overdue.itemconfig(i,bg=pale_red)
                    else:
                        return_checkout_overdue.insert(i,"No")
            else:
                output += "Book ID: "+book_ids[i]+" not owned by library\n"
                return_checkout_invalid_book_label.configure(text=output)

def submit_return():
    """
    Processes a book return then produces an output for the interface,
    detailing whether the book was overdue, and whether the return was
    completed successfully.
    """
    collapse_checkout()
    
    #Returns tuple of IDs in the listbox containing IDs
    book_ids = return_checkout_id.get(0,END)
    return_checkout_complete.delete(0,END)
    for i in range(len(book_ids)):
        output = bookreturn.return_book(book_ids[i])
        return_checkout_complete.insert(i,output)
        #Change colours of text in the table depending on whether
        #the return was successful or not (green for yes, red for no).
        if output == "Return complete":
            return_checkout_complete.itemconfig(i,bg=pale_green)
        else:
            return_checkout_complete.itemconfig(i,bg=pale_red)
    submit_check(check_input,True)

def expand_checkout():
    """
    Shows the frame that asks for member ID in the return/checkout
    tab when the Checkout All button is pressed.
    """
    checkout_member_frame.pack()

def collapse_checkout():
    """
    Hides the frame asking for member ID when certain buttons are
    pressed.
    """
    checkout_member_frame.pack_forget()

def submit_checkout():
    """
    Processes a book being withdrawn by a given member and produces an
    output showing that the withdrawal was successful or not.
    """
    #Clear the previous results from the table
    return_checkout_complete.delete(0,END)
    checkout_invalid_member_label.configure(text="")
    book_ids = return_checkout_id.get(0,END)
    checkout_overdue_id.delete(0,END)
    checkout_overdue_title.delete(0,END)
    checkout_overdue_by.delete(0,END)
    checkout_overdue_label.configure(text="")
    member_id = checkout_member_text_field.get()
    overdue_books = bookcheckout.return_overdue_books_by_member(member_id)
    #Print associated information about overdue books
    #held by the given member ID.
    if overdue_books != []:
        checkout_overdue_frame.pack()
        checkout_overdue_label.configure(text=member_id+"'s overdue books:")
        for i in range(len(overdue_books)):
            checkout_overdue_id.insert(i,overdue_books[i][0])
            checkout_overdue_title.insert(i,overdue_books[i][2])
            print(booksearch.return_overdue_books_by_id(overdue_books[i][0]))
            checkout_overdue_by.insert(i,booksearch.return_overdue_books_by_id\
                                       (overdue_books[i][0])[1])
    else:
        checkout_overdue_frame.pack_forget()
    for i in range(len(book_ids)):
        output = bookcheckout.checkout_book(book_ids[i],member_id)
        return_checkout_complete.insert(i,output)
        if output == "Checkout complete":
            return_checkout_complete.itemconfig(i,bg=pale_green)
        elif output == "Invalid member ID given":
            checkout_invalid_member_label.configure(text=output)
            return_checkout_complete.itemconfig(i,bg=pale_red)
        else:
            return_checkout_complete.itemconfig(i,bg=pale_red)
    submit_check(check_input,True)

def submit_recommend():
    """
    Calls the recommendation functions from the bookrecommendation module
    and presents the output in a line graph, showing the top 5
    recommendations for a given member.
    """
    recommend_invalid_member_label.configure(text="")
    member_id = bookrecommend_text_field.get()
    include_previously_read=read_input.get()
    try:
        num_recommend = recommend_amount.get()
        newness_weighting = newness_weight.get()
        genre_weighting = genre_weight.get()
        genre = genre_input.get()
        #Deal with invalid inputs by setting them to default values instead.
        rank,titles = bookrecommend.return_recommendations(member_id,
                                                    int(num_recommend),
                                                    int(newness_weighting),
                                                    int(genre_weighting),
                                                    genre.strip(),
                                                    include_previously_read)
        wrapped_titles = []
        graph_title.configure(text="Top "+str(num_recommend)+ \
                              " recommendations for: " + member_id)
        #Clear the previous graph
        plt.clf()
        #Draw new graph
        plt.xlabel("Book Titles")
        plt.ylabel("Popularity rank")
        plt.bar(titles,rank,color=dark_purple)
        plt.xticks(fontsize="x-small")
        canvas.draw()
    except:
        recommend_invalid_member_label.configure(text="Invalid member ID")        

window = Tk()
window.title("Library Management System")
window.geometry("")
window.configure(background="white")

#RGB colours for the GUI that are not built into TKinter
yellow = "#FFF700"
dark_purple = "#6B0067"
pale_red = "#F57A7A"
pale_green = "#B4FFA8"

#Title label should be consistent in whole program
title_frame = Frame(window,bg=dark_purple)
title_frame.pack(side=TOP,fill=BOTH,expand=TRUE)
title_label = Label (title_frame, text="Library Management System",\
            bg=dark_purple, fg=yellow,font="none 32 bold")
title_label.pack(side=TOP, pady=25)

#Notebook style
style = ttk.Style()
style.configure("TNotebook.Tab",font="none 14 bold")

#Tabs to navigate to each part of the system
tabs = ttk.Notebook(window)
tabs.pack(expand=TRUE,fill=BOTH,side=TOP)
welcome_tab = ttk.Frame(tabs)
booksearch_tab = ttk.Frame(tabs)
bookreturn_checkout_tab = ttk.Frame(tabs)
bookrecommend_tab = ttk.Frame(tabs)
tabs.add(welcome_tab,text="     Welcome     ")
tabs.add(booksearch_tab,text="     Search     ")
tabs.add(bookreturn_checkout_tab,text="     Return/Checkout     ")
tabs.add(bookrecommend_tab,text="     Recommendations     ")

#Quit button
quit_button=Button(window,text="Quit",font="none 16 bold",command=quit_program)
quit_button.pack(side=BOTTOM,pady=20)

#Welcome label explains how to use program
welcome_frame = Frame(welcome_tab,bg="white")
welcome_frame.pack(expand=TRUE,fill=BOTH)
welcome_text = "Welcome to the Library Management System \n\
To search through the library's books by title, click 'Search'\n\
To return or checkout book(s), click 'Return/Checkout'\n\
To see book recommendations, click 'Recommendations'\n\
To exit the application, click 'Quit'"
welcome_label = Label(welcome_frame,bg="white",text=welcome_text,font="none 24")
welcome_label.pack(side=TOP,pady=100)

#Book search tab:
booksearch_frame = Frame(booksearch_tab,bg="white")
booksearch_frame.pack(expand=TRUE,fill=BOTH)
#Book search label
booksearch_label = Label(booksearch_frame,bg="white",text="Enter book title \
to search through books:", font="none 16 bold")
booksearch_label.pack(side=TOP,padx=50,pady=25,ipadx=15,ipady=5)
#Book title input field
search_input = StringVar()
search_input.trace("w",lambda name, index,mode,search_input=search_input\
                   : get_search_input(search_input))
title_text_field = Entry(booksearch_frame,textvariable=search_input)
title_text_field.pack(side=TOP)
#Invalid book label
booksearch_invalid_book_label = Label(booksearch_frame,bg="white")
booksearch_invalid_book_label.pack(side=TOP,ipadx=10,ipady=5,pady=10)
#Search all button
list_all_button = Button(booksearch_frame,font="none 14", text="List All Books"\
                           ,command=list_all)
list_all_button.pack(side=TOP,pady=5)
#Frame for the search results table
search_output_frame = Frame(booksearch_frame)
search_output_frame.pack(side=TOP,padx=20,pady=20)
search_output_id_frame = Frame(search_output_frame)
search_output_id_frame.pack(side=LEFT)
search_output_id_label = Label(search_output_id_frame,text="Book ID",\
                               font="none 12 bold",bg=yellow)
search_output_id_label.pack(side=TOP,fill=X)
search_output_id = Listbox(search_output_id_frame,height=30)
search_output_id.pack(side=BOTTOM,)
search_output_genre_frame = Frame(search_output_frame)
search_output_genre_frame.pack(side=LEFT)
search_output_genre_label = Label(search_output_genre_frame,text="Book Genre",\
                                  font="none 12 bold",bg=yellow)
search_output_genre_label.pack(side=TOP,fill=X)
search_output_genre = Listbox(search_output_genre_frame,height=30,width=30)
search_output_genre.pack(side=BOTTOM)
search_output_title_frame = Frame(search_output_frame)
search_output_title_frame.pack(side=LEFT,expand=TRUE)
search_output_title_label = Label(search_output_title_frame,text="Book Title",\
                                  font="none 12 bold",bg=yellow)
search_output_title_label.pack(side=TOP,fill=X)
search_output_title = Listbox(search_output_title_frame,height=30,width=60)
search_output_title.pack(side=BOTTOM)
search_output_author_frame = Frame(search_output_frame)
search_output_author_frame.pack(side=LEFT)
search_output_author_label = Label(search_output_author_frame,text="Author",\
                                   font="none 12 bold",bg=yellow)
search_output_author_label.pack(side=TOP,fill=X)
search_output_author = Listbox(search_output_author_frame,height=30,width=30)
search_output_author.pack(side=BOTTOM)
search_output_purchase_frame = Frame(search_output_frame)
search_output_purchase_frame.pack(side=LEFT)
search_output_purchase_label = Label(search_output_purchase_frame,\
                    text="Purchase date",font="none 12 bold",bg=yellow)
search_output_purchase_label.pack(side=TOP,fill=X)
search_output_purchase_date = Listbox(search_output_purchase_frame,height=30)
search_output_purchase_date.pack(side=BOTTOM)
search_output_available_frame = Frame(search_output_frame)
search_output_available_frame.pack(side=LEFT)
search_output_available_label = Label(search_output_available_frame,\
                        text="Available",font="none 12 bold",bg=yellow)
search_output_available_label.pack(side=TOP,fill=X)
search_output_available = Listbox(search_output_available_frame,height=30)
search_output_available.pack(side=BOTTOM)
search_output_member_frame = Frame(search_output_frame)
search_output_member_frame.pack(side=LEFT)
search_output_member_label = Label(search_output_member_frame,\
                text="Withdrawn By",font="none 12 bold",bg=yellow)
search_output_member_label.pack(side=TOP,fill=X)
search_output_member = Listbox(search_output_member_frame,height=30)
search_output_member.pack(side=BOTTOM)
search_output_overdue_frame = Frame(search_output_frame)
search_output_overdue_frame.pack(side=LEFT)
search_output_overdue_label = Label(search_output_overdue_frame,text="Overdue",\
                                    font="none 12 bold",bg=yellow)
search_output_overdue_label.pack(side=TOP,fill=X)
search_output_overdue = Listbox(search_output_overdue_frame,height=30)
search_output_overdue.pack(side=TOP)

#Book return and checkout tab:
return_checkout_frame = Frame(bookreturn_checkout_tab,bg="white")
return_checkout_frame.pack(expand=TRUE,fill=BOTH)
#Book return and checkout label
return_checkout_label = Label(return_checkout_frame,bg="white",text="Enter ID\
 of book to return or checkout:\n\
 To return or checkout multiple books, use a list:\
 e.g. 13,4,24 (no spaces)", font="none 16 bold")
return_checkout_label.pack(side=TOP,padx=50,pady=25,ipadx=15,ipady=5)
#Book return and checkout input field
check_input = StringVar()
check_input.trace("w",lambda name,index,mode,check_input=check_input: \
                  submit_check(check_input,False))
return_checkout_text_field = Entry(return_checkout_frame,\
                                   textvariable=check_input)
return_checkout_text_field.pack(side=TOP)
#Warning should appear if user enters a book ID not in the database
return_checkout_invalid_book_label = Label(return_checkout_frame,\
                                           font="none 14",fg="red",bg="white")
return_checkout_invalid_book_label.pack(side=TOP)
#Frame for the output of pressing the check availability button
return_checkout_output_frame = Frame(return_checkout_frame)
return_checkout_output_frame.pack(side=TOP,padx=20,pady=20)
return_checkout_id_frame = Frame(return_checkout_output_frame)
return_checkout_id_frame.pack(side=LEFT)
return_checkout_id_label = Label(return_checkout_id_frame,text="Book ID",\
                               font="none 12 bold",bg=yellow)
return_checkout_id_label.pack(side=TOP,fill=X)
return_checkout_id = Listbox(return_checkout_id_frame,height=12)
return_checkout_id.pack(side=BOTTOM,)
return_checkout_genre_frame = Frame(return_checkout_output_frame)
return_checkout_genre_frame.pack(side=LEFT)
return_checkout_genre_label = Label(return_checkout_genre_frame,text=\
                        "Book Genre",font="none 12 bold",bg=yellow)
return_checkout_genre_label.pack(side=TOP,fill=X)
return_checkout_genre = Listbox(return_checkout_genre_frame,height=12,width=30)
return_checkout_genre.pack(side=BOTTOM)
return_checkout_title_frame = Frame(return_checkout_output_frame)
return_checkout_title_frame.pack(side=LEFT,expand=TRUE)
return_checkout_title_label = Label(return_checkout_title_frame,text=\
                        "Book Title",font="none 12 bold",bg=yellow)
return_checkout_title_label.pack(side=TOP,fill=X)
return_checkout_title = Listbox(return_checkout_title_frame,height=12,width=60)
return_checkout_title.pack(side=BOTTOM)
return_checkout_author_frame = Frame(return_checkout_output_frame)
return_checkout_author_frame.pack(side=LEFT)
return_checkout_author_label = Label(return_checkout_author_frame,text="Author"\
                                   ,font="none 12 bold",bg=yellow)
return_checkout_author_label.pack(side=TOP,fill=X)
return_checkout_author=Listbox(return_checkout_author_frame,height=12,width=30)
return_checkout_author.pack(side=BOTTOM)
return_checkout_available_frame = Frame(return_checkout_output_frame)
return_checkout_available_frame.pack(side=LEFT)
return_checkout_available_label = Label(return_checkout_available_frame,\
                        text="Available",font="none 12 bold",bg=yellow)
return_checkout_available_label.pack(side=TOP,fill=X)
return_checkout_available = Listbox(return_checkout_available_frame,height=12,\
                                    width = 15)
return_checkout_available.pack(side=BOTTOM)
return_checkout_member_frame = Frame(return_checkout_output_frame)
return_checkout_member_frame.pack(side=LEFT)
return_checkout_member_label = Label(return_checkout_member_frame,\
                        text="Withdrawn By",font="none 12 bold",bg=yellow)
return_checkout_member_label.pack(side=TOP,fill=X)
return_checkout_member = Listbox(return_checkout_member_frame,height=12)
return_checkout_member.pack(side=BOTTOM)
return_checkout_overdue_frame = Frame(return_checkout_output_frame)
return_checkout_overdue_frame.pack(side=LEFT)
return_checkout_overdue_label = Label(return_checkout_overdue_frame,\
                        text="Overdue",font="none 12 bold",bg=yellow)
return_checkout_overdue_label.pack(side=TOP,fill=X)
return_checkout_overdue = Listbox(return_checkout_overdue_frame,height=12)
return_checkout_overdue.pack(side=TOP)
return_checkout_complete_frame = Frame(return_checkout_output_frame)
return_checkout_complete_frame.pack(side=LEFT)
return_checkout_complete_label = Label(return_checkout_complete_frame,text=\
            "Return/Checkout Complete",font="none 12 bold",bg=yellow)
return_checkout_complete_label.pack(side=TOP,fill=X)
return_checkout_complete = Listbox(return_checkout_complete_frame,height=12,\
                                   width=35)
return_checkout_complete.pack(side=TOP)
#Frame for return and checkout buttons
return_checkout_button_frame = Frame(return_checkout_frame)
return_checkout_button_frame.pack(side = TOP)
#Return all button
return_button = Button(return_checkout_button_frame,text=\
                "Return All",font="none 14",command=submit_return)
return_button.pack(side=LEFT)
#Checkout all button
checkout_button = Button(return_checkout_button_frame,text=\
        "Checkout All",font="none 14",command=expand_checkout)
checkout_button.pack(side=RIGHT)
#Input field for member ID needs to appear
#when the user presses the checkout button.
checkout_member_frame = Frame(return_checkout_frame,bg="white")
checkout_member_frame.pack(side=TOP,pady=10)
checkout_member_label = Label(checkout_member_frame,bg="white",text=\
            "Enter ID of member checking out book:",font="none 14 bold")
checkout_member_label.pack(side=TOP)
checkout_member_text_field = Entry(checkout_member_frame)
checkout_member_text_field.pack(side=TOP,pady=10)
checkout_member_submit_button = Button(checkout_member_frame,text="Checkout"\
                                       ,font="none 14",command=submit_checkout)
checkout_member_submit_button.pack(side=TOP)
checkout_invalid_member_label = Label(checkout_member_frame,bg="white",\
                                      fg="red",font="none 14")
checkout_invalid_member_label.pack(side=TOP)
#Frame to display any books held by the member that are overdue
checkout_overdue_frame = Frame(checkout_member_frame,bg="white")
checkout_overdue_frame.pack(side=TOP)
checkout_overdue_label=Label(checkout_overdue_frame,bg="white",\
                             font="none 14 bold")
checkout_overdue_label.pack(side=TOP)
checkout_overdue_id_frame = Frame(checkout_overdue_frame,bg="white")
checkout_overdue_id_frame.pack(side=LEFT)
checkout_overdue_id_label = Label(checkout_overdue_id_frame,text="Book ID"\
                                  ,font="none 10 bold",bg=pale_red)
checkout_overdue_id_label.pack(side=TOP,fill=X)
checkout_overdue_id = Listbox(checkout_overdue_id_frame,height=5)
checkout_overdue_id.pack(side=TOP)
checkout_overdue_title_frame = Frame(checkout_overdue_frame,bg="white")
checkout_overdue_title_frame.pack(side=LEFT)
checkout_overdue_title_label = Label(checkout_overdue_title_frame,text=\
                        "Book Title",font="none 10 bold",bg=pale_red)
checkout_overdue_title_label.pack(side=TOP,fill=X)
checkout_overdue_title = Listbox(checkout_overdue_title_frame,height=5,width=60)
checkout_overdue_title.pack(side=TOP)
checkout_overdue_by_frame = Frame(checkout_overdue_frame,bg="white")
checkout_overdue_by_frame.pack(side=LEFT)
checkout_overdue_by_label = Label(checkout_overdue_by_frame,text=\
                        "Overdue By",font="none 10 bold",bg=pale_red)
checkout_overdue_by_label.pack(side=TOP,fill=X)
checkout_overdue_by = Listbox(checkout_overdue_by_frame,height=5,width=30)
checkout_overdue_by.pack(side=TOP)
checkout_overdue_frame.pack_forget()
checkout_member_frame.pack_forget()

#Book recommend tab:
bookrecommend_frame = Frame(bookrecommend_tab,bg="white")
bookrecommend_frame.pack(expand=TRUE,fill=BOTH)
#Book recommend label
bookrecommend_label = Label(bookrecommend_frame,bg="white", \
                    text="Enter ID of member:",font="none 16 bold")
bookrecommend_label.pack(side=TOP,padx=50,pady=25,ipadx=15,ipady=5)

#Book recommend text field
bookrecommend_text_field = Entry(bookrecommend_frame,bg="white")
bookrecommend_text_field.pack(side=TOP)

#Book recommend submit button
bookrecommend_submit_button = Button(bookrecommend_frame,text="Recommend",\
                        font="none 14",command=submit_recommend)
bookrecommend_submit_button.pack(side=TOP,padx=25,pady=5)
#Label to display warning when invalid member ID is inputted
recommend_invalid_member_label = Label(bookrecommend_frame,bg="white",\
                                       fg="red",font="none 14")
recommend_invalid_member_label.pack(side=TOP,pady=2)
#Recommendation graph frame (for graph configuration as well)
recommendation_frame = Frame(bookrecommend_frame,bg="white")
recommendation_frame.pack(side=TOP)
graph_frame = Frame(recommendation_frame,bg="white")
graph_frame.pack(side=LEFT)
#Configuration panel
config_frame = Frame(recommendation_frame,bg="white",\
            highlightbackground="black",highlightthickness=1)
config_frame.pack(side=RIGHT,ipadx=12,ipady=12)
config_label = Label(config_frame,bg="white",text="Configure Graph"\
                     ,font="none 16 bold")
config_label.pack()
recommend_amount_label = Label(config_frame,bg="white",text=\
    "Enter amount of recommendations:\n(3-8)",font="none 14")
recommend_amount_label.pack()
recommend_amount = Scale(config_frame,from_=3,to=8,\
                         orient=HORIZONTAL,bg="white")
recommend_amount.pack()
recommend_amount.set(5)
favourite_genre_label = Label(config_frame,bg="white",text=\
    "Enter member's favourite genre:",font="none 14")
favourite_genre_label.pack()
genre_input=StringVar()
genres = ["DEFAULT"]+bookrecommend.return_genres()
genre_input.set(genres[0])
genre_dropdown = OptionMenu(config_frame,genre_input,*genres)
genre_dropdown.pack()
read_input = BooleanVar()
read_books_checkbox = Checkbutton(config_frame,text=\
    "Include previously read books",variable=read_input,\
                                  bg="white",font="none 14")
read_books_checkbox.pack()
newness_weight_label = Label(config_frame,bg="white",text=\
                "Newness rank:\n1 (least important) 10 (most important)",\
                font="none 14")
newness_weight_label.pack()
newness_weight = Scale(config_frame,from_=1,to=10,bg="white",orient=HORIZONTAL)
newness_weight.pack()
newness_weight.set(2)
genre_weight_label = Label(config_frame,bg="white",\
    text="Favourite genre rank:\n1 (least important) 10 (most important)",\
    font="none 14")
genre_weight_label.pack()
genre_weight=Scale(config_frame,from_=1,to=10,bg="white",orient=HORIZONTAL)
genre_weight.pack()
genre_weight.set(6)
refresh_button = Button(config_frame,text="Update Graph",\
                        font="none 14",command=submit_recommend)
refresh_button.pack(pady=10,ipady=2,ipadx=4)
#Recommendation graph title
graph_title = Label(graph_frame,font="none 14",bg="white")
graph_title.pack(side=TOP)

#Book recommend bar chart
fig = plt.figure(figsize=(12,5.4))
plt.xlabel("Book Titles")
plt.ylabel("Popularity rank")
canvas = FigureCanvasTkAgg(fig,master=graph_frame)
canvas.draw()
canvas.get_tk_widget().pack(side=TOP)

window.mainloop()

if __name__ == "__main__":
    #menu tested manually.
    pass
