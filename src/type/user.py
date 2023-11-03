'''
Handles GET, INSERT, DELETE, UPDATE functions for users type

@Author: Cole Marino
'''

from datetime import date
from datetime import datetime

import operations.account as acct
import command_prompt as cp

def get():
    '''
    Handles GET command for user type
    @return: SQL command for GET
    '''
    print("Enter username")
    username = input()

    return "SELECT * FROM Users WHERE username LIKE '" + username + "'"

def insert():
    '''
    Handles INSERT command for user type
    @return: SQL command for INSERT
    '''
    print("Enter username")
    username = input()

    # checks if username exists
    ret = (acct.check_if_exists(username))
    if(ret != [] or ret != -1):
        print("\nUsername already exists, please try again.")
        return insert()

    print("\nEnter password")
    password = input()

    print("\nEnter first name")
    f_name = input()

    print("\nEnter last name")
    l_name = input()

    print("\nEnter email")
    email = input()

    print("\nEnter date of birth (usage: [year]-[month]-[day])\n(usage ex: 2001-09-11 [god bless our troops])")
    dob = input()
    
    # gets todays date
    today = str(date.today())
    today.replace('/', '-')


    ### Make it check if username already exists
    cmd = "INSERT INTO users(username, name, email, password, dob, createdate) VALUES ('"+username+"', '"+(f_name+" "+l_name)+"', '"+email+"', '"+password+"', '"+dob+"', '"+today+"');"
    return str(cmd)


def delete(username : str):
    '''
    Deletes an account from the database.
    @param username: The user being deleted. (Screw them, what a loser.)
    @return: SQL statement to delete account.
    '''
    print("Are you sure? (y/n)")
    sure = input()
    sure.lower()
    if(sure == 'y'):
        # TODO: ADD LOG OUT WHEN ACCOUNT DELETED
        return "DELETE FROM  users WHERE username='"+username+"';"
    elif(sure=='n'):
        print("Okay!\n")
        return
    else:
        print("Invalid response..")
        return delete(username)
    

def update(username : str):
    '''
    Prompts user to update whatever data they choose.
    @param username: The username of the user who's account is being updated
    @return: SQL statement to update users data, none if incorrect.
    '''
    print("\nAccount Edit Settings: (Enter number corresponding to setting to be changed.)")
    print("1) Change password\n2) Change username\n3) Change email\n")
    entry = input()

    match entry:
        case "1":    # Change the password
            print("\nEnter new password: ")
            new_pass = input()
            out = "UPDATE users SET password='" + new_pass + "' WHERE username='" + username + "';"
            return out
        case "2":    # Change the username
            print("\nEnter new username: ")
            new_username = input()
            out = "UPDATE users SET username='" + new_username + "' WHERE username='" + username + "';"
            return out
        case "3":       # Change the email
            print("\nEnter new email: ")
            new_email = input()
            out = "UPDATE users SET email='" + new_email + "' WHERE username='" + username + "';"
            return out
        case _:
            print("Invalid entry. Try again.\n")
            return update(username)

    return None



def settings(username : str):
    '''
    Allows the user to edit settings for their account.
    @param username: The username of the user changing settings
    @return: SQL statement for changing certain setting, or None if they want to quit.
    '''
    print("\nSettings: (usage: Type what setting you would like to adjust.)")
    print("1) Edit\n2) Delete\n(Exit)\n")
    req = input()
    req.lower()

    match req:
        case "1":
            return update(username)
        case "2":
            return delete(username)
        case "exit":
            return None
        case _:
            print("Invalid entry. Try again.\n")
            return settings(username)
        

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