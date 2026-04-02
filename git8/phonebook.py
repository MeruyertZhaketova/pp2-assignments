from connect import connect
import csv

# creating table
def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20)
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


#input
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


    # import from csv
def insert_from_csv(file_path):
    conn = connect()
    cur = conn.cursor()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (row['name'], row['phone']))
    conn.commit()
    cur.close()
    conn.close()
    print("CSV imported!")

#export to csv
def export_to_csv(file_path):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name, phone FROM contacts")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'name', 'phone'])
        for row in rows:
            writer.writerow(row)
    print(f"Data exported to {file_path} successfully!")


# contacts upd
def update_contact(contact_id, new_name=None, new_phone=None):
    conn = connect()
    cur = conn.cursor()
    if new_name:
        cur.execute("UPDATE contacts SET name=%s WHERE id=%s", (new_name, contact_id))
    if new_phone:
        cur.execute("UPDATE contacts SET phone=%s WHERE id=%s", (new_phone, contact_id))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated!")


# 5search cont
def search_contacts(name=None, phone_prefix=None):
    conn = connect()
    cur = conn.cursor()
    query = "SELECT * FROM contacts WHERE TRUE"
    params = []
    if name:
        query += " AND name ILIKE %s"
        params.append(f"%{name}%")
    if phone_prefix:
        query += " AND phone LIKE %s"
        params.append(f"{phone_prefix}%")
    cur.execute(query, params)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


# del cont
def delete_contact(contact_id=None, phone=None):
    conn = connect()
    cur = conn.cursor()
    if contact_id:
        cur.execute("DELETE FROM contacts WHERE id=%s", (contact_id,))
    elif phone:
        cur.execute("DELETE FROM contacts WHERE phone=%s", (phone,))
    else:
        print("Provide contact_id or phone to delete.")
        return
    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted!")

if __name__ == "__main__": 
    create_table()
    insert_from_console()     
    export_to_csv("contacts.csv")

"""
impor- from phonebook import connect, delete_contact, search_contacts, insert_from_console, export_to_csv
add- insert_from_console()

search- print(search_contacts())

delete- delete_contact(contact_id=2)
 """