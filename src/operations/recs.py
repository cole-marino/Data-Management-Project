'''
    recs.py handles the various recommendation operations for books.
    
    @Author: Hunter Boggan (hab1466)
'''

import command_prompt as cp
import operations.book as book
import pandas as pd

def get_top_5_month():
    
    # Steps for getting top 5:
    # 1. Find all books released in the past month
    # 2. Find count of each of those books in bookreads
    # 3. Choose top 5 of the count sorted in descending order
    
    command = ""
    
    result = cp.execute_sql(command)
    return 0