'''
Handles account-related data operations
@Author: Cole Marino
'''

import type.user as user
import command_prompt as cp




def signin():
    '''
    Sign in function for a user
        Gets username and password, checks if they are correct, and gets user data

    @return [correct info]: list of user table data
    @return [incorrect info/no user]: empty list
    '''
    print("Enter your username:")
    username = input()

    print("Enter your password:")
    password = input()

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