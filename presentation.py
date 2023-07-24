# Imports
from tkinter import *
import os
from PIL import Image, ImageTk

# Main Screen
master = Tk()
master.title('Banking App')

# Global Variables
balance_label = "None"
transaction_notif = "None"

# Functions
def finish_reg():
    global notif
    name = temp_name.get()
    age = temp_age.get()
    gender = temp_gender.get()
    password = temp_password.get()
    all_accounts = os.listdir()

    if name == "" or age == "" or gender == "" or password == "":
        notif.config(fg="red", text="All fields required")
        print("All fields are required")
        return

    for name_check in all_accounts:
        if name == name_check:
            notif.config(fg="red", text="Account already exists")
            return

    new_file = open(name, "w")
    new_file.write(name + '\n')
    new_file.write(password + '\n')
    new_file.write(age + '\n')
    new_file.write(gender + '\n')
    new_file.write('0\n') 
    new_file.write(' + \n')# Add a new line at the end to ensure account data is complete
    new_file.close()
    notif.config(fg="green", text="Account has been successfully created")

def register():
    # Vars
    global temp_name
    global temp_age
    global temp_gender
    global temp_password
    global notif
    temp_name = StringVar()
    temp_age = StringVar()
    temp_gender = StringVar()
    temp_password = StringVar()

    # Register Screen
    register_screen = Toplevel(master)
    register_screen.title('Register')

    # Labels
    Label(register_screen, text="Please enter your details below to register", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    Label(register_screen, text="Name", font=('Calibri', 12)).grid(row=1, sticky=W)
    Label(register_screen, text="Age", font=('Calibri', 12)).grid(row=2, sticky=W)
    Label(register_screen, text="Gender", font=('Calibri', 12)).grid(row=3, sticky=W)
    Label(register_screen, text="Password", font=('Calibri', 12)).grid(row=4, sticky=W)
    notif = Label(register_screen, font=('Calibri', 12))
    notif.grid(row=6, sticky=N, pady=10)

    # Entries
    Entry(register_screen, textvariable=temp_name).grid(row=1, column=0)
    Entry(register_screen, textvariable=temp_age).grid(row=2, column=0)
    Entry(register_screen, textvariable=temp_gender).grid(row=3, column=0)
    Entry(register_screen, textvariable=temp_password, show="*").grid(row=4, column=0)

    # Buttons
    Button(register_screen, text="Register", command=finish_reg, font=('Calibri', 12)).grid(row=5, sticky=N, pady=10)

def login_session():
    global balance_label

    
    all_accounts = os.listdir()
    login_name = temp_login_name.get()
    login_password = temp_login_password.get()

    for name in all_accounts:
        if name == login_name:
            file = open(name, "r")
            file_data = file.read()
            file_data = file_data.split('\n')
            password = file_data[1]
            # Account Dashboard
            if login_password == password:
                login_screen.destroy()
                show_account_dashboard(login_name)
                return

    login_notif.config(fg="red", text="Invalid username or password")

def login():
    # Vars
    global temp_login_name
    global temp_login_password
    global login_notif
    global login_screen
    temp_login_name = StringVar()
    temp_login_password = StringVar()

    # Login Screen
    login_screen = Toplevel(master)
    login_screen.title('Login')

    # Labels
    Label(login_screen, text="Login to your account", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    Label(login_screen, text="Username", font=('Calibri', 12)).grid(row=1, sticky=W)
    Label(login_screen, text="Password", font=('Calibri', 12)).grid(row=2, sticky=W)
    login_notif = Label(login_screen, font=('Calibri', 12))
    login_notif.grid(row=4, sticky=N)

    # Entry
    Entry(login_screen, textvariable=temp_login_name).grid(row=1, column=1, padx=5)
    Entry(login_screen, textvariable=temp_login_password, show="*").grid(row=2, column=1, padx=5)

    # Button
    Button(login_screen, text="Login", command=login_session, width=15, font=('Calibri', 12)).grid(row=3, sticky=W,
                                                                                                    pady=5, padx=5)
    
def perform_transaction(transaction_type, amount):
    global balance_label, transaction_notif

    account_filename = temp_login_name.get()
    account_file_path = os.path.join(os.getcwd(), account_filename)

    if not os.path.exists(account_file_path):
        transaction_notif.config(fg="red", text="Account not found")
        return

    with open(account_file_path, "r+") as account_file:
        file_data = account_file.readlines()
        print(file_data)  # Debug print statement

        if len(file_data) < 5:
            transaction_notif.config(fg="red", text="Account data is incomplete")
            return

        try:
            balance = float(file_data[4].strip())
        except ValueError:
            transaction_notif.config(fg="red", text="Invalid balance value")
            return

        if transaction_type == "withdraw":
            if balance >= float(amount):
                balance -= float(amount)
                file_data[4] = str(balance) + '\n'
                account_file.seek(0)
                account_file.writelines(file_data)
                account_file.truncate()
                balance_label(text="Balance: R{}".format(balance))
                transaction_notif.config(fg="green", text="Withdrawal successful")
            else:
                transaction_notif.config(fg="red", text="Insufficient funds")
        elif transaction_type == "deposit":
            balance += float(amount)
            file_data[4] = str(balance) + '\n'
            account_file.seek(0)
            account_file.writelines(file_data)
            account_file.truncate()
            balance_label.config(text="Balance: R{}".format(balance))
            transaction_notif.config(fg="green", text="Deposit successful")

    #account_file.close()


def withdraw():
    global balance_label, transaction_notif


    withdraw_screen = Toplevel(master)
    withdraw_screen.title('Withdraw')

    # Labels
    Label(withdraw_screen, text="Withdraw", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    Label(withdraw_screen, text="Amount:", font=('Calibri', 12)).grid(row=1, sticky=W)
    Label(withdraw_screen, text="").grid(row=2, sticky=N, pady=5)

    # Entry
    withdraw_amount = StringVar()
    Entry(withdraw_screen, textvariable=withdraw_amount).grid(row=1, column=1, padx=5)

    # Button
    Button(withdraw_screen, text="Confirm", command=lambda:perform_transaction("withdraw", withdraw_amount.get()),
           width=15, font=('Calibri', 12)).grid(row=3, sticky=W, pady=5, padx=5)
    
    # Transaction Notification Label
    transaction_notif = Label(withdraw_screen, font=('Calibri', 12))
    transaction_notif.grid(row=4, sticky=N, pady=10)

def deposit():
    global balance_label, transaction_notif

    deposit_screen = Toplevel(master)
    deposit_screen.title('Deposit')

    # Labels
    Label(deposit_screen, text="Deposit", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    Label(deposit_screen, text="Amount:", font=('Calibri', 12)).grid(row=1, sticky=W)
    Label(deposit_screen, text="").grid(row=2, sticky=N, pady=5)

    # Entry
    deposit_amount = StringVar()
    Entry(deposit_screen, textvariable=deposit_amount).grid(row=1, column=1, padx=5)

    # Button
    Button(deposit_screen, text="Confirm", command=lambda:perform_transaction("deposit", deposit_amount.get()),
           width=15, font=('Calibri', 12)).grid(row=3, sticky=W, pady=5, padx=5)

    # Transaction Notification Label
    transaction_notif = Label(deposit_screen, font=('Calibri', 12))
    transaction_notif.grid(row=4, sticky=N, pady=10)



# Account Dashboard
def show_account_dashboard(login_name):
    master.withdraw()
    account_dashboard = Toplevel(master)
    account_dashboard.title('Dashboard')

    # Labels
    Label(account_dashboard, text="Welcome, " + login_name, font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    balance_label = Label(account_dashboard, text="Balance: R0", font=('Calibri', 12))
    balance_label.grid(row=1, sticky=N, pady=5)
    Label(account_dashboard, text="").grid(row=2, sticky=N, pady=5)

    # Buttons
    Button(account_dashboard, text="Withdraw", font=('Calibri', 12), width=20, command=withdraw).grid(row=3,
                                                                                                       sticky=N,
                                                                                                       pady=10)
    Button(account_dashboard, text="Deposit", font=('Calibri', 12), width=20, command=deposit).grid(row=4,
                                                                                                     sticky=N,
                                                                                                     pady=10)
    Button(account_dashboard, text="Logout", font=('Calibri', 12), width=20, command=lambda: logout(account_dashboard)).grid(row=5,
                                                                                                              sticky=N,
                                                                                                              pady=10)

    # Transaction Notification
    transaction_notif = Label(account_dashboard, font=('Calibri', 12))
    transaction_notif.grid(row=6, sticky=N, pady=10)

    # Load balance from file
    account_file = open(login_name, "r")
    file_data = account_file.readlines()
    balance = float(file_data[4].strip())  # Remove trailing newline character
    balance_label.config(text="Balance: R{}".format(balance))
    account_file.close()

def logout(account_dashboard):
    account_dashboard.destroy()
    master.deiconify()

# Image import
img = Image.open('PANTHERS.png')
img = img.resize((150, 150))
img = ImageTk.PhotoImage(img)

# Labels
Label(master, text="BLACK PANTHERS BANK", font=('Calibri', 14)).grid(row=0, sticky=N, pady=10)
Label(master, text="The most secure bank you've probably used", font=('Calibri', 12)).grid(row=1, sticky=N)
Label(master, image=img).grid(row=2, sticky=N, pady=15)

# Buttons
Button(master, text="Register", font=('Calibri', 12), width=20, command=register).grid(row=3, sticky=N)
Button(master, text="Login", font=('Calibri', 12), width=20, command=login).grid(row=4, sticky=N, pady=10)

master.mainloop()
