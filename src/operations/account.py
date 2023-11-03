'''
Handles account-related data operations
@Author: Cole Marino
@Author Ben McManus
'''

import type.user as user
import command_prompt as cp


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

def bookRate_parse(username):
    """
    "Houses the bookRate Function for use in the command prompt interface. provides a user prompt for info."
    :return: SQL command
    """

    prompt = input("Please provide the book and its rating (1-5)\n"
                   "Usage: [book], [rating]\n")
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
    

def bookSearch_parse():
    """
    prompts the user for a book search and parses through to pass arguments to bookSearch_cmd
    :return: output of the command
    """
    cmd_input = input("What book are you looking for? (If only title is known, leave other field empty. \n\tOtherwise, enter 'N/A' for specific unknown fields.)\n"
                      "Usage: [book title], [<, > or =][release date (MM/DD/YYYY)], [author], [publisher], [genre]\n")
    (name, r_date, author, publisher, genre) = ["N/A", "N/A", "N/A", "N/A", "N/A"]
    cmd_input = cmd_input.strip().split(", ")
    name = cmd_input[0]
    if(len(cmd_input) > 1):
        r_date = cmd_input[1]
        author = cmd_input[2]
        publisher = cmd_input[3]
        genre = cmd_input[4]

    output = bookSearch_cmd(name, r_date, author, publisher, genre)
    books = cp.execute_sql(output)
    for i in range(0, len(books)):
        print(str(i+1) +") "+books[i][0] + "\n Author: "+ books[i][3]+ "\n Publisher: "+ books[i][4] + "\n Length: "+ str(books[i][1]) + " pages\n Rating: " + str(books[i][2]) + "stars\n")
    return output

def bookSearch_cmd(name, r_date, author, publisher, genre):
    """
    Builds the SQL Command to complete the book search
    :param name: book title to search by
    :param r_date: release data of the book with a prefix <>=
    :param author: author to search by
    :param publisher: publisher to search by
    :param genre: genre to search by
    :return: SQL command as a string
    """

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

    cmd_book = "SELECT b.title, b.length, ROUND(CAST(b.avgrating as numeric), 2), string_agg(DISTINCT(CONCAT(pe.fname,' ', pe.lname)), ', ') AS authors, pu.name AS Publisher, string_agg(DISTINCT(gb.gname), ', ') as genres \n" \
               "FROM (SELECT b1.title, b1.length, b1.bid, b1.pid, b1.releasedate, AVG(br.rating) as avgrating \n" \
               "FROM book b1 \n" \
               "INNER JOIN bookratings br ON b1.bid = br.bid \n" \
               "GROUP BY b1.bid) AS b \n" \
               "INNER JOIN bookratings AS br ON b.bid = br.bid \n" \
               "INNER JOIN authors AS a ON b.bid = a.bid \n" \
               "INNER JOIN genrebook AS gb ON b.bid = gb.bid \n" \
               "INNER JOIN publisher AS pu ON b.pid = pu.pid \n" \
               "INNER JOIN person AS pe ON a.cid = pe.cid \n" \
               "WHERE " + cmd_where + " \n" \
               "GROUP BY b.bid, pu.pid, b.title, b.length, b.avgrating, b.releasedate \n" \
               "ORDER BY b.title ASC, b.releasedate ASC;\n"

    print(cmd_book)

    return cmd_book