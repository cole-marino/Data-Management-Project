from datetime import date
import operations.account as acct



def get():
    print("Enter username")
    username = input()

    return "SELECT * FROM Users WHERE username LIKE '" + username + "'"

def insert():
    print("Enter username")
    username = input()

    # checks if username exists
    ret = (acct.check_if_exists(username))
    if(ret != []):
        print("\nUsername already exists, please try again.")
        return insert()

    print("\nEnter password")
    password = input()

    print("\nEnter first name")
    f_name = input()

    print("\nEnter last name")
    l_name = input()

    print("\nEnter email")
    email = input()

    print("\nEnter date of birth (usage: [year]-[month]-[day])\n(usage ex: 2001-09-11 [god bless our troops])")
    dob = input()
    
    # gets todays date
    today = (str)(date.today())
    today.replace('/', '-')


    ### Make it check if username already exists
    cmd = "INSERT INTO users(username, name, email, password, dob, create_date) VALUES ('"+username+"', '"+(f_name+" "+l_name)+"', '"+email+"', '"+password+"', '"+dob+"', '"+today+"');"
    print(cmd)
    return cmd