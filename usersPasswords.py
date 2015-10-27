#!/usr/bin/env python

# *CBB Can Be Better    
from hashlib import md5 # Message Digest 5 hash/encrypt algorithm
from getpass import getpass # Hide password while typing on terminal
from time import time, ctime # time => seconds, ctime => formatTime
from json import dumps # to print with format/indent


db = {}

def newuser():
    prompt = '\nLogIn User Desired: '
    done = False
    while not done:
        name = raw_input(prompt).lower()
        if db.has_key(name):
            prompt = 'name taken, try another: '
            continue
        elif not name.isalnum():
            prompt = 'Not symbols or whiteSpaces admited, try another: '           
            continue    
        else:
            done = True

    pwd = md5( getpass() ).hexdigest() # eg 0ad066a5d29f3f2a2a1c7c17dd082a79
    
    db[name] = {'passwd': pwd}
    db[name].update({'timeStamp': time()}) # CBB
    print dumps(db, indent=5)


def logIn():

    name = raw_input('\nUser logIn: ').lower() #CBB
    pwd = md5( getpass() ).hexdigest() # CBB

    if db.has_key(name):
        timeStamp = db.get(name)['timeStamp']
        if time() - timeStamp <= 30:
            print "\nYou Already logIn at: < %s >" % ctime(timeStamp)
        else:   #CBB
            passwd = db.get(name)['passwd']
            if passwd == pwd:
                db[name].update({'timeStamp': time()}) #CBB
                print '\nWelcome Back', name.title(), '!!'
            else:
                print '\nLogin Incorrect !!'
    
    else:
        confirm = '\nAre you a new user %s ? Y/N: ' % name
        try:
            confirm = raw_input(confirm).strip().lower()
            if confirm: confirm = confirm[0]
        except (EOFError, KeyboardInterrupt): 
            return
        if confirm == 'y':
            print 'Creating new user...'
            newuser()
        elif confirm == 'n':
            print 'Try to logIn again...'
            logIn()
        else:
            print 'Login Incorrect !!'


def remove(): 
    
    done = False
    display = False
    while not done:

        if not db: print '\nNo users in db to remove, db Empty.'; return

        if not display:
            prompt = """
    Users in db:\n\n    %s\n
    Choose a User to remove or (q)uit: """ % '\n    '.join(sorted(db.keys()))
        
        name = raw_input(prompt).strip().lower()
        if name == 'q': print "    Good Bye !!"; return
        
        if db.has_key(name):
            confirm = '\nAre you sure to delete %s ? Y/N: ' % name.title()
            
            try:
                confirm = raw_input(confirm).strip().lower()
                if confirm: confirm = confirm[0]
            except (EOFError, KeyboardInterrupt):
                print
                confirm = 'no'    
            
            if confirm == 'y':
                del db[name]
                print 'User %s Deleted' % name.title()
                display = False
            else:
                print 'No User Deleted'
                display = False

        else:
            display = True
            prompt = '    Invalid User %s, try again: ' % name


def display():

    if not db: print '\nNo users in db to display, db Empty.'; return
    
    print '\nUsers and Passwords in db:\n'
    
    for key in sorted(db):
        print "%s\t\t%s" % (key, db[key]['passwd'])


def admin():    

    prompt = """
    ****** (A)dministration ******
    (R)emove a User
    (D)isplay Users and Passwords
    (Q)uit

    Enter choice: """

    done = False
    while not done:

        chosen = False
        while not chosen:
            try:
                choice = raw_input(prompt).strip().lower()
                if choice: choice = choice[0]
            except (EOFError, KeyboardInterrupt): # ctrl+d, ctrl+c
                print
                choice = 'q'
            print '    You picked: [%s]' % choice
            if choice not in 'qrd' or not choice:
                print '    Invalid option, try again !!'
            else:
                chosen = True

        if choice == 'q': done = True 
        if choice == 'r': remove() 
        if choice == 'd': display()                    


def showmenu():
    prompt = """
    (N)ew User Login
    (E)xisting User Login
    (A)dministration
    (Q)uit

    Enter choice: """

    done = False
    while not done:

        chosen = False
        while not chosen:
            try:
                choice = raw_input(prompt).strip().lower()
                if choice: choice = choice[0]
            except (EOFError, KeyboardInterrupt):
                print 
                choice = 'q'
            print '    You picked: [%s]' % choice
            if choice not in 'neaq' or not choice:
                print '    Invalid option, try again !!'
            else:
                chosen = True

        if choice == 'q': done = True; print
        if choice == 'n': newuser()
        if choice == 'e': logIn() 
        if choice == 'a': admin() 


if __name__ == '__main__':
    showmenu()
