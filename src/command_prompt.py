import psycopg2 as psy
import ACCTDETAILS as AD

conn = psy.connect("dbname=127.0.0.1 user="+AD.getUsername() +" password="+AD.getPassword())

