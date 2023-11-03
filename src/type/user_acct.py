'''
    user_acct.py handles all data related to a users account. 
        Essentially everything regarding the user except for get, insert, update, and delete.

    @Author: Cole Marino (cvm4043)
'''

import functools
import command_prompt as cp
import operations.book as book


def view_user_list(username, list_name):
    '''
    Prints all the books that are in a users list.
    @param username: The users username
    @param list_name: The name of the list being printed.
    @return none
    '''
    command = "SELECT b.title AS bookname,\
       CONCAT(p.fname, ' ', p.lname) AS author,\
       br.startdate,\
       br.enddate,\
       br.pagesread\
    FROM bookreads br\
    JOIN book b ON br.bid = b.bid\
    JOIN authors a ON b.bid = a.bid\
    JOIN person p ON a.cid = p.cid\
    JOIN bookslist bl ON br.bid = bl.bid\
    JOIN users u ON bl.username = u.username\
    WHERE u.username = '"+username+"'\
    AND bl.listname = '"+list_name+"';"
    
    result = cp.execute_sql(command)

    # Prints books that are in this list
    for i in range(len(result)):
        print("Book " + str(i+1) + ") " + result[i][0]) # Prints book title
        print("\tAuthor(s): " + result[i][1])
        print("\tRelease date: "+ result[i][2].strftime("%m/%d/%y"))
        print("\tPages: " + str(result[i][4]))

def print_all_lists(username : str):
    '''
    Prints all lists for a given user
    @param username: The username for the current user
    @return: 2D array of all lists and their data
    '''
    command = "SELECT bl.username AS listowner,\
            bl.listname,\
            COUNT(bl.bid) AS numberofbooks, \
            SUM(b.length) AS totallength \
            FROM bookslist bl  \
            JOIN book b ON bl.bid = b.bid \
            WHERE bl.username = '"+username+"' \
            GROUP BY bl.username, bl.listname  \
            ORDER BY listname ASC, listowner;" 
            
    
    #options to view lists otherwise       
    result = cp.execute_sql(command)
    
    print("\n") # spacing
    for i in range(0, len(result)):
        print(str(i+1) +") '"+ result[0][1] + "' || Number of Books: " + str(result[0][2]) + " || Total Pages: " + str(result[0][2]))

    return result

def get_user_lists(username):
    '''
    Gets all the lists which a user has.
    @param username: Users username.
    @return: None
    '''
    result = print_all_lists(username)
        
    list_num = int(input("\nEnter list number to view list, hit enter to return to menu.\n"))
    print() # creates spacing
    if isinstance(list_num, int):
        view_user_list(username, result[list_num][1])
    
    # creates spacing
    print()

    return None


def create_user_list(username: str):
    '''
    Creates a new list for the user
        If the name already exists, the user is prompted to come up with a different name
    @param username: The username for the current user
    @return: SQL command to create a new list
    '''
    name = input("Enter the name for your new book list.\n")


    ## checks that list with same name doesnt already exist
    while(True):
        check_if_available = "SELECT * FROM bookslist WHERE username='" + username + "' AND listname='" + name + "';"
        check = cp.execute_sql(check_if_available)
        print(check)
        if(check == -1 or check == []):
            break
        else:
            print("You already have a list with this name. Please choose another.")
            name=input()
            
    
    print("Enter your first book into the list!")

    # Prints all books in DB
    books = cp.execute_sql("SELECT * FROM book;")
    for i in range(0, len(books)):
        author = cp.execute_sql("SELECT cid FROM authors WHERE bid="+str(books[i][0]) + ";")

        ## Gets the authors names
        atmp=""
        if(author == -1 or author == []):
            author = "N/A"
        else:
            # Converts from a list containing a tuple to a string. This sucked.
            for i in range(0, len(author)):
                author[i] = str(author[i])
                author[i] = author[i].replace(',', '')
                author[i] = author[i].replace('(', '')
                author[i] = author[i].replace(')', '')
                a = cp.execute_sql("SELECT fname, lname FROM person WHERE cid="+author[i]+";")
                a = str(a[0][0] + " " + a[0][1])
                author[i] = a
            
            for i in range(0, len(author)):
                atmp+=author[i]
                if(i+1 != len(author)):
                    atmp += ", "
            author=atmp

        publisher = cp.execute_sql("SELECT name from publisher WHERE pid=" + str(books[i][4]) + ";")
        publisher = publisher[0]
        publisher = publisher[0]
        rating = (cp.execute_sql("SELECT rating FROM bookratings WHERE bid=" + str(books[i][0])+";"))

        # Calculates average rating
        if(rating == -1 or rating == []):
            rating = "N/A"
        else:
            rating_avg = 0
            for i in range(0, len(rating)):
                rating[i] = str(rating[i])
                rating[i] = rating[i].replace(',', '')
                rating[i] = rating[i].replace('(', '')
                rating[i] = rating[i].replace(')', '')
                rating_avg += float(rating[i])
            rating_avg = rating_avg/len(rating)

        # Prints book shit
        print(str(i+1) +") "+books[i][1] + "\n Author: "+ str(author)+ "\n Publisher: "+ str(publisher) + "\nLength: "+ str(books[i][3]) + " pages\n Rating: " + str(rating_avg) + " stars\n")
    
    ## Gets first book user wants to add
    while(True):
        book_name = input("Type a book name from the above list of books:\n")
        bid=cp.execute_sql("SELECT bid FROM book WHERE title='" + book_name+"';")
        if(books == [] or books == -1):
            print("No books with this title exists! Please try another book.")
        else:
            break
    bid=bid[0]
    bid = str(bid)
    bid = bid.replace(',', '')
    bid = bid.replace('(', '')
    bid = bid.replace(')', '')
    return "INSERT INTO bookslist(bid, username, listname) VALUES ("+bid + ", '"+username+"', '"+name+"');"


def add_to_list(username : str):
    print("Your book lists are:")
    lists = view_user_list(username)

    if(len(lists) == 0):
        req = input("You do not have any lists. Would you like to create one? (y/n)")
        if(req == "y"):
            return create_user_list(username)
        elif(req == "n"):
            print("Okay.")
            return None
        else:
            print("This is an invalid response. Exiting...")
            return None

    listnum = input("What list are you adding a book to? (Enter list number from above)\n")

    ## Checking that book exists
    name=""
    out=""
    while(True):
        name = input("Enter the title of the book being added to list '" + lists[listnum][0] + "'")

        out = cp.execute_sql(book.book_Search_cmd(name, "N/A", "N/A", "N/A", "N/A"))
        if(out == -1 or out == []):
            print("This book does not exist.")
            continue
        else:
            break

    cmd = "SELECT * FROM bookslist WHERE bid='" + out[0] + "' AND listname='" + name + "'"
    out = cp.execute_sql(cmd)
    if(out != -1 or out != []):
            print("This book is already in the list.")

    cmd = "INSERT INTO bookslist(bid, username, listname) VALUES (" + out[0] + ", '" + username + "' , '" + name + "')"
    return cmd 


def follow_user(username: str):
    '''
    Allows user to follow another user
    @param username: The username wanted to be followed!
    @return: SQL statement or None
    '''
    print("Enter the email of the user you wish to follow: ")
    email = input()
    cmd = "SELECT username FROM users WHERE email = '"+email+"'"
    follower = cp.execute_sql(cmd)
    if(follower != -1):
        return "INSERT INTO followings(followerusername, followingusername) VALUES('"+username+"', '"+follower[0][0]+"')"
    else:
        print("User does not exit")
        return -1
        
def unfollow_user(username:str):
    '''
    Allows a user to unfollow another user that they are following
    @param username: the username being unfollowed
    @return: SQL statement or None
    '''
    cmd = "SELECT followingusername FROM followings WHERE followerusername = '"+username+"'"
    following = cp.execute_sql(cmd)
    if(following != [] or following != -1):
        print("Enter number of person to unfollow")
        for i in range(0, len(following)):
            print(str(i)+") "+following[i][0])
        choice = int(input())
        return "DELETE FROM followings WHERE followerusername = '"+username+"' AND followingusername = '"+following[choice][0]+"'"
    else:
        print("You follow no users")
        return