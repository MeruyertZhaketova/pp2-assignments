import psycopg2
import csv
import json
from connect import connect


def get_conn():
    return connect()


def print_contact(row):
    cid, name, email, bday, group, phones = row
    print(f"[{cid}] {name} | email: {email or '-'} | birthday: {bday or '-'} | group: {group or '-'} | phones: {phones or '-'}")


def add_contact():
    name = input("Name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ") or "mobile"
    email = input("Email: ") or None
    birthday = input("Birthday (YYYY-MM-DD): ") or None
    group = input("Group (Family/Work/Friend/Other): ") or "Other"

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_u(%s, %s, %s)", (name, phone, ptype))
    cur.execute("""
        UPDATE phonebook
        SET email = %s, birthday = %s
        WHERE username = %s
    """, (email, birthday, name))
    cur.execute("CALL move_to_group(%s, %s)", (name, group))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact saved!")


def add_phone():
    name = input("Name: ")
    phone = input("New phone: ")
    ptype = input("Type: ") or "mobile"

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added!")


def move_group():
    name = input("Name: ")
    group = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s)", (name, group))

    conn.commit()
    cur.close()
    conn.close()

    print("Moved to group!")


def search():
    text = input("Search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (text,))
    rows = cur.fetchall()

    for r in rows:
        print_contact(r)

    cur.close()
    conn.close()


def filter_group():
    group = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.username, c.email, c.birthday, g.name,
               STRING_AGG(p.phone, ', ')
        FROM phonebook c
        JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE g.name = %s
        GROUP BY c.id, c.username, c.email, c.birthday, g.name
    """, (group,))

    rows = cur.fetchall()

    for r in rows:
        print_contact(r)

    cur.close()
    conn.close()


def delete():
    name = input("Name: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL del_user(%s)", (name,))

    conn.commit()
    cur.close()
    conn.close()

    print("Deleted!")


def browse():
    page = 0
    size = 5

    while True:
        conn = connect()
        cur = conn.cursor()

        cur.execute("SELECT * FROM pagination(%s, %s)", (size, page * size))
        rows = cur.fetchall()

        print(f"\nPage {page + 1}")
        for r in rows:
            print_contact(r)

        cur.close()
        conn.close()

        cmd = input("next / prev / exit: ")

        if cmd == "next":
            page += 1
        elif cmd == "prev":
            page = max(0, page - 1)
        else:
            break


def import_csv():
    file = "contacts.csv"

    conn = connect()
    cur = conn.cursor()

    with open(file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = row.get('username', '').strip()
            phone = row.get('phone', '').strip()
            ptype = row.get('phone_type', 'mobile').strip() or "mobile"
            email = row.get('email', '').strip() or None
            birthday = row.get('birthday', '').strip() or None
            group = row.get('group', '').strip() or "Other"

            if not name or not phone:
                continue

            cur.execute("CALL upsert_u(%s, %s, %s)", (name, phone, ptype))
            cur.execute("""
                UPDATE phonebook
                SET email = %s, birthday = %s
                WHERE username = %s
            """, (email, birthday, name))
            cur.execute("CALL move_to_group(%s, %s)", (name, group))

    conn.commit()
    cur.close()
    conn.close()

    print("CSV imported!")


def export_json():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.username, c.email, c.birthday, g.name
        FROM phonebook c
        LEFT JOIN groups g ON g.id = c.group_id
    """)

    data = []

    for cid, name, email, bday, group in cur.fetchall():
        cur.execute("SELECT phone, type FROM phones WHERE contact_id=%s", (cid,))
        phones = [{"phone": p, "type": t} for p, t in cur.fetchall()]

        data.append({
            "username": name,
            "email": email,
            "birthday": str(bday) if bday else None,
            "group": group,
            "phones": phones
        })

    with open("contacts.json", "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    cur.close()
    conn.close()

    print("Exported to JSON!")


def import_json():
    with open("contacts.json", encoding='utf-8') as f:
        data = json.load(f)

    conn = connect()
    cur = conn.cursor()

    for c in data:
        name = c["username"]

        cur.execute("SELECT id FROM phonebook WHERE username=%s", (name,))
        existing = cur.fetchone()

        if existing:
            answer = input(f"{name} exists. skip/overwrite? ")

            if answer.lower() != "overwrite":
                print(f"{name} skipped.")
                continue

            cid = existing[0]

            cur.execute("""
                UPDATE phonebook
                SET email = %s, birthday = %s
                WHERE id = %s
            """, (c.get("email"), c.get("birthday"), cid))

            cur.execute("DELETE FROM phones WHERE contact_id=%s", (cid,))

        else:
            cur.execute("""
                INSERT INTO phonebook (username, email, birthday)
                VALUES (%s, %s, %s) RETURNING id
            """, (c["username"], c.get("email"), c.get("birthday")))

            cid = cur.fetchone()[0]

        group = c.get("group") or "Other"
        cur.execute("CALL move_to_group(%s, %s)", (name, group))

        for ph in c.get("phones", []):
            cur.execute("""
                INSERT INTO phones (contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (cid, ph["phone"], ph.get("type", "mobile")))

    conn.commit()
    cur.close()
    conn.close()

    print("JSON imported!")


def menu():
    while True:
        print("""
1 Add contact
2 Add phone
3 Move group
4 Search
5 Filter by group
6 Delete
7 Browse pages
8 Import CSV
9 Export JSON
10 Import JSON
0 Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            add_phone()
        elif choice == "3":
            move_group()
        elif choice == "4":
            search()
        elif choice == "5":
            filter_group()
        elif choice == "6":
            delete()
        elif choice == "7":
            browse()
        elif choice == "8":
            import_csv()
        elif choice == "9":
            export_json()
        elif choice == "10":
            import_json()
        elif choice == "0":
            break


def gui_main():
    import tkinter as tk
    from tkinter import ttk, messagebox

    def get_sort_sql():
        sort_choice = sort_box.get()

        if sort_choice == "Name":
            return "c.username"
        elif sort_choice == "Birthday":
            return "c.birthday"
        else:
            return "c.created_at"

    def refresh():
        for row in table.get_children():
            table.delete(row)

        sort_sql = get_sort_sql()

        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"""
                        SELECT c.username,
                               COALESCE(c.email, '-'),
                               COALESCE(c.birthday::TEXT, '-'),
                               COALESCE(g.name, '-'),
                               COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '-')
                        FROM phonebook c
                        LEFT JOIN groups g ON g.id = c.group_id
                        LEFT JOIN phones p ON p.contact_id = c.id
                        GROUP BY c.id, c.username, c.email, c.birthday, g.name, c.created_at
                        ORDER BY {sort_sql};
                    """)
                    rows = cur.fetchall()

            for r in rows:
                table.insert("", tk.END, values=r)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_contact_gui():
        username = name_entry.get().strip()
        phone = phone_entry.get().strip()
        ptype = type_box.get()
        email = email_entry.get().strip() or None
        birthday = birthday_entry.get().strip() or None
        group = group_box.get()

        if not username or not phone:
            messagebox.showwarning("Warning", "Enter username and phone")
            return

        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("CALL upsert_u(%s, %s, %s);", (username, phone, ptype))

                    cur.execute("""
                        UPDATE phonebook
                        SET email = %s, birthday = %s
                        WHERE username = %s;
                    """, (email, birthday, username))

                    cur.execute("CALL move_to_group(%s, %s);", (username, group))

                conn.commit()

            messagebox.showinfo("Success", "Contact saved")

            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            birthday_entry.delete(0, tk.END)
            group_box.set("Other")
            type_box.set("mobile")

            refresh()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_contact_gui():
        username = name_entry.get().strip()

        if not username:
            messagebox.showwarning("Warning", "Enter username to delete")
            return

        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("CALL del_user(%s);", (username,))
                conn.commit()

            messagebox.showinfo("Success", "Contact deleted")
            refresh()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_gui():
        query = search_entry.get().strip()

        for row in table.get_children():
            table.delete(row)

        try:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM search_contacts(%s);", (query,))
                    rows = cur.fetchall()

            for r in rows:
                table.insert("", tk.END, values=(
                    r[1],
                    r[2] or "-",
                    r[3] or "-",
                    r[4] or "-",
                    r[5] or "-"
                ))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    root = tk.Tk()
    root.title("PhoneBook")
    root.geometry("1100x550")

    tk.Label(root, text="PhoneBook", font=("Arial", 18, "bold")).pack(pady=10)

    form = tk.Frame(root)
    form.pack(pady=10)

    tk.Label(form, text="Username:").grid(row=0, column=0, padx=5)
    name_entry = tk.Entry(form, width=20)
    name_entry.grid(row=0, column=1, padx=5)

    tk.Label(form, text="Phone:").grid(row=0, column=2, padx=5)
    phone_entry = tk.Entry(form, width=20)
    phone_entry.grid(row=0, column=3, padx=5)

    tk.Label(form, text="Type:").grid(row=0, column=4, padx=5)
    type_box = ttk.Combobox(form, values=["mobile", "home", "work"], width=10)
    type_box.set("mobile")
    type_box.grid(row=0, column=5, padx=5)

    tk.Label(form, text="Email:").grid(row=1, column=0, padx=5, pady=5)
    email_entry = tk.Entry(form, width=20)
    email_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form, text="Birthday:").grid(row=1, column=2, padx=5, pady=5)
    birthday_entry = tk.Entry(form, width=20)
    birthday_entry.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(form, text="Group:").grid(row=1, column=4, padx=5, pady=5)
    group_box = ttk.Combobox(form, values=["Family", "Work", "Friend", "Other"], width=10)
    group_box.set("Other")
    group_box.grid(row=1, column=5, padx=5, pady=5)

    buttons = tk.Frame(root)
    buttons.pack(pady=10)

    tk.Button(buttons, text="Add / Update", command=add_contact_gui, width=15).grid(row=0, column=0, padx=5)
    tk.Button(buttons, text="Delete", command=delete_contact_gui, width=15).grid(row=0, column=1, padx=5)
    tk.Button(buttons, text="Show All", command=refresh, width=15).grid(row=0, column=2, padx=5)

    search_frame = tk.Frame(root)
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5)
    search_entry = tk.Entry(search_frame, width=30)
    search_entry.grid(row=0, column=1, padx=5)

    tk.Button(search_frame, text="Search", command=search_gui, width=15).grid(row=0, column=2, padx=5)

    tk.Label(search_frame, text="Sort by:").grid(row=0, column=3, padx=5)
    sort_box = ttk.Combobox(search_frame, values=["Name", "Birthday", "Date added"], width=12)
    sort_box.set("Name")
    sort_box.grid(row=0, column=4, padx=5)

    tk.Button(search_frame, text="Apply Sort", command=refresh, width=12).grid(row=0, column=5, padx=5)

    columns = ("Name", "Email", "Birthday", "Group", "Phones")
    table = ttk.Treeview(root, columns=columns, show="headings")

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=190)

    table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    refresh()
    root.mainloop()


if __name__ == "__main__":
    gui_main()