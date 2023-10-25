import types.user as user

'''
Uses command-line inputs to create SQL commands with different types helpers

@Author Cole Marino
'''

types = ["User", "Book", "Author", "Editor", "Publisher"]


def default_prompt():
    print("What type of data would you like to get?")
    count=1
    for type in types:
        print(count, ") ", type)
        count+=1

    type = input()
    type.lower()

    return type

def get():
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