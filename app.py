# Importing the packages and library files.
# Before run the program, make sure you download the required packages from Python Packages which is provided at below.

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from mysql.connector import connect, Error
import random as random
from functools import partial
from fpdf import FPDF

# Before run the program, make sure you download the required packages from Python Packages which is provided at top.

root = Tk()

# Used StringVar() to manage the value of a widget such as entry boxes.
usernameEntry = StringVar()
passwordEntry = StringVar()


# Created the first class which is going to be the root main. Then we are going to use this class as an inheritance below.
class Main:
    # Created the first frame and giving the details of the frame.
    def __init__(self, root):
        root.title("Login")
        root.geometry("530x180")
        # root.resizable(0, 0)

        self.root = root
        self.rootFrame = Frame(self.root)
        self.rootFrame.pack(fill="both", expand=1)

        # Creating the entry box physical details.
        self.usernameLabel = Label(self.rootFrame, text='Username')
        self.usernameLabel.place(x=10, y=10)
        self.usernameEntry = Entry(self.rootFrame, textvariable=usernameEntry, width=35)
        self.usernameEntry.place(x=10, y=30)

        self.passwordLabel = Label(self.rootFrame, text='Password')
        self.passwordLabel.place(x=10, y=70)
        self.passwordEntry = Entry(self.rootFrame, textvariable=passwordEntry, width=35, show='*')
        self.passwordEntry.place(x=10, y=90)
        self.usernameEntry.delete(0, END)
        self.passwordEntry.delete(0, END)

        # Credentials
        self.studentCredentialsLabel = Label(self.rootFrame, text='Student\nUsername: "cisel"\nPassword: "2"')
        self.studentCredentialsLabel.place(x=380, y=10)

        self.adminCredentialsLabel = Label(self.rootFrame, text='Admin\nUsername: "baris"\nPassword: "3"')
        self.adminCredentialsLabel.place(x=380, y=70)

        # Clicked button will be tested(Black Box!) - Baris
        # Creating a clicked element to clicked on any button or element
        def clicked(event):
            check()

        # test finished

        # Check function will be tested(black box)-Baris
        # Checking the username and password
        def check():
            username = usernameEntry.get()
            password = passwordEntry.get()

            # If there is no value at the entry boxes it will show the messagebox.showinfo()
            if len(username) == 0 or len(password) == 0:
                messagebox.showinfo("Warning!", "Please enter your username and password.")
                return

            # Connecting to the database to check the username and password.
            try:
                with connect(
                        host="auth-db582.hostinger.com",
                        user="u998717846_test_user",
                        password="7$Mw9Q=e",
                        database="u998717846_python_test"
                ) as connection:

                    query = "SELECT * FROM users WHERE username = %s AND password = %s"
                    value = (username, password)

                    with connection.cursor() as cursor:
                        cursor.execute(query, value)
                        result = cursor.fetchone()

                        if result:
                            # We gave the print command to see on terminal for proof if the code is working.
                            print('The user credentials are correct.')

                            # If the value showing "admin" root frame will switch to the admin.panel.frame
                            if result[4] == "Admin":
                                print('The user is admin.')

                                self.rootFrame.destroy()
                                AdminPanel(root)
                                root.mainloop()

                            # If the value showing "student" root frame will switch to the student.panel.frame
                            if result[4] == "Student":
                                print('The user is student.')

                                self.rootFrame.destroy()
                                StudentPanel(root)
                                root.mainloop()

                        # If the entered value is won't matching with database program will print wrong on terminal and messagebox.show info will show the (Warning! Invalid username and password)
                        else:
                            # We gave the print command to see on terminal for proof.
                            print(
                                'The user credentials are invalid!')  # We gave the print command to see on terminal for proof.
                            messagebox.showinfo('Warning!', 'Invalid username or password!')

            # Checking the errors
            except Error as e:
                print(e)

        # Created the main button to click on it for log in.
        self.mainButton = Button(self.rootFrame, text='Login', width=33, command=check)
        self.mainButton.place(x=10, y=130)

        root.bind("<Return>", clicked)


# Starting to crate Admin Panel class and design of the frames.
class AdminPanel:

    def __init__(self, root):
        admin_panel_frame = Frame(root)
        admin_panel_frame.pack(fill='both', expand=1)

        root.title("Admin Panel")
        root.geometry('355x250')

        # Managment panels will be tested(black box)-Baris
        # If user going to click in user management button admin_panel_frame will destroy and UserManagmentPanel will be open on the window. Same for all definitions below
        def user_management():
            admin_panel_frame.destroy()
            UserManagementPanel(root)

        def module_management_panel():
            admin_panel_frame.destroy()
            ModuleManagementPanel(root)

        def topic_management_panel():
            admin_panel_frame.destroy()
            TopicManagementPanel(root)

        def quiz_management_panel():
            admin_panel_frame.destroy()
            QuizManagementPanel(root)

        def question_management_panel():
            admin_panel_frame.destroy()
            QuestionManagement(root)

        # logout function will be test(black box)-Baris
        def logout():
            are_you_sure = messagebox.askyesno("Alert", "Are you sure you want to logout?")

            if are_you_sure:
                admin_panel_frame.destroy()
                Main(root)

        # Creating the buttons for the management frames
        Button(admin_panel_frame, text='User Management', width=33, command=user_management).place(x=10, y=10)
        Button(admin_panel_frame, text='Module Management', width=33, command=module_management_panel).place(x=10, y=50)
        Button(admin_panel_frame, text='Topic Management', width=33, command=topic_management_panel).place(x=10, y=90)
        Button(admin_panel_frame, text='Quiz Management', width=33, command=quiz_management_panel).place(x=10, y=130)
        Button(admin_panel_frame, text='Question Management', command=question_management_panel, width=33).place(x=10,
                                                                                                                 y=170)
        Button(admin_panel_frame, text='Logout', command=logout, width=33).place(x=10, y=210)


# Creating the user management frame and designing the buttons.
class UserManagementPanel:

    def __init__(self, root):
        user_management_panel_frame = Frame(root)
        user_management_panel_frame.pack(fill='both', expand=1)

        root.title("User Management")
        root.geometry('1490x550')

        # Connecting the database again to add/edit/delete/update the all records
        def query_database():
            # Clear the Treeview
            for record in my_tree.get_children():
                my_tree.delete(record)

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            c = conn.cursor()
            # print(conn)

            # Giving the query to access the table.
            query = "SELECT * FROM users"

            c.execute(query)
            records = c.fetchall()

            # Add our data to the screen
            global count
            count = 0

            for record in records:
                if count % 2 == 0:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(record[0], record[1], record[2], record[3], record[4]),
                        tags=("evenrow",)
                    )
                else:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(record[0], record[1], record[2], record[3], record[4]),
                        tags=("oddrow",)
                    )

                # increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        # Add Some Style
        style = ttk.Style()

        # Pick A Theme
        style.theme_use('default')

        # Configure the Treeview Colors
        style.configure(
            "Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
        )

        # Create a Treeview Frame
        tree_frame = Frame(user_management_panel_frame)
        tree_frame.pack(pady=10)

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        my_tree.pack()

        # Configure the Scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define Our Columns
        my_tree['columns'] = ("ID", "Email", "Username", "Password", "Access Level")

        # Format Our Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("ID", anchor=W, width=50)
        my_tree.column("Email", anchor=W, width=140)
        my_tree.column("Username", anchor=W, width=140)
        my_tree.column("Password", anchor=W, width=140)
        my_tree.column("Access Level", anchor=W, width=140)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("ID", text="ID", anchor=W)
        my_tree.heading("Email", text="Email", anchor=W)
        my_tree.heading("Username", text="Username", anchor=W)
        my_tree.heading("Password", text="Password", anchor=W)
        my_tree.heading("Access Level", text="Access Level", anchor=W)

        # Add record part will be test (black box) by Emir
        # Add Record Entry Boxes
        data_frame = LabelFrame(user_management_panel_frame, text="Record")
        data_frame.pack(fill="x", expand="yes", padx=20)

        id_label = Label(data_frame, text="ID")
        id_label.grid(row=0, column=0, padx=10, pady=10)
        id_entry = Entry(data_frame)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        email_label = Label(data_frame, text="Email")
        email_label.grid(row=0, column=2, padx=10, pady=10)
        email_entry = Entry(data_frame)
        email_entry.grid(row=0, column=3, padx=10, pady=10)

        username_label = Label(data_frame, text="Username")
        username_label.grid(row=0, column=4, padx=10, pady=10)
        username_entry = Entry(data_frame)
        username_entry.grid(row=0, column=5, padx=10, pady=10)

        password_label = Label(data_frame, text="Password")
        password_label.grid(row=0, column=6, padx=10, pady=10)
        password_entry = Entry(data_frame)
        password_entry.grid(row=0, column=7, padx=10, pady=10)

        # Access level will be test(black box)-Emir
        # Checking the access level to understand if user student or admin
        access_level = StringVar()
        access_levels = ["Admin", "Student"]

        access_level_label = Label(data_frame, text="Access Level")
        access_level_label.grid(row=0, column=8, padx=10, pady=10)
        access_level_menu = OptionMenu(data_frame, access_level, *access_levels)
        access_level.set("Select Access Level")
        access_level_menu.grid(row=0, column=9, padx=10, pady=10)

        # Move Row Up
        def up():
            rows = my_tree.selection()
            for row in rows:
                my_tree.move(row, my_tree.parent(row), my_tree.index(row) - 1)

        # Move Row Down
        def down():
            rows = my_tree.selection()
            for row in reversed(rows):
                my_tree.move(row, my_tree.parent(row), my_tree.index(row) + 1)

        # Clear entry boxes will be checked by Emir
        # Clear entry boxes
        def clear_entries():
            # Clear entry boxes
            id_entry.delete(0, END)
            email_entry.delete(0, END)
            username_entry.delete(0, END)
            password_entry.delete(0, END)
            access_level.set("Select Access Level")

        # Select record function will be test by Emir
        # Select Record
        def select_record(e):
            # Clear entry boxes
            id_entry.delete(0, END)
            email_entry.delete(0, END)
            username_entry.delete(0, END)
            password_entry.delete(0, END)
            access_level.set("Select Access Level")

            # Grab record number
            selected = my_tree.focus()

            # Grab record values
            values = my_tree.item(selected, 'values')

            # output to entry boxes to see what is chosen
            id_entry.insert(0, values[0])
            email_entry.insert(0, values[1])
            username_entry.insert(0, values[2])
            password_entry.insert(0, values[3])
            access_level.set(values[4])

        # Remove record function will be checked by Emir
        # Remove one record
        def remove_one():

            # If there is no selected record it will show the messagebox.showinfo()
            if len(my_tree.focus()) == 0:
                messagebox.showinfo("Warning!", "Please select the record you want to delete.")
                query_database()
                return

            x = my_tree.selection()[0]
            my_tree.delete(x)

            # Connecting to the database
            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Execute query
            c.execute("DELETE FROM users WHERE id=" + id_entry.get())

            # Commit changes
            conn.commit()

            # Close connection
            conn.close()

            # Clear The Entry Boxes
            clear_entries()

            # Informative message box
            messagebox.showinfo("Deleted!", "Successfully deleted.")

        # remove all entries tested by Chisel
        def remove_all():
            # Informative message box
            response = messagebox.askyesno("Warning!", "Are you sure?\nAll data will be deleted!")

            # Add logic for message box
            if response == 1:
                # Clear the Treeview
                for record in my_tree.get_children():
                    my_tree.delete(record)

                # Connecting to the database
                conn = connect(
                    host="auth-db582.hostinger.com",
                    user="u998717846_test_user",
                    password="7$Mw9Q=e",
                    database="u998717846_python_test"
                )

                # Create a cursor instance
                c = conn.cursor()

                # Execute query
                c.execute("TRUNCATE TABLE users")

                # Commit changes
                conn.commit()

                # Close connection
                conn.close()

                # Clear The Entry Boxes
                clear_entries()

                # Recreate The Table
                # create_table_again()

                # Informative message box
                messagebox.showinfo("Deleted!", "Successfully deleted.")

        # Adding record tested by Chisel
        # Add new record to database
        def add_record():

            # If there is no value at the entry boxes it will show the messagebox.showinfo()
            if len(email_entry.get()) == 0 or len(username_entry.get()) == 0 or len(
                    password_entry.get()) == 0 or access_level.get() == "Select Access Level":
                messagebox.showinfo("Warning!", "Please enter all fields.")
                query_database()
                return

            # Connecting to the database
            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            select_query = "SELECT * FROM users WHERE email=%s OR username=%s"
            user_values = (email_entry.get(), username_entry.get())

            # Execute query
            c.execute(select_query, user_values)

            # Fetch user
            user = c.fetchall()

            # Check if the email and username of the entered user exist.
            if user:
                # Existing user
                print('Existing user!')

                messagebox.showinfo("Warning!", "The user is exist.")

                # Clear The Entry Boxes
                clear_entries()

            else:
                # Not existing user
                print('New user.')

                # SQL query to add users to the "user" table in the database.
                insert_user = "INSERT INTO users (email, username, password, access_level) VALUES (%s, %s, %s, %s)"
                user_credentials = (email_entry.get(), username_entry.get(), password_entry.get(), access_level.get())

                # Execute query
                c.execute(insert_user, user_credentials)

                # Clear The Entry Boxes
                clear_entries()

            # Commit changes
            conn.commit()

            # Close connection
            conn.close()

            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_database()

        # Update selected record tested by Chisel
        # Update record
        def update_record():

            # If there is no value at the entry boxes it will show the messagebox.showinfo()
            if len(email_entry.get()) == 0 or len(username_entry.get()) == 0 or len(
                    password_entry.get()) == 0 or access_level.get() == "Select Access Level":
                messagebox.showinfo("Warning!", "Please enter all fields.")
                query_database()
                return

            # Grab the record number
            selected = my_tree.focus()

            # Update record
            my_tree.item(selected, text="", values=(
                email_entry.get(), username_entry.get(), password_entry.get(), access_level.get()))

            # Calling queries
            query = "UPDATE users SET email = %s, username = %s, password = %s, access_level = %s WHERE id = %s"
            value = (email_entry.get(), username_entry.get(), password_entry.get(), access_level.get(), id_entry.get())

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Execute query
            c.execute(query, value)

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            # Clear The Entry Boxes
            clear_entries()

            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_database()

        # Add Buttons
        button_frame = LabelFrame(user_management_panel_frame, text="Commands")
        button_frame.pack(fill="x", expand="yes", padx=20)

        add_button = Button(button_frame, text="Add Record", command=add_record)
        add_button.grid(row=0, column=0, padx=10, pady=10)

        update_button = Button(button_frame, text="Update Record", command=update_record)
        update_button.grid(row=0, column=1, padx=10, pady=10)

        remove_one_button = Button(button_frame, text="Remove Selected", command=remove_one)
        remove_one_button.grid(row=0, column=2, padx=10, pady=10)

        remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
        remove_all_button.grid(row=0, column=3, padx=10, pady=10)

        move_up_button = Button(button_frame, text="Move Up", command=up)
        move_up_button.grid(row=0, column=4, padx=10, pady=10)

        move_down_button = Button(button_frame, text="Move Down", command=down)
        move_down_button.grid(row=0, column=5, padx=10, pady=10)

        select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
        select_record_button.grid(row=0, column=6, padx=10, pady=10)

        # Going to previous page tested by Chisel
        # If user click on previous page button it will take the frames to back
        def previous_page():
            user_management_panel_frame.destroy()
            AdminPanel(root)

        previous_page_button = Button(button_frame, text="Previous Page", command=previous_page)
        previous_page_button.grid(row=0, column=7, padx=10, pady=10)

        # Bind the treeview
        my_tree.bind("<ButtonRelease-1>", select_record)

        # Run to pull data from database on start
        query_database()


# creating a class for ModuleManagementPanel.
class ModuleManagementPanel:

    def __init__(self, root):
        module_management_panel_frame = Frame(root)
        module_management_panel_frame.pack(fill='both', expand=1)

        root.title("Module Management Panel")
        root.geometry('1230x550')

        def query_database():
            # Clear the Treeview
            for record in my_tree.get_children():
                my_tree.delete(record)

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            c = conn.cursor()
            # print(conn)

            query = "SELECT * FROM modules"

            c.execute(query)
            records = c.fetchall()

            # Add our data to the screen
            global count
            count = 0

            for record in records:
                if count % 2 == 0:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(record[0], record[1], record[2]),
                        tags=("evenrow",)
                    )
                else:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(record[0], record[1], record[2]),
                        tags=("oddrow",)
                    )

                # increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        # Add Some Style
        style = ttk.Style()

        # Pick A Theme
        style.theme_use('default')

        # Configure the Treeview Colors
        style.configure(
            "Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
        )

        # Create a Treeview Frame
        tree_frame = Frame(module_management_panel_frame)
        tree_frame.pack(pady=10)

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        my_tree.pack()

        # Configure the Scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define Our Columns
        my_tree['columns'] = ("ID", "Module Code", "Module Name")

        # Format Our Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("ID", anchor=W, width=50)
        my_tree.column("Module Code", anchor=W, width=140)
        my_tree.column("Module Name", anchor=W, width=140)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("ID", text="ID", anchor=W)
        my_tree.heading("Module Code", text="Module Code", anchor=W)
        my_tree.heading("Module Name", text="Module Name", anchor=W)

        # Add Record Entry Boxes
        data_frame = LabelFrame(module_management_panel_frame, text="Record")
        data_frame.pack(fill="x", expand="yes", padx=20)

        id_label = Label(data_frame, text="ID")
        id_label.grid(row=0, column=0, padx=10, pady=10)
        id_entry = Entry(data_frame)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        module_code_label = Label(data_frame, text="Module Code")
        module_code_label.grid(row=0, column=2, padx=10, pady=10)
        module_code_entry = Entry(data_frame)
        module_code_entry.grid(row=0, column=3, padx=10, pady=10)

        module_name_label = Label(data_frame, text="Module Name")
        module_name_label.grid(row=0, column=4, padx=10, pady=10)
        module_name_entry = Entry(data_frame)
        module_name_entry.grid(row=0, column=5, padx=10, pady=10)

        # Move Row Up
        def up():
            rows = my_tree.selection()
            for row in rows:
                my_tree.move(row, my_tree.parent(row), my_tree.index(row) - 1)

        # Move Row Down
        def down():
            rows = my_tree.selection()
            for row in reversed(rows):
                my_tree.move(row, my_tree.parent(row), my_tree.index(row) + 1)

        # Clear entry boxes
        def clear_entries():
            # Clear entry boxes
            id_entry.delete(0, END)
            module_code_entry.delete(0, END)
            module_name_entry.delete(0, END)

        # Select Record
        def select_record(e):
            # Clear entry boxes
            id_entry.delete(0, END)
            module_code_entry.delete(0, END)
            module_name_entry.delete(0, END)

            # Grab record number
            selected = my_tree.focus()

            # Grab record values
            values = my_tree.item(selected, 'values')

            # Output to entry boxes
            id_entry.insert(0, values[0])
            module_code_entry.insert(0, values[1])
            module_name_entry.insert(0, values[2])

        # Remove one record
        def remove_one():

            # If there is no selected record it will show the messagebox.showinfo()
            if len(my_tree.focus()) == 0:
                messagebox.showinfo("Warning!", "Please select the record you want to delete.")
                query_database()
                return

            x = my_tree.selection()[0]
            my_tree.delete(x)

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Execute query
            c.execute("DELETE FROM modules WHERE id=" + id_entry.get())

            # Commit changes
            conn.commit()

            # Close connection
            conn.close()

            # Clear The Entry Boxes
            clear_entries()

            # Informative message box
            messagebox.showinfo("Deleted!", "Successfully deleted.")

        def remove_all():
            # Informative message box
            response = messagebox.askyesno("Warning!", "Are you sure?\nAll data will be deleted!")

            # Add logic for message box
            if response == 1:
                # Clear the Treeview
                for record in my_tree.get_children():
                    my_tree.delete(record)

                conn = connect(
                    host="auth-db582.hostinger.com",
                    user="u998717846_test_user",
                    password="7$Mw9Q=e",
                    database="u998717846_python_test"
                )

                # Create a cursor instance
                c = conn.cursor()

                # Execute query
                c.execute("TRUNCATE TABLE modules")

                # Commit changes
                conn.commit()

                # Close connection
                conn.close()

                # Clear The Entry Boxes
                clear_entries()

                # Recreate The Table
                # create_table_again()

                # Informative message box
                messagebox.showinfo("Deleted!", "Successfully deleted.")

        # Add new record to database
        def add_record():

            # If there is no value at the entry boxes it will show the messagebox.showinfo()
            if len(module_code_entry.get()) == 0 or len(module_name_entry.get()) == 0:
                messagebox.showinfo("Warning!", "Please enter all fields.")
                query_database()
                return

            ##########

            # Connecting to the database
            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            check_query = "SELECT * FROM modules WHERE moduleCode=%s OR moduleName=%s"
            check_values = (module_code_entry.get(), module_name_entry.get())

            # Execute query
            c.execute(check_query, check_values)

            # Fetch user
            check = c.fetchall()

            # Check if the email and username of the entered user exist.
            if check:
                # Existing user
                print('Existing module!')

                messagebox.showinfo("Warning!", "The module is exist.")

                # Clear The Entry Boxes
                clear_entries()

            else:
                # Not existing user
                print('New module.')

                query = "INSERT INTO modules (moduleCode, moduleName) VALUES (%s, %s)"
                value = (module_code_entry.get(), module_name_entry.get())

                conn = connect(
                    host="auth-db582.hostinger.com",
                    user="u998717846_test_user",
                    password="7$Mw9Q=e",
                    database="u998717846_python_test"
                )

                # Create a cursor instance
                c = conn.cursor()

                # Execute query
                c.execute(query, value)

                # Commit changes
                conn.commit()

                # Close connection
                conn.close()

            ##########

            # Clear The Entry Boxes
            clear_entries()

            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_database()

        # Update record
        def update_record():

            # If there is no value at the entry boxes it will show the messagebox.showinfo()
            if len(module_code_entry.get()) == 0 or len(module_name_entry.get()) == 0:
                messagebox.showinfo("Warning!", "Please enter all fields.")
                query_database()
                return

            # Grab the record number
            selected = my_tree.focus()

            # Update record
            my_tree.item(selected, text="", values=(
                module_code_entry.get(), module_name_entry.get()))

            # If there is no value at the entry boxes it will show the messagebox.showinfo()
            if len(module_code_entry.get()) == 0 or len(module_name_entry.get()) == 0:
                messagebox.showinfo("Warning!", "Please enter all fields.")
                query_database()
                return

            query = "UPDATE modules SET moduleCode = %s, moduleName = %s WHERE id = %s"
            value = (module_code_entry.get(), module_name_entry.get(), id_entry.get())

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Execute query
            c.execute(query, value)

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            # Clear The Entry Boxes
            clear_entries()

            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_database()

        # Add Buttons
        button_frame = LabelFrame(module_management_panel_frame, text="Commands")
        button_frame.pack(fill="x", expand="yes", padx=20)

        add_button = Button(button_frame, text="Add Record", command=add_record)
        add_button.grid(row=0, column=0, padx=10, pady=10)

        update_button = Button(button_frame, text="Update Record", command=update_record)
        update_button.grid(row=0, column=1, padx=10, pady=10)

        remove_one_button = Button(button_frame, text="Remove Selected", command=remove_one)
        remove_one_button.grid(row=0, column=2, padx=10, pady=10)

        remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
        remove_all_button.grid(row=0, column=3, padx=10, pady=10)

        move_up_button = Button(button_frame, text="Move Up", command=up)
        move_up_button.grid(row=0, column=4, padx=10, pady=10)

        move_down_button = Button(button_frame, text="Move Down", command=down)
        move_down_button.grid(row=0, column=5, padx=10, pady=10)

        select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
        select_record_button.grid(row=0, column=6, padx=10, pady=10)

        def previous_page():
            module_management_panel_frame.destroy()
            AdminPanel(root)

        previous_page_button = Button(button_frame, text="Previous Page", command=previous_page)
        previous_page_button.grid(row=0, column=7, padx=10, pady=10)

        # Bind the treeview
        my_tree.bind("<ButtonRelease-1>", select_record)

        # Run to pull data from database on start
        query_database()


class TopicManagementPanel:

    def __init__(self, root):
        topic_management_panel_frame = Frame(root)
        topic_management_panel_frame.pack(fill='both', expand=1)

        root.title("Topic Management Panel")
        root.geometry('1230x550')

        def query_database():
            # Clear the Treeview
            for record in my_tree.get_children():
                my_tree.delete(record)

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            c = conn.cursor()
            # print(conn)

            query = "SELECT * FROM topics INNER JOIN modules ON topics.moduleID = modules.id"

            c.execute(query)
            records = c.fetchall()

            # Add our data to the screen
            global count
            count = 0

            for record in records:
                if count % 2 == 0:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(record[0], record[5], record[2]),
                        tags=("evenrow",)
                    )
                else:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(record[0], record[5], record[2]),
                        tags=("oddrow",)
                    )

                # increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        # Add Some Style
        style = ttk.Style()

        # Pick A Theme
        style.theme_use('default')

        # Configure the Treeview Colors
        style.configure(
            "Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
        )

        # Create a Treeview Frame
        tree_frame = Frame(topic_management_panel_frame)
        tree_frame.pack(pady=10)

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        my_tree.pack()

        # Configure the Scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define Our Columns
        my_tree['columns'] = ("ID", "Module Name", "Topic Name")

        # Format Our Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("ID", anchor=W, width=50)
        my_tree.column("Module Name", anchor=W, width=140)
        my_tree.column("Topic Name", anchor=W, width=140)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("ID", text="ID", anchor=W)
        my_tree.heading("Module Name", text="Module Name", anchor=W)
        my_tree.heading("Topic Name", text="Topic Name", anchor=W)

        # Add Record Entry Boxes
        data_frame = LabelFrame(topic_management_panel_frame, text="Record")
        data_frame.pack(fill="x", expand="yes", padx=20)

        id_label = Label(data_frame, text="ID")
        id_label.grid(row=0, column=0, padx=10, pady=10)
        id_entry = Entry(data_frame)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        # MODULE MENU START #

        conn = connect(
            host="auth-db582.hostinger.com",
            user="u998717846_test_user",
            password="7$Mw9Q=e",
            database="u998717846_python_test"
        )

        query = "SELECT * FROM modules"

        c = conn.cursor()
        # print(conn)

        c.execute(query)
        records = c.fetchall()

        # datatype of menu text
        module_menu = StringVar()

        module_list = dict()
        for record in records:
            module_list[record[0]] = record[2]

        module_name_label = Label(data_frame, text="Module Name")
        module_name_label.grid(row=0, column=2, padx=10, pady=10)
        module_name_menu = OptionMenu(data_frame, module_menu, *module_list.values())
        module_menu.set("Select Module")
        module_name_menu.grid(row=0, column=3, padx=10, pady=10)

        # MODULE MENU END #

        topic_name_label = Label(data_frame, text="Topic Name")
        topic_name_label.grid(row=0, column=4, padx=10, pady=10)
        topic_name_entry = Entry(data_frame)
        topic_name_entry.grid(row=0, column=5, padx=10, pady=10)

        # Move Row Up
        def up():
            rows = my_tree.selection()
            for row in rows:
                my_tree.move(row, my_tree.parent(row), my_tree.index(row) - 1)

        # Move Row Down
        def down():
            rows = my_tree.selection()
            for row in reversed(rows):
                my_tree.move(row, my_tree.parent(row), my_tree.index(row) + 1)

        # Clear entry boxes
        def clear_entries():
            # Clear entry boxes
            id_entry.delete(0, END)
            module_menu.set("Select Module")
            topic_name_entry.delete(0, END)

        # Select Record
        def select_record(e):
            # Clear entry boxes
            id_entry.delete(0, END)
            module_menu.set("Select Module")

            topic_name_entry.delete(0, END)

            # Grab record number
            selected = my_tree.focus()

            # Grab record values
            values = my_tree.item(selected, 'values')

            # Output to entry boxes
            id_entry.insert(0, values[0])
            module_menu.set(values[1])
            topic_name_entry.insert(0, values[2])

        # Remove one record
        def remove_one():

            # If there is no selected record it will show the messagebox.showinfo()
            if len(my_tree.focus()) == 0:
                messagebox.showinfo("Warning!", "Please select the record you want to delete.")
                query_database()
                return

            x = my_tree.selection()[0]
            my_tree.delete(x)

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Execute query
            c.execute("DELETE FROM topics WHERE id=" + id_entry.get())

            # Commit changes
            conn.commit()

            # Close connection
            conn.close()

            # Clear The Entry Boxes
            clear_entries()

            # Informative message box
            messagebox.showinfo("Deleted!", "Successfully deleted.")

        def remove_all():
            # Informative message box
            response = messagebox.askyesno("Warning!", "Are you sure?\nAll data will be deleted!")

            # Add logic for message box
            if response == 1:
                # Clear the Treeview
                for record in my_tree.get_children():
                    my_tree.delete(record)

                conn = connect(
                    host="auth-db582.hostinger.com",
                    user="u998717846_test_user",
                    password="7$Mw9Q=e",
                    database="u998717846_python_test"
                )

                # Create a cursor instance
                c = conn.cursor()

                # Execute query
                c.execute("TRUNCATE TABLE topics")

                # Commit changes
                conn.commit()

                # Close connection
                conn.close()

                # Clear The Entry Boxes
                clear_entries()

                # Recreate The Table
                # create_table_again()

                # Informative message box
                messagebox.showinfo("Deleted!", "Successfully deleted.")

        # Add new record to database
        def add_record():

            # If there is no value at the entry boxes it will show the messagebox.showinfo()
            if module_menu.get() == "Select Module" or len(topic_name_entry.get()) == 0:
                messagebox.showinfo("Warning!", "Please enter all fields.")
                query_database()
                return

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            query = "SELECT * FROM modules WHERE moduleName='{}'".format(module_menu.get())
            c.execute(query)
            result = c.fetchone()

            query2 = "INSERT INTO topics (moduleID, topicName) VALUES (%s, %s)"
            value = (result[0], topic_name_entry.get())
            c.execute(query2, value)

            # Commit changes
            conn.commit()

            # Close connection
            conn.close()

            # Clear The Entry Boxes
            clear_entries()

            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_database()

        # Update record
        def update_record():

            # If there is no value at the entry boxes it will show the messagebox.showinfo()
            if module_menu.get() == "Select Module" or len(topic_name_entry.get()) == 0:
                messagebox.showinfo("Warning!", "Please enter all fields.")
                query_database()
                return

            # Grab the record number
            selected = my_tree.focus()

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            fetch_modules = "SELECT * FROM modules WHERE moduleName='{}'".format(module_menu.get())
            c.execute(fetch_modules)
            module_result = c.fetchone()

            update_topic = "UPDATE topics SET moduleID = %s, topicName = %s WHERE id = %s"
            value = (module_result[0], topic_name_entry.get(), id_entry.get())
            c.execute(update_topic, value)

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            # Update record
            my_tree.item(selected, text="", values=(
                module_result[0], topic_name_entry.get()))

            # Clear The Entry Boxes
            clear_entries()

            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_database()

        # Add Buttons
        button_frame = LabelFrame(topic_management_panel_frame, text="Commands")
        button_frame.pack(fill="x", expand="yes", padx=20)

        add_button = Button(button_frame, text="Add Record", command=add_record)
        add_button.grid(row=0, column=0, padx=10, pady=10)

        update_button = Button(button_frame, text="Update Record", command=update_record)
        update_button.grid(row=0, column=1, padx=10, pady=10)

        remove_one_button = Button(button_frame, text="Remove Selected", command=remove_one)
        remove_one_button.grid(row=0, column=2, padx=10, pady=10)

        remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
        remove_all_button.grid(row=0, column=3, padx=10, pady=10)

        move_up_button = Button(button_frame, text="Move Up", command=up)
        move_up_button.grid(row=0, column=4, padx=10, pady=10)

        move_down_button = Button(button_frame, text="Move Down", command=down)
        move_down_button.grid(row=0, column=5, padx=10, pady=10)

        select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
        select_record_button.grid(row=0, column=6, padx=10, pady=10)

        def previous_page():
            topic_management_panel_frame.destroy()
            AdminPanel(root)

        previous_page_button = Button(button_frame, text="Previous Page", command=previous_page)
        previous_page_button.grid(row=0, column=7, padx=10, pady=10)

        # Bind the treeview
        my_tree.bind("<ButtonRelease-1>", select_record)

        # Run to pull data from database on start
        query_database()


class QuizManagementPanel:

    def __init__(self, root):
        quiz_management_panel_frame = Frame(root)
        quiz_management_panel_frame.pack(fill='both', expand=1)

        root.title("Quiz Management Panel")
        root.geometry('1230x550')

        def query_database():
            # Clear the Treeview
            for record in my_tree.get_children():
                my_tree.delete(record)

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            c = conn.cursor()
            # print(conn)

            query = "SELECT * FROM quizzes INNER JOIN topics ON quizzes.topicID = topics.id INNER JOIN modules ON topics.moduleID = modules.id"

            c.execute(query)
            records = c.fetchall()

            # Add our data to the screen
            global count
            count = 0

            for record in records:
                if count % 2 == 0:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(record[0], record[8], record[5], record[2]),
                        tags=("evenrow",)
                    )
                else:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(record[0], record[8], record[5], record[2]),
                        tags=("oddrow",)
                    )

                # increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        # Add Some Style
        style = ttk.Style()

        # Pick A Theme
        style.theme_use('default')

        # Configure the Treeview Colors
        style.configure(
            "Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
        )

        # Create a Treeview Frame
        tree_frame = Frame(quiz_management_panel_frame)
        tree_frame.pack(pady=10)

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        my_tree.pack()

        # Configure the Scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define Our Columns
        my_tree['columns'] = ("ID", "Module Name", "Topic Name", "Quiz Name")

        # Format Our Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("ID", anchor=W, width=50)
        my_tree.column("Module Name", anchor=W, width=140)
        my_tree.column("Topic Name", anchor=W, width=140)
        my_tree.column("Quiz Name", anchor=W, width=140)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("ID", text="ID", anchor=W)
        my_tree.heading("Module Name", text="Module Name", anchor=W)
        my_tree.heading("Topic Name", text="Topic Name", anchor=W)
        my_tree.heading("Quiz Name", text="Quiz Name", anchor=W)

        # Add Record Entry Boxes
        data_frame = LabelFrame(quiz_management_panel_frame, text="Record")
        data_frame.pack(fill="x", expand="yes", padx=20)

        id_label = Label(data_frame, text="ID")
        id_label.grid(row=0, column=0, padx=10, pady=10)
        id_entry = Entry(data_frame)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        # TOPIC MENU START #

        conn = connect(
            host="auth-db582.hostinger.com",
            user="u998717846_test_user",
            password="7$Mw9Q=e",
            database="u998717846_python_test"
        )

        query = "SELECT * FROM topics"

        c = conn.cursor()
        # print(conn)

        c.execute(query)
        records = c.fetchall()

        # Datatype of menu text
        topic_menu = StringVar()

        topic_list = dict()
        for record in records:
            topic_list[record[0]] = record[2]

        topic_name_label = Label(data_frame, text="Topic Name")
        topic_name_label.grid(row=0, column=2, padx=10, pady=10)
        topic_name_menu = OptionMenu(data_frame, topic_menu, *topic_list.values())
        topic_menu.set("Select Topic")
        topic_name_menu.grid(row=0, column=3, padx=10, pady=10)

        # TOPIC MENU END #

        quiz_name_label = Label(data_frame, text="Quiz Name")
        quiz_name_label.grid(row=0, column=4, padx=10, pady=10)
        quiz_name_entry = Entry(data_frame)
        quiz_name_entry.grid(row=0, column=5, padx=10, pady=10)

        # Move Row Up
        def up():
            rows = my_tree.selection()
            for row in rows:
                my_tree.move(row, my_tree.parent(row), my_tree.index(row) - 1)

        # Move Row Down
        def down():
            rows = my_tree.selection()
            for row in reversed(rows):
                my_tree.move(row, my_tree.parent(row), my_tree.index(row) + 1)

        # Clear entry boxes
        def clear_entries():
            # Clear entry boxes
            id_entry.delete(0, END)
            topic_menu.set("Select Topic")
            quiz_name_entry.delete(0, END)

        # Select Record
        def select_record(e):
            # Clear entry boxes
            id_entry.delete(0, END)
            topic_menu.set("Select Topic")
            quiz_name_entry.delete(0, END)

            # Grab record number
            selected = my_tree.focus()

            # Grab record values
            values = my_tree.item(selected, 'values')

            # Output to entry boxes
            id_entry.insert(0, values[0])
            topic_menu.set(values[2])
            quiz_name_entry.insert(0, values[3])

        # Remove one record
        def remove_one():

            # If there is no selected record it will show the messagebox.showinfo()
            if len(my_tree.focus()) == 0:
                messagebox.showinfo("Warning!", "Please select the record you want to delete.")
                query_database()
                return

            x = my_tree.selection()[0]
            my_tree.delete(x)

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Execute query
            c.execute("DELETE FROM quizzes WHERE id=" + id_entry.get())

            # Commit changes
            conn.commit()

            # Close connection
            conn.close()

            # Clear The Entry Boxes
            clear_entries()

            # Informative message box
            messagebox.showinfo("Deleted!", "Successfully deleted.")

        def remove_all():
            # Informative message box
            response = messagebox.askyesno("Warning!", "Are you sure?\nAll data will be deleted!")

            # Add logic for message box
            if response == 1:
                # Clear the Treeview
                for record in my_tree.get_children():
                    my_tree.delete(record)

                conn = connect(
                    host="auth-db582.hostinger.com",
                    user="u998717846_test_user",
                    password="7$Mw9Q=e",
                    database="u998717846_python_test"
                )

                # Create a cursor instance
                c = conn.cursor()

                # Execute query
                c.execute("TRUNCATE TABLE quizzes")

                # Commit changes
                conn.commit()

                # Close connection
                conn.close()

                # Clear The Entry Boxes
                clear_entries()

                # Recreate The Table
                # create_table_again()

                # Informative message box
                messagebox.showinfo("Deleted!", "Successfully deleted.")

        # Add new record to database
        def add_record():

            # If there is no value at the entry boxes it will show the messagebox.showinfo()
            if topic_menu.get() == "Select Topic" or len(quiz_name_entry.get()) == 0:
                messagebox.showinfo("Warning!", "Please enter all fields.")
                query_database()
                return

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Fetch selected topic
            fetch_topic = "SELECT * FROM topics WHERE topicName='{}'".format(topic_menu.get())
            c.execute(fetch_topic)
            topic_result = c.fetchone()

            insert_quiz = "INSERT INTO quizzes (topicID, quizName) VALUES (%s, %s)"
            value = (topic_result[0], quiz_name_entry.get())
            c.execute(insert_quiz, value)

            # Commit changes
            conn.commit()

            # Close connection
            conn.close()

            # Clear The Entry Boxes
            clear_entries()

            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_database()

        # Update record
        def update_record():

            # If there is no value at the entry boxes it will show the messagebox.showinfo()
            if topic_menu.get() == "Select Topic" or len(quiz_name_entry.get()) == 0:
                messagebox.showinfo("Warning!", "Please enter all fields.")
                query_database()
                return

            # Grab the record number
            selected = my_tree.focus()

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Fetch selected topic
            fetch_topic = "SELECT * FROM topics WHERE topicName='{}'".format(topic_menu.get())
            c.execute(fetch_topic)
            topic_result = c.fetchone()

            update_quiz = "UPDATE quizzes SET topicID = %s, quizName = %s WHERE id = %s"
            value = (topic_result[0], quiz_name_entry.get(), id_entry.get())
            c.execute(update_quiz, value)

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            # Update record
            my_tree.item(selected, text="", values=(
                topic_result[0], quiz_name_entry.get()))

            # Clear The Entry Boxes
            clear_entries()

            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_database()

        # Add Buttons
        button_frame = LabelFrame(quiz_management_panel_frame, text="Commands")
        button_frame.pack(fill="x", expand="yes", padx=20)

        add_button = Button(button_frame, text="Add Record", command=add_record)
        add_button.grid(row=0, column=0, padx=10, pady=10)

        update_button = Button(button_frame, text="Update Record", command=update_record)
        update_button.grid(row=0, column=1, padx=10, pady=10)

        remove_one_button = Button(button_frame, text="Remove Selected", command=remove_one)
        remove_one_button.grid(row=0, column=2, padx=10, pady=10)

        remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
        remove_all_button.grid(row=0, column=3, padx=10, pady=10)

        move_up_button = Button(button_frame, text="Move Up", command=up)
        move_up_button.grid(row=0, column=4, padx=10, pady=10)

        move_down_button = Button(button_frame, text="Move Down", command=down)
        move_down_button.grid(row=0, column=5, padx=10, pady=10)

        select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
        select_record_button.grid(row=0, column=6, padx=10, pady=10)

        def previous_page():
            quiz_management_panel_frame.destroy()
            AdminPanel(root)

        previous_page_button = Button(button_frame, text="Previous Page", command=previous_page)
        previous_page_button.grid(row=0, column=7, padx=10, pady=10)

        # Bind the treeview
        my_tree.bind("<ButtonRelease-1>", select_record)

        # Run to pull data from database on start
        query_database()


class QuestionManagement:

    def __init__(self, root):
        question_management_panel_frame = Frame(root)
        question_management_panel_frame.pack(fill='both', expand=1)

        root.title("Question Management Panel")
        root.geometry('355x170')

        def mc_question_management_panel():
            question_management_panel_frame.destroy()
            MCQuestionManagement(root)

        def tf_question_management_panel():
            question_management_panel_frame.destroy()
            TFQuestionManagement(root)

        def fb_question_management_panel():
            question_management_panel_frame.destroy()
            FBQuestionManagement(root)

        def previous_page():
            question_management_panel_frame.destroy()
            AdminPanel(root)

        Button(question_management_panel_frame, text='Multiple Choice Question Management',
               command=mc_question_management_panel, width=33).place(x=10, y=10)
        Button(question_management_panel_frame, text='True and False Question Management', width=33,
               command=tf_question_management_panel).place(x=10, y=50)
        Button(question_management_panel_frame, text='Fill in the Blank Question Management', width=33,
               command=fb_question_management_panel).place(x=10, y=90)
        Button(question_management_panel_frame, text='Previous Page', command=previous_page, width=33).place(x=10,
                                                                                                             y=130)


class MCQuestionManagement:

    def __init__(self, root):
        mc_question_management_panel_frame = Frame(root)
        mc_question_management_panel_frame.pack(fill='both', expand=1)

        root.title("Multiple Choice Question Management Panel")
        root.geometry('1490x700')

        def query_database():
            # Clear the Treeview
            for record in my_tree.get_children():
                my_tree.delete(record)

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            c = conn.cursor()
            # print(conn)

            query = "SELECT * FROM questionsMC INNER JOIN quizzes ON questionsMC.quizID = quizzes.id INNER JOIN topics ON quizzes.topicID = topics.id INNER JOIN modules ON topics.moduleID = modules.id;"

            c.execute(query)
            records = c.fetchall()

            # Add our data to the screen
            global count
            count = 0

            for record in records:
                if count % 2 == 0:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(
                            record[0], record[18], record[15], record[12], record[2], record[4], record[5], record[6],
                            record[7], record[8]),
                        tags=("evenrow",)
                    )
                else:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(
                            record[0], record[18], record[15], record[12], record[2], record[4], record[5], record[6],
                            record[7], record[8]),
                        tags=("oddrow",)
                    )

                # increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        # Add Some Style
        style = ttk.Style()

        # Pick A Theme
        style.theme_use('default')

        # Configure the Treeview Colors
        style.configure(
            "Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
        )

        # Create a Treeview Frame
        tree_frame = Frame(mc_question_management_panel_frame)
        tree_frame.pack(pady=10)

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        my_tree.pack()

        # Configure the Scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define Our Columns
        my_tree['columns'] = (
            "ID", "Module Name", "Topic Name", "Quiz Name", "Question", "Option A", "Option B", "Option C", "Option D",
            "Answer")

        # Format Our Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("ID", anchor=W, width=50)
        my_tree.column("Module Name", anchor=W, width=140)
        my_tree.column("Quiz Name", anchor=W, width=140)
        my_tree.column("Topic Name", anchor=W, width=140)
        my_tree.column("Question", anchor=W, width=140)
        my_tree.column("Option A", anchor=W, width=140)
        my_tree.column("Option B", anchor=W, width=140)
        my_tree.column("Option C", anchor=W, width=140)
        my_tree.column("Option D", anchor=W, width=140)
        my_tree.column("Answer", anchor=W, width=140)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("ID", text="ID", anchor=W)
        my_tree.heading("Module Name", text="Module Name", anchor=W)
        my_tree.heading("Quiz Name", text="Quiz Name", anchor=W)
        my_tree.heading("Topic Name", text="Topic Name", anchor=W)
        my_tree.heading("Question", text="Question", anchor=W)
        my_tree.heading("Option A", text="Option A", anchor=W)
        my_tree.heading("Option B", text="Option B", anchor=W)
        my_tree.heading("Option C", text="Option C", anchor=W)
        my_tree.heading("Option D", text="Option D", anchor=W)
        my_tree.heading("Answer", text="Answer", anchor=W)

        # Add Record Entry Boxes
        data_frame = LabelFrame(mc_question_management_panel_frame, text="Record")
        data_frame.pack(fill="x", expand="yes", padx=20)

        id_label = Label(data_frame, text="ID")
        id_label.grid(row=0, column=0, padx=10, pady=10)
        id_entry = Entry(data_frame)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        # QUIZ MENU START #

        conn = connect(
            host="auth-db582.hostinger.com",
            user="u998717846_test_user",
            password="7$Mw9Q=e",
            database="u998717846_python_test"
        )

        query = "SELECT * FROM topics INNER JOIN modules ON topics.moduleID = modules.id INNER JOIN quizzes ON topics.id = quizzes.topicID"

        c = conn.cursor()
        c.execute(query)
        records = c.fetchall()

        # Datatype of menu text
        quiz_menu = StringVar()

        quiz_list = dict()
        for record in records:
            quiz_list[record[6]] = record[8]

        quiz_name_label = Label(data_frame, text="Quiz Name")
        quiz_name_label.grid(row=0, column=2, padx=10, pady=10)
        quiz_name_menu = OptionMenu(data_frame, quiz_menu, *quiz_list.values())
        quiz_menu.set("Select Quiz")
        quiz_name_menu.grid(row=0, column=3, padx=10, pady=10)

        # QUIZ MENU END #

        # Add Question Entry Boxes
        question_frame = LabelFrame(mc_question_management_panel_frame, text="Question")
        question_frame.pack(fill="x", expand="yes", padx=20)

        question_label = Label(question_frame, text="Question")
        question_label.grid(row=0, column=0, padx=10, pady=10)
        question_entry = Entry(question_frame, width=148)
        question_entry.grid(row=0, column=1, padx=10, pady=10)

        # Add Options Entry Boxes
        option_frame = LabelFrame(mc_question_management_panel_frame, text="Options & Answer")
        option_frame.pack(fill="x", expand="yes", padx=20)

        option_a_label = Label(option_frame, text="Option A")
        option_a_label.grid(row=0, column=0, padx=10, pady=10)
        option_a_entry = Entry(option_frame)
        option_a_entry.grid(row=0, column=1, padx=10, pady=10)

        option_b_label = Label(option_frame, text="Option B")
        option_b_label.grid(row=0, column=2, padx=10, pady=10)
        option_b_entry = Entry(option_frame)
        option_b_entry.grid(row=0, column=3, padx=10, pady=10)

        option_c_label = Label(option_frame, text="Option C")
        option_c_label.grid(row=0, column=4, padx=10, pady=10)
        option_c_entry = Entry(option_frame)
        option_c_entry.grid(row=0, column=5, padx=10, pady=10)

        option_d_label = Label(option_frame, text="Option D")
        option_d_label.grid(row=0, column=6, padx=10, pady=10)
        option_d_entry = Entry(option_frame)
        option_d_entry.grid(row=0, column=7, padx=10, pady=10)

        # datatype of menu text
        answer_entry = StringVar()

        answer_list = ['A', 'B', 'C', 'D']

        answer_label = Label(option_frame, text="Answer")
        answer_label.grid(row=0, column=8, padx=10, pady=10)
        answer_menu = OptionMenu(option_frame, answer_entry, *answer_list)
        answer_entry.set("Select Correct Answer")
        answer_menu.grid(row=0, column=9, padx=10, pady=10)

        # Move Row Up
        def up():
            rows = my_tree.selection()
            for row in rows:
                my_tree.move(row, my_tree.parent(row), my_tree.index(row) - 1)

        # Move Row Down
        def down():
            rows = my_tree.selection()
            for row in reversed(rows):
                my_tree.move(row, my_tree.parent(row), my_tree.index(row) + 1)

        # Clear entry boxes
        def clear_entries():
            # Clear entry boxes
            id_entry.delete(0, END)
            quiz_menu.set("Select Quiz")
            question_entry.delete(0, END)
            option_a_entry.delete(0, END)
            option_b_entry.delete(0, END)
            option_c_entry.delete(0, END)
            option_d_entry.delete(0, END)
            answer_entry.set("Select Correct Answer")

        # Select Record
        def select_record(e):
            # Clear entry boxes
            id_entry.delete(0, END)
            quiz_menu.set("Select Quiz")
            question_entry.delete(0, END)
            option_a_entry.delete(0, END)
            option_b_entry.delete(0, END)
            option_c_entry.delete(0, END)
            option_d_entry.delete(0, END)
            answer_entry.set("Select Correct Answer")

            # Grab record number
            selected = my_tree.focus()

            # Grab record values
            values = my_tree.item(selected, 'values')

            # Output to entry boxes
            id_entry.insert(0, values[0])
            quiz_menu.set(values[3])
            question_entry.insert(0, values[4])
            option_a_entry.insert(0, values[5])
            option_b_entry.insert(0, values[6])
            option_c_entry.insert(0, values[7])
            option_d_entry.insert(0, values[8])
            answer_entry.set(values[9])

        # Remove one record
        def remove_one():

            # If there is no selected record it will show the messagebox.showinfo()
            if len(my_tree.focus()) == 0:
                messagebox.showinfo("Warning!", "Please select the record you want to delete.")
                query_database()
                return

            x = my_tree.selection()[0]
            my_tree.delete(x)

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Execute query
            c.execute("DELETE FROM questionsMC WHERE id=" + id_entry.get())

            # Commit changes
            conn.commit()

            # Close connection
            conn.close()

            # Clear The Entry Boxes
            clear_entries()

            # Informative message box
            messagebox.showinfo("Deleted!", "Successfully deleted.")

        def remove_all():
            # Informative message box
            response = messagebox.askyesno("Warning!", "Are you sure?\nAll data will be deleted!")

            # Add logic for message box
            if response == 1:
                # Clear the Treeview
                for record in my_tree.get_children():
                    my_tree.delete(record)

                conn = connect(
                    host="auth-db582.hostinger.com",
                    user="u998717846_test_user",
                    password="7$Mw9Q=e",
                    database="u998717846_python_test"
                )

                # Create a cursor instance
                c = conn.cursor()

                # Execute query
                c.execute("TRUNCATE TABLE questionsMC")

                # Commit changes
                conn.commit()

                # Close connection
                conn.close()

                # Clear The Entry Boxes
                clear_entries()

                # Recreate The Table
                # create_table_again()

                # Informative message box
                messagebox.showinfo("Deleted!", "Successfully deleted.")

        # Add new record to database
        def add_record():

            # If there is no value at the entry boxes it will show the messagebox.showinfo()
            if quiz_menu.get() == "Select Quiz" or len(question_entry.get()) == 0 or len(
                    option_a_entry.get()) == 0 or len(option_b_entry.get()) == 0 or len(
                option_c_entry.get()) == 0 or len(option_d_entry.get()) == 0 or len(answer_entry.get()) == 0:
                messagebox.showinfo("Warning!", "Please enter all fields.")
                query_database()
                return

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Fetch selected quiz
            fetch_quiz = "SELECT * FROM quizzes WHERE quizName='{}'".format(quiz_menu.get())
            c.execute(fetch_quiz)
            quiz_result = c.fetchone()

            # Insert question
            insert_question = "INSERT INTO questionsMC (quizID, question, optionA, optionB, optionC, optionD, answer) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            value = (
                quiz_result[0], question_entry.get(), option_a_entry.get(), option_b_entry.get(), option_c_entry.get(),
                option_d_entry.get(),
                answer_entry.get())
            c.execute(insert_question, value)

            # Commit changes
            conn.commit()

            # Close connection
            conn.close()

            # Clear The Entry Boxes
            clear_entries()

            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_database()

        # Update record
        def update_record():

            # If there is no value at the entry boxes it will show the messagebox.showinfo()
            if quiz_menu.get() == "Select Quiz" or len(question_entry.get()) == 0 or len(
                    option_a_entry.get()) == 0 or len(option_b_entry.get()) == 0 or len(
                option_c_entry.get()) == 0 or len(option_d_entry.get()) == 0 or len(answer_entry.get()) == 0:
                messagebox.showinfo("Warning!", "Please enter all fields.")
                query_database()
                return

            # Grab the record number
            selected = my_tree.focus()

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Fetch selected quiz
            fetch_quiz = "SELECT * FROM quizzes WHERE quizName='{}'".format(quiz_menu.get())
            c.execute(fetch_quiz)
            quiz_result = c.fetchone()

            # Update question
            update_question = "UPDATE questionsMC SET quizID = %s, question = %s, optionA = %s, optionB = %s, optionC = %s, optionD = %s, answer = %s WHERE id = %s"
            value = (
                quiz_result[0], question_entry.get(), option_a_entry.get(), option_b_entry.get(), option_c_entry.get(),
                option_d_entry.get(), answer_entry.get(), id_entry.get())
            c.execute(update_question, value)

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            # Update record
            my_tree.item(selected, text="", values=(
                quiz_result[0], question_entry.get(), option_a_entry.get(), option_b_entry.get(), option_c_entry.get(),
                answer_entry.get()))

            # Clear The Entry Boxes
            clear_entries()

            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_database()

        # Add Buttons
        button_frame = LabelFrame(mc_question_management_panel_frame, text="Commands")
        button_frame.pack(fill="x", expand="yes", padx=20)

        add_button = Button(button_frame, text="Add Record", command=add_record)
        add_button.grid(row=0, column=0, padx=10, pady=10)

        update_button = Button(button_frame, text="Update Record", command=update_record)
        update_button.grid(row=0, column=1, padx=10, pady=10)

        remove_one_button = Button(button_frame, text="Remove Selected", command=remove_one)
        remove_one_button.grid(row=0, column=2, padx=10, pady=10)

        remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
        remove_all_button.grid(row=0, column=3, padx=10, pady=10)

        move_up_button = Button(button_frame, text="Move Up", command=up)
        move_up_button.grid(row=0, column=4, padx=10, pady=10)

        move_down_button = Button(button_frame, text="Move Down", command=down)
        move_down_button.grid(row=0, column=5, padx=10, pady=10)

        select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
        select_record_button.grid(row=0, column=6, padx=10, pady=10)

        def previous_page():
            mc_question_management_panel_frame.destroy()
            QuestionManagement(root)

        previous_page_button = Button(button_frame, text="Previous Page", command=previous_page)
        previous_page_button.grid(row=0, column=7, padx=10, pady=10)

        # Bind the treeview
        my_tree.bind("<ButtonRelease-1>", select_record)

        # Run to pull data from database on start
        query_database()


class TFQuestionManagement:

    def __init__(self, root):
        tf_question_management_panel_frame = Frame(root)
        tf_question_management_panel_frame.pack(fill='both', expand=1)

        root.title("True and False Question Management Panel")
        root.geometry('1490x700')

        def query_database():
            # Clear the Treeview
            for record in my_tree.get_children():
                my_tree.delete(record)

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            c = conn.cursor()
            # print(conn)

            query = "SELECT * FROM questionsTF INNER JOIN quizzes ON questionsTF.quizID = quizzes.id INNER JOIN topics ON quizzes.topicID = topics.id INNER JOIN modules ON topics.moduleID = modules.id;"

            c.execute(query)
            records = c.fetchall()

            # Add our data to the screen
            global count
            count = 0

            for record in records:
                if count % 2 == 0:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(
                            record[0], record[16], record[13], record[10], record[2], record[4], record[5], record[6]),
                        tags=("evenrow",)
                    )
                else:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(
                            record[0], record[16], record[13], record[10], record[2], record[4], record[5], record[6]),
                        tags=("oddrow",)
                    )

                # increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        # Add Some Style
        style = ttk.Style()

        # Pick A Theme
        style.theme_use('default')

        # Configure the Treeview Colors
        style.configure(
            "Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
        )

        # Create a Treeview Frame
        tree_frame = Frame(tf_question_management_panel_frame)
        tree_frame.pack(pady=10)

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        my_tree.pack()

        # Configure the Scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define Our Columns
        my_tree['columns'] = ("ID", "Module Name", "Topic Name", "Quiz Name", "Question", "False", "True", "Answer")

        # Format Our Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("ID", anchor=W, width=50)
        my_tree.column("Module Name", anchor=W, width=140)
        my_tree.column("Quiz Name", anchor=W, width=140)
        my_tree.column("Topic Name", anchor=W, width=140)
        my_tree.column("Question", anchor=W, width=140)
        my_tree.column("True", anchor=W, width=140)
        my_tree.column("False", anchor=W, width=140)
        my_tree.column("Answer", anchor=W, width=140)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("ID", text="ID", anchor=W)
        my_tree.heading("Module Name", text="Module Name", anchor=W)
        my_tree.heading("Quiz Name", text="Quiz Name", anchor=W)
        my_tree.heading("Topic Name", text="Topic Name", anchor=W)
        my_tree.heading("Question", text="Question", anchor=W)
        my_tree.heading("True", text="True", anchor=W)
        my_tree.heading("False", text="False", anchor=W)
        my_tree.heading("Answer", text="Answer", anchor=W)

        # Add Record Entry Boxes
        data_frame = LabelFrame(tf_question_management_panel_frame, text="Record")
        data_frame.pack(fill="x", expand="yes", padx=20)

        id_label = Label(data_frame, text="ID")
        id_label.grid(row=0, column=0, padx=10, pady=10)
        id_entry = Entry(data_frame)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        # QUIZ MENU START #

        conn = connect(
            host="auth-db582.hostinger.com",
            user="u998717846_test_user",
            password="7$Mw9Q=e",
            database="u998717846_python_test"
        )

        query = "SELECT * FROM topics INNER JOIN modules ON topics.moduleID = modules.id INNER JOIN quizzes ON topics.id = quizzes.topicID"

        c = conn.cursor()
        c.execute(query)
        records = c.fetchall()

        # datatype of menu text
        quiz_menu = StringVar()

        quiz_list = dict()
        for record in records:
            quiz_list[record[6]] = record[8]

        quiz_name_label = Label(data_frame, text="Quiz Name")
        quiz_name_label.grid(row=0, column=2, padx=10, pady=10)
        quiz_name_menu = OptionMenu(data_frame, quiz_menu, *quiz_list.values())
        quiz_menu.set("Select Quiz")
        quiz_name_menu.grid(row=0, column=3, padx=10, pady=10)

        # QUIZ MENU END #

        # Add Question Entry Boxes
        question_frame = LabelFrame(tf_question_management_panel_frame, text="Question")
        question_frame.pack(fill="x", expand="yes", padx=20)

        question_label = Label(question_frame, text="Question")
        question_label.grid(row=0, column=0, padx=10, pady=10)
        question_entry = Entry(question_frame, width=148)
        question_entry.grid(row=0, column=1, padx=10, pady=10)

        # Add Options Entry Boxes
        option_frame = LabelFrame(tf_question_management_panel_frame, text="Options & Answer")
        option_frame.pack(fill="x", expand="yes", padx=20)

        true_label = Label(option_frame, text="True")
        true_label.grid(row=0, column=0, padx=10, pady=10)
        true_entry = Entry(option_frame)
        true_entry.grid(row=0, column=1, padx=10, pady=10)

        false_label = Label(option_frame, text="False")
        false_label.grid(row=0, column=2, padx=10, pady=10)
        false_entry = Entry(option_frame)
        false_entry.grid(row=0, column=3, padx=10, pady=10)

        answer_label = Label(option_frame, text="Answer")
        answer_label.grid(row=0, column=4, padx=10, pady=10)
        answer_entry = Entry(option_frame)
        answer_entry.grid(row=0, column=5, padx=10, pady=10)

        # Move Row Up
        def up():
            rows = my_tree.selection()
            for row in rows:
                my_tree.move(row, my_tree.parent(row), my_tree.index(row) - 1)

        # Move Row Down
        def down():
            rows = my_tree.selection()
            for row in reversed(rows):
                my_tree.move(row, my_tree.parent(row), my_tree.index(row) + 1)

        # Clear entry boxes
        def clear_entries():
            # Clear entry boxes
            id_entry.delete(0, END)
            quiz_menu.set("Select Quiz")
            question_entry.delete(0, END)
            true_entry.delete(0, END)
            false_entry.delete(0, END)
            answer_entry.delete(0, END)

        # Select Record
        def select_record(e):
            # Clear entry boxes
            id_entry.delete(0, END)
            quiz_menu.set("Select Quiz")
            question_entry.delete(0, END)
            true_entry.delete(0, END)
            false_entry.delete(0, END)
            answer_entry.delete(0, END)

            # Grab record number
            selected = my_tree.focus()

            # Grab record values
            values = my_tree.item(selected, 'values')

            # Output to entry boxes
            id_entry.insert(0, values[0])
            quiz_menu.set(values[3])
            question_entry.insert(0, values[4])
            true_entry.insert(0, values[5])
            false_entry.insert(0, values[6])
            answer_entry.insert(0, values[7])

        # Remove one record
        def remove_one():

            # If there is no selected record it will show the messagebox.showinfo()
            if len(my_tree.focus()) == 0:
                messagebox.showinfo("Warning!", "Please select the record you want to delete.")
                query_database()
                return

            x = my_tree.selection()[0]
            my_tree.delete(x)

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Execute query
            c.execute("DELETE FROM questionsTF WHERE id=" + id_entry.get())

            # Commit changes
            conn.commit()

            # Close connection
            conn.close()

            # Clear The Entry Boxes
            clear_entries()

            # Informative message box
            messagebox.showinfo("Deleted!", "Successfully deleted.")

        def remove_all():
            # Informative message box
            response = messagebox.askyesno("Warning!", "Are you sure?\nAll data will be deleted!")

            # Add logic for message box
            if response == 1:
                # Clear the Treeview
                for record in my_tree.get_children():
                    my_tree.delete(record)

                conn = connect(
                    host="auth-db582.hostinger.com",
                    user="u998717846_test_user",
                    password="7$Mw9Q=e",
                    database="u998717846_python_test"
                )

                # Create a cursor instance
                c = conn.cursor()

                # Execute query
                c.execute("TRUNCATE TABLE questionsTF")

                # Commit changes
                conn.commit()

                # Close connection
                conn.close()

                # Clear The Entry Boxes
                clear_entries()

                # Recreate The Table
                # create_table_again()

                # Informative message box
                messagebox.showinfo("Deleted!", "Successfully deleted.")

        # Add new record to database
        def add_record():

            # If there is no value at the entry boxes it will show the messagebox.showinfo()
            if quiz_menu.get() == "Select Quiz" or len(question_entry.get()) == 0 or len(
                    true_entry.get()) == 0 or len(false_entry.get()) == 0 or len(
                answer_entry.get()) == 0:
                messagebox.showinfo("Warning!", "Please enter all fields.")
                query_database()
                return

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Fetch selected quiz
            fetch_quiz = "SELECT * FROM quizzes WHERE quizName='{}'".format(quiz_menu.get())
            c.execute(fetch_quiz)
            quiz_result = c.fetchone()

            # Insert question
            insert_question = "INSERT INTO questionsTF (quizID, question, optionTrue, optionFalse, answer) VALUES (%s, %s, %s, %s, %s)"
            value = (quiz_result[0], question_entry.get(), true_entry.get(), false_entry.get(), answer_entry.get())
            c.execute(insert_question, value)

            # Commit changes
            conn.commit()

            # Close connection
            conn.close()

            # Clear The Entry Boxes
            clear_entries()

            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_database()

        # Update record
        def update_record():

            # If there is no value at the entry boxes it will show the messagebox.showinfo()
            if quiz_menu.get() == "Select Quiz" or len(question_entry.get()) == 0 or len(
                    true_entry.get()) == 0 or len(false_entry.get()) == 0 or len(
                answer_entry.get()) == 0:
                messagebox.showinfo("Warning!", "Please enter all fields.")
                query_database()
                return

            # Grab the record number
            selected = my_tree.focus()

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Fetch selected quiz
            fetch_quiz = "SELECT * FROM quizzes WHERE quizName='{}'".format(quiz_menu.get())
            c.execute(fetch_quiz)
            quiz_result = c.fetchone()

            # Update question
            update_question = "UPDATE questionsTF SET quizID = %s, question = %s, optionTrue = %s, optionFalse = %s, answer = %s WHERE id = %s"
            value = (quiz_result[0], question_entry.get(), true_entry.get(), false_entry.get(), answer_entry.get(),
                     id_entry.get())
            c.execute(update_question, value)

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            # Update record
            my_tree.item(selected, text="", values=(
                quiz_result[0], question_entry.get(), true_entry.get(), false_entry.get(), answer_entry.get()))

            # Clear The Entry Boxes
            clear_entries()

            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_database()

        # Add Buttons
        button_frame = LabelFrame(tf_question_management_panel_frame, text="Commands")
        button_frame.pack(fill="x", expand="yes", padx=20)

        add_button = Button(button_frame, text="Add Record", command=add_record)
        add_button.grid(row=0, column=0, padx=10, pady=10)

        update_button = Button(button_frame, text="Update Record", command=update_record)
        update_button.grid(row=0, column=1, padx=10, pady=10)

        remove_one_button = Button(button_frame, text="Remove Selected", command=remove_one)
        remove_one_button.grid(row=0, column=2, padx=10, pady=10)

        remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
        remove_all_button.grid(row=0, column=3, padx=10, pady=10)

        move_up_button = Button(button_frame, text="Move Up", command=up)
        move_up_button.grid(row=0, column=4, padx=10, pady=10)

        move_down_button = Button(button_frame, text="Move Down", command=down)
        move_down_button.grid(row=0, column=5, padx=10, pady=10)

        select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
        select_record_button.grid(row=0, column=6, padx=10, pady=10)

        def previous_page():
            tf_question_management_panel_frame.destroy()
            QuestionManagement(root)

        previous_page_button = Button(button_frame, text="Previous Page", command=previous_page)
        previous_page_button.grid(row=0, column=7, padx=10, pady=10)

        # Bind the treeview
        my_tree.bind("<ButtonRelease-1>", select_record)

        # Run to pull data from database on start
        query_database()


class FBQuestionManagement:

    def __init__(self, root):
        fb_question_management_panel_frame = Frame(root)
        fb_question_management_panel_frame.pack(fill='both', expand=1)

        root.title("Fill in the Blank Question Management Panel")
        root.geometry('1490x700')

        def query_database():
            # Clear the Treeview
            for record in my_tree.get_children():
                my_tree.delete(record)

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            c = conn.cursor()
            # print(conn)

            query = "SELECT * FROM questionsFB INNER JOIN quizzes ON questionsFB.quizID = quizzes.id INNER JOIN topics ON quizzes.topicID = topics.id INNER JOIN modules ON topics.moduleID = modules.id;"

            c.execute(query)
            records = c.fetchall()

            # Add our data to the screen
            global count
            count = 0

            for record in records:
                if count % 2 == 0:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(record[0], record[14], record[11], record[8], record[2], record[4]),
                        tags=("evenrow",)
                    )
                else:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(record[0], record[14], record[11], record[8], record[2], record[4]),
                        tags=("oddrow",)
                    )

                # increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        # Add Some Style
        style = ttk.Style()

        # Pick A Theme
        style.theme_use('default')

        # Configure the Treeview Colors
        style.configure(
            "Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
        )

        # Create a Treeview Frame
        tree_frame = Frame(fb_question_management_panel_frame)
        tree_frame.pack(pady=10)

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        my_tree.pack()

        # Configure the Scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define Our Columns
        my_tree['columns'] = ("ID", "Module Name", "Topic Name", "Quiz Name", "Question", "Answer")

        # Format Our Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("ID", anchor=W, width=50)
        my_tree.column("Module Name", anchor=W, width=140)
        my_tree.column("Quiz Name", anchor=W, width=140)
        my_tree.column("Topic Name", anchor=W, width=140)
        my_tree.column("Question", anchor=W, width=140)
        my_tree.column("Answer", anchor=W, width=140)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("ID", text="ID", anchor=W)
        my_tree.heading("Module Name", text="Module Name", anchor=W)
        my_tree.heading("Quiz Name", text="Quiz Name", anchor=W)
        my_tree.heading("Topic Name", text="Topic Name", anchor=W)
        my_tree.heading("Question", text="Question", anchor=W)
        my_tree.heading("Answer", text="Answer", anchor=W)

        # Add Record Entry Boxes
        data_frame = LabelFrame(fb_question_management_panel_frame, text="Record")
        data_frame.pack(fill="x", expand="yes", padx=20)

        id_label = Label(data_frame, text="ID")
        id_label.grid(row=0, column=0, padx=10, pady=10)
        id_entry = Entry(data_frame)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        # QUIZ MENU START #

        conn = connect(
            host="auth-db582.hostinger.com",
            user="u998717846_test_user",
            password="7$Mw9Q=e",
            database="u998717846_python_test"
        )

        query = "SELECT * FROM topics INNER JOIN modules ON topics.moduleID = modules.id INNER JOIN quizzes ON topics.id = quizzes.topicID"

        c = conn.cursor()
        c.execute(query)
        records = c.fetchall()

        # datatype of menu text
        quiz_menu = StringVar()

        quiz_list = dict()
        for record in records:
            quiz_list[record[6]] = record[8]

        quiz_name_label = Label(data_frame, text="Quiz Name")
        quiz_name_label.grid(row=0, column=2, padx=10, pady=10)
        quiz_name_menu = OptionMenu(data_frame, quiz_menu, *quiz_list.values())
        quiz_menu.set("Select Quiz")
        quiz_name_menu.grid(row=0, column=3, padx=10, pady=10)

        # QUIZ MENU END #

        # Add Question Entry Boxes
        question_frame = LabelFrame(fb_question_management_panel_frame, text="Question")
        question_frame.pack(fill="x", expand="yes", padx=20)

        question_label = Label(question_frame, text="Question")
        question_label.grid(row=0, column=0, padx=10, pady=10)
        question_entry = Entry(question_frame, width=148)
        question_entry.grid(row=0, column=1, padx=10, pady=10)

        # Add Options Entry Boxes
        option_frame = LabelFrame(fb_question_management_panel_frame, text="Options & Answer")
        option_frame.pack(fill="x", expand="yes", padx=20)

        answer_label = Label(option_frame, text="Answer")
        answer_label.grid(row=0, column=0, padx=10, pady=10)
        answer_entry = Entry(option_frame)
        answer_entry.grid(row=0, column=1, padx=10, pady=10)

        # Move Row Up
        def up():
            rows = my_tree.selection()
            for row in rows:
                my_tree.move(row, my_tree.parent(row), my_tree.index(row) - 1)

        # Move Row Down
        def down():
            rows = my_tree.selection()
            for row in reversed(rows):
                my_tree.move(row, my_tree.parent(row), my_tree.index(row) + 1)

        # Clear entry boxes
        def clear_entries():
            # Clear entry boxes
            id_entry.delete(0, END)
            quiz_menu.set("Select Quiz")
            question_entry.delete(0, END)
            answer_entry.delete(0, END)

        # Select Record
        def select_record(e):
            # Clear entry boxes
            id_entry.delete(0, END)
            quiz_menu.set("Select Quiz")
            question_entry.delete(0, END)
            answer_entry.delete(0, END)

            # Grab record number
            selected = my_tree.focus()

            # Grab record values
            values = my_tree.item(selected, 'values')

            # Output to entry boxes
            id_entry.insert(0, values[0])
            quiz_menu.set(values[3])
            question_entry.insert(0, values[4])
            answer_entry.insert(0, values[5])

        # Remove one record
        def remove_one():

            # If there is no selected record it will show the messagebox.showinfo()
            if len(my_tree.focus()) == 0:
                messagebox.showinfo("Warning!", "Please select the record you want to delete.")
                query_database()
                return

            x = my_tree.selection()[0]
            my_tree.delete(x)

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Execute query
            c.execute("DELETE FROM questionsFB WHERE id=" + id_entry.get())

            # Commit changes
            conn.commit()

            # Close connection
            conn.close()

            # Clear The Entry Boxes
            clear_entries()

            # Informative message box
            messagebox.showinfo("Deleted!", "Successfully deleted.")

        def remove_all():
            # Informative message box
            response = messagebox.askyesno("Warning!", "Are you sure?\nAll data will be deleted!")

            # Add logic for message box
            if response == 1:
                # Clear the Treeview
                for record in my_tree.get_children():
                    my_tree.delete(record)

                conn = connect(
                    host="auth-db582.hostinger.com",
                    user="u998717846_test_user",
                    password="7$Mw9Q=e",
                    database="u998717846_python_test"
                )

                # Create a cursor instance
                c = conn.cursor()

                # Execute query
                c.execute("TRUNCATE TABLE questionsFB")

                # Commit changes
                conn.commit()

                # Close connection
                conn.close()

                # Clear The Entry Boxes
                clear_entries()

                # Recreate The Table
                # create_table_again()

                # Informative message box
                messagebox.showinfo("Deleted!", "Successfully deleted.")

        # Add new record to database
        def add_record():

            # If there is no value at the entry boxes it will show the messagebox.showinfo()
            if quiz_menu.get() == "Select Quiz" or len(question_entry.get()) == 0 or len(
                    answer_entry.get()) == 0:
                messagebox.showinfo("Warning!", "Please enter all fields.")
                query_database()
                return

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Fetch selected quiz
            fetch_quiz = "SELECT * FROM quizzes WHERE quizName='{}'".format(quiz_menu.get())
            c.execute(fetch_quiz)
            quiz_result = c.fetchone()

            # Insert question
            insert_question = "INSERT INTO questionsFB (quizID, question, answer) VALUES (%s, %s, %s)"
            value = (quiz_result[0], question_entry.get(), answer_entry.get())
            c.execute(insert_question, value)

            # Commit changes
            conn.commit()

            # Close connection
            conn.close()

            # Clear The Entry Boxes
            clear_entries()

            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_database()

        # Update record
        def update_record():

            # If there is no value at the entry boxes it will show the messagebox.showinfo()
            if quiz_menu.get() == "Select Quiz" or len(question_entry.get()) == 0 or len(
                    answer_entry.get()) == 0:
                messagebox.showinfo("Warning!", "Please enter all fields.")
                query_database()
                return

            # Grab the record number
            selected = my_tree.focus()

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            # Fetch selected quiz
            fetch_quiz = "SELECT * FROM quizzes WHERE quizName='{}'".format(quiz_menu.get())
            c.execute(fetch_quiz)
            quiz_result = c.fetchone()

            # Update question
            update_question = "UPDATE questionsFB SET quizID = %s, question = %s, answer = %s WHERE id = %s"
            value = (quiz_result[0], question_entry.get(), answer_entry.get(), id_entry.get())
            c.execute(update_question, value)

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

            # Update record
            my_tree.item(selected, text="", values=(
                quiz_result[0], question_entry.get(), answer_entry.get()))

            # Clear The Entry Boxes
            clear_entries()

            # Clear The Treeview Table
            my_tree.delete(*my_tree.get_children())

            # Run to pull data from database on start
            query_database()

        # Add Buttons
        button_frame = LabelFrame(fb_question_management_panel_frame, text="Commands")
        button_frame.pack(fill="x", expand="yes", padx=20)

        add_button = Button(button_frame, text="Add Record", command=add_record)
        add_button.grid(row=0, column=0, padx=10, pady=10)

        update_button = Button(button_frame, text="Update Record", command=update_record)
        update_button.grid(row=0, column=1, padx=10, pady=10)

        remove_one_button = Button(button_frame, text="Remove Selected", command=remove_one)
        remove_one_button.grid(row=0, column=2, padx=10, pady=10)

        remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
        remove_all_button.grid(row=0, column=3, padx=10, pady=10)

        move_up_button = Button(button_frame, text="Move Up", command=up)
        move_up_button.grid(row=0, column=4, padx=10, pady=10)

        move_down_button = Button(button_frame, text="Move Down", command=down)
        move_down_button.grid(row=0, column=5, padx=10, pady=10)

        select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
        select_record_button.grid(row=0, column=6, padx=10, pady=10)

        def previous_page():
            fb_question_management_panel_frame.destroy()
            QuestionManagement(root)

        previous_page_button = Button(button_frame, text="Previous Page", command=previous_page)
        previous_page_button.grid(row=0, column=7, padx=10, pady=10)

        # Bind the treeview
        my_tree.bind("<ButtonRelease-1>", select_record)

        # Run to pull data from database on start
        query_database()


class StudentPanel:

    def __init__(self, root):
        student_panel_frame = Frame(root)
        student_panel_frame.pack(fill='both', expand=1)

        root.title("Student Panel")
        root.geometry('355x130')

        def my_reports():
            student_panel_frame.destroy()
            MyReports(root)

        # Take the quiz tested by Chisel
        def take_a_quiz():
            student_panel_frame.destroy()
            abc = QuizList(root)
            abc.get_list()

        def logout():
            are_you_sure = messagebox.askyesno("Alert", "Are you sure you want to logout?")
            if are_you_sure:
                student_panel_frame.destroy()
                Main(root)

        Button(student_panel_frame, text='My Reports', width=33, command=my_reports).place(x=10, y=10)
        Button(student_panel_frame, text='Take a quiz', width=33, command=take_a_quiz).place(x=10, y=50)
        Button(student_panel_frame, text='Logout', command=logout, width=33).place(x=10, y=90)


class MyReports:

    def __init__(self, root):
        my_reports_panel_frame = Frame(root)
        my_reports_panel_frame.pack(fill='both', expand=1)

        root.title("My Reports")
        root.geometry('1150x400')

        def query_database():
            # Clear the Treeview
            for record in my_tree.get_children():
                my_tree.delete(record)

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            c = conn.cursor()
            # print(conn)

            query = "SELECT * FROM reports INNER JOIN quizzes ON reports.quizID = quizzes.id INNER JOIN topics ON quizzes.topicID = topics.id INNER JOIN modules ON topics.moduleID = modules.id WHERE studentID='{}'".format(
                usernameEntry.get())

            c.execute(query)
            records = c.fetchall()

            if not records:
                messagebox.showinfo("Warning!", "You have not taken a quiz yet.")
                my_reports_panel_frame.destroy()
                StudentPanel(root)
                return

            # Add our data to the screen
            global count
            count = 0

            for record in records:

                if count % 2 == 0:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(
                        record[17], record[14], record[11], record[3], record[4], record[5], record[6], record[7],
                        record[8].strftime("%d/%m/%Y %H:%M")),
                        tags=("evenrow",)
                    )
                else:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(
                        record[17], record[14], record[11], record[3], record[4], record[5], record[6], record[7],
                        record[8].strftime("%d/%m/%Y %H:%M")),
                        tags=("oddrow",)
                    )

                # increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        # Add Some Style
        style = ttk.Style()

        # Pick A Theme
        style.theme_use('default')

        # Configure the Treeview Colors
        style.configure(
            "Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
        )

        # Create a Treeview Frame
        tree_frame = Frame(my_reports_panel_frame)
        tree_frame.pack(pady=10)

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        my_tree.pack()

        # Configure the Scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define Our Columns
        my_tree['columns'] = (
        "Module Name", "Topic Name", "Quiz Name", "Total Score", "Average Score", "Lowest Score", "Highest Score",
        "Attempts", "Attempt Date")

        # Format Our Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Module Name", anchor=W, width=140)
        my_tree.column("Topic Name", anchor=W, width=140)
        my_tree.column("Quiz Name", anchor=W, width=150)
        my_tree.column("Total Score", anchor=W, width=100)
        my_tree.column("Average Score", anchor=W, width=100)
        my_tree.column("Lowest Score", anchor=W, width=100)
        my_tree.column("Highest Score", anchor=W, width=100)
        my_tree.column("Attempts", anchor=W, width=100)
        my_tree.column("Attempt Date", anchor=W, width=140)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("Module Name", text="Module Name", anchor=W)
        my_tree.heading("Topic Name", text="Topic Name", anchor=W)
        my_tree.heading("Quiz Name", text="Quiz Name", anchor=W)
        my_tree.heading("Total Score", text="Total Score", anchor=W)
        my_tree.heading("Average Score", text="Average Score", anchor=W)
        my_tree.heading("Lowest Score", text="Lowest Score", anchor=W)
        my_tree.heading("Highest Score", text="Highest Score", anchor=W)
        my_tree.heading("Attempts", text="Attempts", anchor=W)
        my_tree.heading("Attempt Date", text="Attempt Date", anchor=W)

        # If user click on previous page button it will take the frames to back.
        def previous_page():
            my_reports_panel_frame.destroy()
            StudentPanel(root)

        # It will download the report as a PDF file.
        def download_pdf():
            # Create instance of FPDF class
            # Letter size paper, use inches as unit of measure
            pdf = FPDF(format='letter', unit='in', orientation='L')

            # Add new page. Without this you cannot create the document.
            pdf.add_page()

            # Remember to always put one of these at least once.
            pdf.set_font('Times', '', 10.0)

            # Effective page width, or just epw
            epw = pdf.w - 2 * pdf.l_margin

            # Set column width to 1/4 of effective page width to distribute content
            # evenly across table and page
            col_width = epw / 6

            # Since we do not need to draw lines anymore, there is no need to separate
            # headers from data matrix.

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            # Create a cursor instance
            c = conn.cursor()

            query = "SELECT moduleName, quizName, averagescore, lowestscore, highestscore, attemptdate FROM reports INNER JOIN quizzes ON reports.quizID = quizzes.id INNER JOIN topics ON quizzes.topicID = topics.id INNER JOIN modules ON topics.moduleID = modules.id WHERE studentID='{}'".format(
                usernameEntry.get())

            c.execute(query)
            reports = c.fetchall()

            data = [
                ["Module Name", "Quiz Name", "Average Score", "Lowest Score", "Highest Score", "Attempt Date"]
            ]

            for rows in reports:
                data.append(rows)

            # Document title centered, bold, 14 pt
            pdf.set_font('Times', 'B', 14.0)
            pdf.cell(epw, 0.0, 'My Reports', align='C')
            pdf.set_font('Times', '', 10.0)

            # Text height is the same as current font size
            th = pdf.font_size

            pdf.set_font('Times', 'B', 14.0)
            pdf.set_font('Times', '', 10.0)
            pdf.ln(0.5)

            # Here we add more padding by passing 2*th as height
            for row in data:
                for datum in row:
                    # Enter data in columns
                    pdf.cell(col_width, 2 * th, str(datum), border=1)

                pdf.ln(2 * th)

            pdf.output('my_reports.pdf', 'F')
            messagebox.showinfo("Successful",
                                "Your report has been saved to the directory of the program file as my_reports.pdf file.")

        # It will download most seen questions as a PDF file.
        def most_seen_questions():
            my_reports_panel_frame.destroy()
            MostSeenQuestions(root)

        # Add Buttons
        button_frame = LabelFrame(my_reports_panel_frame)
        button_frame.pack(fill="x", expand=1, padx=20)

        previous_page_button = Button(button_frame, text="Previous Page", command=previous_page)
        previous_page_button.grid(row=0, column=0, padx=10, pady=10)

        download_pdf_button = Button(button_frame, text="Download PDF", command=download_pdf)
        download_pdf_button.grid(row=0, column=2, padx=10, pady=10)

        most_seen_question = Button(button_frame, text="Most Seen Questions", command=most_seen_questions)
        most_seen_question.grid(row=0, column=3, padx=10, pady=10)

        # Run to pull data from database on start
        query_database()


class MostSeenQuestions:

    def __init__(self, root):
        msq_panel_frame = Frame(root)
        msq_panel_frame.pack(fill='both', expand=1)

        root.title("Most Seen Questions")
        root.geometry('800x400')

        def query_database():
            # Clear the Treeview
            for record in my_tree.get_children():
                my_tree.delete(record)

            conn = connect(
                host="auth-db582.hostinger.com",
                user="u998717846_test_user",
                password="7$Mw9Q=e",
                database="u998717846_python_test"
            )

            c = conn.cursor()
            # print(conn)

            query = "SELECT * FROM questionsMC ORDER BY view DESC"

            c.execute(query)
            records = c.fetchall()

            if not records:
                messagebox.showinfo("Warning!", "You have not taken a quiz yet.")
                msq_panel_frame.destroy()
                StudentPanel(root)
                return

            # Add our data to the screen
            global count
            count = 0

            for record in records:

                if count % 2 == 0:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(record[2], record[9]),
                        tags=("evenrow",)
                    )
                else:
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        values=(record[2], record[9]),
                        tags=("oddrow",)
                    )

                # increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        # Add Some Style
        style = ttk.Style()

        # Pick A Theme
        style.theme_use('default')

        # Configure the Treeview Colors
        style.configure(
            "Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
        )

        # Create a Treeview Frame
        tree_frame = Frame(msq_panel_frame)
        tree_frame.pack(pady=10)

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        my_tree.pack()

        # Configure the Scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define Our Columns
        my_tree['columns'] = ("Questions", "Number of views")

        # Format Our Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Questions", anchor=W, width=400)
        my_tree.column("Number of views", anchor=W, width=150)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("Questions", text="Questions", anchor=W)
        my_tree.heading("Number of views", text="Number of views", anchor=W)

        # If user click on previous page button it will take the frames to back.
        def previous_page():
            msq_panel_frame.destroy()
            MyReports(root)

        # It will download most seen questions as a PDF file.
        # def download_most_seen_questions():

        # Add Buttons
        button_frame = LabelFrame(msq_panel_frame)
        button_frame.pack(fill="x", expand=1, padx=20)

        previous_page_button = Button(button_frame, text="Previous Page", command=previous_page)
        previous_page_button.grid(row=0, column=0, padx=10, pady=10)

        # Run to pull data from database on start
        query_database()


class QuizList:

    def __init__(self, root):
        self.root = root

    def get_list(self):

        self.quiz_list_frame = Frame(self.root)
        self.quiz_list_frame.pack(fill='both', expand=1)

        self.root.title("Quiz List")
        self.root.geometry('825x400')
        self.selected_quiz = IntVar()

        # Add Some Style
        style = ttk.Style()

        # Pick A Theme
        style.theme_use('default')

        # Configure the Treeview Colors
        style.configure(
            "Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
        )

        # Create a Treeview Frame
        self.tree_frame = Frame(self.quiz_list_frame)
        self.tree_frame.pack(pady=10)

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(self.tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        self.my_tree.pack()

        # Configure the Scrollbar
        tree_scroll.config(command=self.my_tree.yview)

        # Define Our Columns
        self.my_tree['columns'] = ("ID", "Module Name", "Topic Name", "Quiz Name")

        # Format Our Columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("ID", anchor=W, width=50)
        self.my_tree.column("Module Name", anchor=W, width=140)
        self.my_tree.column("Topic Name", anchor=W, width=140)
        self.my_tree.column("Quiz Name", anchor=W, width=200)

        # Create Headings
        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("ID", text="ID", anchor=W)
        self.my_tree.heading("Module Name", text="Module Name", anchor=W)
        self.my_tree.heading("Topic Name", text="Topic Name", anchor=W)
        self.my_tree.heading("Quiz Name", text="Quiz Name", anchor=W)

        # Add Buttons
        self.button_frame = LabelFrame(self.quiz_list_frame)
        self.button_frame.pack(fill="x", expand=1, padx=20)

        self.previous_page_button = Button(self.button_frame, text="Previous Page", command=self.previous_page)
        self.previous_page_button.grid(row=0, column=0, padx=10, pady=10)

        self.start_mc_quiz_button = Button(self.button_frame, text="Start Multiple Choice Quiz",
                                           command=self.mc_question_quiz)
        self.start_mc_quiz_button.grid(row=0, column=1, padx=10, pady=10)

        self.start_tf_quiz_button = Button(self.button_frame, text="Start True and False Quiz",
                                           command=self.tf_question_quiz)
        self.start_tf_quiz_button.grid(row=0, column=2, padx=10, pady=10)

        self.start_fb_quiz_button = Button(self.button_frame, text="Start Fill in the Blank Quiz",
                                           command=self.fb_question_quiz)
        self.start_fb_quiz_button.grid(row=0, column=3, padx=10, pady=10)

        # Clear The Treeview Table
        self.my_tree.delete(*self.my_tree.get_children())

        # Run to pull data from database on start
        self.query_database()

    def query_database(self):
        # Clear the Treeview
        for record in self.my_tree.get_children():
            self.my_tree.delete(record)

        conn = connect(
            host="auth-db582.hostinger.com",
            user="u998717846_test_user",
            password="7$Mw9Q=e",
            database="u998717846_python_test"
        )

        c = conn.cursor()
        # print(conn)

        query = "SELECT * FROM quizzes INNER JOIN topics ON quizzes.topicID = topics.id INNER JOIN modules ON topics.moduleID = modules.id"

        c.execute(query)
        records = c.fetchall()

        # Add our data to the screen
        global count
        count = 0

        for record in records:
            if count % 2 == 0:
                self.my_tree.insert(
                    parent="",
                    index="end",
                    iid=count,
                    text="",
                    values=(record[0], record[8], record[5], record[2]),
                    tags=("evenrow",)
                )
            else:
                self.my_tree.insert(
                    parent="",
                    index="end",
                    iid=count,
                    text="",
                    values=(record[0], record[8], record[5], record[2]),
                    tags=("oddrow",)
                )

            # increment counter
            count += 1

        # Commit changes
        conn.commit()

        # Close our connection
        conn.close()

    def mc_question_quiz(self):

        # Grab quiz ID number
        selected = self.my_tree.focus()

        # Grab quiz ID values
        values = self.my_tree.item(selected, 'values')

        self.selected_quiz = values[0]
        # print(self.selected_quiz)

        self.quiz_list_frame.destroy()
        MCQuiz(self.root, self.selected_quiz)

    def tf_question_quiz(self):

        # Grab quiz ID number
        selected = self.my_tree.focus()

        # Grab quiz ID values
        values = self.my_tree.item(selected, 'values')

        self.selected_quiz = values[0]
        # print(self.selected_quiz)

        self.quiz_list_frame.destroy()
        TFQuiz(self.root, self.selected_quiz)

    def fb_question_quiz(self):

        # Grab quiz ID number
        selected = self.my_tree.focus()

        # Grab quiz ID values
        values = self.my_tree.item(selected, 'values')

        self.selected_quiz = values[0]
        # print(self.selected_quiz)

        self.quiz_list_frame.destroy()
        FBQuiz(self.root, self.selected_quiz)

    # If user click on previous page button it will take the frames to back
    def previous_page(self):
        self.quiz_list_frame.destroy()
        StudentPanel(self.root)


class MCQuiz(QuizList):

    def __init__(self, root, selected_quiz):
        self.selected_quiz = selected_quiz
        self.questions = []
        self.options = []

        self.mc_question_page_1 = Frame(root, width=33)
        self.mc_question_page_2 = Frame(root, width=33)
        self.mc_question_page_3 = Frame(root, width=33)
        self.mc_question_page_4 = Frame(root, width=33)
        self.mc_question_page_5 = Frame(root, width=33)
        self.mc_question_page_1.pack(fill='both', expand=1)

        root.title("Multiple Choice Quiz")
        root.geometry('700x400')

        super().__init__(root)

        # Normal version
        # print(self.get_tf_questions()[0][2])

        # Random Shuffle
        random.shuffle(self.get_mc_questions())
        random.shuffle(self.get_options(self.get_mc_questions()[0][0]))

        self.q1_value = StringVar()
        self.q2_value = StringVar()
        self.q3_value = StringVar()
        self.q4_value = StringVar()
        self.q5_value = StringVar()

        self.q1_value.set(0)
        self.q2_value.set(0)
        self.q3_value.set(0)
        self.q4_value.set(0)
        self.q5_value.set(0)

        # Question Labels
        self.question1_label = Label(self.mc_question_page_1, text='Q1: ' + self.get_mc_questions()[0][2],
                                     wraplength=650)
        self.question2_label = Label(self.mc_question_page_2, text='Q2: ' + self.get_mc_questions()[1][2],
                                     wraplength=650)
        self.question3_label = Label(self.mc_question_page_3, text='Q3: ' + self.get_mc_questions()[2][2],
                                     wraplength=650)
        self.question4_label = Label(self.mc_question_page_4, text='Q4: ' + self.get_mc_questions()[3][2],
                                     wraplength=650)
        self.question5_label = Label(self.mc_question_page_5, text='Q5: ' + self.get_mc_questions()[4][2],
                                     wraplength=650)
        self.question1_label.pack(fill='x', ipady=25)

        # Question Description Labels
        self.q1_description_label = Label(self.mc_question_page_1, text='Description: ' + self.get_mc_questions()[0][3],
                                          wraplength=650)
        self.q2_description_label = Label(self.mc_question_page_2, text='Description: ' + self.get_mc_questions()[1][3],
                                          wraplength=650)
        self.q3_description_label = Label(self.mc_question_page_3, text='Description: ' + self.get_mc_questions()[2][3],
                                          wraplength=650)
        self.q4_description_label = Label(self.mc_question_page_4, text='Description: ' + self.get_mc_questions()[3][3],
                                          wraplength=650)
        self.q5_description_label = Label(self.mc_question_page_5, text='Description: ' + self.get_mc_questions()[4][3],
                                          wraplength=650)

        # Next Buttons
        self.next_button_1 = Button(self.mc_question_page_1, text='Next',
                                    command=partial(self.change_frame, self.mc_question_page_1,
                                                    self.mc_question_page_2))
        self.next_button_2 = Button(self.mc_question_page_2, text='Next',
                                    command=partial(self.change_frame, self.mc_question_page_2,
                                                    self.mc_question_page_3))
        self.next_button_3 = Button(self.mc_question_page_3, text='Next',
                                    command=partial(self.change_frame, self.mc_question_page_3,
                                                    self.mc_question_page_4))
        self.next_button_4 = Button(self.mc_question_page_4, text='Next',
                                    command=partial(self.change_frame, self.mc_question_page_4,
                                                    self.mc_question_page_5))
        self.submit_button = Button(self.mc_question_page_5, text='Submit', command=self.submit)
        self.next_button_1.place(rely=1, relx=1, anchor="se")

        # Question 1
        self.q1_radio_list = []
        for q1_options in self.get_options(self.get_mc_questions()[0][0])[0]:
            self.q1_radio_button = Radiobutton(self.mc_question_page_1, text=q1_options, value=q1_options,
                                               variable=self.q1_value)

            self.q1_radio_list.append(self.q1_radio_button)
            self.q1_radio_button.pack()

        # Question 2
        self.question2_label.pack(fill='x', ipady=25)

        self.q2_radio_list = []
        for q2_options in self.get_options(self.get_mc_questions()[1][0])[0]:
            self.q2_radio_button = Radiobutton(self.mc_question_page_2, text=q2_options, value=q2_options,
                                               variable=self.q2_value)

            self.q2_radio_list.append(self.q2_radio_button)
            self.q2_radio_button.pack()

        self.next_button_2.place(rely=1, relx=1, anchor="se")

        # Question 3
        self.question3_label.pack(fill='x', ipady=25)

        self.q3_radio_list = []
        for q3_options in self.get_options(self.get_mc_questions()[2][0])[0]:
            self.q3_radio_button = Radiobutton(self.mc_question_page_3, text=q3_options, value=q3_options,
                                               variable=self.q3_value)

            self.q3_radio_list.append(self.q3_radio_button)
            self.q3_radio_button.pack()

        self.next_button_3.place(rely=1, relx=1, anchor="se")

        # Question 4
        self.question4_label.pack(fill='x', ipady=25)

        self.q4_radio_list = []
        for q4_options in self.get_options(self.get_mc_questions()[3][0])[0]:
            self.q4_radio_button = Radiobutton(self.mc_question_page_4, text=q4_options, value=q4_options,
                                               variable=self.q4_value)

            self.q4_radio_list.append(self.q4_radio_button)
            self.q4_radio_button.pack()

        self.next_button_4.place(rely=1, relx=1, anchor="se")

        # Question 5
        self.question5_label.pack(fill='x', ipady=25)

        self.q5_radio_list = []
        for q5_options in self.get_options(self.get_mc_questions()[4][0])[0]:
            self.q5_radio_button = Radiobutton(self.mc_question_page_5, text=q5_options, value=q5_options,
                                               variable=self.q5_value)

            self.q5_radio_list.append(self.q5_radio_button)
            self.q5_radio_button.pack()

        self.submit_button.place(rely=1, relx=1, anchor="se")
        self.exit_button = Button(self.mc_question_page_5, text='Exit', command=self.exit_quiz)

        # Previous Buttons
        self.previous_button_1 = Button(self.mc_question_page_2, text='Previous',
                                        command=partial(self.change_frame, self.mc_question_page_2,
                                                        self.mc_question_page_1))
        self.previous_button_2 = Button(self.mc_question_page_3, text='Previous',
                                        command=partial(self.change_frame, self.mc_question_page_3,
                                                        self.mc_question_page_2))
        self.previous_button_3 = Button(self.mc_question_page_4, text='Previous',
                                        command=partial(self.change_frame, self.mc_question_page_4,
                                                        self.mc_question_page_3))
        self.previous_button_4 = Button(self.mc_question_page_5, text='Previous',
                                        command=partial(self.change_frame, self.mc_question_page_5,
                                                        self.mc_question_page_4))
        self.previous_button_1.place(rely=1, relx=0, anchor="sw")
        self.previous_button_2.place(rely=1, relx=0, anchor="sw")
        self.previous_button_3.place(rely=1, relx=0, anchor="sw")
        self.previous_button_4.place(rely=1, relx=0, anchor="sw")

        self.correct = 0
        self.options = ['A', 'B', 'C', 'D']

    def change_frame(self, frame_to_forget, frame_to_pack):
        frame_to_forget.forget()
        frame_to_pack.pack(fill='both', expand=1)

    def submit(self):

        self.submit_button.destroy()
        self.exit_button.place(rely=1, relx=1, anchor="se")

        self.q1_description_label.pack(fill='x', ipady=25)
        self.q2_description_label.pack(fill='x', ipady=25)
        self.q3_description_label.pack(fill='x', ipady=25)
        self.q4_description_label.pack(fill='x', ipady=25)
        self.q5_description_label.pack(fill='x', ipady=25)

        for my_radio_list in [self.q1_radio_list, self.q2_radio_list, self.q3_radio_list, self.q4_radio_list,
                              self.q5_radio_list]:
            for radio_button in my_radio_list:
                radio_button.config(state=DISABLED)

        value_get_list = [
            self.q1_value.get(),
            self.q2_value.get(),
            self.q3_value.get(),
            self.q4_value.get(),
            self.q5_value.get()
        ]

        # DB Connection START

        conn = connect(
            host="auth-db582.hostinger.com",
            user="u998717846_test_user",
            password="7$Mw9Q=e",
            database="u998717846_python_test"
        )

        c = conn.cursor()

        # DB Connection END

        for index in range(5):
            option_index = 4

            for option in self.options:

                if self.get_mc_questions()[index][8] == option:
                    if self.get_mc_questions()[index][option_index] == value_get_list[index]:
                        self.correct += 1

                option_index += 1

            # Select the question from the database
            select_seen_value = "SELECT view FROM questionsMC WHERE id='{}'".format(
                self.get_mc_questions()[index][0])
            c.execute(select_seen_value)

            seen_value = c.fetchone()
            seen = seen_value[0]
            seen += 1

            # Update the view value on the database
            update_seen_value = "UPDATE questionsMC SET view='{}' WHERE id='{}'".format(seen, self.get_mc_questions()[index][0])
            c.execute(update_seen_value)
            conn.commit()

        # Select the report from the database
        select_report = "SELECT attempts, totalscore FROM reports WHERE studentID='{}' AND quizID='{}'".format(
            usernameEntry.get(), self.selected_quiz)
        c.execute(select_report)
        report = c.fetchone()

        score = self.correct

        if report:

            # Increase the attempt
            attempts = report[0]
            attempts += 1

            total_score = score + report[1]
            average_score = total_score / attempts

            # Update the report on the database
            update_report = "UPDATE reports SET totalscore='{}', averagescore='{}', attempts ='{}' WHERE studentID='{}' AND quizID='{}'".format(
                total_score, average_score, attempts, usernameEntry.get(), self.selected_quiz)
            c.execute(update_report)
            conn.commit()

            # Select the report from the database
            select_report = "SELECT highestscore, lowestscore FROM reports WHERE studentID='{}' AND quizID='{}'".format(
                usernameEntry.get(), self.selected_quiz)
            c.execute(select_report)
            scores = c.fetchone()

            highestscore = scores[0]
            lowestscore = scores[1]

            if score < lowestscore:
                lowestscore = score

            if score > highestscore:
                highestscore = score

            # Update the lowest and highest score on the database
            update_scores = "UPDATE reports SET highestscore='{}', lowestscore='{}' WHERE studentID='{}' AND quizID='{}'".format(
                highestscore, lowestscore, usernameEntry.get(), self.selected_quiz)

            c.execute(update_scores)
            conn.commit()

        else:

            # Insert a report to the database
            insert_report = "INSERT INTO reports (studentID, quizID, totalscore, averagescore, lowestscore, highestscore, attempts) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            report_value = (usernameEntry.get(), self.selected_quiz, score, score, 6, -1, 1)
            c.execute(insert_report, report_value)
            conn.commit()

            # Select the report from the database
            select_report = "SELECT highestscore, lowestscore FROM reports WHERE studentID='{}' AND quizID='{}'".format(
                usernameEntry.get(), self.selected_quiz)
            c.execute(select_report)
            scores = c.fetchone()

            highestscore = scores[0]
            lowestscore = scores[1]

            if score < lowestscore:
                lowestscore = score

            if score > highestscore:
                highestscore = score

            # Update the lowest and highest score on the database
            update_scores = "UPDATE reports SET highestscore='{}', lowestscore='{}' WHERE studentID='{}' AND quizID='{}'".format(
                highestscore, lowestscore, usernameEntry.get(), self.selected_quiz)

            c.execute(update_scores)
            conn.commit()

        # Display correct answer
        print(f"Your score is: {score}/5")
        messagebox.showinfo("Result", f"Your score is: {score}/5")
        conn.close()

    def get_mc_questions(self):

        conn = connect(
            host="auth-db582.hostinger.com",
            user="u998717846_test_user",
            password="7$Mw9Q=e",
            database="u998717846_python_test"
        )

        c = conn.cursor()
        # print(conn)

        query = "SELECT * FROM questionsMC WHERE quizID='{}'".format(self.selected_quiz)

        c.execute(query)

        my_list = c.fetchall()

        for question in my_list:
            self.questions.append(question)
        return self.questions

    def get_options(self, questionID):

        conn = connect(
            host="auth-db582.hostinger.com",
            user="u998717846_test_user",
            password="7$Mw9Q=e",
            database="u998717846_python_test"
        )

        c = conn.cursor()
        # print(conn)

        query = "SELECT optionA, optionB, optionC, optionD FROM questionsMC WHERE id='{}'".format(questionID)

        c.execute(query)

        my_list = c.fetchall()

        return my_list

    def exit_quiz(self):
        self.mc_question_page_1.destroy()
        self.mc_question_page_2.destroy()
        self.mc_question_page_3.destroy()
        self.mc_question_page_4.destroy()
        self.mc_question_page_5.destroy()
        StudentPanel(root)


class TFQuiz(QuizList):

    def __init__(self, root, selected_quiz):
        self.selected_quiz = selected_quiz
        self.questions = []
        self.options = []

        self.tf_question_page_1 = Frame(root, width=33)
        self.tf_question_page_2 = Frame(root, width=33)
        self.tf_question_page_3 = Frame(root, width=33)
        self.tf_question_page_4 = Frame(root, width=33)
        self.tf_question_page_5 = Frame(root, width=33)
        self.tf_question_page_1.pack(fill='both', expand=1)

        root.title("True and False Quiz")
        root.geometry('700x400')

        super().__init__(root)

        # Normal version
        # print(self.get_tf_questions()[0][2])

        # Random Shuffle
        random.shuffle(self.get_tf_questions())
        random.shuffle(self.get_options(self.get_tf_questions()[0][0]))

        self.q1_value = StringVar()
        self.q2_value = StringVar()
        self.q3_value = StringVar()
        self.q4_value = StringVar()
        self.q5_value = StringVar()

        self.q1_value.set(0)
        self.q2_value.set(0)
        self.q3_value.set(0)
        self.q4_value.set(0)
        self.q5_value.set(0)

        # Question Labels
        self.question1_label = Label(self.tf_question_page_1, text='Q1: ' + self.get_tf_questions()[0][2],
                                     wraplength=650)
        self.question2_label = Label(self.tf_question_page_2, text='Q2: ' + self.get_tf_questions()[1][2],
                                     wraplength=650)
        self.question3_label = Label(self.tf_question_page_3, text='Q3: ' + self.get_tf_questions()[2][2],
                                     wraplength=650)
        self.question4_label = Label(self.tf_question_page_4, text='Q4: ' + self.get_tf_questions()[3][2],
                                     wraplength=650)
        self.question5_label = Label(self.tf_question_page_5, text='Q5: ' + self.get_tf_questions()[4][2],
                                     wraplength=650)
        self.question1_label.pack(fill='x', ipady=25)

        # Question Description Labels
        self.q1_description_label = Label(self.tf_question_page_1, text='Description: ' + self.get_tf_questions()[0][3],
                                          wraplength=650)
        self.q2_description_label = Label(self.tf_question_page_2, text='Description: ' + self.get_tf_questions()[1][3],
                                          wraplength=650)
        self.q3_description_label = Label(self.tf_question_page_3, text='Description: ' + self.get_tf_questions()[2][3],
                                          wraplength=650)
        self.q4_description_label = Label(self.tf_question_page_4, text='Description: ' + self.get_tf_questions()[3][3],
                                          wraplength=650)
        self.q5_description_label = Label(self.tf_question_page_5, text='Description: ' + self.get_tf_questions()[4][3],
                                          wraplength=650)

        # Next Buttons
        self.next_button_1 = Button(self.tf_question_page_1, text='Next',
                                    command=partial(self.change_frame, self.tf_question_page_1,
                                                    self.tf_question_page_2))
        self.next_button_2 = Button(self.tf_question_page_2, text='Next',
                                    command=partial(self.change_frame, self.tf_question_page_2,
                                                    self.tf_question_page_3))
        self.next_button_3 = Button(self.tf_question_page_3, text='Next',
                                    command=partial(self.change_frame, self.tf_question_page_3,
                                                    self.tf_question_page_4))
        self.next_button_4 = Button(self.tf_question_page_4, text='Next',
                                    command=partial(self.change_frame, self.tf_question_page_4,
                                                    self.tf_question_page_5))
        self.submit_button = Button(self.tf_question_page_5, text='Submit', command=self.submit)
        self.next_button_1.place(rely=1, relx=1, anchor="se")

        # Question 1
        self.q1_radio_list = []
        for q1_options in self.get_options(self.get_tf_questions()[0][0])[0]:
            self.q1_radio_button = Radiobutton(self.tf_question_page_1, text=q1_options, value=q1_options,
                                               variable=self.q1_value)

            self.q1_radio_list.append(self.q1_radio_button)
            self.q1_radio_button.pack()

        # Question 2
        self.question2_label.pack(fill='x', ipady=25)

        self.q2_radio_list = []
        for q2_options in self.get_options(self.get_tf_questions()[1][0])[0]:
            self.q2_radio_button = Radiobutton(self.tf_question_page_2, text=q2_options, value=q2_options,
                                               variable=self.q2_value)

            self.q2_radio_list.append(self.q2_radio_button)
            self.q2_radio_button.pack()

        self.next_button_2.place(rely=1, relx=1, anchor="se")

        # Question 3
        self.question3_label.pack(fill='x', ipady=25)

        self.q3_radio_list = []
        for q3_options in self.get_options(self.get_tf_questions()[2][0])[0]:
            self.q3_radio_button = Radiobutton(self.tf_question_page_3, text=q3_options, value=q3_options,
                                               variable=self.q3_value)

            self.q3_radio_list.append(self.q3_radio_button)
            self.q3_radio_button.pack()

        self.next_button_3.place(rely=1, relx=1, anchor="se")

        # Question 4
        self.question4_label.pack(fill='x', ipady=25)

        self.q4_radio_list = []
        for q4_options in self.get_options(self.get_tf_questions()[3][0])[0]:
            self.q4_radio_button = Radiobutton(self.tf_question_page_4, text=q4_options, value=q4_options,
                                               variable=self.q4_value)

            self.q4_radio_list.append(self.q4_radio_button)
            self.q4_radio_button.pack()

        self.next_button_4.place(rely=1, relx=1, anchor="se")

        # Question 5
        self.question5_label.pack(fill='x', ipady=25)

        self.q5_radio_list = []
        for q5_options in self.get_options(self.get_tf_questions()[4][0])[0]:
            self.q5_radio_button = Radiobutton(self.tf_question_page_5, text=q5_options, value=q5_options,
                                               variable=self.q5_value)

            self.q5_radio_list.append(self.q5_radio_button)
            self.q5_radio_button.pack()

        self.submit_button.place(rely=1, relx=1, anchor="se")
        self.exit_button = Button(self.tf_question_page_5, text='Exit', command=self.exit_quiz)

        # Previous Buttons
        self.previous_button_1 = Button(self.tf_question_page_2, text='Previous',
                                        command=partial(self.change_frame, self.tf_question_page_2,
                                                        self.tf_question_page_1))
        self.previous_button_2 = Button(self.tf_question_page_3, text='Previous',
                                        command=partial(self.change_frame, self.tf_question_page_3,
                                                        self.tf_question_page_2))
        self.previous_button_3 = Button(self.tf_question_page_4, text='Previous',
                                        command=partial(self.change_frame, self.tf_question_page_4,
                                                        self.tf_question_page_3))
        self.previous_button_4 = Button(self.tf_question_page_5, text='Previous',
                                        command=partial(self.change_frame, self.tf_question_page_5,
                                                        self.tf_question_page_4))
        self.previous_button_1.place(rely=1, relx=0, anchor="sw")
        self.previous_button_2.place(rely=1, relx=0, anchor="sw")
        self.previous_button_3.place(rely=1, relx=0, anchor="sw")
        self.previous_button_4.place(rely=1, relx=0, anchor="sw")

        self.correct = 0
        self.options = ['True', 'False']

    def change_frame(self, frame_to_forget, frame_to_pack):
        frame_to_forget.forget()
        frame_to_pack.pack(fill='both', expand=1)

    def submit(self):

        self.submit_button.destroy()
        self.exit_button.place(rely=1, relx=1, anchor="se")

        self.q1_description_label.pack(fill='x', ipady=25)
        self.q2_description_label.pack(fill='x', ipady=25)
        self.q3_description_label.pack(fill='x', ipady=25)
        self.q4_description_label.pack(fill='x', ipady=25)
        self.q5_description_label.pack(fill='x', ipady=25)

        for my_radio_list in [self.q1_radio_list, self.q2_radio_list, self.q3_radio_list, self.q4_radio_list,
                              self.q5_radio_list]:
            for radio_button in my_radio_list:
                radio_button.config(state=DISABLED)

        value_get_list = [
            self.q1_value.get(),
            self.q2_value.get(),
            self.q3_value.get(),
            self.q4_value.get(),
            self.q5_value.get()
        ]

        # DB Connection START

        conn = connect(
            host="auth-db582.hostinger.com",
            user="u998717846_test_user",
            password="7$Mw9Q=e",
            database="u998717846_python_test"
        )

        c = conn.cursor()

        # DB Connection END

        for index in range(5):
            option_index = 5

            for option in self.options:

                if self.get_tf_questions()[index][5] == option:
                    if self.get_tf_questions()[index][option_index] == value_get_list[index]:
                        self.correct += 1
                option_index += 1

            # Select the question from the database
            select_seen_value = "SELECT view FROM questionsTF WHERE id='{}'".format(
                self.get_tf_questions()[index][0])
            c.execute(select_seen_value)

            seen_value = c.fetchone()
            seen = seen_value[0]
            seen += 1

            # Update the view value on the database
            update_seen_value = "UPDATE questionsTF SET view='{}' WHERE id='{}'".format(seen, self.get_tf_questions()[index][0])
            c.execute(update_seen_value)
            conn.commit()

        # Select the report from the database
        select_report = "SELECT attempts, totalscore FROM reports WHERE studentID='{}' AND quizID='{}'".format(
            usernameEntry.get(), self.selected_quiz)
        c.execute(select_report)
        report = c.fetchone()

        score = self.correct

        if report:

            # Increase the attempt
            attempts = report[0]
            attempts += 1

            total_score = score + report[1]
            average_score = total_score / attempts

            # Update the report on the database
            update_report = "UPDATE reports SET totalscore='{}', averagescore='{}', attempts ='{}' WHERE studentID='{}' AND quizID='{}'".format(
                total_score, average_score, attempts, usernameEntry.get(), self.selected_quiz)
            c.execute(update_report)
            conn.commit()

            # Select the report from the database
            select_report = "SELECT highestscore, lowestscore FROM reports WHERE studentID='{}' AND quizID='{}'".format(
                usernameEntry.get(), self.selected_quiz)
            c.execute(select_report)
            scores = c.fetchone()

            highestscore = scores[0]
            lowestscore = scores[1]

            if score < lowestscore:
                lowestscore = score

            if score > highestscore:
                highestscore = score

            # Update the lowest and highest score on the database
            update_scores = "UPDATE reports SET highestscore='{}', lowestscore='{}' WHERE studentID='{}' AND quizID='{}'".format(
                highestscore, lowestscore, usernameEntry.get(), self.selected_quiz)

            c.execute(update_scores)
            conn.commit()

        else:

            # Insert a report to the database
            insert_report = "INSERT INTO reports (studentID, quizID, totalscore, averagescore, lowestscore, highestscore, attempts) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            report_value = (usernameEntry.get(), self.selected_quiz, score, score, 6, -1, 1)
            c.execute(insert_report, report_value)
            conn.commit()

            # Select the report from the database
            select_report = "SELECT highestscore, lowestscore FROM reports WHERE studentID='{}' AND quizID='{}'".format(
                usernameEntry.get(), self.selected_quiz)
            c.execute(select_report)
            scores = c.fetchone()

            highestscore = scores[0]
            lowestscore = scores[1]

            if score < lowestscore:
                lowestscore = score

            if score > highestscore:
                highestscore = score

            # Update the lowest and highest score on the database
            update_scores = "UPDATE reports SET highestscore='{}', lowestscore='{}' WHERE studentID='{}' AND quizID='{}'".format(
                highestscore, lowestscore, usernameEntry.get(), self.selected_quiz)

            c.execute(update_scores)
            conn.commit()

        # Display correct answer
        print(f"Your score is: {score}/5")
        messagebox.showinfo("Result", f"Your score is: {score}/5")
        conn.close()

    def get_tf_questions(self):

        conn = connect(
            host="auth-db582.hostinger.com",
            user="u998717846_test_user",
            password="7$Mw9Q=e",
            database="u998717846_python_test"
        )

        c = conn.cursor()
        # print(conn)

        query = "SELECT * FROM questionsTF WHERE quizID='{}'".format(self.selected_quiz)

        c.execute(query)

        my_list = c.fetchall()

        for question in my_list:
            self.questions.append(question)
        return self.questions

    def get_options(self, questionID):

        conn = connect(
            host="auth-db582.hostinger.com",
            user="u998717846_test_user",
            password="7$Mw9Q=e",
            database="u998717846_python_test"
        )

        c = conn.cursor()
        # print(conn)

        query = "SELECT optionTrue, optionFalse FROM questionsTF WHERE id='{}'".format(questionID)

        c.execute(query)

        my_list = c.fetchall()

        return my_list

    def exit_quiz(self):
        self.tf_question_page_1.destroy()
        self.tf_question_page_2.destroy()
        self.tf_question_page_3.destroy()
        self.tf_question_page_4.destroy()
        self.tf_question_page_5.destroy()
        StudentPanel(root)


class FBQuiz(QuizList):

    def __init__(self, root, selected_quiz):
        self.selected_quiz = selected_quiz
        self.questions = []
        self.options = []

        self.fb_question_page_1 = Frame(root, width=33)
        self.fb_question_page_2 = Frame(root, width=33)
        self.fb_question_page_3 = Frame(root, width=33)
        self.fb_question_page_4 = Frame(root, width=33)
        self.fb_question_page_5 = Frame(root, width=33)
        self.fb_question_page_1.pack(fill='both', expand=1)

        root.title("Fill in the Blank Quiz")
        root.geometry('700x400')

        super().__init__(root)

        # Normal version
        # print(self.get_fb_questions()[0][2])

        # Random Shuffle
        random.shuffle(self.get_fb_questions())

        self.q1_value = StringVar()
        self.q2_value = StringVar()
        self.q3_value = StringVar()
        self.q4_value = StringVar()
        self.q5_value = StringVar()

        # Question Labels
        self.question1_label = Label(self.fb_question_page_1, text='Q1: ' + self.get_fb_questions()[0][2],
                                     wraplength=650)
        self.question2_label = Label(self.fb_question_page_2, text='Q2: ' + self.get_fb_questions()[1][2],
                                     wraplength=650)
        self.question3_label = Label(self.fb_question_page_3, text='Q3: ' + self.get_fb_questions()[2][2],
                                     wraplength=650)
        self.question4_label = Label(self.fb_question_page_4, text='Q4: ' + self.get_fb_questions()[3][2],
                                     wraplength=650)
        self.question5_label = Label(self.fb_question_page_5, text='Q5: ' + self.get_fb_questions()[4][2],
                                     wraplength=650)

        # Question Description Labels
        self.q1_description_label = Label(self.fb_question_page_1, text='Description: ' + self.get_fb_questions()[0][3],
                                          wraplength=650)
        self.q2_description_label = Label(self.fb_question_page_2, text='Description: ' + self.get_fb_questions()[1][3],
                                          wraplength=650)
        self.q3_description_label = Label(self.fb_question_page_3, text='Description: ' + self.get_fb_questions()[2][3],
                                          wraplength=650)
        self.q4_description_label = Label(self.fb_question_page_4, text='Description: ' + self.get_fb_questions()[3][3],
                                          wraplength=650)
        self.q5_description_label = Label(self.fb_question_page_5, text='Description: ' + self.get_fb_questions()[4][3],
                                          wraplength=650)

        # Next Buttons
        self.next_button_1 = Button(self.fb_question_page_1, text='Next',
                                    command=partial(self.change_frame, self.fb_question_page_1,
                                                    self.fb_question_page_2))
        self.next_button_2 = Button(self.fb_question_page_2, text='Next',
                                    command=partial(self.change_frame, self.fb_question_page_2,
                                                    self.fb_question_page_3))
        self.next_button_3 = Button(self.fb_question_page_3, text='Next',
                                    command=partial(self.change_frame, self.fb_question_page_3,
                                                    self.fb_question_page_4))
        self.next_button_4 = Button(self.fb_question_page_4, text='Next',
                                    command=partial(self.change_frame, self.fb_question_page_4,
                                                    self.fb_question_page_5))
        self.submit_button = Button(self.fb_question_page_5, text='Submit', command=self.submit)

        # Question 1
        self.question1_label.pack(fill='x', ipady=25)
        self.question1_entry = Entry(self.fb_question_page_1, textvariable=self.q1_value, width=35)
        self.question1_entry.pack()
        self.next_button_1.place(rely=1, relx=1, anchor="se")

        # Question 2
        self.question2_label.pack(fill='x', ipady=25)
        self.question2_entry = Entry(self.fb_question_page_2, textvariable=self.q2_value, width=35)
        self.question2_entry.pack()
        self.next_button_2.place(rely=1, relx=1, anchor="se")

        # Question 3
        self.question3_label.pack(fill='x', ipady=25)
        self.question3_entry = Entry(self.fb_question_page_3, textvariable=self.q3_value, width=35)
        self.question3_entry.pack()
        self.next_button_3.place(rely=1, relx=1, anchor="se")

        # Question 4
        self.question4_label.pack(fill='x', ipady=25)
        self.question4_entry = Entry(self.fb_question_page_4, textvariable=self.q4_value, width=35)
        self.question4_entry.pack()
        self.next_button_4.place(rely=1, relx=1, anchor="se")

        # Question 5
        self.question5_label.pack(fill='x', ipady=25)
        self.question5_entry = Entry(self.fb_question_page_5, textvariable=self.q5_value, width=35)
        self.question5_entry.pack()
        self.submit_button.place(rely=1, relx=1, anchor="se")
        self.exit_button = Button(self.fb_question_page_5, text='Exit', command=self.exit_quiz)

        # Previous Buttons
        self.previous_button_1 = Button(self.fb_question_page_2, text='Previous',
                                        command=partial(self.change_frame, self.fb_question_page_2,
                                                        self.fb_question_page_1))
        self.previous_button_2 = Button(self.fb_question_page_3, text='Previous',
                                        command=partial(self.change_frame, self.fb_question_page_3,
                                                        self.fb_question_page_2))
        self.previous_button_3 = Button(self.fb_question_page_4, text='Previous',
                                        command=partial(self.change_frame, self.fb_question_page_4,
                                                        self.fb_question_page_3))
        self.previous_button_4 = Button(self.fb_question_page_5, text='Previous',
                                        command=partial(self.change_frame, self.fb_question_page_5,
                                                        self.fb_question_page_4))
        self.previous_button_1.place(rely=1, relx=0, anchor="sw")
        self.previous_button_2.place(rely=1, relx=0, anchor="sw")
        self.previous_button_3.place(rely=1, relx=0, anchor="sw")
        self.previous_button_4.place(rely=1, relx=0, anchor="sw")

        self.correct = 0
        self.options = ['True', 'False']

    def change_frame(self, frame_to_forget, frame_to_pack):
        frame_to_forget.forget()
        frame_to_pack.pack(fill='both', expand=1)

    def submit(self):

        self.submit_button.destroy()
        self.exit_button.place(rely=1, relx=1, anchor="se")

        self.q1_description_label.pack(fill='x', ipady=25)
        self.q2_description_label.pack(fill='x', ipady=25)
        self.q3_description_label.pack(fill='x', ipady=25)
        self.q4_description_label.pack(fill='x', ipady=25)
        self.q5_description_label.pack(fill='x', ipady=25)

        self.question1_entry.config(state=DISABLED)
        self.question2_entry.config(state=DISABLED)
        self.question3_entry.config(state=DISABLED)
        self.question4_entry.config(state=DISABLED)
        self.question5_entry.config(state=DISABLED)

        value_get_list = [
            self.q1_value.get(),
            self.q2_value.get(),
            self.q3_value.get(),
            self.q4_value.get(),
            self.q5_value.get()
        ]

        # DB Connection START

        conn = connect(
            host="auth-db582.hostinger.com",
            user="u998717846_test_user",
            password="7$Mw9Q=e",
            database="u998717846_python_test"
        )

        c = conn.cursor()

        # DB Connection END

        for index in range(5):

            for que in value_get_list:
                if self.get_fb_questions()[index][4] == que:
                    self.correct += 1

            # Select the question from the database
            select_seen_value = "SELECT view FROM questionsFB WHERE id='{}'".format(self.get_fb_questions()[index][0])
            c.execute(select_seen_value)

            seen_value = c.fetchone()
            seen = seen_value[0]
            seen += 1

            # Update the view value on the database
            update_seen_value = "UPDATE questionsFB SET view='{}' WHERE id='{}'".format(seen, self.get_fb_questions()[index][0])
            c.execute(update_seen_value)
            conn.commit()

        # Select the report from the database
        select_report = "SELECT attempts, totalscore FROM reports WHERE studentID='{}' AND quizID='{}'".format(
            usernameEntry.get(), self.selected_quiz)
        c.execute(select_report)
        report = c.fetchone()

        score = self.correct

        if report:

            # Increase the attempt
            attempts = report[0]
            attempts += 1

            total_score = score + report[1]
            average_score = total_score / attempts

            # Update the report on the database
            update_report = "UPDATE reports SET totalscore='{}', averagescore='{}', attempts ='{}' WHERE studentID='{}' AND quizID='{}'".format(
                total_score, average_score, attempts, usernameEntry.get(), self.selected_quiz)
            c.execute(update_report)
            conn.commit()

            # Select the report from the database
            select_report = "SELECT highestscore, lowestscore FROM reports WHERE studentID='{}' AND quizID='{}'".format(
                usernameEntry.get(), self.selected_quiz)
            c.execute(select_report)
            scores = c.fetchone()

            highestscore = scores[0]
            lowestscore = scores[1]

            if score < lowestscore:
                lowestscore = score

            if score > highestscore:
                highestscore = score

            # Update the lowest and highest score on the database
            update_scores = "UPDATE reports SET highestscore='{}', lowestscore='{}' WHERE studentID='{}' AND quizID='{}'".format(
                highestscore, lowestscore, usernameEntry.get(), self.selected_quiz)

            c.execute(update_scores)
            conn.commit()

        else:

            # Insert a report to the database
            insert_report = "INSERT INTO reports (studentID, quizID, totalscore, averagescore, lowestscore, highestscore, attempts) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            report_value = (usernameEntry.get(), self.selected_quiz, score, score, 6, -1, 1)
            c.execute(insert_report, report_value)
            conn.commit()

            # Select the report from the database
            select_report = "SELECT highestscore, lowestscore FROM reports WHERE studentID='{}' AND quizID='{}'".format(
                usernameEntry.get(), self.selected_quiz)
            c.execute(select_report)
            scores = c.fetchone()

            highestscore = scores[0]
            lowestscore = scores[1]

            if score < lowestscore:
                lowestscore = score

            if score > highestscore:
                highestscore = score

            # Update the lowest and highest score on the database
            update_scores = "UPDATE reports SET highestscore='{}', lowestscore='{}' WHERE studentID='{}' AND quizID='{}'".format(
                highestscore, lowestscore, usernameEntry.get(), self.selected_quiz)

            c.execute(update_scores)
            conn.commit()

        # Display correct answer
        print(f"Your score is: {score}/5")
        messagebox.showinfo("Result", f"Your score is: {score}/5")
        conn.close()

    def get_fb_questions(self):

        conn = connect(
            host="auth-db582.hostinger.com",
            user="u998717846_test_user",
            password="7$Mw9Q=e",
            database="u998717846_python_test"
        )

        c = conn.cursor()
        # print(conn)

        query = "SELECT * FROM questionsFB WHERE quizID='{}'".format(self.selected_quiz)

        c.execute(query)

        my_list = c.fetchall()

        for question in my_list:
            self.questions.append(question)
        return self.questions

    def exit_quiz(self):
        self.fb_question_page_1.destroy()
        self.fb_question_page_2.destroy()
        self.fb_question_page_3.destroy()
        self.fb_question_page_4.destroy()
        self.fb_question_page_5.destroy()
        StudentPanel(root)


Main(root)
root.mainloop()
