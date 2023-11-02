'''
Handles GET, INSERT, DELETE, UPDATE functions for users type

@Author: Cole Marino
'''

from datetime import date
from datetime import datetime

import operations.account as acct

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
    if(ret != []):
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
    print("\nAccount Edit Settings:")
    print("1) Change password : 'password'\n2) Change username : 'username'\n3) Change email : 'email'\n")
    entry = input()

    match entry:
        case "password":    # Change the password
            print("\nEnter new password: ")
            new_pass = input()
            out = "UPDATE users SET password='" + new_pass + "' WHERE username='" + username + "';"
            return out
        case "username":    # Change the username
            print("\nEnter new username: ")
            new_username = input()
            out = "UPDATE users SET username='" + new_username + "' WHERE username='" + username + "';"
            return out
        case "email":       # Change the email
            print("\nEnter new email: ")
            new_email = input()
            out = "UPDATE users SET email='" + new_email + "' WHERE username='" + username + "';"
            return out

    return None



def settings(username : str):
    '''
    Allows the user to edit settings for their account.
    @param username: The username of the user changing settings
    @return: SQL statement for changing certain setting, or None if they want to quit.
    '''
    print("\nSettings: (usage: Type what setting you would like to adjust.)")
    print("Edit\nDelete\nExit\n")
    req = input()
    req.lower()

    match req:
        case "edit":
            return update(username)
        case "delete":
            return delete(username)
        case "exit":
            return None
        
    