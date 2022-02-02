#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from os import system
words_dict=''

def editLogins(masterKeyInput):
    '''
    This is a function that facilitates modification of entered login details - in case the user needs
    to rectify something entered wrongly. Can be used in conjunction with 'displayLogins()'.
    '''
    actualMasterKey = ((open(r'.MasterKey.txt')).read()).strip() # obscuring actualMasterKey - hence in a different file.
    from getpass import getpass
    import csv
    import sys
    if masterKeyInput==actualMasterKey:
        csvFile = open(r'Passwds.csv','r')
        names,urls,usernames,passwords = [],[],[],[]
        for row in csvFile:
            if row != '\n':
                line = (row.rstrip("\n")).split(',')
                names = names + [(str(line[0]))]
                urls = urls + [(str(line[1]))]
                usernames = usernames + [(str(line[2]))]
                passwords = passwords + [(str(line[3]))]
            else:
                row = '"","","",""'

        print('1.Change website name')
        print('2.Change website URL')
        print('3.Change saved username')
        print('4.Change saved password for the website')
        choice = int(input('Choose 1,2,3 or 4: '))
        if choice==1:
            oldWebsiteName = input('Enter old website\'s name: ')
            newWebsiteName = input(f'Replace \"{oldWebsiteName}\" with: ' )
            for i in names:
                if i==oldWebsiteName:
                    names[names.index(i)] = newWebsiteName
        elif choice==2:
            oldURLName = input('Enter old URL: ')
            newURLName = input(f'Replace \"{oldURLName}\" with: ')
            for i in urls:
                if i==oldURLName:
                    urls[urls.index(i)] = newURLName
        elif choice==3:
            oldUserName = input('Enter old username: ')
            newUserName = input(f'Replace \"{oldUserName}\" with: ')
            for i in usernames:
                if i==oldUserName:
                    usernames[usernames.index(i)] = newUserName
        elif choice==4:
            oldPassword = getpass('Enter old password: ')
            newPassword = getpass(f'Replace \"{oldPassword}\" with: ')
            for i in passwords:
                if i==oldPassword:
                    passwords[passwords.index(i)] = newPassword
        else:
            print(f'{choice} is not in (1,2,3,4).')

        csvFile = open('Passwds.csv','w')
        csvWriter = csv.writer(csvFile,lineterminator='\n')
        csvWriter.writerow(('name','url','username','password'))
        csvFile.close()
        csvFile = open('Passwds.csv','a')
        csvWriter = csv.writer(csvFile,lineterminator='\n')
        for i in range(1,len(names)):
            csvWriter.writerow((names[i],urls[i],usernames[i],passwords[i]))

    else:
        sys.stderr.write('\n \n Authorization failure. You can\'t edit passwords.')


def importPasswords():
    csvFile = open(r'Passwds.csv','w+') # will contain the imported/new login credentials.
    browserCsvLocation = input('Enter path to file: ')
    browserPwds = open(browserCsvLocation) #'browserpwds' contains the passwords from browsers' csv files.

    blank = ''
    for row in browserPwds:
        blank+=str(row)
    csvFile.write(blank)
    csvFile.close()

def lower(inp):
    return (str(inp)).lower()

# Checks how many times a password has been breached
def breachCheck(passwd):
    import pwnedpasswords
    # Using external APIs to test how many times a password has been breached
    print(pwnedpasswords.check(passwd))



words_dict= ''

def dictionary():
    global words_dict
    import platform
    os=platform.system()
    from os import system,getcwd
    if os == "Windows":
        import os
        if not os.path.isfile('./dictionary.txt'):        
            system(f'curl --silent -o {getcwd()}/dictionary.txt https://raw.githubusercontent.com/dolph/dictionary/master/popular.txt ')

        words_dict = (open("./dictionary.txt").read()).strip() # sorry , curl doesn't hide output
    elif os=='Darwin' or os=='Linux':
        import os
        if not os.path.isfile('./dictionary.txt'):    
            system('curl -s -o /dev/null https://raw.githubusercontent.com/dolph/dictionary/master/popular.txt > dictionary.txt')
            
        words_dict= system('cat dictionary.txt')
        words_dict = str(words_dict)




def passgen(no_of_passwords=1):
    import random
    import os

    os.system("clear")
    os.system("cls")
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890' # total_chars
    # Password generation
    min_passwd_length = int(input("What password length do you want to get?: "))
    for n in range(no_of_passwords):
        password = ''
        for i in range(min_passwd_length):
            password += random.choice(chars) # random new password
        print(password)

def strength():
    global words_dict
    words_dict=lower(words_dict)
    total_chars =len('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()[]{}\|;:\'\",<.>`~/?')
    import math,getpass
    passwd=getpass.getpass("Enter password: ")
    passwordStrength=math.log2(total_chars) * len(passwd)

    if passwd.islower() or passwd.isupper() or passwd.isalpha() or passwd.isnumeric()  :
        passwordStrength-=5
    if passwd in words_dict: # checking dictionary files
        passwordStrength-=10

    print(f"Strength of the password is : {round(passwordStrength,4)}")

def get_os():

    qn = input("Do you want to install the required packages ? [y]/n ")
    if qn=='y':
        from os import system
        import platform
        os = platform.system()
        if os == 'Windows':
            system('pip install -U pandas sympy jupyter ipython pwnedpasswords')
            return 'Installed all requirements for Windows !'
        elif os == 'Linux' or os == 'Darwin':
            system('pip3 install -U pandas sympy jupyter ipython pwnedpasswords')
            if os=='Linux':
                return 'Installed all requirements for Linux !'
            elif os=='Darwin':
                return 'Installed all requirements for macOS !'
        else:
            return 'Unknown OS - please run \n \t pip install -U pandas sympy jupyter\n in the terminal '
    elif qn=='n':
        return 'No problem - just run \n \t pip install -U sympy pandas sympy jupyter\n in your system terminal '
    else:
        return 'Please enter y or n'


def eval_time():
    from getpass import getpass
    passwd=getpass("Enter password")
    from sympy import Sum,symbols
    k=symbols('k')
    no_of_cracked_passwords_per_sec=int(input("How many passwords should i attempt cracking per second? "))
    no_of_possible_passwords = Sum(94**k,(k,4,256)).doit()
    time = no_of_possible_passwords * (1/no_of_cracked_passwords_per_sec) # time is in seconds
    print(f"It takes {time} seconds to crack {passwd} @ {no_of_cracked_passwords_per_sec} cracked per second")

def breachCheck(passwd):
    from pwnedpasswords import check
    breach_test_results = check(passwd)
    return breach_test_results


def displayLogins(masterKeyInput):
    '''
    This is a function that helps display the contents of "Passwds.csv", which may be imported directly
    from the browser, or modified using the other functions below.
    It uses a library called "pandas" to display the passwords in a neat tabular form.

    '''
    import pandas as pd
    import sys
    actualMasterKey = ((open(r'.MasterKey.txt')).read()).strip() # obscuring actualMasterKey - hence in a different file.
    if masterKeyInput==actualMasterKey:
        print('Authorization success. Displaying gathered passwords : \n\n')
        return pd.read_csv(r'Passwds.csv') # the standard csv.reader() gives an ugly output.

    else:
        sys.stderr.write('\n \n Authorization failure. Unable to fetch passwords right now. \n \n')



def writeLogins(masterKeyInput):
    '''
    This is a function that facilitates the addition of new login details to the "Passwds.csv" file.
    '''
    actualMasterKey = ((open(r'.MasterKey.txt')).read()).strip() # obscuring actualMasterKey - hence in a different file.
    if masterKeyInput==actualMasterKey:
        print('Authorization success. Initializing edit mode \n\n')
        from getpass import getpass
        import csv
        import sys

        logins = list(str(input('Enter name,url,username: ')).split(','))
        pwd = getpass('Enter password: ') ; logins += (pwd,)
        csvFile = open(r'Passwds.csv','a')
        csvFile.write('\n')
        csvWriter = csv.writer(csvFile)
        if breachCheck(pwd)<1.5 and (strength(pwd)>='25' or eval_time(pwd)>='3600') :
            csvWriter.writerow(logins)
        else:
            ch= input("Weak password ! Auto-generate new password? [y]/n")
            if ch=='y' or ch=='':
                pwd = passgen() # made it generate only 1 password - 1 is the default argument for passgen()
                del logins[-1]
                logins.append(pwd)
                csvWriter = csv.writer(csvFile)
                csvWriter.writerow(logins)
                print("Added the random password...")

            elif ch=='n':
                csvWriter.writerow(logins)
                print("No problem - password unchanged ")

    else:
        import sys
        sys.stderr.write('\n \n Authorization failure. You can\'t append passwords.')


def editLogins(masterKeyInput):
    '''
    This is a function that facilitates modification of entered login details - in case the user needs
    to rectify something entered wrongly. Can be used in conjunction with 'displayLogins()'.
    '''
    from getpass import getpass
    import csv
    import sys
    actualMasterKey = ((open(r'.MasterKey.txt')).read()).strip() # obscuring actualMasterKey - hence in a different file.
    if masterKeyInput==actualMasterKey:
        csvFile = open(r'Passwds.csv','r')
        names,urls,usernames,passwords = [],[],[],[]
        for row in csvFile:
            if row != '\n':
                line = (row.rstrip("\n")).split(',')
                names = names + [(str(line[0]))]
                urls = urls + [(str(line[1]))]
                usernames = usernames + [(str(line[2]))]
                passwords = passwords + [(str(line[3]))]
            else:
                row = '"","","",""'

        print('1.Change website name')
        print('2.Change website URL')
        print('3.Change saved username')
        print('4.Change saved password for the website')
        choice = int(input('Choose 1,2,3 or 4: '))
        if choice==1:
            oldWebsiteName = input('Enter old website\'s name: ')
            newWebsiteName = input(f'Replace \"{oldWebsiteName}\" with: ' )
            for i in names:
                if i==oldWebsiteName:
                    names[names.index(i)] = newWebsiteName
        elif choice==2:
            oldURLName = input('Enter old URL: ')
            newURLName = input(f'Replace \"{oldURLName}\" with: ')
            for i in urls:
                if i==oldURLName:
                    urls[urls.index(i)] = newURLName
        elif choice==3:
            oldUserName = input('Enter old username: ')
            newUserName = input(f'Replace \"{oldUserName}\" with: ')
            for i in usernames:
                if i==oldUserName:
                    usernames[usernames.index(i)] = newUserName
        elif choice==4:
            oldPassword = getpass('Enter old password: ')
            newPassword = getpass(f'Replace \"{oldPassword}\" with: ')
            for i in passwords:
                if i==oldPassword:
                    passwords[passwords.index(i)] = newPassword
        else:
            print(f'{choice} is not in (1,2,3,4).')

        csvFile = open('Passwds.csv','w')
        csvWriter = csv.writer(csvFile,lineterminator='\n')
        csvWriter.writerow(('name','url','username','password'))
        csvFile.close()
        csvFile = open('Passwds.csv','a')
        csvWriter = csv.writer(csvFile,lineterminator='\n')
        for i in range(1,len(names)):
            csvWriter.writerow((names[i],urls[i],usernames[i],passwords[i]))

    else:
        sys.stderr.write('\n \n Authorization failure. You can\'t edit passwords.')


def question():
    from getpass  import getpass
    qn = input("Do you now want to see the imported logins? [y]/n")
    if qn=='y' or qn=='':
        imk = getpass('Enter master key first: ')
        print(displayLogins(imk))
    elif qn=='n':
        print("No problem")
    else:
        print("Enter yes or no !")
        question()



def mainMenu():
    from time import sleep
    from getpass import getpass
    from os import path
    print('Initialising database...',end=' ')
    dictionary()
    print('Done.')
    get_os()
    header = r'''
 ____                                     _
|  _ \ __ _ ___ _____      _____  _ __ __| |
| |_) / _` / __/ __\ \ /\ / / _ \| '__/ _` |
|  __/ (_| \__ \__ \\ V  V / (_) | | | (_| |
|_|   \__,_|___/___/ \_/\_/ \___/|_|  \__,_|
    _                _           _        ____  _
   / \   _ __   __ _| |_   _ ___(_)___   / ___|| |_ ___  _ __ __ _  __ _  ___
  / _ \ | '_ \ / _` | | | | / __| / __|  \___ \| __/ _ \| '__/ _` |/ _` |/ _ \
 / ___ \| | | | (_| | | |_| \__ \ \__ \   ___) | || (_) | | | (_| | (_| |  __/
/_/   \_\_| |_|\__,_|_|\__, |___/_|___/  |____/ \__\___/|_|  \__,_|\__, |\___|
                       |___/                                       |___/
 ____            _
/ ___| _   _ ___| |_ ___ _ __ ___
\___ \| | | / __| __/ _ \ '_ ` _ \
 ___) | |_| \__ \ | | __/ | | | | |
|____/ \__, |___/\__\___|_| |_| |_|
       |___/
    '''
    print(header)

    print('\n\n')
    print('Happy to see that you\'re using this System!! \n\n')
    print('Getting ready... ',end=' ')
    sleep(1.0)
    if path.isfile('./.MasterKey.txt')==False:
        qn = getpass("Create a MasterKey for accessing all your passwords !")
        system('echo {qn} > ./.MasterKey.txt') # sends the new password to the MasterKey file
        print("MasterKey generated ! Hope you remember it ;) ")

    print('''

    1.Import logins from a browser
    2.View the logins imported
    3.Write new login credentials to be exported to the browser
    4.Edit incorrect logins in the file
    5. Check for breaches
    6. Find out the strength of your passwords
    7. Find out the time needed to break your password
    8. Generate passwords
    9. Change MasterKey
    10. Quit (q or quit or exit)

    ''')


def main_func():
    from getpass import getpass
    from time import sleep
    choice = input('Enter 1,2,3,4,5,6,7,8,9 (or q) : ')
    if str(choice)=='1':
        from os import getcwd
        print('Authenticate yourself !  ')
        imk = getpass('Enter master key first: ')
        print('Let\'s  import passwords from your web browser...',end=' ')
        importPasswords()
        sleep(1.0)
        print(f'Done.\nFile saved at {getcwd()}/Passwds.csv .\nRename and move as you like, and maybe DELETE the file after use.')
        question()
    if str(choice)=='2':
        print('Authenticate yourself !  ')
        imk = getpass('Enter master key first: ')
        import os
        if os.path.isfile('./Passwds.csv'): # if the file already exists , why not just view the file?
            def func():
                from getpass import getpass
                qn = input("Passwords file already exists!   Do you now want to see the already existing logins? [y]/n")
                if qn=='y' or qn=='':
                    imk = getpass('Enter master key first: ')
                    print(displayLogins(imk))
                elif qn=='n':
                    print("Fine - just note that the passwords have already been imported! ")
                else:
                    print("Enter yes or no !")
                    func()
            func()
        elif os.path.isfile('./Passwds.csv')==False: # if the file doesnt exist
                print('You don\'t have a passwords file ? No problem !  Let\'s  import passwords from your web browser...',end=' ')
                importPasswords()
                sleep(1.0)
                print('Done.')
                question()

    if str(choice)=='3':
        print('Authenticate yourself !  ')
        imk = getpass('Enter master key first: ')
        writeLogins(imk)
    if str(choice)=='4':
        print('Authenticate yourself !  ')
        imk = getpass('Enter master key first: ')
        editLogins(imk)
    if str(choice)=='5':
        paswd = getpass("Enter password: ")
        print(f"Password has been breached {breachCheck(paswd)} times")
    if str(choice)=='6':
        strength()
    if str(choice)=='7':
        eval_time()
    if str(choice)=='8':
        nop=int(input("How many passwords should be generated? "))
        sleep(0.5)
        print("Generating passwords...",end=' ')
        sleep(1.0)
        print('Done')
        passgen(nop)
    if str(choice)=='9':
        print("Forgot MasterKey ? No problem ! ")
        q = str(input("What's the new MasterKey?"))
        system('echo {q} > ./.MasterKey.txt')
        print("MasterKey changed succesfully !")
    if str(choice)=='10' or str(choice)=='q' or str(choice)=='quit' or str(choice)=='exit':
        print("Thanks for using PASS!!!🥳 \nShutting down..",end='')
        sleep(1)
        print('..')
        import sys
        sys.exit()
    else:
        main_func()

def PASS_cli():
    mainMenu()
    main_func()
PASS_cli()
