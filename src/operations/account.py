'''
Handles account-related data operations
@Author: Cole Marino
@Author: Ben McManus
@Author: Hunter Boggan (hab1466)
'''

import type.user as user
import command_prompt as cp
from datetime import datetime
from datetime import date


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

def record_access(username:str):
    '''
    Records access times for a user
        Is to be executed upon each user sign in. Gets the username, current date, and current time
    @param username: The username of the person signing in
    @return: SQL command to be executed
    '''
    today = str(date.today())
    today.replace('/', '-')
    
    time = str(datetime.now())
    
    cmd = "INSERT INTO accesses(username, accessdate, accesstime) VALUES('"+username+"', '"+today+"', '"+time+"')"
    return cmd
    


def new_List(username):
    #TODO need a table to store user book lists
    return 0

def view_Lists(username):
    #TODO need same thing as newList()
    return 0


    
def follow_User(username: str):
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
        
def unfollow_User(username:str):
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