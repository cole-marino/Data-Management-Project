import type.user as user
'''
Uses command-line inputs to create SQL commands with different types helpers

@Author Cole Marino
'''

types = ["User", "Book", "Author", "Editor", "Publisher"]


def default_prompt():
    '''
    Asks user that kind of data would they like to get
    @return: the type being searched for
    '''
    print("What type of data would you like to get?")
    count=1
    for type in types:
        print(count, ") ", type)
        count+=1

    type = input()

    # TODO: ADD checks if valid type
    

    type.lower()

    return type

def get():
    '''
    Function to handle if entered GET command
    @return: output from teach types GET command
    '''
    type = default_prompt()

    match type:
        case "user":
            return user.get()
        case "book":
            return -1
        case "author":
            return -1
        case "editor":
            return -1
        case "publisher":
            return -1
        case _:
            print("Invalid input, please try again.")
            get()
    

def insert():
    '''
    Function to handle if entered INSERT command
    @return: output from teach types INSERT command
    '''
    type = default_prompt()

    match type:
        case "user":
            return user.insert()
        case "book":
            return -1
        case "author":
            return -1
        case "editor":
            return -1
        case "publisher":
            return -1
        case _:
            print("Invalid input, please try again.")
            insert()

def delete():
    '''
    Function to handle if entered DELETE command
    @return: output from teach types DELETE command
    '''
    type = default_prompt()

    match type:
        case "user":
            return user.delete()
        case "book":
            return -1
        case "author":
            return -1
        case "editor":
            return -1
        case "publisher":
            return -1
        case _:
            print("Invalid input, please try again.")
            delete()

def update():
    '''
    Function to handle if entered UPDATE command
    @return: output from teach types UPDATE command
    '''
    type = default_prompt()

    match type:
        case "user":
            return user.update()
        case "book":
            return -1
        case "author":
            return -1
        case "editor":
            return -1
        case "publisher":
            return -1
        case _:
            print("Invalid input, please try again.")
            update()