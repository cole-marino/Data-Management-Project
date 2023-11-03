'''
Handles account-related data operations
@Author: Cole Marino
@Author: Ben McManus
@Author: Hunter Boggan (hab1466)
'''

import type.user as user
import command_prompt as cp
from datetime import datetime


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
    today = str(datetime.now())
    today.replace('/', '-')
    
    
    cmd = "INSERT INTO access(username, accesstime) VALUES('"+username+"', '"+today+"')"
    return cmd