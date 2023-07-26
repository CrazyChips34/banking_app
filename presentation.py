# Imports
from tkinter import *
import os
import re
from datetime import datetime
from PIL import Image, ImageTk

# Main Screen
master = Tk()
master.title('Banking App')
master.geometry('300x370')
master.configure(background='White')

# Global Variables
transaction_notif = "None"

#Function to validate password
def validate_password(password):
    if (len(password) >= 8 and 
        re.search(r"\d", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[A-Z]", password) and
        re.search(r"[!@#$%^&*()_+{}:;\"'?<>,.\/\|\\-]", password)):
        return True
    else:
        return False

# Functions+
notif:None
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
        
        
     #Check if the password.txt file exists, create it if it does not exist
    if not os.path.exists("passwords.txt"):
        open("passwords.txt", "w").close()

    with open("passwords.txt", "r") as f:
        used_passwords = f.read().splitlines()

    if password in used_passwords:
        notif.config(fg="red", text="Password not avaible")
        return
    
    if not validate_password(password):
        notif.config(fg="red", text="Invalid password")
        return

    #Save password to file
    with open("passwords.txt", "a") as f:
        f.write(password + "\n")
        
    #User Account Data
    new_file = open(name, "w")
    new_file.write(name + '\n')
    new_file.write(password + '\n')
    new_file.write(age + '\n')
    new_file.write(gender + '\n')
    new_file.write('0\n') 
    new_file.write('\n')# Add a new line at the end to ensure account data is complete
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
    register_screen.geometry("400x300")
    register_screen.configure(background='White')
    
    # function to close the window
    def close_register_window():
         register_screen.destroy()

   

    # Labels
    Label(register_screen, text="Please enter your details below to register", font=('Calibri', 12), bg='White').grid(row=0, columnspan=2, sticky=N)
    Label(register_screen, text="Name", font=('Calibri', 12), bg='White').grid(row=2, column=0, sticky=N)
    Label(register_screen, text="Age", font=('Calibri', 12), bg='White').grid(row=3, column=0, sticky=N)
    Label(register_screen, text="Gender", font=('Calibri', 12), bg='White').grid(row=4, column=0, sticky=N)
    Label(register_screen, text="Password", font=('Calibri', 12), bg='White').grid(row=5, column=0, sticky=N)
    notif = Label(register_screen, font=('Calibri', 12), bg='White')
    notif.grid(row=9, sticky=N, pady=10)

    # Entries
    Entry(register_screen, textvariable=temp_name, width=40).grid(row=2, column=1, sticky=NW)
    Entry(register_screen, textvariable=temp_age, width=40).grid(row=3, column=1)
    Entry(register_screen, textvariable=temp_gender, width=40).grid(row=4, column=1)
    Entry(register_screen, textvariable=temp_password, width=40).grid(row=5, column=1)
    password_entry = Entry(register_screen, textvariable=temp_password, width=40, show="*")
    password_entry.grid(row=5, column=1)
    show_password_var = BooleanVar()
    show_password_checkbox = Checkbutton(register_screen, text="Show password", variable=show_password_var, command=lambda: toggle_password_visibility(password_entry, show_password_var.get()))
    show_password_checkbox.grid(row=6, column=1)
    
    # Buttons
    Button(register_screen, text="Register", command=finish_reg, font=('Calibri', 12), bg='LightBlue', width=15).grid(row=7, column=1, sticky=N, pady=10)

    # create a button to close the window

    Button(register_screen, text="Close", command=close_register_window, font=('Calibri', 12), bg='LightGreen', width=15).grid(row=8, column=1, sticky=N, pady=10)
    
def toggle_password_visibility(password_entry, show_password):
        if show_password:
            password_entry.config(show="")
        else:
            password_entry.config(show="*")


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
    login_screen.geometry("400x300")
    login_screen.configure(background='White')
    
    # function to close the login window
    def close_login_window():
        login_screen.destroy()

    # Labels
    Label(login_screen, text="Login to your account", font=('Calibri', 12), bg='White').grid(row=0, column=2, columnspan=2, pady=4, padx=4, sticky='N')
    Label(login_screen, text="Username", font=('Calibri', 12), bg='White').grid(row=1, column=0, columnspan=2, pady=5, sticky='NE')
    Label(login_screen, text="Password", font=('Calibri', 12), bg='White').grid(row=2, column=0, columnspan=2, pady=5, sticky='NE')
    login_notif = Label(login_screen, font=('Calibri', 12), bg='White')
    login_notif.grid(row=6,columnspan=2, column=2, pady=4, padx=4, sticky='N')

    # Entry
    Entry(login_screen, textvariable=temp_login_name, width=45).grid(row=1, column=2,columnspan=4, pady=10, padx=10,  sticky='NE')
    Entry(login_screen, textvariable=temp_login_password, width=45).grid(row=2, column=2, pady=10 ,padx=10)
    password_entry = Entry(login_screen, textvariable=temp_login_password, width=45, show="*")
    password_entry.grid(row=2, column=2)
    show_password_var = BooleanVar()
    show_password_checkbox = Checkbutton(login_screen, text="Show password", variable=show_password_var, command=lambda: toggle_password_visibility(password_entry, show_password_var.get()))
    show_password_checkbox.grid(row=3, column=2)

    # Button
    Button(login_screen, text="Login", command=login_session, width=15, font=('Calibri', 12), bg='LightBlue').grid(row=4,  column=2, columnspan=2, pady=5, sticky='N')
    Button(login_screen, text="Close", command=close_login_window, width=18,font=('Calibri', 12), bg='LightGreen').grid(row=5,  column=2, columnspan=2, pady=5, sticky='N')

#function to view the transaction logs
def view_transaction_logs():
    account_filename = temp_login_name.get()
    account_file_path = os.path.join(os.getcwd(), account_filename)

    if not os.path.exists(account_file_path):
        print("Account not found")
        return

    with open(account_file_path, "r") as account_file:
        file_data = account_file.readlines()

        #Extracts the transaction logs from the file data starting from the sixth line 
        #and stores them in a list called transaction_logs.
        transaction_logs = file_data[5:]
        transaction_logs = [log.strip() for log in transaction_logs]

        # Create a new window to display the logs
        log_screen = Toplevel(master)
        log_screen.title('Transaction Logs')

        # Labels
        Label(log_screen, text="Transaction Logs", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)

        for i, log in enumerate(transaction_logs):
            Label(log_screen, text=log, font=('Calibri', 12)).grid(row=i+1, sticky=W, padx=5)
            
#Function that completes tranaction on the transaction type  
def perform_transaction(transaction_type, amount):
    global balance_label, transaction_notif
    
    #first retrieves the filename of the bank account and constructs the file path
    account_filename = temp_login_name.get() 
    account_file_path = os.path.join(os.getcwd(), account_filename)

    #Checks if the bank account file exists 
    if not os.path.exists(account_file_path):
        #if file doesn't this will display
        transaction_notif.config(fg="red", text="Account not found")
        return

    #If file does exist it reads the contents of the file and stores them in a variable
    with open(account_file_path, "r+") as account_file:
        file_data = account_file.readlines()
        #print(file_data)  # Debug print statement

        #Checks if the file contains at least 5 lines
        if len(file_data) < 5:
            transaction_notif.config(fg="red", text="Account data is incomplete")
            return

       #Attempts to extract the current balance of the account from the fifth line of the file data
        try:
            balance = float(file_data[4].strip())
        except ValueError:
            transaction_notif.config(fg="red", text="Invalid balance value")
            return

        #Extracts the transaction logs from the file data starting from the sixth line 
        #and stores them in a list called transaction_logs.
        transaction_logs = file_data[5:]
        transaction_logs = [log.strip() for log in transaction_logs]
        
        
        if transaction_type == "withdraw":
            if balance >= float(amount):
                balance -= float(amount)
                file_data[4] = str(balance) + '\n'
                account_file.seek(0)
                account_file.writelines(file_data)
                account_file.truncate()
                balance_label.config(text="Balance: R{}".format(balance))
                transaction_notif.config(fg="green", text="Withdrawal successful")
                
                #After withrawal is made it appends to the transaction_logs list.
                transaction_log = "Withdrawal: R{}, Date-Time: {}".format(amount, datetime.now())
                transaction_logs.append(transaction_log)
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
            
             #After deposit is made it appends to the transaction_logs list.
            transaction_log = "Deposit: R{}, Date-Time: {}".format(amount, datetime.now())
            transaction_logs.append(transaction_log)

        # Write transaction logs back to file
    with open(account_file_path, "a") as account_file:
        for log in transaction_logs[len(transaction_logs)-1:]:
            account_file.seek(0, 2)
            account_file.write(log + '\n')


    #account_file.close()

def withdraw():
    global balance_label, transaction_notif

    withdraw_screen = Toplevel(master)
    withdraw_screen.title('Withdraw')
    withdraw_screen.geometry("400x200")
    withdraw_screen.configure(background='LightBlue')      

     # function to close the login window
    def cancel_withdrawal():
        withdraw_screen.destroy()
        
    # Labels
    Label(withdraw_screen, text="Withdraw", font=('Calibri', 15), bg='LightBlue').grid(row=0, columnspan=2,column=0, pady=5, padx=145)
    Label(withdraw_screen, text="Amount Withdrawing:    R", font=('Calibri', 12), bg='LightBlue').grid(row=1, sticky=W, padx=10)
    Label(withdraw_screen, text="", bg='LightBlue').grid(row=2, sticky=N, pady=5)

    # Entry
    withdraw_amount = IntVar()
    Entry(withdraw_screen, textvariable=withdraw_amount, width=30).grid(row=1, column=1, padx=5)

    # Button
    Button(withdraw_screen, text="Confirm", command=lambda:perform_transaction("withdraw", withdraw_amount.get()),
           width=15, font=('Calibri', 12), bg='LightGreen').grid(row=3, sticky=W, pady=5, padx=30)
    Button(withdraw_screen, text="Cancel", command=cancel_withdrawal, width=15,font=('Calibri', 12), bg='Red').grid(row=3, column=1,sticky=N, pady=5)
    
    # Transaction Notification Label
    transaction_notif = Label(withdraw_screen, font=('Calibri', 12), bg='LightBlue')
    transaction_notif.grid(row=5, sticky=N, pady=10)
    
    

def deposit():
    global balance_label, transaction_notif

    deposit_screen = Toplevel(master)
    deposit_screen.title('Deposit')
    deposit_screen.geometry("400x200")
    deposit_screen.configure(background='LightBlue')

    # function to close the login window
    def cancel_deposit():
        deposit_screen.destroy()
        
    # Labels
    Label(deposit_screen, text="Deposit", font=('Calibri', 15), bg='LightBlue').grid(row=0, columnspan=2, column=0, pady=5, padx=160)
    Label(deposit_screen, text="Amount Depositing:  R", font=('Calibri', 12), bg='LightBlue').grid(row=1, sticky=W, padx=10)
    Label(deposit_screen, text="", bg='LightBlue').grid(row=2, sticky=N, pady=5)

    # Entry
    deposit_amount = IntVar()
    Entry(deposit_screen, textvariable=deposit_amount, width=30).grid(row=1, column=1, padx=5)

    # Button
    Button(deposit_screen, text="Confirm", command=lambda:perform_transaction("deposit", deposit_amount.get()), width=15, font=('Calibri', 12), bg='LightGreen').grid(row=3, sticky=W, pady=5, padx=30)
    Button(deposit_screen, text="Cancel", command=cancel_deposit, width=15,font=('Calibri', 12), bg='Red').grid(row=3, column=1,sticky=N, pady=5)

    # Transaction Notification Label
    transaction_notif = Label(deposit_screen, font=('Calibri', 12), bg='LightBlue')
    transaction_notif.grid(row=4, sticky=N, pady=10)


            
# Account Dashboard
def show_account_dashboard(login_name):
    global balance_label
    master.withdraw()
    account_dashboard = Toplevel(master)
    account_dashboard.title('Dashboard')
    account_dashboard.geometry("400x350")
    account_dashboard.configure(background='White')

    # Labels
    Label(account_dashboard, text="Welcome, " + login_name, font=('Calibri', 12), bg='White').grid(row=0, columnspan=2, column=0, sticky=N, pady=5, padx=125)
    balance_label = Label(account_dashboard, text="Balance: R0", font=('Calibri', 12), bg='White')
    balance_label.grid(row=1, columnspan=2, column=0, sticky=N, pady=5, padx=125)
    Label(account_dashboard, text="", bg='White').grid(row=2, sticky=N, pady=5)

    # Buttons
    Button(account_dashboard, text="Withdraw", font=('Calibri', 12), width=20, command=withdraw,  bg='LightGreen').grid(row=3, columnspan=2, column=0, pady=5, padx=125)
    Button(account_dashboard, text="Deposit", font=('Calibri', 12), width=20, command=deposit,  bg='LightGreen').grid(row=4, columnspan=2, column=0, pady=5, padx=125)
    Button(account_dashboard, text="View Transaction Logs", font=('Calibri', 12), width=20, command=view_transaction_logs,  bg='LightGreen').grid(row=5, columnspan=2, column=0, pady=5, padx=125)
    Button(account_dashboard, text="Logout", font=('Calibri', 12), width=20, command=lambda: logout(account_dashboard),  bg='LightBlue').grid(row=6, columnspan=2, column=0, pady=5, padx=125)

    # Transaction Notification
    transaction_notif = Label(account_dashboard, font=('Calibri', 12), bg='White')
    transaction_notif.grid(row=7, sticky=N, pady=10)

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
img = img.resize((200, 170))
img = ImageTk.PhotoImage(img)

# Labels
Label(master, text="BLACK PANTHERS BANK", font=('Calibri', 14), bg='White').grid(row=0, column=2, sticky=N, pady=5)
Label(master, text="The most secure bank you've probably used", font=('Calibri', 12), bg='White').grid(row=1, column=2, pady=5, sticky=N)
Label(master, image=img).grid(row=2, column=2, sticky=N, pady=15)

# Buttons
Button(master, text="Register", font=('Calibri', 12), width=15, command=register, bg='LightBlue').grid(row=3, column=2, sticky=N)
Button(master, text="Login", font=('Calibri', 12), width=15, command=login, bg='LightBlue').grid(row=4,  column=2, sticky=N, pady=10)

master.mainloop()
