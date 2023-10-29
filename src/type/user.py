'''
Handles GET, INSERT, DELETE, UPDATE functions for users type

@Author: Cole Marino
'''

from datetime import date
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
    today = (str)(date.today())
    today.replace('/', '-')


    ### Make it check if username already exists
    cmd = "INSERT INTO users(username, name, email, password, dob, create_date) VALUES ('"+username+"', '"+(f_name+" "+l_name)+"', '"+email+"', '"+password+"', '"+dob+"', '"+today+"');"
    print(cmd)
    return cmd


def delete(username : str):
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
    

def edit(username : str):
    print("\nAccount Edit Settings:")
    print("1) Change password : password\n2) Change username : username\n3) Change email : email\n")
    entry = input()

    match entry:
        case "password":
            return 
        case "username":
            return 
        case "email":
            return

    return



def settings(username : str):
    print("\nSettings: (usage: Type what setting you would like to adjust.)")
    print("Edit\nDelete\n")
    req = input()
    req.lower()

    match req:
        case "edit":
            return edit(username)
        case "delete":
            return delete(username)