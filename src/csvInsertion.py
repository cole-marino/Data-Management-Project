'''
File created to insert data in bulk into the data base. PLEASE READ WARNING IN MAIN FUNCTION

@Author: Ben McManus (bdm3509)
'''
import csv
import psycopg2 as psy
from sshtunnel import SSHTunnelForwarder

import command_handler as ch
import operations.account as acct

# This is not contained in github because it holds personal account info.
# Contains a getUsername() function and getPassword() function which returns the coders username and password
##  MAKE YOUR OWN, OTHER BOOKHUB DEVS ##
import ACCTDETAILS as AD 

def execute_sql(sql):
    '''
    Executes given sql commands using an SSH tunnel to connect to the database.
    @pre: Param 'sql' must be a string or a list of strings, where the list can contain multiple commands

    @param sql: sql commands given by the user, translated from simpler text to SQL.

    @return -1: Error with accessing database or executing SQL commands.
    @return 1: Success executing SQL commands.
    @return (str): Success/Error given by database server if execution succeeded.

    @Author: Cole Marino
    '''
    try:
        with SSHTunnelForwarder(
                    ('starbug.cs.rit.edu', 22),
                    ssh_username=AD.getUsername(),
                    ssh_password=AD.getPassword(),
                    remote_bind_address=('127.0.0.1', 5432)
                    #local_bind_address=('127.0.0.1', 22)
                    ) as server:
            server.start()
            print("SSH tunnel connected!")

            # params for connect
            params = {
            'dbname':'p320_08',
            'user':AD.getUsername(),
            'password':AD.getPassword(),
            'host':'127.0.0.1',
            'port':server.local_bind_port
            }

            # connects to server and creates cursor
            conn = psy.connect(**params)
            curs = conn.cursor()

            print("DataBase connected!")

            # executes command
            try:
                if isinstance(sql, str):
                    curs.execute(sql)
                elif isinstance(sql, list):
                    for cmd in sql:
                        curs.execute(cmd)
                else:
                    print("ERROR: SQL Command invalid type. \nusecase: str, list")
                    conn.close()
                    return -1
            except Exception as e: print(e)
            
            # checks if it worked
            try:
                result = curs.fetchall()
            except psy.ProgrammingError:
                result = 1
            
            # commits SQL statement
            conn.commit()
            conn.close()
            print("SQL Statement was successfully executed!")
            return result
    except Exception as e: print(e)
    
    
    
def insertUsers():
    file = open('src/samples/user.csv', 'r')
    for x in file:
        strip = x.strip('\n')
        data = strip.split(',')
        name = data[1].split(' ')
        cmd = "INSERT INTO users(username, name, email, password, dob, create_date) VALUES ('"+data[0]+"', '"+(name[0]+" "+name[1])+"', '"+data[2]+"', '"+data[3]+"', '"+data[4]+"', '"+data[5]+"');"
        execute_sql(cmd)
        
def insertBooks():
    file = open('src/samples/book.csv')
    for x in file:
        strip = x.strip('\n')
        data = strip.split(',')
        cmd = "INSERT INTO book(bid, title, releasedate, length, pid) VALUES ('"+data[0]+"', '"+data[1]+"', '"+data[2]+"', '"+data[3]+"', '"+data[4]+"')"
        execute_sql(cmd)
        
def insertPublishers():
    file = open('src/samples/publisher.csv')
    for x in file:
        strip = x.strip('\n')
        data = strip.split(',')
        cmd = "INSERT INTO publisher(pid, name) VALUES('"+data[0]+"', '"+data[1]+"')"
        execute_sql(cmd)
        
def insertPersons():
    file = open('src/samples/person.csv')
    for x in file:
        strip = x.strip('\n')
        data = strip.split(',')
        cmd = "INSERT INTO person(cid, f_name, l_name) VALUES('"+data[0]+"', '"+data[1]+"', '"+data[2]+"')"
        execute_sql(cmd)
        
def insertGenre():
    file = open('src/samples/genre.csv')
    for x in file:
        strip = x.strip('\n')
        cmd = "INSERT INTO genre(g_name) VALUES('"+strip+"')"
        execute_sql(cmd)
        
def insertBookGenre():
    file = open('src/samples/genre_book.csv')
    for x in file:
        strip = x.strip('\n')
        data = strip.split(',')
        cmd = "INSERT INTO genrebook(bid, g_name) VALUES('"+data[0]+"', '"+data[1]+"')"
        execute_sql(cmd)
        
def insertEdits():
    file = open('src/samples/edits.csv')
    for x in file:
        strip = x.strip('\n')
        data = strip.split(',')
        cmd = "INSERT INTO edits(bid, cid) VALUES('"+data[0]+"', '"+data[1]+"')"
        execute_sql(cmd)
        
def insertAudience():
    file = open('src/samples/audience.csv')
    for x in file:
        strip = x.strip('\n')
        data = strip.split(',')
        cmd = "INSERT INTO audience(audience_name, min_age, max_age) VALUES('"+data[0]+"', '"+data[1]+"', '"+data[2]+"')"
        execute_sql(cmd)
        
def insertAudienceBook():
    file = open('src/samples/audience_book.csv')
    for x in file:
        strip = x.strip('\n')
        data = strip.split(',')
        cmd = "INSERT INTO audiencebook(bid, audience_name) VALUES('"+data[0]+"', '"+data[1]+"')"
        execute_sql(cmd)
        
def insertBookReads():
    file = open('src/samples/book_reads.csv')
    for x in file:
        strip = x.strip('\n')
        data = strip.split(',')
        cmd = "INSERT INTO bookreads(bid, username, start_date, end_date, pages_read) VALUES('"+data[0]+"', '"+data[1]+"', '"+data[2]+"', '"+data[3]+"', '"+data[4]+"')"
        execute_sql(cmd)
        
def insertBookList():
    file = open('src/samples/books_list.csv')
    for x in file:
        strip = x.strip('\n')
        data = strip.split(',')
        cmd = "INSERT INTO bookslist(bid, username, list_name) VALUES('"+data[0]+"', '"+data[1]+"', '"+data[2]+"')"
        execute_sql(cmd)
        
def insertFollowers():
    file = open('src/samples/followers.csv')
    for x in file:
        strip = x.strip('\n')
        data = strip.split(',')
        cmd = "INSERT INTO followings(follower_username, following_username) VALUES('"+data[0]+"', '"+data[1]+"')"
        execute_sql(cmd)
        
def insertBookRatings():
    file = open('src/samples/book_ratings.csv')
    for x in file:
        strip = x.strip('\n')
        data = strip.split(',')
        cmd = "INSERT INTO bookratings(bid, username, rating) VALUES('"+data[0]+"', '"+data[1]+"', '"+data[2]+"')"
        execute_sql(cmd)
        
    
    
def main():
    '''
    WARNING: VERIFY DATA IN COMMANDS ARE CORRECTLY PLACED AND YOUR READING
    THE CORRECT FILE. INSERTING BULK DATA INCORRECTLY [[WILL]] BE A PAIN IN THE 
    ASS
    1: CHECK YOUR READING THE CORRECT FILE
    2: CONFIRM THE COMMANDS ARE CORRECT BY PRINTING THEM
    3: MAKE SURE YOUR RUNNING THE RIGHT FUNCTION
    '''
    cmd = "SELECT following_username FROM followings WHERE follower_username = 'jane_smith'"
    output = execute_sql(cmd)
    for i in range(0, len(output)):
        print(str(i) +") "+ output[i][0])
    
if __name__ == "__main__":
    main()