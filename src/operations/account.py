'''
Handles account-related data operations
@Author: Cole Marino
@Author Ben McManus
'''

import src.type.user as user
import src.command_prompt as cp


def check_if_exists(username : str):
    '''
    Checks if a user exists by checking SQL users table
    @param username: checking if this username is taken
    @return: the output from SQL
    '''
    cmd = "SELECT * FROM users WHERE username='" + username + "';"
    out = cp.execute_sql(cmd)

    return out

def signin(username, password):
    '''
    Sign in function for a user
        Gets username and password, checks if they are correct, and gets user data

    @return [correct info]: list of user table data
    @return [incorrect info/no user]: empty list
    '''
    cmd = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "';"
    return cmd

def signup():
    '''
    Signs up a new user
        Directs to insert function for user
    '''
    return user.insert()

def newList(username):
    #TODO need a table to store user book lists
    return 0

def viewLists(username):
    #TODO need same thing as newList()
    return 0

def bookRatePrompt(username):
    """
    "Houses the bookRate Function for use in the command prompt interface"
    :return: SQL command
    """

    prompt = input("Please provide the book and its rating (1-5)\n"
                   "Usage: [book], [rating]")
    cmd_input = prompt.strip().split(", ")
    out = bookRate(cmd_input[0], cmd_input[1], username)
    return out


def bookRate(book, rating, username):
    """
    returns an SQL command as a string to rate the book as named by the variable book
    :param book: exact title of the book
    :param rating: the rating of the book
    :param username: username of the user rating the book
    :return: SQL command as a string
    """
    cmd = "INSERT INTO bookratings(bid, username, rating)\n" \
            "SELECT bid, '" + username + "', " + rating + "\n"  \
            "FROM book\n" \
            "WHERE title = '" + book + "'\n" \
            "LIMIT 1;" \

    return cmd

def bookSearch():
    return 0
    
def followUser(username: str):
    '''
    Allows user to follow another user
    @param username: The username wanted to be followed!
    @return: SQL statement or None
    '''
    print("Enter the email of the user you wish to follow: ")
    email = input()
    cmd = "SELECT username FROM users WHERE email = '"+email+"'"
    follower = cp.execute_sql(cmd)
    if(follower != []):
        return "INSERT INTO followings(followerusername, followingusername) VALUES('"+username+"', '"+follower[0][0]+"')"
    else:
        print("User does not exit")
        
def unfollowUser(username:str):
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
    