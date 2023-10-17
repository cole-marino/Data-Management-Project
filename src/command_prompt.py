import psycopg2 as psy
import os
from sshtunnel import SSHTunnelForwarder

import ACCTDETAILS as AD

def execute_sql(sql):
    try:
        with SSHTunnelForwarder(
                    ('starbug.cs.rit.edu', 22),
                    ssh_username=AD.getUsername(),
                    ssh_password=AD.getPassword(),
                    remote_bind_address=('127.0.0.1', 5432)
                    #local_bind_address=('127.0.0.1', 22)
                    ) as server:
            server.start()
            
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

            if isinstance(sql, str):
                curs.execute(sql)
            elif isinstance(sql, list):
                for cmd in sql:
                    curs.execute(cmd)
            else:
                print("ERROR: SQL Command invalid type. \nusecase: str, list")
                return -1

    except:
        print("FATAL ERROR: DataBase Connection Failed!")
        return -1



def main():
    print("Welcome to BookHub!")


    # read from stdin
    while(True):
        command = input()
        print("Running command....")
        out_code = execute_sql(command)


if __name__ == "__main__":
    main()

#conn = psy.connect(connect)
