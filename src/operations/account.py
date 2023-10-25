import type.user as user
import command_prompt as cp







def signin():
    print("Enter your username:")
    username = input()

    print("Enter your password:")
    password = input()

    cmd = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "';"
    return cmd

def signup():
    return user.insert()


def check_if_exists(username : str):
    cmd = "SELECT * FROM users WHERE username='" + username + "';"
    out = cp.execute_sql(cmd)

    return out