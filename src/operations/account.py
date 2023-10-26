'''
Handles account-related data operations
@Author: Cole Marino
@Author Ben McManus
'''

import type.user as user
import command_prompt as cp


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


def check_if_exists(username : str):
    '''
    Checks if a user exists by checking SQL users table
    @param username: checking if this username is taken
    @return: the output from SQL
    '''
    cmd = "SELECT * FROM users WHERE username='" + username + "';"
    out = cp.execute_sql(cmd)

    return out

def newList(username):
    #TODO need a table to store user book lists
    return 0

def viewLists(username):
    #TODO need same thing as newList()
    return 0

def bookSearch():
    return 0
    
def followUser(username):
    print("Enter the email of the user you wish to follow: ")
    email = input()
    cmd = "SELECT username FROM users WHERE email = '"+email+"'"
    follower = cp.execute_sql(cmd)
    if(follower != []):
        return "INSERT INTO followings(follower_username, following_username) VALUES('"+username+"', '"+follower[0][0]+"')"
    else:
        print("User does not exit")
        
def unfollowUser(username):
    cmd = "SELECT following_username FROM followings WHERE follower_username = '"+username+"'"
    following = cp.execute_sql(cmd)
    if(following != []):
        print("Enter number of person to unfollow")
        print(type(following))
        for i in range(0, len(following)):
            print(str(i)+") "+following[i][0])
        choice = int(input())
        return "DELETE FROM followings WHERE follower_username = '"+username+"' AND following_username = '"+following[choice][0]+"'"
    else:
        print("You follow no users")
        return
    