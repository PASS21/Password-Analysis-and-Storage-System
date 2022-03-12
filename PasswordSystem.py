#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

words_dict=""

def importPasswords():
    """Function to import passwords from a csv file exported from browsers."""
    csvFile = open(r"Passwds.csv","w+") # will contain the imported/new login credentials.
    browserCsvLocation = input("Enter path to file: ")
    browserPwds = open(browserCsvLocation) #"browserpwds" contains the passwords from browsers" csv files.

    blank = ""
    for row in browserPwds:
        blank+=str(row)
    csvFile.write(blank)
    csvFile.close()



def lower(inp):
    """Function to convert all the strings in a string to lowercase."""
    return (str(inp)).lower()



def dictionary():
    """Function to retreive the dictionary files from the internet."""
    global words_dict
    import platform
    os=platform.system()
    from os import getcwd, system , path
    if os == "Windows":
        if not path.isfile("./dictionary.txt"):        
            s =f"curl --silent -o {getcwd()}/dictionary.txt  https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt "
            system(s)
        words_dict = (open("./dictionary.txt").read()).strip() 
    elif os=="Darwin" or os=="Linux":
        if not path.isfile("./dictionary.txt"):    
            system("curl -s   https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt > dictionary.txt")
            
        words_dict= system("cat dictionary.txt")
        words_dict = str(words_dict)


def passgen(no_of_passwords=1):
    """A simple m-length n-count Password generator."""
    import os
    import random
    chars = "+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890" # total_chars
    # Password generation
    min_passwd_length = int(input("What password length do you want to get?: "))
    for n in range(no_of_passwords):
        password = ""
        for i in range(min_passwd_length):
            password += random.choice(chars) # random new password
        print(password)


def strength(passwd):
    """Function to check the strength of a password.Calculates using mathematical formulae."""
    global words_dict
    words_dict=lower(words_dict)
    total_chars =len("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()[]{}\|;:\"\",<.>`~/?")
    import getpass
    import math
    passwordStrength=math.log2(total_chars) * len(passwd)
    if passwd.islower() or passwd.isupper() or passwd.isalpha() or passwd.isnumeric()  :
        passwordStrength-=5
    if passwd in words_dict: # checking dictionary files
        passwordStrength-=10
    #print(f"Strength of the password is : {round(passwordStrength,4)}")
    return round(passwordStrength,4)


def get_os():
    """Function to get the OS of the user, and to install the necessary Python packages."""
    qn = input("Do you want to install the required packages ? [y]/n ")
    if qn=="y" or qn=='':
        import platform
        from os import system
        opsys = platform.system()
        if opsys == "Windows":
            system("pip install -U pandas sympy pwnedpasswords") # depending on your config , pip or pip3 will work
            system("pip3 install -U pandas sympy pwnedpasswords")
            return "Installed all requirements for Windows !"
        elif opsys == "Linux" or opsys == "Darwin":
            system("pip3 install -U pandas sympy  pwnedpasswords") # for *NIX, pip refers to Python 2 ,and pip3 to Python 3
            if opsys=="Linux":
                return "Installed all requirements for Linux !"
            elif opsys=="Darwin":
                return "Installed all requirements for macOS !"
        else:
            return "Unknown OS - please run \n \t pip install -U pandas sympy jupyter\n in the terminal "
    elif qn=="n":
        return "No problem - just run \n \t pip install -U sympy pandas sympy jupyter\n in your system terminal "
    else:
        return "Please enter y or n"


def eval_time():
    """Function to evaluate the time taken to crack the user-specified password."""
    from getpass import getpass
    passwd=getpass("Enter password: ")
    from sympy import Sum,symbols
    k=symbols('k')
    try:
        no_of_cracked_passwords_per_sec=int(input("How many passwords should i attempt cracking per second? "))
    except:
        print("Defaulting to 5 passwords/sec")
        no_of_cracked_passwords_per_sec=5
    no_of_possible_passwords = Sum(94**k,(k,4,256)).doit()
    time = no_of_possible_passwords * (1/no_of_cracked_passwords_per_sec) # time is in seconds 
    print(f"It takes {time} seconds to crack {passwd} @ {no_of_cracked_passwords_per_sec} cracked per second")



def breachCheck(passwd):
    """ Function to check if the password is in the pwnedpasswords.com database."""
    from pwnedpasswords import check
    breach_test_results = check(passwd)
    print(f"Password has been breached {breach_test_results} times")

def displayLogins(masterKeyInput):
    """
    This is a function that helps display the contents of "Passwds.csv", which may be imported directly
    from the browser, or modified using the other functions below.
    It uses a library called "pandas" to display the passwords in a neat tabular form.
    """
    import sys

    import pandas as pd
    actualMasterKey = ((open(r"./.MasterKey.txt")).read()).strip() # masterKeyInput
    if masterKeyInput==actualMasterKey:
        print("\nAuthorization success. Displaying gathered passwords : \n\n")
        return pd.read_csv(r"Passwds.csv") # the standard csv.reader() gives an ugly output.
    else:
        sys.stderr.write("\n \n Authorization failure. Unable to fetch passwords right now. \n \n")

def writeLogins(masterKeyInput):
    """
    This is a function that facilitates the addition of new login details to the "Passwds.csv" file.
    """
    actualMasterKey = ((open(r".MasterKey.txt")).read()).strip() 
    if masterKeyInput==actualMasterKey:
        print("\nAuthorization success. Initializing edit mode \n\n")
        import csv
        import sys
        from getpass import getpass
        logins = list(str(input("Enter name,url,username: ")).split(","))
        pwd = getpass("Enter password: ") ; logins += (pwd,)
        csvFile = open(r"Passwds.csv","a")
        csvFile.write("\n")
        csvWriter = csv.writer(csvFile)
        from pwnedpasswords import check
        if check(pwd)<1.5 and (strength(pwd)>=25 or eval_time(pwd)>=3600) :
            csvWriter.writerow(logins)
            print("\nLogin added successfully.\n")
        else:
            ch= input("Weak password ! Auto-generate new password? [y]/n ")
            if ch=="y" or ch=="":
                pwd = passgen() # made it generate only 1 password - 1 is the default argument for passgen()
                del logins[-1]
                logins.append(pwd)
                csvWriter = csv.writer(csvFile)
                csvWriter.writerow(logins)
                print("Added the random password...")
            elif ch=="n":
                csvWriter.writerow(logins)
                print("No problem - password unchanged.\nAdded to the file.")
    else:
        import sys
        sys.stderr.write("\nAuthorization failure. You can\'t append passwords.\n")

def editLogins(masterKeyInput):
    """
    This is a function that facilitates modification of entered login details - in case the user needs
    to rectify something entered wrongly. Can be used in conjunction with "displayLogins()".
    """
    import csv
    import sys
    from getpass import getpass
    actualMasterKey = ((open(r".MasterKey.txt")).read()).strip() 
    if masterKeyInput==actualMasterKey:
        csvFile = open(r"Passwds.csv","r")
        names,urls,usernames,passwords = [],[],[],[]
        for row in csvFile:
            if row != "\n":
                line = (row.rstrip("\n")).split(",")
                names = names + [(str(line[0]))]
                urls = urls + [(str(line[1]))]
                usernames = usernames + [(str(line[2]))]
                passwords = passwords + [(str(line[3]))]
            else:
                row = ""","","","""
        print("1.Change website name")
        print("2.Change website URL")
        print("3.Change saved username")
        print("4.Change saved password for the website")
        choice = int(input("Choose 1,2,3 or 4: "))
        if choice==1:
            oldWebsiteName = input("Enter old website\"s name: ")
            newWebsiteName = input(f"Replace \"{oldWebsiteName}\" with: " )
            for i in names:
                if i==oldWebsiteName:
                    names[names.index(i)] = newWebsiteName
        elif choice==2:
            oldURLName = input("Enter old URL: ")
            newURLName = input(f"Replace \"{oldURLName}\" with: ")
            for i in urls:
                if i==oldURLName:
                    urls[urls.index(i)] = newURLName
        elif choice==3:
            oldUserName = input("Enter old username: ")
            newUserName = input(f"Replace \"{oldUserName}\" with: ")
            for i in usernames:
                if i==oldUserName:
                    usernames[usernames.index(i)] = newUserName
        elif choice==4:
            oldPassword = getpass("Enter old password: ")
            newPassword = getpass(f"Replace \"{oldPassword}\" with: ")
            for i in passwords:
                if i==oldPassword:
                    passwords[passwords.index(i)] = newPassword
        else:
            print(f"{choice} is not in (1,2,3,4).")

        csvFile = open("Passwds.csv","w")
        csvWriter = csv.writer(csvFile,lineterminator="\n")
        csvWriter.writerow(("name","url","username","password"))
        csvFile.close()
        csvFile = open("Passwds.csv","a")
        csvWriter = csv.writer(csvFile,lineterminator="\n")
        for i in range(1,len(names)):
            csvWriter.writerow((names[i],urls[i],usernames[i],passwords[i]))
        print("Logins edited/added successfully! ")
    else:
        sys.stderr.write("\nAuthorization failure. You can\'t edit passwords.")


def question():
    """
    This is a function that facilitates the user to choose the appropriate answer to a question
    """
    from getpass import getpass
    qn = input("Do you now want to see the imported logins? [y]/n ")
    if qn=="y" or qn=="":
        imk = getpass("Enter master key first: ")
        print(displayLogins(imk))
    elif qn=="n":
        print("No problem")
    else:
        print("Enter yes or no !")
        question()


def reset():
    """ Lets you change and reset the master key """
    import os
    from getpass import getpass
    if os.path.exists("./.MasterKey.txt"):
        os.remove("./.MasterKey.txt")
    pswd=getpass("Enter new master key: ")
    confirmation = getpass("Confirm new master key: ")
    if pswd==confirmation:
            s = f"echo {pswd} > .MasterKey.txt"
            os.system(s)
            print("MasterKey  changed!")
    else:
        print("MasterKeys don't match. Please try again.")
        reset()


def deleteLogins():
    """Function to delete logins from the database"""
    import csv
    import os
    from getpass import getpass
    if os.path.exists("./.MasterKey.txt"):
        actualMasterKey = ((open(r".MasterKey.txt")).read()).strip()
        imk = getpass("Enter master key : ")
        if imk==actualMasterKey:
            nm = input("Enter website name: ")
            url = input("Enter website URL: ")
            usrnm = input("Enter username: ")
            pswd = getpass("Enter password: ")
            csvFile = open("Passwds.csv","r")
            names,urls,usernames,passwords = [],[],[],[]
            for row in csvFile:
                if row != "\n":
                    line = (row.rstrip("\n")).split(",")
                    names = names + [(str(line[0]))]
                    urls = urls + [(str(line[1]))]
                    usernames = usernames + [(str(line[2]))]
                    passwords = passwords + [(str(line[3]))]
                else:
                    row = ""","","","""
            for i in range(1,len(names)):
                if names[i]==nm and urls[i]==url and usernames[i]==usrnm and passwords[i]==pswd:
                    del names[i]
                    del urls[i]
                    del usernames[i]
                    del passwords[i]
            csvFile = open("Passwds.csv","w")
            csvWriter = csv.writer(csvFile,lineterminator="\n")
            csvWriter.writerow(("name","url","username","password"))
            csvFile.close()
            csvFile = open("Passwds.csv","a")
            csvWriter = csv.writer(csvFile,lineterminator="\n")
            for i in range(1,len(names)):
                csvWriter.writerow((names[i],urls[i],usernames[i],passwords[i]))
            print("Deleted successfully (if present) !")
        else:
            import sys
            sys.stderr.write("\nAuthorization failure. Try again.\n")
            deleteLogins()
    elif not os.path.exists("./.MasterKey.txt"):
        q()


def q():
    """Simple question"""
    from getpass import getpass
    qn = getpass("Create a MasterKey for accessing all your passwords !")
    confirmation = getpass("Confirm MasterKey: ")
    if qn==confirmation:
        with open("./.MasterKey.txt","w") as f:
            f.write(qn)
        print("MasterKey created !")
    else:
        print("MasterKeys don't match. Please try again.")
        q()

def q12():
    """Asks user if the program can force-import passwords from the file"""
    qn = input("A Password file already exists !\nDo you want to (forcefully) import passwords from your browser again?\nThis will override the passwords file ! [y]/n ")
    if qn=="y" or qn=="":
        from time import sleep
        importPasswords()
        sleep(1.0)
        print(f"Done.\nFile overwritten.\nRename and move as you like, and maybe DELETE the file after use.")
        question()
    elif qn=="n":
        print("No problem - the password file remains unchanged.")
        question()
    else:
        q12()


def mainMenu():
    """Main menu"""
    from os import path
    print("Initialising database...",end=" ")
    # dictionary()
    print("Done.")
    get_os()
    header = r"""
 ____                                     _
|  _ \ __ _ ___ _____      _____  _ __ __| |
| |_) / _` / __/ __\ \ /\ / / _ \| "__/ _` |
|  __/ (_| \__ \__ \\ V  V / (_) | | | (_| |
|_|   \__,_|___/___/ \_/\_/ \___/|_|  \__,_|
    _                _           _        ____  _
   / \   _ __   __ _| |_   _ ___(_)___   / ___|| |_ ___  _ __ __ _  __ _  ___
  / _ \ | "_ \ / _` | | | | / __| / __|  \___ \| __/ _ \| "__/ _` |/ _` |/ _ \
 / ___ \| | | | (_| | | |_| \__ \ \__ \   ___) | || (_) | | | (_| | (_| |  __/
/_/   \_\_| |_|\__,_|_|\__, |___/_|___/  |____/ \__\___/|_|  \__,_|\__, |\___|
                       |___/                                       |___/
 ____            _
/ ___| _   _ ___| |_ ___ _ __ ___
\___ \| | | / __| __/ _ \ "_ ` _ \
 ___) | |_| \__ \ | | __/ | | | | |
|____/ \__, |___/\__\___|_| |_| |_|
       |___/
    """
    print(header)

    print("\n\n")
    print("Happy to see that you\'re using this System!! \n\n")
    print("Getting ready.. ",end="")
    print("Done.")
    if path.isfile("./.MasterKey.txt")==False:
        q()
        print("MasterKey generated! Hope you remember it ;) ")

    print(
    """
    1.Import logins from a browser
    2.View the logins imported
    3.Write new login credentials to be exported to the browser
    4.Edit incorrect logins in the file
    5.Delete logins from the file
    6.Check for breaches
    7.Find out the strength of your passwords
    8.Find out the time needed to break your password
    9.Generate passwords
    10.Change MasterKey
    11. Quit (q or quit or exit)
    """
    )


def main_func():
    """Core function"""
    from getpass import getpass
    from time import sleep
    choice = input("Enter 1,2,3,4,5,6,7,8,9,10 or 11(or q) : ")
    
    if str(choice)=="1":
        import os
        if os.path.isfile("./Passwds.csv"):
            q12()

        elif not os.path.isfile("./Passwds.csv"):
            from os import getcwd
            print("Let\'s  import passwords from your web browser...",end=" ")
            importPasswords()
            sleep(1.0)
            print(f"Done.\nFile saved at {getcwd()}/Passwds.csv .\nRename and move as you like, and maybe DELETE the file after use.")
            question()

    if str(choice)=="2":
        import os
        if os.path.isfile("./Passwds.csv"):
            if not os.path.getsize("./Passwds.csv")==0: # if the file already exists (or isn't empty) , why not just view the file?
                def func():
                    from getpass import getpass
                    qn = input("Passwords file already exists! Do you now want to see the already existing logins? [y]/n ")
                    if qn=="y" or qn=="":
                        imk=getpass("Enter master key first: ")
                        print(displayLogins(imk))
                    elif qn=="n":
                        print("Fine - just note that the passwords have already been imported! ")
                    else:
                        print("Enter yes or no !")
                        func()
                func()
        elif os.path.isfile("./Passwds.csv")==False: # if the file doesnt exist
                print("You don\'t have a passwords file ? No problem! Let\'s  import passwords from your web browser...",end=" ")
                importPasswords()
                sleep(1.0)
                print("Done.")
                question()

    if str(choice)=="3":
        import os
        if os.path.isfile("./Passwds.csv"):
            print("Authenticate yourself !  ")
            imk = getpass("Enter master key first: ")
            writeLogins(imk)
        if os.path.isfile("./Passwds.csv")==False:
            print("You don\'t have a passwords file ? No problem! Let\'s  import passwords from your web browser...",end=" ")
            importPasswords()
            sleep(1.0)
            print("Done.")

    if str(choice)=="4":
        import os
        if os.path.isfile("./Passwds.csv"):
            print("Authenticate yourself !  ")
            imk = getpass("Enter master key first: ")
            editLogins(imk)
        elif os.path.isfile("./Passwds.csv")==False:
            print("You don\'t have a passwords file ? No problem! Let\'s import passwords from your web browser...",end=" ")
            importPasswords()
            sleep(1.0)
            print("Done.")
            print("Authenticate yourself !  ")
            imk = getpass("Enter master key first: ") #no need to ask it again ???
            editLogins(imk)
            print("Logins edited/added successfully !")

    if str(choice)=="5":
        deleteLogins()

    if str(choice)=="6":
        paswd = getpass("Enter password: ")
        breachCheck(paswd)

    if str(choice)=="7":
        paswd = getpass("Enter password: ")
        strength(paswd)

    if str(choice)=="8":
        eval_time()

    if str(choice)=="9": 
        def qqqq():
            nop=input("How many passwords should be generated? ")
            if nop.isdigit():
                nop=int(nop)
                if nop>0:
                    sleep(1.5)
                    print(f"Generating {round(nop)} passwords...",end=" ")
                    sleep(0.75)
                    print("Done")
                    passgen(nop)
            else:
                print("Enter a positive integer !")
                qqqq()
        qqqq()


    if str(choice)=="10":
        reset()
    if str(choice)=="":
            print(
    """
    1.Import logins from a browser
    2.View the logins imported
    3.Write new login credentials to be exported to the browser
    4.Edit incorrect logins in the file
    5.Delete logins from the file
    6.Check for breaches
    7.Find out the strength of your passwords
    8.Find out the time needed to break your password
    9.Generate passwords
    10.Change MasterKey
    11. Quit (q or quit or exit)
    """
    )

    if str(choice)=="11" or str(choice)=="q" or str(choice)=="quit" or str(choice)=="exit":
        print("Thanks for using PASS!!! :) \nShutting down..  ",end="")
        sleep(1)
        print("..")
        import sys
        sys.exit()

    else:
        main_func()

def PASS_cli():
    mainMenu()
    main_func()

PASS_cli()

