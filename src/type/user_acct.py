'''
    user_acct.py handles all data related to a users account. 
        Essentially everything regarding the user except for get, insert, update, and delete.

    @Author: Cole Marino (cvm4043)
'''

import command_prompt as cp


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

def get_user_lists(username):
    '''
    Gets all the lists which a user has.
    @param username: Users username.
    @return: None
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
        
    list_num = int(input("\nEnter list number to view list, hit enter to return to menu.\n"))
    print() # creates spacing
    if isinstance(list_num, int):
        view_user_list(username, result[list_num][1])
    
    # creates spacing
    print()

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