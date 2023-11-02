import type.user as user
import command_prompt as cp

def viewUserList(username, listName):
    command = "SELECT b.title AS book_name, \
       CONCAT(p.f_name, ' ', p.l_name) AS author, \
       br.start_date, \
       br.end_date, \
       br.pages_read \
    FROM bookreads br \
    JOIN book b ON br.bid = b.bid \
    JOIN authors a ON b.bid = a.bid \
    JOIN person p ON a.cid = p.cid \
    JOIN bookslist bl ON br.bid = bl.bid \
    JOIN users u ON bl.username = u.username \
    WHERE u.username = 'your_username' \
    AND bl.list_name = 'your_list_name';"
    
    result = cp.execute_sql(command)
    print(result)


def getUserLists(username, listOnly):
    command = "SELECT bl.username AS list_owner,\
            bl.listname,\
            COUNT(bl.bid) AS number_of_books, \
            SUM(b.length) AS total_length \
            FROM bookslist bl  \
            JOIN book b ON bl.bid = b.bid \
            WHERE bl.username = '"+username+"' \
            GROUP BY bl.username, bl.listname  \
            ORDER BY listname ASC, list_owner;" 
            
    #If List only true, returns command for other fucntion to access lists
    if listOnly:
        return result
    
    #options to view lists otherwise       
    result = cp.execute_sql(command)
    
    for i in range(0, len(result)):
        print(str(i) +") "+ result[0][1] + ", Number of Books: " + str(result[0][2]) + ", Total Pages: " + str(result[0][2]))
        
    listNum = input("Enter list number to view list, hit enter to return to menu")
    if isinstance(list, int):
        viewUserList(username, result[listNum][1])
        
    return None