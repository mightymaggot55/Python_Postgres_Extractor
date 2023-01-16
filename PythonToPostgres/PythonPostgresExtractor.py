#library to use to connect to postgres database
import psycopg2
import psycopg2.extras

hostname = 'localhost'
database = 'colourmatchdb'
username = 'postgres'
pwd = 'MRaccess2312!'
portID = '5433'
conn = None
cur = None


def SelectAll(tableName):
    selectAll = 'SELECT * FROM' + tableName
    cur.execute(selectAll)
    

def DropTable(tableName):
    dropTable = 'DROP TABLE ' + tableName
    cur.execute(dropTable)
    

try:
    #connection to database using above credentials
    with psycopg2.connect(
    host = hostname,
    dbname = database,
    user = username,
    password = pwd,
    port = portID
    ) as conn:
        #to perform transactions, you need a cursor, which will handle these operations and data
        #The cursor_factory=psycopg2.extras.DictCursor means that data returned will be pur into a dictornary
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            dropScript = ('DROP TABLE IF EXISTS employee')
            cur.execute(dropScript)

            #Create table script
            createScript = ''' CREATE TABLE IF NOT EXISTS employee (
                                    id      int PRIMARY KEY,
                                    name    varchar(40) NOT NULL,
                                    salary  int,
                                    dept_id varchar(30)
                                    )'''
            #execute the create table script
            cur.execute(createScript)

            #Script to insert into Postgres DB
            #Never put the actual data within the insert script. Use placeholders to avoid SQL Injection
            insertScript = 'INSERT INTO employee (id, name, salary, dept_id) VALUES (%s, %s, %s, %s)'
            
            #how to insert a single value into Postgres DB
            insertOneValue = (1, 'james', 12000, 'IT')
            cur.execute(insertScript, insertOneValue)

            #for multiple values, needs to be contained within '[]' and use a for loop to loop through the data
            insertMultiValue = [(2, 'Robin', 15000, 'Sales'), (3, 'Bob', 18000, 'QC'), (4, 'Bill', 28000, 'Purchasing')]
            for record in insertMultiValue:
                cur.execute(insertScript, record)

            #Just a example of type of scripts that can be run
            updateScript = 'UPDATE employee SET salary = salary + (salary * 0.8)'
            cur.execute(updateScript)

            #delete script - again important to state variables in a seperate variable. Use placeholder instead of hard coding in values
            deleteScript = 'DELETE FROM employee WHERE name = %s'
            deleteRecord = ('james',)
            cur.execute(deleteScript, deleteRecord)

            #view all data within a table in python
            cur.execute('SELECT * FROM employee')
            for record in cur.fetchall():
                print(record['name'], record['salary'])


            #tells database to save any transactions we have done
            conn.commit()
            #After use, close cursor and close connection to database
            #Using the cur.close() not needed when using a with statement at the top            
            #cur.close()    
            conn.close()
            
except Exception as error:
    print(error)

finally:
    #Using the WITH statement on the cursor, we don't need to handle the cursor close() as it is done after it has executed.
    '''if cur is not None:
        cur.close()'''
    if conn is not None:
        conn.close()

