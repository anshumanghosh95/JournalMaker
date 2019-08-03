# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 17:31:17 2019

@author: ANSHUMAN
"""

import pandas as pd
from datetime import datetime

def login(error,data):
    logon = int(input('Welcome to your personal journal\n Select the option below\n1 Login\n2 Sign Up\n'))
    if logon == 1 and error == 'ok':
        print('Welcome User:\n')
        username = str(input('Provide Username: \n'))
        password = input('Provide Password: \n')
        username = username.upper()
        try:
            user = data[data['username'] == username]
            if user['password'].all() == password:
                print('password authenticated\n')
                journal(username)
            else:
                raise Exception
        except:
            print('User or Password incorrect')
    elif logon == 2:
#check for total number of user
        if data.shape == (10,2):
            print('Maximum 10 users only\n')            
            return
        print('Please provide the details to create a journal:\n')
        username = str(input('Provide Username: \n'))
        username = username.upper()
        password = str(input('Provide Password: \n'))
        user = pd.DataFrame()
        user.loc[0,'username'] = username
        user.loc[0,'password'] = password
        if error == 'ok':
            usercheck = data[data['username'] == username]
            if usercheck.shape == (0,2): 
                frames = [data, user]
                data = pd.concat(frames)
                data.to_pickle('login.pkl')
                journal(username)
            else:
                print('User already exsists, Login using credentials')
                return
        else:
            user.to_pickle('login.pkl')
            journal(username)
    else:
        print('Please Signup, No user currently present')
                
def journal(username):

    userfile = username + '_journal.pkl'

    try:
        journal = pd.read_pickle(userfile)
        r = int(input('Do you want to read your journal:\n1 Read Journal\n2 Create New Entry\n'))
        if r == 1:
            print('\n\n')
            for i,k in journal.iloc[:,:].values:
                print(i,' - ',k)
        else:
            journal_new = pd.DataFrame()
            journal_new.loc[0,'DateTime'] = datetime.now().strftime('%d %b %Y %I.%M%p')
            journal_new.loc[0,'JournalEntry'] = str(input('Write you journal: \n'))
#check and purge old entries of journal            
            if journal.shape == (50,2):
                journal = journal.iloc[1:,:]
            frames1 = [journal, journal_new]
            journal = pd.concat(frames1)
            journal.to_pickle(userfile)
    except Exception:
        print('Creating New Journal\n')
        journal = pd.DataFrame()
        journal.loc[0,'DateTime'] = datetime.now().strftime('%d %b %Y %I.%M%p')
        journal.loc[0,'JournalEntry'] = str(input('Write you journal: \n'))
        journal.to_pickle(userfile)

if __name__ == '__main__':
    try:
        data = pd.read_pickle('login.pkl')
        e = 'ok'
    except:
        e = 'fail'
        data = pd.DataFrame()
    login(e,data)
    input('\n\nPress any key to exit\n')