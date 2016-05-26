#!/usr/bin/env python3.4
import os
import sys
import shutil
#returns the current date
def date():
    import time
    return(time.strftime("%d/%m/%Y"))
#Opens the logfile and writes the current date if it's not present.
def openlog(logtype):
    #define counters for new date(n), new local log(l) and new carbon log (c)
    n = 0
    l = 0
    c = 0
    #opens the log file (hardcoded)
#    f = open('testlog','r+') #opens a testlog
    f = open(os.path.expanduser('~/Documents/master_stage/logs/project_log'),'r+')
    #See if there is already a log of this date and of the specified logtype
    for line in f:
        if (str(line) == str(date()+":\n")): n = 1
        if (n == 1 and str(line) == str("Local:\n")): l = 1
        if (n == 1 and str(line) == str("Carbon:\n")): c = 1
    #Generate standard log syntax for the logfile
    if n == 0:
        print("First log of today.")
        f.write('\n'+date()+':\n')
    if l == 0 and logtype == 'local':
        print("First local log of today.")
        if c == 0:
            f.write('Local:\n')
        else:
            f.write('\nLocal:\n')
    if c == 0 and logtype == 'carbon':
        print("First carbon log of today.")
        if l == 0:
            f.write('Carbon:\n')
        else:
            f.write('\nCarbon:\n')
    return(f)

#Gets user input to put in the log if no arguments were given.
def get_log_old():
    new_log = ""
    usr_input = input("Please enter your log lines:\n")
    #While the input is not empty append each line to the new log with propper punctuation.
    while (usr_input != ""):
        usr_input = proppunc(usr_input)
        new_log = str(new_log+usr_input+"\n")
        usr_input = input("Please enter your next log line:\n")
    return new_log

#Writes the given arguments to the log variables if arguments are givven.
def get_log(n):
    i = 0
    new_log = ""
    for text in sys.argv:
        if i > n:
            new_log=str(new_log+text+" ")
        i += 1
    new_log = str(new_log+"\n")
    new_log = proppunc(new_log)
    return new_log

#Reads a sentence and returns it with propper punctuation.
def proppunc(string):
    if len(string) == 0:
        return string
    upper = string.upper()
    #Capitalizes the first letter.
    if string[0] != upper[0]:
        string = upper[0]+string[1:]
    #Appends a . if no final character is pressent.
    if "." not in string[-3:] and '!' not in string[-3:] and '?' not in string[-3:]:
        if string[-1] == "\n":
            if string[-2] == " ":
                string = string[:-2]+"."+string[-1]
            else:
                string = string[:-1]+"."+string[-1]
        elif string[-1] == " ":
            string = string[:-1]+"."
        else:
            string = string + "."
    return string

#Puts the given log under the correct logtype in file f.
def write_log(f,logtype,log):
    #Counters for the date(n), local(l) or carbon(c) logpoint, written log(w) and current logname.
    n = 0
    l = 0
    c = 0
    w = 0
    fname = f.name

    #Closes the log, backs it up to old and (re)open both.
    f.close()
    shutil.copy(fname, fname+'_old')
    old = open(fname+'_old','r+')
    new = open(fname,'r+')

    #Makes sure both files are read and written from the beginning.
    old.seek(0, 0)
    new.seek(0, 0)

    #Reads the old log file and appends the new log entry at the appropriate point.
    for line in old:
        if (str(line) == str(date()+":\n")): n = 1
        if (n == 1 and str(line) == str("Local:\n")): l = 1
        if (n == 1 and str(line) == str("Carbon:\n")): c = 1
        if (logtype == 'local' and l == 1 and str(line) == '\n'):
            new.write(log)
            w = 1
        if (logtype == 'carbon' and c == 1 and str(line) == '\n'):
            new.write(log)
            w = 1
        new.write(line)

    #If the log is not written at this point append it to the end of the file.
    if w == 0:
       new.write(log)
    return old,new

#Gets the logtype and log from the user and make a new log file.
def main():
    #Declares the logtype and a counter to see if an argument is given (l) and if the sys.argv[1] is a log type (n).
    logtype = ''
    l = 0
    n = 1

    #Gets the logtype from the user and ajust the counters.
    while logtype.upper() != 'LOCAL' and logtype.upper() != 'CARBON':
        if (len(sys.argv) == 1 or l == 1):
            logtype = input('Is this a carbon or local log?\n')
            n = 0
        else:
            logtype = str(sys.argv[1])
            l = 1

    #Converts the logtype.
    logtype = logtype.lower()

    #Open the log file.
    f = openlog(logtype)

    #Determine which function to use to get the log (old if no arguments were given or just a logtype).
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and n == 1):
        log = get_log_old()
    else:
        log = get_log(n)

    #Writes the log and gets the new logfile.
    old,f = write_log(f,logtype,log)
    new_file = f.name
    old_file = old.name

    #Closes both logfiles.
    f.close()
    old.close()


    #Print the new log entry
    print('\"'+log[:-1]+'\" saved to the '+logtype+' log')

#Only call main when this script is the main script
if __name__ == "__main__":main()
