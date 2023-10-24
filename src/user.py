


def get():
    print("Enter username")
    username = input()

    return "SELECT * FROM Users WHERE username LIKE '" + username + "'"


def insert():
    print("Enter username")
    username = input()

    print("Enter first name")
    f_name = input()

    print("Enter last name")
    l_name = input()

    print("Enter email")
    email = input()

    print("Enter date of birth (usage: [month] [day] [year])")
    dob = input()


    ### Make it check if username already exists
    return "insert into users(username, name, email, password, dob, create_date) values ('"+username+ "', '"+f_name+" "+l_name+"', '"+email+"', '1one2two:3three4four', '"+dob+"', '10/17/2023');"