'''
Handles account-related data operations
@Author: Cole Marino
@Author Ben McManus
'''

import src.type.user as user
import src.command_prompt as cp


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

def bookSearch(name, r_date, author, publisher, genre):

    valid_date = "<>="

    cmd_list = []

    # look through each parameter being inputted and

    if name != "N/A" :
        cmd_list.append("title LIKE \"%" + name + "%\"")

    if r_date != "N/A" and r_date[0] in valid_date:
        cmd_list.append("release_date " + r_date[0] + " " + r_date[1:])

    if author != "N/A" :
        if " " in author :
            fname, lname = author.split(" ")
            cmd_list.append("(f_name LIKE \"%" + fname + "%\" AND l_name LIKE \"%" + lname + "%\")")
        else :
            cmd_list.append("(f_name LIKE \"%" + author + "%\" OR l_name LIKE \"%" + author + "%\")")

    if publisher != "N/A" :
        cmd_list.append("name LIKE \"%" + publisher + "%\"")

    if genre != "N/A" :
        cmd_list.append("g_name LIKE \"%" + genre + "%\"")

    i = 0
    cmd_where = ""

    while i < len(cmd_list) - 1 :
        cmd_where += cmd_list[i] + " AND "

    cmd_where += cmd_list[i + 1]

    cmd_book = "SELECT b.title, b.length, b.bid " \
               "FROM book AS b" \
               "INNER JOIN authors AS a ON b.bid = a.bid" \
               "INNER JOIN edits AS e ON b.bid = e.bid" \
               "INNER JOIN publisher AS pu ON b.pid = pu.pid" \
               "INNER JOIN person AS pe ON a.cid = pe.cid OR e.cid = pe.cid" \
               "WHERE" + cmd_where + \
               "ORDER BY title ASC, release_date ASC"


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
    