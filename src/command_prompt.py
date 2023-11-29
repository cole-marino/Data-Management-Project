'''
This is the main file to run the command-line program.
    Connection to database and execution of SQL commands occurs here.

@Author: Cole Marino (cvm4043)
'''

import sys
import psycopg2 as psy
from sshtunnel import SSHTunnelForwarder

import operations.account as acct
import operations.book as bk
import type.user as user
import type.user_acct as user_acct

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
    @Author: Ben McManus
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
            #print("SSH tunnel connected!")

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

            #print("DataBase connected!")

            # executes command
            try:
                if isinstance(sql, str):
                    curs.execute(sql)
                elif isinstance(sql, list):
                    for cmd in sql:
                        curs.execute(cmd)
                else:
                    print("ERROR: SQL Command invalid type. \nusecase: str, list")
                    print(sql)
                    conn.close()
                    return -1
            except Exception as e:
                print("ERROR: SQL Command invalid.")
                print(e)
                return -1
            
            # checks if it worked
            try:
                result = curs.fetchall()
            except psy.ProgrammingError:
                result = 1
            
            # commits SQL statement
            conn.commit()
            conn.close()
            #print("SQL Statement was successfully executed!")
            return result
    except Exception as e: print(e)

def main():
    print("Welcome to BookHub!")
    username = ''
    # sign in page
    while(True):
        print("Would you like to sign in or sign up? (signin/signup)")
        entry = input()
        if(entry == 'signin'):
            print("Enter your username:")
            username = input()
            print("Enter your password:")
            password = input()
            res = execute_sql(acct.signin(username, password))
            if(res == []):
                print("\nERROR with entry, please try again and make sure formatting is valid.")
                continue
            execute_sql(acct.record_access(username))
            break
        elif(entry == 'signup'):
            cmd = acct.signup()
            res = execute_sql(cmd)
            if(res == []):
                print("\nERROR with entry, please try again and make sure formatting is valid.")
                continue
            break
        else:
            print("Invalid entry, try again.")

    print() # Creates spacing

    # read from stdin
    while(True):

        print("\nMain Menu, choose action with corresponding number \
              \n1) Account Settings\
              \n2) Follow user\
              \n3) Unfollow user\
              \n4) View followings\
              \n5) Search books\
              \n6) Rate a book\
              \n7) View top 10 books\
              \n8) View your book lists\
              \n9) Create a book list\
              \n10) Delete a book list\
              \n11) Edit a book list\
              \n12) Add a book to a book list\
              \n13) Delete a book from a book list\
              \n14) Record a reading session\
              \n15) View top 5 books of the month\
              \n16) View top 20 books among followers\
              \n17) View your reccomended books\
              \n(exit)")
              
        exe = input()
        exe.lower()

        command = None

        match exe:
            case "1": 
                command = user.settings(username) 
            case "2":
                command = user_acct.follow_user(username)
                if(command == -1):
                    continue
            case "3":
                command = user_acct.unfollow_user(username)
            case "4":
                ignore = user_acct.get_followings(username)
            case "5":
                command = bk.book_Search_parse()
            case "6":
                command = bk.book_rate_parse(username)
            case "7":
                ignore = user_acct.get_top_books(username)
            case "8":
                ignore = user_acct.get_user_lists(username)
            case "9":
                command = user_acct.create_user_list(username)
            case "10":
                command = user_acct.delete_user_list(username)
            case "11":
                command = user_acct.edit_user_list(username)
            case "12":
                command = user_acct.add_to_list(username)
            case "13":
                command = user_acct.delete_from_list(username)
            case "14":
                command = bk.book_Read_Parse(username)
            case "15":
                command = user_acct.get_top_five_new_books_of_month()
            case "16":
                command = user_acct.get_top_books_followers(username)
            case "17":
                command = user_acct.get_book_reccomendations(username)
            case "exit":
                sys.exit()
            case _:
                print("Invalid entry, please try again.")
                continue
            
            

        if command != None:
            print("\nRunning command....")
            result = execute_sql(command)
            print(result)

        # if isinstance(result, str):
        #     print(result)


if __name__ == "__main__":
    main()

#conn = psy.connect(connect)
