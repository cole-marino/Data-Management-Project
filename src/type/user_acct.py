'''
    user_acct.py handles all data related to a users account. 
        Essentially everything regarding the user except for get, insert, update, and delete.

    @Author: Cole Marino (cvm4043)
    @Author: Hunter Boggan(hab1466)
'''
import command_prompt as cp
import operations.book as book
import pandas as pd


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

    print("You have (" + str(len(result))+ ") collections!")
    
    for i in range(0, len(result)):
        print(str(i+1) +") '"+ result[i][1] + "' || Number of Books: " + str(result[i][2]) + " || Total Pages: " + str(result[i][3]))

    return result


def edit_user_list(username : str):
    '''
    Edits a user list.

    @param username: The username of the user who is editing one of their lists.
    @return: String of SQL command which updates a list.
    '''
    prompt = input("Please provide the name of the book list you would like to change and its new name\n"
                "If you would like to review your list(s) or their name(s), please use one of the previously defined actions\n"
                "Usage: [list name], [new list name]\n")
    
    cmd_input = prompt.strip().split(", ")
    
    cmd = "UPDATE bookslist SET listname='"+ cmd_input[1] + "'WHERE username ='"+username+"' AND listname='"+ cmd_input[0] +"';"
    
    return cmd
    
    
def delete_user_list(username : str):
    '''
    Deletes an entire user list.

    @param username: The username of the user who is deleting one of their lists.
    @return: String of SQL command that deletes a list for a user.
    '''
    lists = get_user_lists(username)
    if (len(lists) == 0):
        print("You do not have any lists to delete.")
        return None
    
    prompt = input("Please provide the name of the book list you would like to delete\n"
                   "If you would like to review your list(s) or their name(s), please use one of the previously defined actions\n"
                   "Usage: [list name]\n")
    
    cmd = "DELETE FROM bookslist WHERE username ='"+username+"' AND listname='"+ prompt +"';"
    
    return cmd
     

def get_user_lists(username):
    '''
    Gets all the lists which a user has.
    @param username: Users username.
    @return: None
    '''
    
    print("\nYour Collections:")
    result = print_all_lists(username)
        
    # Showing all books within a list isn't required in this phase and it doesn't work correctly anyways
    # so I decided to comment it out - Hunter
    
    # list_num = input("\nEnter list number to view list, type 'menu' to return to menu.\n")
    # if (list_num != 'menu'):
    #     list_num = int(list_num)
    #     print() # creates spacing
    #     if isinstance(list_num, int):
    #         view_user_list(username, result[list_num-1][1])
    
    print() #spacing
    
    return result


def create_user_list(username: str):
    '''
    Creates a new list for the user
        If the name already exists, the user is prompted to come up with a different name
    @param username: The username for the current user
    @return: SQL command to create a new list
    '''
    list_name = input("Enter the name for your new book list.\n")


    ## checks that list with same name doesnt already exist
    while(True):
        check_if_available = "SELECT * FROM bookslist WHERE username='" + username + "' AND listname='" + list_name + "';"
        check = cp.execute_sql(check_if_available)
        print(check)
        if(check == -1 or check == []):
            break
        else:
            print("You already have a list with this name. Please choose another.")
            list_name = input()
            
    
    print("Enter your first book into the list!")

    ## Gets first book user wants to add
    while(True):
        book_name = input("Type the name of a book:\n")
        bid=cp.execute_sql("SELECT bid, title FROM book WHERE title LIKE \'%" + book_name + "%\'")
        book_num = 0
        if(bid == [] or bid == -1):
            print("\nNo books with this title exists in our system! Please give a more specific title or try another book.")
        elif(len(bid) > 1):
            bid_df = pd.DataFrame(bid, columns=["ID", "Title"])
            print("\n" + bid_df.to_string())
            book_num = input("\nType the number of the book you'd like to select \n(This is the first number shown, NOT the ID)\n")
            book_num = int(book_num)
            if(book_num < len(bid) and book_num >= 0):
                break
        else:
            break
    bid_str = str(bid[book_num][0])
    # bid = bid.replace(',', '')
    # bid = bid.replace('(', '')
    # bid = bid.replace(')', '')
    return "INSERT INTO bookslist(bid, username, listname) VALUES ("+bid_str+", '"+username+"', '"+list_name+"');"


def add_to_list(username : str):
    '''
    Allows a user to add a book to one of their lists.

    @param username: The username of the user tho is adding a book to their list.
    @return: Either string of SQL command or None.
    '''
    lists = get_user_lists(username)

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

    list_num = input("What list are you adding a book to? (Enter list number from above)\n")
    list_num = int(list_num)

    ## Checking that book exists
    list_name = lists[list_num-1][1]
    out=""
    while(True):
        book_name = input("\nEnter the title of the book being added to list '" + list_name + "'\n")

        bid=cp.execute_sql("SELECT bid, title FROM book WHERE title LIKE \'%" + book_name + "%\'")
        if(bid == [] or bid == -1):
            print("\nNo books with this title exists in our system! Please give a more specific title or try another book.")
        elif(len(bid) > 1):
            bid_df = pd.DataFrame(bid, columns=["ID", "Title"])
            print("\n" + bid_df.to_string())
            book_num = input("\nType the number of the book you'd like to select \n(This is the first number shown, NOT the ID)\n")
            book_num = int(book_num)
            if(book_num < len(bid) and book_num >= 0):
                break
        else:
            book_num = 0
            break

    bid_str = str(bid[book_num][0])

    cmd = "SELECT * FROM bookslist WHERE bid='" + bid_str + "' AND username='"+ username +"' AND listname='" + list_name + "'"
    out = cp.execute_sql(cmd)
    if(out == [] or out == -1):
        cmd = "INSERT INTO bookslist(bid, username, listname) VALUES (" + bid_str + ", '" + username + "' , '" + list_name + "')"
        return cmd
    
    print("This book is already in the list.")
    return None


def delete_from_list(username : str):
    '''
    Deletes a book from a booklist.

    @param username: The username of the user who is deleting a book from their list.
    @return: SQL command to create a new list or None.
    '''
    lists = get_user_lists(username)

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
        
    list_num = input("What list are you deleting a book from? (Enter list number from above)\n")
    list_num = int(list_num)
    list_name = lists[list_num-1][1]
    
    cmd = "SELECT b.bid, b.title \
        FROM book AS b INNER JOIN bookslist AS bl ON b.bid = bl.bid \
        WHERE bl.username='"+ username +"' AND bl.listname ='"+ list_name +"';"
    
    list_books = cp.execute_sql(cmd)
    
    print("\nThe books in this list are:")
    list_books_df = pd.DataFrame(list_books, columns=["ID", "Title"])
    print("\n" + list_books_df.to_string())
    
    book_num = input("\nType the number of the book you'd like to delete \n(This is the first number shown, NOT the ID)\n")
    book_num = int(book_num)
    
    bid_str = str(list_books[book_num][0])
    
    cmd = "DELETE FROM bookslist WHERE bid='" + bid_str + "' AND username='"+ username +"' AND listname='" + list_name + "'"
    out = cp.execute_sql(cmd)
    if (out == -1):
        print("Could not find book to delete from list\n")
    
    return None


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
    
def get_followings(username : str):
    '''
    Tells the user who they are following and how many followers they have.

    @param username: The username of the user who is getting their followings.
    @return: 1 if success or -1 if unsuccessful
    '''
    print("\nPeople you are following:")
    cmd = "SELECT followingusername FROM followings WHERE followerusername='" + username + "';"
    follow = cp.execute_sql(cmd)
    #print(follow)

    if(follow==-1):
        return -1
    
    print("You are following (" + str(len(follow)) + ") users!")
    for user in follow:
        print(user[0])
    print()

    cmd = "SELECT followerusername FROM followings WHERE followingusername='" + username + "';"
    following = cp.execute_sql(cmd)
    if(following==-1):
        return-1
    print("You have (" + str(len(following)) + ") followers!")
    for user in following:
        print(user[0])
    print()



    return 1

def get_top_books(username : str):
    '''
    Gets the top 10 books for a user based on their rating
    @param username: Username of the user
    @return: Output of SQL command
    '''
    print("Your top 10 books by your rating are:")
    cmd = "SELECT DISTINCT avg(br.rating) as avgrating, b.title, b.length \n" \
            "FROM bookratings br \n" \
            "INNER JOIN book b ON b.bid = br.bid \n" \
            "INNER JOIN bookreads bre ON b.bid = bre.bid \n" \
            "WHERE bre.username='" \
            + username + "' \n" \
            "GROUP BY b.bid, br.bid, b.length \n" \
            "ORDER BY avgrating DESC \n" \
            "LIMIT 10;\n"

    out = cp.execute_sql(cmd)

    # prints books or gives error
    if(len(out) is 0):
        print("You have not read any books. Maybe you should some time!")
    elif(out is not [] and out is not -1):
        # prints the books
        count=0
        for book in out:
            count+=1
            print((str(count))+") " + book[1] + " || Rating: " + (str(book[0])) + " || Pages: " + (str(book[2])))
        
        # if there were not 10 books prints, the empty entries are listed.
        if(count is not 10):
            count+=1
            for i in range(count, 11):
                print((str(i)) + ") None. You should read more books!")

        return 1
    else:
        print("Could not retrieve your top 10 books read.")
        return -1