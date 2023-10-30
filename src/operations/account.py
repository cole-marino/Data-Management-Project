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
        cmd_list.append("b.title LIKE \'%" + name + "%\'")

    if r_date != "N/A" and r_date[0] in valid_date:
        cmd_list.append("b.releasedate " + r_date[0] + " \'" + r_date[1:] + "\'")

    if author != "N/A" :
        if " " in author :
            fname, lname = author.split(" ")
            cmd_list.append("(pe.fname LIKE \'%" + fname + "%\' AND pe.lname LIKE \'%" + lname + "%\')")
        else :
            cmd_list.append("(pe.fname LIKE \'%" + author + "%\' OR pe.lname LIKE \'%" + author + "%\')")

    if publisher != "N/A" :
        cmd_list.append("pu.name LIKE \'%" + publisher + "%\'")

    if genre != "N/A" :
        cmd_list.append("gb.gname LIKE \'%" + genre + "%\'")

    i = 0
    cmd_where = ""

    while i < len(cmd_list) - 1 :
        cmd_where += cmd_list[i] + " AND "
        i += 1

    cmd_where += cmd_list[i]

    cmd_book = "SELECT b.title, b.length, b.avgrating, pe.fname, pe.lname, pu.name, gb.gname " \
               "FROM (SELECT b1.title, b1.length, b1.bid, b1.pid, b1.releasedate, AVG(br.rating) as avgrating " \
               "FROM book b1 " \
               "INNER JOIN bookratings br ON b1.bid = br.bid " \
               "GROUP BY b1.bid) AS b " \
               "INNER JOIN bookratings AS br ON b.bid = br.bid " \
               "INNER JOIN authors AS a ON b.bid = a.bid " \
               "INNER JOIN genrebook AS gb ON b.bid = gb.bid " \
               "INNER JOIN publisher AS pu ON b.pid = pu.pid " \
               "INNER JOIN person AS pe ON a.cid = pe.cid OR e.cid = pe.cid " \
               "WHERE " + cmd_where + " " \
               "ORDER BY title ASC, releasedate ASC "

    print(cmd_book)

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
    