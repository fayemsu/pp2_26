import csv
import psycopg2
from config import load_config

config = load_config()
conn = psycopg2.connect(**config)

upsertPROC = '''CREATE OR REPLACE PROCEDURE upsert(
    n_name VARCHAR,
    n_surname VARCHAR,
    n_phone VARCHAR
)
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phb WHERE name = n_name) THEN
        UPDATE phb SET surname = n_surname, phone = n_phone
        WHERE name = n_name;
    ELSE
        INSERT INTO phb(name, surname, phone)
        VALUES(n_name, n_surname, n_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;
'''

bulk_insertPROC = '''CREATE OR REPLACE PROCEDURE bulk_insert(
    names VARCHAR[],
    surnames VARCHAR[],
    phones VARCHAR[]
)
AS $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        IF phones[i] ~ '[a-zA-Z_!@#$%^&*()_~]' THEN 
            RAISE NOTICE 'Number %s is invalid.', phones[i];
        ELSIF names[i] ~ '[0-9~!@#$%^&*()_+=-]' THEN
            RAISE NOTICE 'Name %s is invalid.', names[i];
        ELSIF surnames[i] ~ '[0-9~!@#$%^&*()_+=-]' THEN
            RAISE NOTICE 'Surname %s is invalid.', surnames[i];
        ELSE
            CALL upsert(names[i], surnames[i], phones[i]);
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
'''

deletePROC = ''' CREATE OR REPLACE PROCEDURE delete(d_name VARCHAR)
    AS
    $$
    BEGIN
        DELETE FROM phb WHERE name = d_name or surname = d_name or phone = d_name;
    END;
    $$
    LANGUAGE plpgsql;
'''

searchFUNC = '''create or replace function search(pattern varchar)
RETURNS TABLE( id int, name varchar, surname varchar, phone varchar)
AS $$
BEGIN
return query
select p.id, p.name, p.surname, p.phone from phb as p
WHERE p.name ILIKE '%' || pattern || '%'
       OR p.surname ILIKE '%' || pattern || '%'
       OR p.phone ILIKE '%' || pattern || '%'
    ORDER BY id;
end;
$$
LANGUAGE plpgsql;
'''

pagiFUNC = '''create or replace function pagination(lim int, os int)
RETURNS TABLE( id int, name varchar, surname varchar, phone varchar)
AS $$
BEGIN
return query
select p.id, p.name, p.surname, p.phone from phb as p ORDER BY id LIMIT lim OFFSET os;
end;
$$
LANGUAGE plpgsql;
'''


def createTable():
     command = """CREATE TABLE IF NOT EXISTS phb (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                surname VARCHAR(255),
                phone VARCHAR(31)
            )"""

    # conn.cursor() creates a cursor - an object that executes SQL commands
    # "with ... as cur" ensures the cursor is closed automatically when done
     with conn.cursor() as cur:
          cur.execute(command)
          # conn.commit() saves (commits) the changes to the database
          # Without commit, the changes would be lost when the connection closes
          conn.commit()

def execute_query(query):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

execute_query(upsertPROC)
execute_query(bulk_insertPROC)
execute_query(deletePROC)
execute_query(searchFUNC)
execute_query(pagiFUNC)


def pagin():
    lim = int(input("Enter limit: "))
    ofs = int(input("Enter offset: "))

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM pagination(%s, %s)", (lim, ofs))
        rows = cur.fetchall()
    
    print('')
    if rows:
             print(f"{'id':<5}{'name':<12}{'surname':<12}phone")
             for row in rows:
                print(f"{row[0]:<5}{row[1]:<12}{row[2]:<12}{row[3]}")
    else:
        print("No contacts found.")

def searchPattern():
    pattern = input("Enter pattern: ")

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM search(%s)", (pattern,))
        rows = cur.fetchall()

    print('')
    if rows:
             print(f"{'id':<5}{'name':<12}{'surname':<12}phone")
             for row in rows:
                print(f"{row[0]:<5}{row[1]:<12}{row[2]:<12}{row[3]}")
    else:
        print("No contacts found.")

def upsert():
    n_name = input("\nEnter contact name: ")
    n_surname = input("Enter contact surname: ")
    n_phone = input("Enter contact phone number: ")
    command = "CALL upsert(%s, %s, %s)"
    try:
        with conn.cursor() as cur:
            cur.execute(command, (n_name, n_surname, n_phone, ))
            conn.commit()
            print(f"\nUpserted: {n_name} {n_surname}")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def bulkInsert():
    
    num = int(input("Enter the amount of desirable users: "))
    names = []
    surnames = []
    phones = []

    for i in range(num):
        name = input(f'Enter name({i}): ')
        surname = input(f'Enter surname({i}): ')
        phone = input(f'Enter phone({i}): ')
        names.append(name)
        surnames.append(surname)
        phones.append(phone)
    
    command = "CALL bulk_insert(%s, %s, %s)"
    try:
        with conn.cursor() as cur:
            cur.execute(command, (names, surnames, phones))
            conn.commit()
            print(f"\nBulk insert done ({len(names)} entries processed)")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def delete():
    d_name = input("Enter contact's name/surname/phone to delete: ")

    command = "CALL delete(%s)"
    try:
        with conn.cursor() as cur:
            cur.execute(command, (d_name,))
            conn.commit()
            print('\nContact deleted.')
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)




def menu():
     while True:
        print("\nPHONEBOOK MENU")
        print("6 - search contact")
        print("7 - Pagination")
        print("8 - Upsert")
        print("9 - Bulk insert")
        print("10 - Delete")
        print("0 - Exit")

        ch = input("\nEnter choice: ")
        
      
        if ch == "6":
            searchPattern()
        elif ch == "7":
            pagin()
        elif ch == "8":
            upsert()
        elif ch == "9":
            bulkInsert()
        elif ch == "10":
            delete()
        elif ch == "0":
            print('''\n  Bye bye!     
                   
   ######
##      ##
##     ###
 #   #
  #   #
   #   #
    #    #
      #    #####
       ##        ##
         ##      ##
           #####
''')
            break
        else:
            print("INVALID CHOICE.")
        
        print('\n------------------------------------------------------')

createTable()
menu()


conn.close()


