import psycopg2 as psy
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
            if isinstance(sql, str):
                curs.execute(sql)
            elif isinstance(sql, list):
                for cmd in sql:
                    curs.execute(cmd)
            else:
                print("ERROR: SQL Command invalid type. \nusecase: str, list")
                conn.close()
                return -1
            
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
    except:
        print("FATAL ERROR: DataBase Connection Failed!")
        return -1



def main():
    print("Welcome to BookHub!")


    # read from stdin
    while(True):
        command = input()
        print("Running command....")
        result = execute_sql(command)

        if isinstance(result, str):
            print(result)


if __name__ == "__main__":
    main()

#conn = psy.connect(connect)
