'''
This handles book related functions such as grabbing book lists and such.

@Author: Tomasz Mazur
@Author: Cole Marino (cvm4043)
'''
import type.user as user
import command_prompt as cp
import pandas as pd

from datetime import datetime


def book_Search_parse():
    """
    prompts the user for a book search and parses through to pass arguments to bookSearch_cmd
    :return: output of the command
    """
    SORT_TYPES = ["b.title", "Publisher", "genres", "b.releasedate"]
    SORT_KINDS = ["ASC", "DESC"]
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
    books_df = pd.DataFrame(books,
                            columns=["Title", "Length (pages)", "Average Rating", "Authors", "Publisher", "Genres"])
    print(books_df.to_string())

    sort_cmd = output[0:-41]  # -41 is where the sort by commmand is

    exit_prompt = False
    while (exit_prompt == False):

        # taking user input
        sort_num = input("sort by: 1)title 2)publisher 3)genre 4)release date\n")

        sort_att = SORT_TYPES[int(sort_num) - 1]
        sort_t_num = input("sort by: 1)ascending 2)descending\n")
        sort_t = SORT_KINDS[int(sort_t_num) - 1]

        # get the book search command with everything but the sort


        # create the sort line
        sort_sec = "ORDER BY " + sort_att + " " + sort_t + ";"

        books = cp.execute_sql(sort_cmd + sort_sec)
        books_df = pd.DataFrame(books,
                                columns=["Title", "Length (pages)", "Average Rating", "Authors", "Publisher", "Genres"])
        print(books_df.to_string())
        exit_prompt = ("yes" == input("return to main menu?(yes/no)\n"))

    # deprecated
    # for i in range(0, len(books)):
    #     print(str(i+1) +") "+books[i][0] + "\n Author: "+ books[i][3]+ "\n Publisher: "+ books[i][4] + "\n Length: "+ str(books[i][1]) + " pages\n Rating: " + str(books[i][2]) + "stars\n")
    # return output

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


def book_rate_parse(username):
    """
    "Houses the bookRate Function for use in the command prompt interface. provides a user prompt for info."
    :return: SQL command
    """

    prompt = input("Please provide the book and its rating (1-5)\n"
                   "Usage: [book], [rating]\n")
    cmd_input = prompt.strip().split(", ")
    out = book_rate(cmd_input[0], cmd_input[1], username)
    return out


def book_rate(book, rating, username):
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