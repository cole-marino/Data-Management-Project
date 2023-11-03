'''
This handles book related functions such as grabbing book lists and such.

@Author: Tomasz Mazur
@Author: Cole Marino (cvm4043)
@Author: Hunter Boggan (hab1466)
'''
import type.user as user
import command_prompt as cp
from datetime import date
from datetime import datetime

def view_User_List(username, listName):
    '''
    
    '''
    command = "SELECT b.title AS book_name, \
       CONCAT(p.f_name, ' ', p.l_name) AS author, \
       br.start_date, \
       br.end_date, \
       br.pages_read \
    FROM bookreads br \
    JOIN book b ON br.bid = b.bid \
    JOIN authors a ON b.bid = a.bid \
    JOIN person p ON a.cid = p.cid \
    JOIN bookslist bl ON br.bid = bl.bid \
    JOIN users u ON bl.username = u.username \
    WHERE u.username = 'your_username' \
    AND bl.list_name = 'your_list_name';"
    
    result = cp.execute_sql(command)
    #print(result)


def get_User_Lists(username, listOnly):
    '''
    Gets all the lists which a user has.
    @param username: Users username.
    @param listOnly: boolean to display user lists or not
    @return (listsonly true): string of command to select lists
    @return (listsonly false): None
    '''
    command = "SELECT bl.username AS list_owner,\
            bl.listname,\
            COUNT(bl.bid) AS number_of_books, \
            SUM(b.length) AS total_length \
            FROM bookslist bl  \
            JOIN book b ON bl.bid = b.bid \
            WHERE bl.username = '"+username+"' \
            GROUP BY bl.username, bl.listname  \
            ORDER BY listname ASC, list_owner;" 
            
    #If List only true, returns command for other fucntion to access lists
    if listOnly:
        return result
    
    #options to view lists otherwise       
    result = cp.execute_sql(command)
    
    for i in range(0, len(result)):
        print(str(i) +") "+ result[0][1] + ", Number of Books: " + str(result[0][2]) + ", Total Pages: " + str(result[0][2]))
        
    listNum = input("Enter list number to view list, hit enter to return to menu")
    if isinstance(list, int):
        view_User_List(username, result[listNum][1])
        
    return None


def book_Search_parse():
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

    output = book_Search_cmd(name, r_date, author, publisher, genre)
    books = cp.execute_sql(output)
    for i in range(0, len(books)):
        print(str(i+1) +") "+books[i][0] + "\n Author: "+ books[i][3]+ "\n Publisher: "+ books[i][4] + "\n Length: "+ str(books[i][1]) + " pages\n Rating: " + str(books[i][2]) + "stars\n")
    return output


def book_Search_cmd(name, r_date, author, publisher, genre):
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

    #print(cmd_book)

    return cmd_book


def book_Rate_parse(username):
    """
    "Houses the bookRate Function for use in the command prompt interface. provides a user prompt for info."
    :return: SQL command
    """

    prompt = input("Please provide the book and its rating (1-5)\n"
                   "Usage: [book], [rating]\n")
    cmd_input = prompt.strip().split(", ")
    out = book_Rate(cmd_input[0], cmd_input[1], username)
    return out


def book_Rate(book, rating, username):
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


def book_Read_Parse(username):
    '''
    Parses the input for recording a reading session for a user and calls the command function
    @param username: The username of the user recording a reading session
    @return: SQL command to be executed
    '''
    
    prompt = input("Please provide the title of the book and the starting and ending pages of your session\n"
                   "Usage: [book title], [start time], [end time], [starting page], [ending page]\n"
                   "Start time and End Time should be entered in a MM DD YYYY  HH:MM(AM/PM) format\n")
    cmd_input = prompt.strip().split(", ")
    out = book_Read(username, cmd_input[0], cmd_input[1], cmd_input[2], cmd_input[3], cmd_input[4])
    return out
    
    

def book_Read(username, book, starttime, endtime, startpage, endpage):
    '''
    Records a reading session for a user and returns the necessary command
    @param username: The username of the user recording a reading session
    @param book: The title of the book the user read
    @param starttime: The time the user started reading
    @param endtime: The time the user stopped reading
    @param startpage: The page the user started on
    @param endpage: The page the user ended on
    @return: SQL command to be executed
    '''
    
    cmd = "SELECT bid FROM book WHERE title = '"+book+"'"
    res = cp.execute_sql(cmd)
    res_str = str(res[0][0])
    
    pages = int(endpage) - int(startpage)
    pages_str = str(pages)
    
    start = datetime.strptime(starttime, '%b %d %Y %I:%M%p')
    start_str = str(start)

    end = datetime.strptime(endtime, '%b %d %Y %I:%M%p')
    end_str = str(end)
    
    read_cmd = "INSERT INTO bookreads(bid, username, startdate, enddate, pagesread) VALUES ('"+res_str+"', '"+username+"', '"+start_str+"', '"+end_str+"', '"+pages_str+"')"
    
    return read_cmd