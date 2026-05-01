import csv
import json
import psycopg2
from config import load_config

config = load_config()
conn = psycopg2.connect(**config)


create_tables = """
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    surname VARCHAR(255),
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id)
);

CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('home','work','mobile'))
);
"""


add_phonePROC = """
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
AS $$
DECLARE cid INT;
BEGIN
    SELECT id INTO cid FROM contacts WHERE name = p_contact_name LIMIT 1;

    IF cid IS NULL THEN
        RAISE NOTICE 'Contact not found.';
    ELSE
        INSERT INTO phones(contact_id, phone, type)
        VALUES (cid, p_phone, p_type);
    END IF;
END;
$$ LANGUAGE plpgsql;
"""

move_groupPROC = """
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
AS $$
DECLARE gid INT;
DECLARE cid INT;
BEGIN
    SELECT id INTO gid FROM groups WHERE name = p_group_name;

    IF gid IS NULL THEN
        INSERT INTO groups(name) VALUES(p_group_name) RETURNING id INTO gid;
    END IF;

    SELECT id INTO cid FROM contacts WHERE name = p_contact_name LIMIT 1;

    IF cid IS NULL THEN
        RAISE NOTICE 'Contact not found.';
    ELSE
        UPDATE contacts SET group_id = gid WHERE id = cid;
    END IF;
END;
$$ LANGUAGE plpgsql;
"""

searchFUNC = """
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id INT,
    name VARCHAR,
    surname VARCHAR,
    email VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
RETURN QUERY
SELECT c.id, c.name, c.surname, c.email, p.phone
FROM contacts c
LEFT JOIN phones p ON c.id = p.contact_id
WHERE c.name ILIKE '%' || p_query || '%'
   OR c.surname ILIKE '%' || p_query || '%'
   OR c.email ILIKE '%' || p_query || '%'
   OR p.phone ILIKE '%' || p_query || '%'
ORDER BY c.id;
END;
$$ LANGUAGE plpgsql;
"""


def execute_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()

def init_db():
    execute_query(create_tables)
    execute_query(add_phonePROC)
    execute_query(move_groupPROC)
    execute_query(searchFUNC)



def add_contact():
    name = input("Name: ")
    surname = input("Surname: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")

    with conn.cursor() as cur:
        cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
        res = cur.fetchone()

        if res:
            gid = res[0]
        else:
            cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id", (group,))
            gid = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO contacts(name, surname, email, birthday, group_id)
            VALUES (%s,%s,%s,%s,%s)
        """, (name, surname, email, birthday, gid))

        conn.commit()

    print("Contact added.")

def add_phone():
    name = input("Contact name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    with conn.cursor() as cur:
        cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, ptype))
        conn.commit()

def move_group():
    name = input("Contact name: ")
    group = input("New group: ")

    with conn.cursor() as cur:
        cur.execute("CALL move_to_group(%s,%s)", (name, group))
        conn.commit()



def search():
    q = input("Search: ")

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM search_contacts(%s)", (q,))
        rows = cur.fetchall()

    print("")
    for r in rows:
        print(r)




def filter_group():
    group = input("Group: ")

    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.name, c.surname, c.email
            FROM contacts c
            JOIN groups g ON c.group_id = g.id
            WHERE g.name = %s
        """, (group,))
        rows = cur.fetchall()

    print("")
    for r in rows:
        print(r)

def search_email():
    q = input("Email search: ")

    with conn.cursor() as cur:
        cur.execute("""
            SELECT name, surname, email
            FROM contacts
            WHERE email ILIKE %s
        """, ('%' + q + '%',))
        rows = cur.fetchall()

    print("")
    for r in rows:
        print(r)



def sort_contacts():
    print("Sort by: name / birthday")
    choice = input("> ")

    query = "SELECT name, surname, birthday FROM contacts ORDER BY " + choice

    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()

    print("")
    for r in rows:
        print(r)




def paginate():
    limit = 3
    offset = 0

    while True:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT name, surname FROM contacts
                ORDER BY id LIMIT %s OFFSET %s
            """, (limit, offset))
            rows = cur.fetchall()

        print("\nPage:")
        for r in rows:
            print(r)

        cmd = input("next(n) / prev(p) / quit(q): ")

        if cmd == "n":
            offset += limit
        elif cmd == "p":
            offset = max(0, offset - limit)
        else:
            break

def import_csv():
    filename = 'cont1.csv'

    with open(filename, newline='') as f:
        reader = csv.DictReader(f)

        with conn.cursor() as cur:
            for row in reader:
                name = row['name']
                surname = row['surname']
                email = row['email']
                birthday = row['birthday']
                group = row['group']
                phone = row['phone']
                ptype = row['type']

                cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
                exists = cur.fetchone()

                if exists:
                    choice = input(f"{name} exists. skip/overwrite: ")

                    if choice == "skip":
                        continue
                    else:
                        cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

                cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
                g = cur.fetchone()

                if g:
                    gid = g[0]
                else:
                    cur.execute(
                        "INSERT INTO groups(name) VALUES(%s) RETURNING id",
                        (group,)
                    )
                    gid = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO contacts(name, surname, email, birthday, group_id)
                    VALUES (%s,%s,%s,%s,%s)
                    RETURNING id
                """, (name, surname, email, birthday, gid))

                cid = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s,%s,%s)
                """, (cid, phone, ptype))

            conn.commit()

    print("\nCSV import completed.")

def export_json():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.name, c.surname, c.email, c.birthday, g.name, p.phone, p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
        """)
        rows = cur.fetchall()

    with open("exp_contacts.json", "w") as f:
        json.dump(rows, f, default=str, indent=4)

    print("Exported.")

def import_json():

    with open("imp_contacts.json", "r") as f:
        data = json.load(f)

    with conn.cursor() as cur:
        for row in data:
            name = row[0]
            surname = row[1]
            email = row[2]
            birthday = row[3]
            group = row[4]
            phone = row[5]
            ptype = row[6]

    
            cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
            exists = cur.fetchone()

            if exists:
                choice = input(f"{name} exists. skip/overwrite: ")
                if choice == "skip":
                    continue
                else:
                    cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

            
            cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
            g = cur.fetchone()

            if g:
                gid = g[0]
            else:
                cur.execute(
                    "INSERT INTO groups(name) VALUES(%s) RETURNING id",
                    (group,)
                )
                gid = cur.fetchone()[0]

        
            cur.execute("""
                INSERT INTO contacts(name, surname, email, birthday, group_id)
                VALUES (%s,%s,%s,%s,%s)
                RETURNING id
            """, (name, surname, email, birthday, gid))

            cid = cur.fetchone()[0]

            
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s,%s,%s)
            """, (cid, phone, ptype))

        conn.commit()

    print("\nJSON import completed.")


def menu():
    while True:
        print("\nMENU")
        print("1 - Add contact")
        print("2 - Add phone")
        print("3 - Move group")
        print("4 - Search")
        print("5 - Filter group")
        print("6 - Email search")
        print("7 - Sort")
        print("8 - Pagination")
        print("9 - Export JSON")
        print("10 - Import JSON")
        print("11 - Import CSV")
        print("q - Exit")

        ch = input("\n> ")

        if ch == "1":
            add_contact()
        elif ch == "2":
            add_phone()
        elif ch == "3":
            move_group()
        elif ch == "4":
            search()
        elif ch == "5":
            filter_group()
        elif ch == "6":
            search_email()
        elif ch == "7":
            sort_contacts()
        elif ch == "8":
            paginate()
        elif ch == "9":
            export_json()
        elif ch == "10":
            import_json()
        elif ch == "11":
            import_csv()
        elif ch == "q":
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

init_db()
menu()
conn.close()