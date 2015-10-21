#!/usr/bin/env python

''' Excercise Add password-encryption
'''

'''MD5 'Message Digest 5' means a 128-bit encryption algorithm, 
generating a 32-character hexadecimal hash,
e.g ( 4d186321c1a7f0f354b297e8914ab240 )
whatever the captcha. This algorithm is not reversible, 
ie it is normally impossible to find the original word 
from the md5 hash.'''

from hashlib import md5 # message digest 5 algorithm info above
from getpass import getpass # hide the password typing on command-line
from time import time, ctime

db = {}

def newuser():
    prompt = '\nLogIn User desired: '
    done = False
    while not done:
        name = raw_input(prompt)
        if db.has_key(name):
            prompt = 'name taken, try another: '
            continue
        else:
            done = True

    # getpass() prompt"ask" and hide the password
    # md5 encrypt the password
    pwd = md5( getpass() ).hexdigest() # eg 0ad066a5d29f3f2a2a1c7c17dd082a79
    
    db[name] = {'passwd': pwd}
    db[name].update({'timeStamp': time()})
    print db

def olduser():

    name = raw_input('\nUser logIn: ')
    
    # getpass prompt and hide the password
    # md5 encrypt the password
    pwd = md5(getpass()).hexdigest() # eg 0ad066a5d29f3f2a2a1c7c17dd082a79
    
    if db.has_key(name):
        timeStamp = db.get(name)['timeStamp']
        if time() - timeStamp <= 30:
            print "\nYou Already logIn at: < %s >" % ctime(timeStamp)
        else:   
            passwd = db.get(name)['passwd']
            # here an encryption is needed
            if passwd == pwd:
                db[name].update({'timeStamp': time()})
                print '\nWelcome Back', name.title(), '!!'
            else:
                print '\nLogin Incorrect !!'
    else:
        print '\nLogin Incorrect !!'

def remove(): 
    
    done = False
    display = False
    while not done:

        if not db: print '\nNo users in db to remove, db Empty.'; return

        if not display:
            prompt = """
    Users in db:\n\n    %s\n
    Choose a User to remove or (q)uit: """ % '\n    '.join(sorted(db.keys()))
        
        name = raw_input(prompt).strip()
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
            print '\nYou picked: [%s]' % choice
            if choice not in 'qrd' or not choice:
                print '\nInvalid option, try again !!'
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
            print '\nYou picked: [%s]' % choice
            if choice not in 'qnea' or not choice:
                print 'Invalid option, try again !!'
            else:
                chosen = True

        if choice == 'q': done = True; print
        if choice == 'n': newuser()
        if choice == 'e': olduser() 
        if choice == 'a': admin() 


if __name__ == '__main__':
    showmenu()
